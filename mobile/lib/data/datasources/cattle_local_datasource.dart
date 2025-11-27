/// DataSource: CattleLocalDataSource
///
/// DataSource para almacenamiento local (SQLite) de ganado.
/// Single Responsibility: Operaciones CRUD de ganado en SQLite.
///
/// Data Layer - Clean Architecture
library;

import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart' as sqflite;

import '../../core/errors/exceptions.dart';
import '../../domain/entities/cattle.dart';
import '../models/cattle_model.dart';

/// DataSource para almacenamiento local de ganado
abstract class CattleLocalDataSource {
  /// Guarda un animal
  Future<void> saveCattle(CattleModel cattle);

  /// Obtiene un animal por ID
  Future<CattleModel?> getCattleById(String id);

  /// Obtiene un animal por caravana
  Future<CattleModel?> getCattleByEarTag(String earTag);

  /// Obtiene todos los animales
  Future<List<CattleModel>> getAllCattle();

  /// Obtiene animales activos
  Future<List<CattleModel>> getActiveCattle();

  /// Busca animales por término
  Future<List<CattleModel>> searchCattle(String searchTerm);

  /// Actualiza un animal
  Future<void> updateCattle(CattleModel cattle);

  /// Elimina un animal
  Future<void> deleteCattle(String id);

  /// Verifica si existe una caravana
  Future<bool> earTagExists(String earTag, {String? excludeId});

  /// Obtiene conteo por estado
  Future<Map<CattleStatus, int>> getCattleCountByStatus();

  /// ===== Métodos de Sincronización (US-005) =====

  /// Obtiene animales no sincronizados
  Future<List<CattleModel>> getUnsyncedCattle();

  /// Marca un animal como sincronizado
  Future<void> markAsSynced(String id);

  /// Marca un animal con error de sincronización
  Future<void> markAsSyncError(String id, String error);

  /// Obtiene el conteo de animales pendientes de sincronización
  Future<int> getUnsyncedCount();

  /// Cierra la base de datos
  Future<void> close();
}

/// Implementación con SQLite
class CattleLocalDataSourceImpl implements CattleLocalDataSource {
  sqflite.Database? _database;

  static const String _databaseName = 'bovine_weight.db';
  static const int _databaseVersion = 2; // v2: Columnas sync (US-005)
  static const String _tableCattle = 'cattle';

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

      final db = await sqflite.openDatabase(
        path,
        version: _databaseVersion,
        onCreate: _onCreate,
        onUpgrade: _onUpgrade,
      );

      // Asegurar que las tablas existan (por si otro DataSource creó la DB primero)
      await _ensureTablesExist(db);

