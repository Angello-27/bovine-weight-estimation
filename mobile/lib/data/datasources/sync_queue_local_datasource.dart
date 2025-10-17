/// DataSource: SyncQueueLocalDataSource
///
/// DataSource para almacenamiento local (SQLite) de la cola de sincronización.
/// Single Responsibility: Operaciones CRUD de items pendientes de sync.
///
/// Data Layer - Clean Architecture
library;

import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart' as sqflite;

import '../../core/errors/exceptions.dart';
import '../../domain/entities/sync_queue_item.dart';
import '../../domain/entities/sync_status.dart';

/// DataSource para almacenamiento local de la cola de sincronización
abstract class SyncQueueLocalDataSource {
  /// Agrega un item a la cola
  Future<void> enqueue(SyncQueueItem item);

  /// Obtiene todos los items pendientes ordenados por prioridad
  Future<List<SyncQueueItem>> getPendingItems();

  /// Obtiene items listos para reintento (según backoff exponencial)
  Future<List<SyncQueueItem>> getItemsReadyForRetry();

  /// Actualiza el estado de un item
  Future<void> updateItemStatus(
    String itemId,
    SyncStatus status, {
    String? errorMessage,
  });

  /// Incrementa el contador de reintentos
  Future<void> incrementRetryCount(String itemId);

  /// Elimina un item de la cola (sync exitoso)
  Future<void> removeItem(String itemId);

  /// Obtiene la cantidad de items pendientes
  Future<int> getPendingCount();

  /// Obtiene items por tipo de entidad
  Future<List<SyncQueueItem>> getItemsByEntityType(SyncEntityType entityType);

  /// Limpia items antiguos con demasiados reintentos
  Future<int> cleanupStaleItems({int maxRetryCount = 10});

  /// Cierra la base de datos
  Future<void> close();
}

/// Implementación con SQLite
class SyncQueueLocalDataSourceImpl implements SyncQueueLocalDataSource {
  sqflite.Database? _database;

  static const String _databaseName = 'bovine_weight.db';
  static const int _databaseVersion = 2; // Incrementado para migración
  static const String _tableSyncQueue = 'sync_queue';

  /// Obtiene la instancia de la base de datos
  Future<sqflite.Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  /// Inicializa la base de datos
  Future<sqflite.Database> _initDatabase() async {
    try {
      final databasesPath = await sqflite.getDatabasesPath();
      final path = join(databasesPath, _databaseName);

      return await sqflite.openDatabase(
        path,
        version: _databaseVersion,
        onCreate: _onCreate,
        onUpgrade: _onUpgrade,
      );
    } catch (e) {
      throw DatabaseException(
        message: 'Error al inicializar DB sync queue: $e',
      );
    }
  }

  /// Crea las tablas (solo se llama en instalación nueva)
  Future<void> _onCreate(sqflite.Database db, int version) async {
    // Esta tabla se creará en _onUpgrade si la DB ya existía
    await _createSyncQueueTable(db);
  }

  /// Crea la tabla sync_queue
  Future<void> _createSyncQueueTable(sqflite.Database db) async {
    await db.execute('''
      CREATE TABLE IF NOT EXISTS $_tableSyncQueue (
        id TEXT PRIMARY KEY,
        entity_type TEXT NOT NULL,
        entity_id TEXT NOT NULL,
        operation TEXT NOT NULL,
        data TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        retry_count INTEGER NOT NULL DEFAULT 0,
        last_retry_at INTEGER,
        created_at INTEGER NOT NULL,
        error_message TEXT
      )
    ''');

    // Índices para optimizar queries
    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_sync_queue_status 
      ON $_tableSyncQueue (status)
    ''');

    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_sync_queue_entity_type 
      ON $_tableSyncQueue (entity_type)
    ''');

