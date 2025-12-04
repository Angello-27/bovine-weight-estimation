/// DataSource: WeightEstimationLocalDataSource
///
/// DataSource para almacenamiento local (SQLite) de estimaciones de peso.
/// Single Responsibility: Operaciones CRUD de estimaciones en SQLite.
///
/// Data Layer - Clean Architecture
library;

import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart' as sqflite;

import '../../core/errors/exceptions.dart';
import '../models/weight_estimation_model.dart';

/// DataSource para almacenamiento local de estimaciones
abstract class WeightEstimationLocalDataSource {
  /// Guarda una estimación
  Future<void> saveEstimation(WeightEstimationModel estimation);

  /// Obtiene una estimación por ID
  Future<WeightEstimationModel?> getEstimation(String estimationId);

  /// Obtiene todas las estimaciones
  Future<List<WeightEstimationModel>> getAllEstimations();

  /// Obtiene estimaciones de un animal específico
  Future<List<WeightEstimationModel>> getEstimationsByCattle(String cattleId);

  /// Obtiene la última estimación de un animal
  Future<WeightEstimationModel?> getLastEstimation(String cattleId);

  /// Elimina una estimación
  Future<void> deleteEstimation(String estimationId);

  /// ===== Métodos de Sincronización (US-005) =====

  /// Obtiene estimaciones no sincronizadas
  Future<List<WeightEstimationModel>> getUnsyncedEstimations();

  /// Marca una estimación como sincronizada
  Future<void> markAsSynced(String id);

  /// Marca una estimación con error de sincronización
  Future<void> markAsSyncError(String id, String error);

  /// Obtiene el conteo de estimaciones pendientes de sincronización
  Future<int> getUnsyncedCount();

  /// Cierra la base de datos
  Future<void> close();
}