      return db;
    } catch (e) {
      throw DatabaseException(message: 'Error al inicializar DB: $e');
    }
  }

  /// Verifica y crea las tablas si no existen
  Future<void> _ensureTablesExist(sqflite.Database db) async {
    // Verificar si la tabla de cattle existe
    final cattleTable = await db.rawQuery(
      "SELECT name FROM sqlite_master WHERE type='table' AND name='$_tableCattle'",
    );
    if (cattleTable.isEmpty) {
      await _onCreate(db, _databaseVersion);
    }
  }

  /// Crea las tablas
  Future<void> _onCreate(sqflite.Database db, int version) async {
    // Tabla de ganado
    await db.execute('''
      CREATE TABLE $_tableCattle (
        id TEXT PRIMARY KEY,
        ear_tag TEXT UNIQUE NOT NULL,
        name TEXT,
        breed TEXT NOT NULL,
        birth_date INTEGER NOT NULL,
        gender TEXT NOT NULL,
        color TEXT,
        birth_weight REAL,
        mother_id TEXT,
        father_id TEXT,
        observations TEXT,
        status TEXT NOT NULL DEFAULT 'active',
        registration_date INTEGER NOT NULL,
        last_updated INTEGER NOT NULL,
        photo_path TEXT,
        created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
        synced INTEGER NOT NULL DEFAULT 0,
        sync_status TEXT NOT NULL DEFAULT 'pending',
        last_sync_at INTEGER
      )
    ''');

    // Índices para mejorar performance
    await db.execute('''
      CREATE UNIQUE INDEX idx_cattle_ear_tag ON $_tableCattle (ear_tag)
    ''');

    await db.execute('''
      CREATE INDEX idx_cattle_breed ON $_tableCattle (breed)
    ''');

    await db.execute('''
      CREATE INDEX idx_cattle_status ON $_tableCattle (status)
    ''');

    await db.execute('''
      CREATE INDEX idx_cattle_registration_date ON $_tableCattle (registration_date DESC)
    ''');

    await db.execute('''
      CREATE INDEX idx_cattle_search ON $_tableCattle (ear_tag, name)
    ''');

    // Índice para sincronización (US-005)
    await db.execute('''
      CREATE INDEX idx_cattle_sync_status ON $_tableCattle (sync_status, synced)
    ''');
  }

  Future<void> _onUpgrade(
    sqflite.Database db,
    int oldVersion,
    int newVersion,
  ) async {
    // Migración v1 -> v2: Agregar columnas de sincronización (US-005)
    if (oldVersion < 2) {
      await db.execute('''
        ALTER TABLE $_tableCattle ADD COLUMN synced INTEGER NOT NULL DEFAULT 0
      ''');
      await db.execute('''
        ALTER TABLE $_tableCattle ADD COLUMN sync_status TEXT NOT NULL DEFAULT 'pending'
      ''');
      await db.execute('''
        ALTER TABLE $_tableCattle ADD COLUMN last_sync_at INTEGER
      ''');
      await db.execute('''
        CREATE INDEX IF NOT EXISTS idx_cattle_sync_status 
        ON $_tableCattle (sync_status, synced)
      ''');
    }
  }

  @override
  Future<void> saveCattle(CattleModel cattle) async {
    try {
      final db = await database;
      await db.insert(
        _tableCattle,
        cattle.toSQLite(),
        conflictAlgorithm: sqflite.ConflictAlgorithm.replace,
      );
    } catch (e) {
      throw DatabaseException(message: 'Error al guardar ganado: $e');
    }
  }

  @override
  Future<CattleModel?> getCattleById(String id) async {
    try {
      final db = await database;
      final maps = await db.query(
        _tableCattle,
        where: 'id = ?',
        whereArgs: [id],
        limit: 1,
      );

      if (maps.isEmpty) return null;
      return CattleModel.fromSQLite(maps.first);
    } catch (e) {
      throw DatabaseException(message: 'Error al obtener ganado: $e');
    }
  }

  @override
  Future<CattleModel?> getCattleByEarTag(String earTag) async {
    try {
      final db = await database;
      final maps = await db.query(
        _tableCattle,
        where: 'ear_tag = ?',
        whereArgs: [earTag],
        limit: 1,
      );

      if (maps.isEmpty) return null;
      return CattleModel.fromSQLite(maps.first);
    } catch (e) {
      throw DatabaseException(message: 'Error al buscar por caravana: $e');
    }
  }

  @override
  Future<List<CattleModel>> getAllCattle() async {
    try {
      final db = await database;
      final maps = await db.query(
        _tableCattle,
        orderBy: 'registration_date DESC',
      );

      return maps.map((map) => CattleModel.fromSQLite(map)).toList();
    } catch (e) {
      throw DatabaseException(message: 'Error al obtener ganado: $e');
    }
  }

  @override
  Future<List<CattleModel>> getActiveCattle() async {
    try {
      final db = await database;
      final maps = await db.query(
        _tableCattle,
        where: 'status = ?',
        whereArgs: ['active'],
        orderBy: 'registration_date DESC',
      );

      return maps.map((map) => CattleModel.fromSQLite(map)).toList();
    } catch (e) {
      throw DatabaseException(message: 'Error al obtener ganado activo: $e');
    }
  }

  @override
  Future<List<CattleModel>> searchCattle(String searchTerm) async {
    try {
      final db = await database;
      final term = '%$searchTerm%';

      final maps = await db.query(
        _tableCattle,
        where: 'ear_tag LIKE ? OR name LIKE ?',
        whereArgs: [term, term],
        orderBy: 'registration_date DESC',
      );

      return maps.map((map) => CattleModel.fromSQLite(map)).toList();
    } catch (e) {
      throw DatabaseException(message: 'Error en búsqueda: $e');
    }
  }

  @override
  Future<void> updateCattle(CattleModel cattle) async {
    try {
      final db = await database;
      await db.update(
        _tableCattle,
        cattle.toSQLite(),
        where: 'id = ?',
        whereArgs: [cattle.id],
      );
    } catch (e) {
      throw DatabaseException(message: 'Error al actualizar ganado: $e');
    }
  }

  @override
  Future<void> deleteCattle(String id) async {
    try {
      final db = await database;
      await db.delete(_tableCattle, where: 'id = ?', whereArgs: [id]);
    } catch (e) {
      throw DatabaseException(message: 'Error al eliminar ganado: $e');
    }
  }

  @override
  Future<bool> earTagExists(String earTag, {String? excludeId}) async {
    try {
      final db = await database;

      String whereClause = 'ear_tag = ?';
      List<dynamic> whereArgs = [earTag];

      if (excludeId != null) {
        whereClause += ' AND id != ?';
        whereArgs.add(excludeId);
      }

      final maps = await db.query(
        _tableCattle,
        where: whereClause,
        whereArgs: whereArgs,
        limit: 1,
      );

      return maps.isNotEmpty;
    } catch (e) {
      throw DatabaseException(message: 'Error al verificar caravana: $e');
    }
  }

  @override
  Future<Map<CattleStatus, int>> getCattleCountByStatus() async {
    try {
      final db = await database;
      final result = <CattleStatus, int>{};

      for (final status in CattleStatus.values) {
        final maps = await db.rawQuery(
          'SELECT COUNT(*) as count FROM $_tableCattle WHERE status = ?',
          [status.value],
        );

        result[status] = maps.first['count'] as int;
      }

      return result;
    } catch (e) {
      throw DatabaseException(message: 'Error al contar ganado: $e');
    }
  }

  // ===== Métodos de Sincronización (US-005) =====

  @override
  Future<List<CattleModel>> getUnsyncedCattle() async {
    try {
      final db = await database;

      final maps = await db.query(
        _tableCattle,
        where: 'synced = ?',
        whereArgs: [0],
        orderBy: 'last_updated ASC',
      );

      return maps.map((map) => CattleModel.fromSQLite(map)).toList();
    } catch (e) {
      throw DatabaseException(message: 'Error al obtener no sincronizados: $e');
    }
  }

  @override
  Future<void> markAsSynced(String id) async {
    try {
      final db = await database;
      final now = DateTime.now().millisecondsSinceEpoch;

      await db.update(
        _tableCattle,
        {'synced': 1, 'sync_status': 'synced', 'last_sync_at': now},
        where: 'id = ?',
        whereArgs: [id],
      );
    } catch (e) {
      throw DatabaseException(message: 'Error al marcar sincronizado: $e');
    }
  }

  @override
  Future<void> markAsSyncError(String id, String error) async {
    try {
      final db = await database;

      await db.update(
        _tableCattle,
        {'synced': 0, 'sync_status': 'error'},
        where: 'id = ?',
        whereArgs: [id],
      );
    } catch (e) {
      throw DatabaseException(message: 'Error al marcar error sync: $e');
    }
  }

  @override
  Future<int> getUnsyncedCount() async {
    try {
      final db = await database;

      final result = await db.rawQuery('''
        SELECT COUNT(*) as count 
        FROM $_tableCattle 
        WHERE synced = 0
      ''');

      return sqflite.Sqflite.firstIntValue(result) ?? 0;
    } catch (e) {
      throw DatabaseException(message: 'Error al contar no sincronizados: $e');
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
}