    await db.execute('''
      CREATE INDEX IF NOT EXISTS idx_sync_queue_priority 
      ON $_tableSyncQueue (status, operation, entity_type, created_at)
    ''');
  }

  /// Maneja upgrades de versión
  Future<void> _onUpgrade(
    sqflite.Database db,
    int oldVersion,
    int newVersion,
  ) async {
    // Migración de v1 a v2: agregar tabla sync_queue
    if (oldVersion < 2) {
      await _createSyncQueueTable(db);
    }
  }

  @override
  Future<void> enqueue(SyncQueueItem item) async {
    try {
      final db = await database;

      await db.insert(
        _tableSyncQueue,
        _itemToMap(item),
        conflictAlgorithm: sqflite.ConflictAlgorithm.replace,
      );
    } catch (e) {
      throw DatabaseException(message: 'Error al agregar item a cola: $e');
    }
  }

  @override
  Future<List<SyncQueueItem>> getPendingItems() async {
    try {
      final db = await database;

      final maps = await db.query(
        _tableSyncQueue,
        where: 'status IN (?, ?)',
        whereArgs: ['pending', 'error'],
        orderBy: 'operation ASC, entity_type ASC, created_at ASC',
      );

      final items = maps.map((map) => _mapToItem(map)).toList();

      // Ordenar por prioridad calculada
      items.sort((a, b) => a.priority.compareTo(b.priority));

      return items;
    } catch (e) {
      throw DatabaseException(message: 'Error al obtener items pendientes: $e');
    }
  }

  @override
  Future<List<SyncQueueItem>> getItemsReadyForRetry() async {
    try {
      final db = await database;

      final maps = await db.query(
        _tableSyncQueue,
        where: 'status = ?',
        whereArgs: ['error'],
        orderBy: 'last_retry_at ASC',
      );

      final items = maps.map((map) => _mapToItem(map)).toList();

      // Filtrar items listos para reintento (según backoff)
      return items.where((item) => item.shouldRetry).toList();
    } catch (e) {
      throw DatabaseException(
        message: 'Error al obtener items para reintento: $e',
      );
    }
  }

  @override
  Future<void> updateItemStatus(
    String itemId,
    SyncStatus status, {
    String? errorMessage,
  }) async {
    try {
      final db = await database;

      await db.update(
        _tableSyncQueue,
        {
          'status': status.toSqlite(),
          if (errorMessage != null) 'error_message': errorMessage,
        },
        where: 'id = ?',
        whereArgs: [itemId],
      );
    } catch (e) {
      throw DatabaseException(message: 'Error al actualizar estado: $e');
    }
  }

  @override
  Future<void> incrementRetryCount(String itemId) async {
    try {
      final db = await database;
      final now = DateTime.now().millisecondsSinceEpoch;

      await db.rawUpdate(
        '''
        UPDATE $_tableSyncQueue 
        SET retry_count = retry_count + 1, 
            last_retry_at = ?,
            status = 'error'
        WHERE id = ?
      ''',
        [now, itemId],
      );
    } catch (e) {
      throw DatabaseException(
        message: 'Error al incrementar contador reintentos: $e',
      );
    }
  }

  @override
  Future<void> removeItem(String itemId) async {
    try {
      final db = await database;

      await db.delete(_tableSyncQueue, where: 'id = ?', whereArgs: [itemId]);
    } catch (e) {
      throw DatabaseException(message: 'Error al eliminar item: $e');
    }
  }

  @override
  Future<int> getPendingCount() async {
    try {
      final db = await database;

      final result = await db.rawQuery('''
        SELECT COUNT(*) as count 
        FROM $_tableSyncQueue 
        WHERE status IN ('pending', 'error')
      ''');

      return sqflite.Sqflite.firstIntValue(result) ?? 0;
    } catch (e) {
      throw DatabaseException(message: 'Error al contar pendientes: $e');
    }
  }

  @override
  Future<List<SyncQueueItem>> getItemsByEntityType(
    SyncEntityType entityType,
  ) async {
    try {
      final db = await database;

      final maps = await db.query(
        _tableSyncQueue,
        where: 'entity_type = ?',
        whereArgs: [entityType.toSqlite()],
        orderBy: 'created_at DESC',
      );

      return maps.map((map) => _mapToItem(map)).toList();
    } catch (e) {
      throw DatabaseException(message: 'Error al obtener items por tipo: $e');
    }
  }

  @override
  Future<int> cleanupStaleItems({int maxRetryCount = 10}) async {
    try {
      final db = await database;

      final result = await db.delete(
        _tableSyncQueue,
        where: 'retry_count >= ?',
        whereArgs: [maxRetryCount],
      );

      return result;
    } catch (e) {
      throw DatabaseException(message: 'Error al limpiar items: $e');
    }
  }

  @override
  Future<void> close() async {
    final db = _database;
    if (db != null) {
      await db.close();
      _database = null;
    }
  }

  /// Convierte SyncQueueItem a Map para SQLite
  Map<String, dynamic> _itemToMap(SyncQueueItem item) {
    return {
      'id': item.id,
      'entity_type': item.entityType.toSqlite(),
      'entity_id': item.entityId,
      'operation': item.operation.toSqlite(),
      'data': item.data,
      'status': item.status.toSqlite(),
      'retry_count': item.retryCount,
      'last_retry_at': item.lastRetryAt?.millisecondsSinceEpoch,
      'created_at': item.createdAt.millisecondsSinceEpoch,
      'error_message': item.errorMessage,
    };
  }

  /// Convierte Map de SQLite a SyncQueueItem
  SyncQueueItem _mapToItem(Map<String, dynamic> map) {
    return SyncQueueItem(
      id: map['id'] as String,
      entityType: SyncEntityType.fromString(map['entity_type'] as String),
      entityId: map['entity_id'] as String,
      operation: SyncOperation.fromString(map['operation'] as String),
      data: map['data'] as String,
      status: SyncStatus.fromString(map['status'] as String),
      retryCount: map['retry_count'] as int,
      lastRetryAt: map['last_retry_at'] != null
          ? DateTime.fromMillisecondsSinceEpoch(map['last_retry_at'] as int)
          : null,
      createdAt: DateTime.fromMillisecondsSinceEpoch(map['created_at'] as int),
      errorMessage: map['error_message'] as String?,
    );
  }
}
