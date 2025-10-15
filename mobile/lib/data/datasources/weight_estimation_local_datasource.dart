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

  /// Cierra la base de datos
  Future<void> close();
}

/// Implementación con SQLite
class WeightEstimationLocalDataSourceImpl
    implements WeightEstimationLocalDataSource {
  sqflite.Database? _database;

  static const String _databaseName = 'bovine_weight.db';
  static const int _databaseVersion = 1;
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

      return await sqflite.openDatabase(
        path,
        version: _databaseVersion,
        onCreate: _onCreate,
        onUpgrade: _onUpgrade,
      );
    } catch (e) {
      throw DatabaseException(
        message: 'Error al inicializar base de datos: $e',
      );
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
        updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
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
  }

  /// Maneja upgrades
  Future<void> _onUpgrade(
    sqflite.Database db,
    int oldVersion,
    int newVersion,
  ) async {
    // TODO: Implementar migraciones
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

  @override
  Future<void> close() async {
    final db = _database;
    if (db != null) {
      await db.close();
      _database = null;
    }
  }
}
