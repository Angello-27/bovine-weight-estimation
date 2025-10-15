/// Unit Test: CaptureFramesUseCase
///
/// Tests unitarios para el caso de uso de captura continua de fotogramas.
///
/// Testing Layer
library;

import 'package:bovine_weight_mobile/core/errors/failures.dart';
import 'package:bovine_weight_mobile/domain/entities/capture_session.dart';
import 'package:bovine_weight_mobile/domain/repositories/frame_repository.dart';
import 'package:bovine_weight_mobile/domain/usecases/capture_frames_usecase.dart';
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

// Generar mocks: flutter pub run build_runner build
@GenerateMocks([FrameRepository])
import 'capture_frames_usecase_test.mocks.dart';

void main() {
  late CaptureFramesUseCase useCase;
  late MockFrameRepository mockRepository;

  setUp(() {
    mockRepository = MockFrameRepository();
    useCase = CaptureFramesUseCase(mockRepository);
  });

  group('CaptureFramesUseCase', () {
    const tSessionId = 'test-session-id';
    final tSession = CaptureSession(
      id: tSessionId,
      startTime: DateTime.now(),
      frames: const [],
      status: CaptureSessionStatus.idle,
      targetFps: 12,
      targetDurationSeconds: 4,
    );

    test('debe iniciar sesión de captura correctamente', () async {
      // Arrange
      when(
        mockRepository.startCaptureSession(
          targetFps: anyNamed('targetFps'),
          durationSeconds: anyNamed('durationSeconds'),
        ),
      ).thenAnswer((_) async => Right(tSession));

      const tParams = CaptureParams(targetFps: 12, durationSeconds: 4);

      // Act
      final result = await useCase.call(tParams);

      // Assert
      expect(result.isRight(), true);
      verify(
        mockRepository.startCaptureSession(targetFps: 12, durationSeconds: 4),
      ).called(1);
    });

    test('debe retornar ValidationFailure con FPS inválido', () async {
      // Arrange
      // FPS fuera de rango 10-15

      // Act & Assert
      expect(
        () => CaptureParams(targetFps: 9, durationSeconds: 4),
        throwsA(isA<AssertionError>()),
      );
    });

    test('debe retornar ValidationFailure con duración inválida', () async {
      // Arrange
      // Duración fuera de rango 3-5

      // Act & Assert
      expect(
        () => CaptureParams(targetFps: 12, durationSeconds: 6),
        throwsA(isA<AssertionError>()),
      );
    });

    test('debe manejar error del repositorio correctamente', () async {
      // Arrange
      when(
        mockRepository.startCaptureSession(
          targetFps: anyNamed('targetFps'),
          durationSeconds: anyNamed('durationSeconds'),
        ),
      ).thenAnswer(
        (_) async =>
            const Left(CameraFailure(message: 'Error al acceder a la cámara')),
      );

      const tParams = CaptureParams(targetFps: 12, durationSeconds: 4);

      // Act
      final result = await useCase.call(tParams);

      // Assert
      expect(result.isLeft(), true);
      result.fold(
        (failure) => expect(failure, isA<CameraFailure>()),
        (_) => fail('Should return failure'),
      );
    });
  });
}
