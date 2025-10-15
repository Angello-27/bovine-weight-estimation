/// Repository Implementation: FrameRepositoryImpl
/// 
/// Implementación del FrameRepository que coordina CameraDataSource y LocalDataSource.
/// Maneja la lógica de almacenamiento offline-first.
///
/// Data Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';
import 'package:uuid/uuid.dart';

import '../../core/errors/exceptions.dart';
import '../../core/errors/failures.dart';
import '../../domain/entities/capture_session.dart';
import '../../domain/entities/frame.dart';
import '../../domain/repositories/frame_repository.dart';
import '../datasources/camera_datasource.dart';
import '../datasources/frame_local_datasource.dart';
import '../models/capture_session_model.dart';
import '../models/frame_model.dart';

/// Implementación del repositorio de fotogramas
class FrameRepositoryImpl implements FrameRepository {
  final CameraDataSource cameraDataSource;
  final FrameLocalDataSource localDataSource;
  final Uuid _uuid = const Uuid();

  /// Sesión actual en memoria
  CaptureSessionModel? _currentSession;

  FrameRepositoryImpl({
    required this.cameraDataSource,
    required this.localDataSource,
  });

  @override
  Future<Either<Failure, CaptureSession>> startCaptureSession({
    int targetFps = 12,
    int durationSeconds = 4,
  }) async {
    try {
      // Validar parámetros
      if (targetFps < 10 || targetFps > 15) {
        return const Left(ValidationFailure(
          message: 'FPS debe estar entre 10-15',
        ));
      }

      if (durationSeconds < 3 || durationSeconds > 5) {
        return const Left(ValidationFailure(
          message: 'Duración debe estar entre 3-5 segundos',
        ));
      }

      // Crear nueva sesión
      final sessionId = _uuid.v4();
      final session = CaptureSessionModel(
        id: sessionId,
        startTime: DateTime.now(),
        frames: const [],
        status: CaptureSessionStatus.capturing,
        targetFps: targetFps,
        targetDurationSeconds: durationSeconds,
      );

      // Guardar sesión en memoria
      _currentSession = session;

      return Right(session);
    } on ValidationException catch (e) {
      return Left(ValidationFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al iniciar sesión: $e'));
    }
  }

  @override
  Future<Either<Failure, Frame>> captureFrame(String sessionId) async {
    try {
      // Verificar que existe sesión activa
      if (_currentSession == null || _currentSession!.id != sessionId) {
        return const Left(ValidationFailure(
          message: 'No hay sesión activa con ese ID',
        ));
      }

      // TODO: Inicializar cámara si no está inicializada
      // Por ahora, creamos fotograma mock para testing
      // En producción, usar: cameraDataSource.captureFrame(controller)

      // MOCK: Crear fotograma de prueba
      final frame = FrameModel(
        id: _uuid.v4(),
        timestamp: DateTime.now(),
        imagePath: '/tmp/mock_frame_${DateTime.now().millisecondsSinceEpoch}.jpg',
        quality: const FrameQuality(
          sharpness: 0.75,
          brightness: 0.6,
          contrast: 0.65,
          silhouetteVisibility: 0.85,
          angleScore: 0.7,
        ),
        globalScore: 0.75,
      );

      // Agregar fotograma a la sesión actual
      final updatedFrames = List<Frame>.from(_currentSession!.frames)..add(frame);
      _currentSession = _currentSession!.copyWith(frames: updatedFrames);

      return Right(frame);
    } on CameraException catch (e) {
      return Left(CameraFailure(message: e.message));
    } on StorageException catch (e) {
      return Left(StorageFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al capturar fotograma: $e'));
    }
  }

  @override
  Future<Either<Failure, FrameQuality>> evaluateFrameQuality(
    String imagePath,
  ) async {
    try {
      // Evaluar calidad usando CameraDataSource
      final quality = await cameraDataSource.evaluateFrameQuality(imagePath);
      return Right(quality);
    } on CameraException catch (e) {
      return Left(FrameQualityFailure(message: e.message));
    } on StorageException catch (e) {
      return Left(StorageFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al evaluar calidad: $e'));
    }
  }

  @override
  Future<Either<Failure, CaptureSession>> endCaptureSession(
    String sessionId,
  ) async {
    try {
      if (_currentSession == null || _currentSession!.id != sessionId) {
        return const Left(ValidationFailure(
          message: 'No hay sesión activa con ese ID',
        ));
      }

      // Marcar sesión como completada
      final completedSession = _currentSession!.copyWith(
        endTime: DateTime.now(),
        status: CaptureSessionStatus.completed,
      );

      // Guardar sesión en SQLite
      await localDataSource.saveCaptureSession(completedSession);

      // Limpiar sesión actual
      _currentSession = null;

      return Right(completedSession);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al finalizar sesión: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> cancelCaptureSession(String sessionId) async {
    try {
      if (_currentSession == null || _currentSession!.id != sessionId) {
        return const Left(ValidationFailure(
          message: 'No hay sesión activa con ese ID',
        ));
      }

      // Marcar sesión como cancelada
      _currentSession = _currentSession!.copyWith(
        endTime: DateTime.now(),
        status: CaptureSessionStatus.cancelled,
      );

      // Limpiar sesión actual (no guardar sesiones canceladas)
      _currentSession = null;

      return const Right(null);
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al cancelar sesión: $e'));
    }
  }

  @override
  Future<Either<Failure, CaptureSession?>> getCurrentSession() async {
    try {
      return Right(_currentSession);
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al obtener sesión actual: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> saveCaptureSession(
    CaptureSession session,
  ) async {
    try {
      final sessionModel = CaptureSessionModel.fromEntity(session);
      await localDataSource.saveCaptureSession(sessionModel);
      return const Right(null);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al guardar sesión: $e'));
    }
  }

  @override
  Future<Either<Failure, List<CaptureSession>>> getSavedSessions() async {
    try {
      final sessions = await localDataSource.getAllCaptureSessions();
      return Right(sessions);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al obtener sesiones: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> deleteCaptureSession(String sessionId) async {
    try {
      await localDataSource.deleteCaptureSession(sessionId);
      return const Right(null);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al eliminar sesión: $e'));
    }
  }
}

