/// DataSource: FrameLocalDataSource
///
/// DataSource para almacenamiento local (SQLite) de fotogramas y sesiones.
/// Implementa operaciones CRUD offline-first.
///
/// Data Layer - Clean Architecture
library;

import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart' as sqflite;

import '../../core/errors/exceptions.dart';
import '../models/capture_session_model.dart';
import '../models/frame_model.dart';

/// DataSource para almacenamiento local de frames
abstract class FrameLocalDataSource {
  /// Guarda una sesión de captura
  Future<void> saveCaptureSession(CaptureSessionModel session);

  /// Obtiene una sesión por ID
  Future<CaptureSessionModel?> getCaptureSession(String sessionId);

  /// Obtiene todas las sesiones guardadas
  Future<List<CaptureSessionModel>> getAllCaptureSessions();

  /// Elimina una sesión por ID
  Future<void> deleteCaptureSession(String sessionId);

  /// Guarda un fotograma asociado a una sesión
  Future<void> saveFrame(FrameModel frame, String sessionId);

  /// Obtiene todos los fotogramas de una sesión
  Future<List<FrameModel>> getFramesBySession(String sessionId);

  /// Cierra la base de datos
  Future<void> close();
}

/// Implementación del FrameLocalDataSource usando SQLite
class FrameLocalDataSourceImpl implements FrameLocalDataSource {
  sqflite.Database? _database;

  /// Nombre de la base de datos
  static const String _databaseName = 'bovine_weight.db';
  static const int _databaseVersion = 1;

  /// Nombres de tablas
  static const String _tableSessions = 'capture_sessions';
  static const String _tableFrames = 'frames';

  /// Obtiene la instancia de la base de datos (lazy loading)
  Future<sqflite.Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  /// Inicializa la base de datos SQLite
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

  /// Crea las tablas de la base de datos
  Future<void> _onCreate(sqflite.Database db, int version) async {
    // Tabla de sesiones de captura
    await db.execute('''
      CREATE TABLE $_tableSessions (
        id TEXT PRIMARY KEY,
        start_time INTEGER NOT NULL,
        end_time INTEGER,
        status TEXT NOT NULL,
        selected_frame_id TEXT,
        target_fps INTEGER NOT NULL DEFAULT 12,
        target_duration_seconds INTEGER NOT NULL DEFAULT 4,
        created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
        updated_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
      )
    ''');

    // Tabla de fotogramas
    await db.execute('''
      CREATE TABLE $_tableFrames (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        sharpness REAL NOT NULL,
        brightness REAL NOT NULL,
        contrast REAL NOT NULL,
        silhouette_visibility REAL NOT NULL,
        angle_score REAL NOT NULL,
        global_score REAL NOT NULL,
        created_at INTEGER NOT NULL DEFAULT (strftime('%s', 'now')),
        FOREIGN KEY (session_id) REFERENCES $_tableSessions (id) ON DELETE CASCADE
      )
    ''');

    // Índices para mejorar performance
    await db.execute('''
      CREATE INDEX idx_frames_session_id ON $_tableFrames (session_id)
    ''');

    await db.execute('''
      CREATE INDEX idx_sessions_status ON $_tableSessions (status)
    ''');

    await db.execute('''
      CREATE INDEX idx_frames_global_score ON $_tableFrames (global_score DESC)
    ''');
  }

  /// Maneja upgrades de la base de datos
  Future<void> _onUpgrade(
    sqflite.Database db,
    int oldVersion,
    int newVersion,
  ) async {
    // TODO: Implementar migraciones si cambia el esquema
    if (oldVersion < newVersion) {
      // Ejemplo: ALTER TABLE, CREATE INDEX, etc.
    }
  }

  @override
  Future<void> saveCaptureSession(CaptureSessionModel session) async {
    try {
      final db = await database;

      // Guardar sesión
      await db.insert(
        _tableSessions,
        session.toSQLite(),
        conflictAlgorithm: sqflite.ConflictAlgorithm.replace,
      );

      // Guardar fotogramas asociados
      for (final frame in session.frames) {
        await saveFrame(FrameModel.fromEntity(frame), session.id);
      }
    } catch (e) {
      throw DatabaseException(message: 'Error al guardar sesión: $e');
    }
  }

  @override
  Future<CaptureSessionModel?> getCaptureSession(String sessionId) async {
    try {
      final db = await database;

      // Obtener sesión
      final sessionMaps = await db.query(
        _tableSessions,
        where: 'id = ?',
        whereArgs: [sessionId],
        limit: 1,
      );

      if (sessionMaps.isEmpty) return null;

      final sessionModel = CaptureSessionModel.fromSQLite(sessionMaps.first);

      // Obtener fotogramas de la sesión
      final frames = await getFramesBySession(sessionId);

      // Obtener fotograma seleccionado si existe
      FrameModel? selectedFrame;
      final selectedFrameId = sessionMaps.first['selected_frame_id'] as String?;
      if (selectedFrameId != null) {
        selectedFrame = frames.firstWhere(
          (frame) => frame.id == selectedFrameId,
          orElse: () => frames.first,
        );
      }

      return sessionModel.copyWith(
        frames: frames,
        selectedFrame: selectedFrame,
      );
    } catch (e) {
      throw DatabaseException(message: 'Error al obtener sesión: $e');
    }
  }

  @override
  Future<List<CaptureSessionModel>> getAllCaptureSessions() async {
    try {
      final db = await database;

      final sessionMaps = await db.query(
        _tableSessions,
        orderBy: 'start_time DESC',
      );

      final sessions = <CaptureSessionModel>[];

      for (final sessionMap in sessionMaps) {
        final sessionId = sessionMap['id'] as String;
        final session = await getCaptureSession(sessionId);
        if (session != null) {
          sessions.add(session);
        }
      }

      return sessions;
    } catch (e) {
      throw DatabaseException(message: 'Error al obtener sesiones: $e');
    }
  }

  @override
  Future<void> deleteCaptureSession(String sessionId) async {
    try {
      final db = await database;

      // Eliminar sesión (CASCADE eliminará los fotogramas automáticamente)
      await db.delete(_tableSessions, where: 'id = ?', whereArgs: [sessionId]);
    } catch (e) {
      throw DatabaseException(message: 'Error al eliminar sesión: $e');
    }
  }

  @override
  Future<void> saveFrame(FrameModel frame, String sessionId) async {
    try {
      final db = await database;

      final frameData = frame.toSQLite();
      frameData['session_id'] = sessionId;

      await db.insert(
        _tableFrames,
        frameData,
        conflictAlgorithm: sqflite.ConflictAlgorithm.replace,
      );
    } catch (e) {
      throw DatabaseException(message: 'Error al guardar fotograma: $e');
    }
  }

  @override
  Future<List<FrameModel>> getFramesBySession(String sessionId) async {
    try {
      final db = await database;

      final frameMaps = await db.query(
        _tableFrames,
        where: 'session_id = ?',
        whereArgs: [sessionId],
        orderBy: 'timestamp ASC',
      );

      return frameMaps.map((map) => FrameModel.fromSQLite(map)).toList();
    } catch (e) {
      throw DatabaseException(message: 'Error al obtener fotogramas: $e');
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
