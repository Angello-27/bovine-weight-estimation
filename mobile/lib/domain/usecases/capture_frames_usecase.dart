/// UseCase: CaptureFramesUseCase
/// 
/// US-001: Captura Continua de Fotogramas
/// 
/// Caso de uso que implementa la lógica de captura continua de fotogramas
/// a 10-15 FPS durante 3-5 segundos, con evaluación automática de calidad.
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/capture_session.dart';
import '../entities/frame.dart';
import '../repositories/frame_repository.dart';

/// Caso de uso para captura continua de fotogramas (US-001)
class CaptureFramesUseCase implements UseCase<CaptureSession, CaptureParams> {
  final FrameRepository repository;

  CaptureFramesUseCase(this.repository);

  /// Ejecuta la captura continua de fotogramas
  /// 
  /// Parámetros:
  /// - [params]: Parámetros de captura (FPS, duración)
  /// 
  /// Retorna:
  /// - [Right(CaptureSession)]: Sesión completada con fotogramas capturados
  /// - [Left(Failure)]: Error durante la captura
  @override
  Future<Either<Failure, CaptureSession>> call(CaptureParams params) async {
    // 1. Iniciar sesión de captura
    final sessionResult = await repository.startCaptureSession(
      targetFps: params.targetFps,
      durationSeconds: params.durationSeconds,
    );

    return sessionResult.fold(
      (failure) => Left(failure),
      (session) async {
        // 2. Capturar fotogramas continuamente
        final frames = <Frame>[];
        final startTime = DateTime.now();
        final targetFrames = params.targetFps * params.durationSeconds;

        while (frames.length < targetFrames) {
          // Verificar tiempo transcurrido
          final elapsed = DateTime.now().difference(startTime);
          if (elapsed.inSeconds >= params.durationSeconds) {
            break;
          }

          // Capturar fotograma
          final frameResult = await repository.captureFrame(session.id);

          frameResult.fold(
            (failure) {
              // Si hay error en un fotograma, continuar con el siguiente
              // pero registrar el error
              print('Error capturando fotograma: $failure');
            },
            (frame) {
              frames.add(frame);
            },
          );

          // Esperar para mantener FPS objetivo
          // Cálculo: 1000ms / targetFps = ms por fotograma
          final msPerFrame = (1000 / params.targetFps).round();
          await Future.delayed(Duration(milliseconds: msPerFrame));
        }

        // 3. Actualizar sesión con fotogramas capturados
        final completedSession = session.copyWith(
          frames: frames,
          endTime: DateTime.now(),
          status: CaptureSessionStatus.completed,
        );

        // 4. Guardar sesión en SQLite
        await repository.saveCaptureSession(completedSession);

        // 5. Finalizar sesión
        return repository.endCaptureSession(session.id);
      },
    );
  }
}

/// Parámetros para la captura continua de fotogramas
class CaptureParams {
  /// Fotogramas por segundo objetivo (10-15)
  final int targetFps;

  /// Duración de captura en segundos (3-5)
  final int durationSeconds;

  const CaptureParams({
    this.targetFps = 12, // Default: 12 FPS (cumple requisito 10-15 FPS)
    this.durationSeconds = 4, // Default: 4 segundos (cumple requisito 3-5 seg)
  }) : assert(targetFps >= 10 && targetFps <= 15, 'FPS debe estar entre 10-15'),
       assert(durationSeconds >= 3 && durationSeconds <= 5,
           'Duración debe estar entre 3-5 segundos');

  @override
  String toString() =>
      'CaptureParams(targetFps: $targetFps, durationSeconds: $durationSeconds)';
}