/// Implementación con SQLite
class WeightEstimationLocalDataSourceImpl
    implements WeightEstimationLocalDataSource {
  sqflite.Database? _database;

  static const String _databaseName = 'bovine_weight.db';
  static const int _databaseVersion = 2; // v2: Columnas sync (US-005)
  static const String _tableEstimations = 'weight_estimations';

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
      throw DatabaseException(
        message: 'Error al inicializar base de datos: $e',
      );
    }
  }

  /// Asegura que las tablas existan (por si otro DataSource creó la DB primero)
  Future<void> _ensureTablesExist(sqflite.Database db) async {
    try {
      // Verificar si la tabla existe
      final tables = await db.rawQuery(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        [_tableEstimations],
      );

      if (tables.isEmpty) {
        // La tabla no existe, crearla
        await _onCreate(db, _databaseVersion);
      }
    } catch (e) {
      // Si hay error, intentar crear la tabla de nuevo
      try {
        await _onCreate(db, _databaseVersion);
      } catch (e2) {
        // Ignorar si la tabla ya existe
      }
    }
  }

  /// Crea las tablas
  Future<void> _onCreate(sqflite.Database db, int version) async {
    // Tabla de estimaciones de peso
    await db.execute('''
      CREATE TABLE $_tableEstimations (
        id TEXT PRIMARY KEY,
        cattle_id TEXT,
        breed TEXT NOT NULL,
        estimated_weight REAL NOT NULL,
        confidence_score REAL NOT NULL,
        frame_image_path TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        gps_latitude REAL,
        gps_longitude REAL,
        method TEXT NOT NULL DEFAULT 'tflite',
        model_version TEXT NOT NULL DEFAULT '1.0.0',
        processing_time_ms INTEGER NOT NULL,
        created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
        updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
        synced INTEGER NOT NULL DEFAULT 0,
        sync_status TEXT NOT NULL DEFAULT 'pending',
        last_sync_at INTEGER
      )
    ''');

    // Índices para mejorar performance
    await db.execute('''
      CREATE INDEX idx_estimations_cattle_id ON $_tableEstimations (cattle_id)
    ''');

    await db.execute('''
      CREATE INDEX idx_estimations_timestamp ON $_tableEstimations (timestamp DESC)
    ''');

    await db.execute('''
      CREATE INDEX idx_estimations_breed ON $_tableEstimations (breed)
    ''');

    await db.execute('''
      CREATE INDEX idx_estimations_confidence ON $_tableEstimations (confidence_score DESC)
    ''');

    // Índice para sincronización (US-005)
    await db.execute('''
      CREATE INDEX idx_estimations_sync_status ON $_tableEstimations (sync_status, synced)
    ''');
  }

  /// Maneja upgrades
  Future<void> _onUpgrade(
    sqflite.Database db,
    int oldVersion,
    int newVersion,
  ) async {
    // Migración v1 -> v2: Agregar columnas de sincronización (US-005)
    if (oldVersion < 2) {
      await db.execute('''
        ALTER TABLE $_tableEstimations ADD COLUMN synced INTEGER NOT NULL DEFAULT 0
      ''');
      await db.execute('''
        ALTER TABLE $_tableEstimations ADD COLUMN sync_status TEXT NOT NULL DEFAULT 'pending'
      ''');
      await db.execute('''
        ALTER TABLE $_tableEstimations ADD COLUMN last_sync_at INTEGER
      ''');
      await db.execute('''
        CREATE INDEX IF NOT EXISTS idx_estimations_sync_status 
        ON $_tableEstimations (sync_status, synced)
      ''');
    }
  }

  @override
  Future<void> saveEstimation(WeightEstimationModel estimation) async {
    try {
      final db = await database;

      await db.insert(
        _tableEstimations,
        estimation.toSQLite(),
        conflictAlgorithm: sqflite.ConflictAlgorithm.replace,
      );
    } catch (e) {
      throw DatabaseException(message: 'Error al guardar estimación: $e');
    }
  }

  @override
  Future<WeightEstimationModel?> getEstimation(String estimationId) async {
    try {
      final db = await database;

      final maps = await db.query(
        _tableEstimations,
        where: 'id = ?',
        whereArgs: [estimationId],
        limit: 1,
      );

      if (maps.isEmpty) return null;

      return WeightEstimationModel.fromSQLite(maps.first);
    } catch (e) {
      throw DatabaseException(message: 'Error al obtener estimación: $e');
    }
  }

  @override
  Future<List<WeightEstimationModel>> getAllEstimations() async {
    try {
      final db = await database;

      final maps = await db.query(_tableEstimations, orderBy: 'timestamp DESC');

      return maps.map((map) => WeightEstimationModel.fromSQLite(map)).toList();
    } catch (e) {
      throw DatabaseException(message: 'Error al obtener estimaciones: $e');
    }
  }

  @override
  Future<List<WeightEstimationModel>> getEstimationsByCattle(
    String cattleId,
  ) async {
    try {
      final db = await database;

      final maps = await db.query(
        _tableEstimations,
        where: 'cattle_id = ?',
        whereArgs: [cattleId],
        orderBy: 'timestamp DESC',
      );

      return maps.map((map) => WeightEstimationModel.fromSQLite(map)).toList();
    } catch (e) {
      throw DatabaseException(
        message: 'Error al obtener estimaciones del animal: $e',
      );
    }
  }

  @override
  Future<WeightEstimationModel?> getLastEstimation(String cattleId) async {
    try {
      final db = await database;

      final maps = await db.query(
        _tableEstimations,
        where: 'cattle_id = ?',
        whereArgs: [cattleId],
        orderBy: 'timestamp DESC',
        limit: 1,
      );

      if (maps.isEmpty) return null;

      return WeightEstimationModel.fromSQLite(maps.first);
    } catch (e) {
      throw DatabaseException(
        message: 'Error al obtener última estimación: $e',
      );
    }
  }

  @override
  Future<void> deleteEstimation(String estimationId) async {
    try {
      final db = await database;

      await db.delete(
        _tableEstimations,
        where: 'id = ?',
        whereArgs: [estimationId],
      );
    } catch (e) {
      throw DatabaseException(message: 'Error al eliminar estimación: $e');
    }
  }

  // ===== Métodos de Sincronización (US-005) =====

  @override
  Future<List<WeightEstimationModel>> getUnsyncedEstimations() async {
    try {
      final db = await database;

      final maps = await db.query(
        _tableEstimations,
        where: 'synced = ?',
        whereArgs: [0],
        orderBy: 'timestamp ASC',
      );

      return maps.map((map) => WeightEstimationModel.fromSQLite(map)).toList();
    } catch (e) {
      throw DatabaseException(
        message: 'Error al obtener estimaciones no sincronizadas: $e',
      );
    }
  }

  @override
  Future<void> markAsSynced(String id) async {
    try {
      final db = await database;
      final now = DateTime.now().millisecondsSinceEpoch;

      await db.update(
        _tableEstimations,
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
        _tableEstimations,
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
        FROM $_tableEstimations 
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
