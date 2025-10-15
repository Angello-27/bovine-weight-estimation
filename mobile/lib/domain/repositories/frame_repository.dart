/// Repository Interface: FrameRepository
/// 
/// Define el contrato para operaciones relacionadas con fotogramas.
/// Siguiendo Clean Architecture, la implementación estará en Data Layer.
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../entities/capture_session.dart';
import '../entities/frame.dart';

/// Repositorio para operaciones de captura y gestión de fotogramas
abstract class FrameRepository {
  /// Inicia una nueva sesión de captura continua
  /// 
  /// Parámetros:
  /// - [targetFps]: Fotogramas por segundo objetivo (10-15, default: 12)
  /// - [durationSeconds]: Duración de captura en segundos (3-5, default: 4)
  /// 
  /// Retorna:
  /// - [Right(CaptureSession)]: Sesión iniciada correctamente
  /// - [Left(Failure)]: Error al iniciar sesión
  Future<Either<Failure, CaptureSession>> startCaptureSession({
    int targetFps = 12,
    int durationSeconds = 4,
  });

  /// Captura un fotograma durante la sesión activa
  /// 
  /// Parámetros:
  /// - [sessionId]: ID de la sesión de captura activa
  /// 
  /// Retorna:
  /// - [Right(Frame)]: Fotograma capturado con métricas de calidad
  /// - [Left(Failure)]: Error al capturar fotograma
  Future<Either<Failure, Frame>> captureFrame(String sessionId);

  /// Evalúa la calidad de un fotograma
  /// 
  /// Calcula métricas de calidad (nitidez, iluminación, contraste, silueta, ángulo)
  /// 
  /// Parámetros:
  /// - [imagePath]: Path de la imagen a evaluar
  /// 
  /// Retorna:
  /// - [Right(FrameQuality)]: Métricas calculadas
  /// - [Left(Failure)]: Error al evaluar calidad
  Future<Either<Failure, FrameQuality>> evaluateFrameQuality(String imagePath);

  /// Finaliza la sesión de captura actual
  /// 
  /// Parámetros:
  /// - [sessionId]: ID de la sesión a finalizar
  /// 
  /// Retorna:
  /// - [Right(CaptureSession)]: Sesión finalizada con todos los fotogramas
  /// - [Left(Failure)]: Error al finalizar sesión
  Future<Either<Failure, CaptureSession>> endCaptureSession(String sessionId);

  /// Cancela la sesión de captura actual
  /// 
  /// Parámetros:
  /// - [sessionId]: ID de la sesión a cancelar
  /// 
  /// Retorna:
  /// - [Right(void)]: Sesión cancelada exitosamente
  /// - [Left(Failure)]: Error al cancelar sesión
  Future<Either<Failure, void>> cancelCaptureSession(String sessionId);

  /// Obtiene la sesión de captura actual (si existe)
  /// 
  /// Retorna:
  /// - [Right(CaptureSession?)]: Sesión actual o null si no hay sesión activa
  /// - [Left(Failure)]: Error al obtener sesión
  Future<Either<Failure, CaptureSession?>> getCurrentSession();

  /// Guarda una sesión de captura en almacenamiento local (SQLite)
  /// 
  /// Parámetros:
  /// - [session]: Sesión a guardar
  /// 
  /// Retorna:
  /// - [Right(void)]: Sesión guardada exitosamente
  /// - [Left(Failure)]: Error al guardar sesión
  Future<Either<Failure, void>> saveCaptureSession(CaptureSession session);

  /// Obtiene todas las sesiones de captura guardadas
  /// 
  /// Retorna:
  /// - [Right(List<CaptureSession>)]: Lista de sesiones guardadas
  /// - [Left(Failure)]: Error al obtener sesiones
  Future<Either<Failure, List<CaptureSession>>> getSavedSessions();

  /// Elimina una sesión de captura guardada
  /// 
  /// Parámetros:
  /// - [sessionId]: ID de la sesión a eliminar
  /// 
  /// Retorna:
  /// - [Right(void)]: Sesión eliminada exitosamente
  /// - [Left(Failure)]: Error al eliminar sesión
  Future<Either<Failure, void>> deleteCaptureSession(String sessionId);
}

