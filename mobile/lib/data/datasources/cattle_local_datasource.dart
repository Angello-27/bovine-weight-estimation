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

  /// Cierra la base de datos
  Future<void> close();
}

/// Implementación con SQLite
class CattleLocalDataSourceImpl implements CattleLocalDataSource {
  sqflite.Database? _database;

  static const String _databaseName = 'bovine_weight.db';
  static const int _databaseVersion = 1;
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

      return await sqflite.openDatabase(
        path,
        version: _databaseVersion,
        onCreate: _onCreate,
        onUpgrade: _onUpgrade,
      );
    } catch (e) {
      throw DatabaseException(message: 'Error al inicializar DB: $e');
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
        created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
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
  }

  Future<void> _onUpgrade(
    sqflite.Database db,
    int oldVersion,
    int newVersion,
  ) async {
    // TODO: Migraciones futuras
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

  @override
  Future<void> close() async {
    final db = _database;
    if (db != null) {
      await db.close();
      _database = null;
    }
  }
}
