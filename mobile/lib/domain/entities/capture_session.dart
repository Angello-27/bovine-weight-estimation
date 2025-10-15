/// Entity: CaptureSession (Sesión de Captura)
///
/// Representa una sesión completa de captura continua de fotogramas.
/// Agrupa todos los fotogramas capturados en una sesión de 3-5 segundos.
///
/// Domain Layer - Clean Architecture
library;

import 'package:equatable/equatable.dart';

import 'frame.dart';

/// Sesión de captura continua de fotogramas
class CaptureSession extends Equatable {
  /// Identificador único de la sesión
  final String id;

  /// Timestamp de inicio de la sesión
  final DateTime startTime;

  /// Timestamp de fin de la sesión
  final DateTime? endTime;

  /// Lista de fotogramas capturados
  final List<Frame> frames;

  /// Estado actual de la sesión
  final CaptureSessionStatus status;

  /// Fotograma seleccionado como mejor (si ya se seleccionó)
  final Frame? selectedFrame;

  /// Fotogramas por segundo (FPS) objetivo: 10-15
  final int targetFps;

  /// Duración objetivo en segundos: 3-5
  final int targetDurationSeconds;

  const CaptureSession({
    required this.id,
    required this.startTime,
    this.endTime,
    required this.frames,
    required this.status,
    this.selectedFrame,
    this.targetFps = 12, // Default: 12 FPS
    this.targetDurationSeconds = 4, // Default: 4 segundos
  });

  /// Duración real de la sesión
  Duration? get duration => endTime?.difference(startTime);

  /// Número total de fotogramas capturados
  int get frameCount => frames.length;

  /// FPS real alcanzado
  double? get actualFps {
    if (duration == null || frameCount == 0) return null;
    return frameCount / duration!.inSeconds;
  }

  /// Número esperado de fotogramas (FPS × segundos)
  int get expectedFrameCount => targetFps * targetDurationSeconds;

  /// Porcentaje de progreso (0.0 - 1.0)
  double get progress {
    if (frameCount >= expectedFrameCount) return 1.0;
    return frameCount / expectedFrameCount;
  }

  /// Fotogramas que cumplen criterios óptimos
  List<Frame> get optimalFrames =>
      frames.where((frame) => frame.isOptimal).toList();

  /// Mejor fotograma por score global
  Frame? get bestFrame {
    if (frames.isEmpty) return null;
    return frames.reduce(
      (current, next) =>
          next.globalScore > current.globalScore ? next : current,
    );
  }

  /// Copia la sesión con nuevos valores
  CaptureSession copyWith({
    String? id,
    DateTime? startTime,
    DateTime? endTime,
    List<Frame>? frames,
    CaptureSessionStatus? status,
    Frame? selectedFrame,
    int? targetFps,
    int? targetDurationSeconds,
  }) {
    return CaptureSession(
      id: id ?? this.id,
      startTime: startTime ?? this.startTime,
      endTime: endTime ?? this.endTime,
      frames: frames ?? this.frames,
      status: status ?? this.status,
      selectedFrame: selectedFrame ?? this.selectedFrame,
      targetFps: targetFps ?? this.targetFps,
      targetDurationSeconds:
          targetDurationSeconds ?? this.targetDurationSeconds,
    );
  }

  @override
  List<Object?> get props => [
    id,
    startTime,
    endTime,
    frames,
    status,
    selectedFrame,
    targetFps,
    targetDurationSeconds,
  ];

  @override
  String toString() =>
      'CaptureSession(id: $id, frames: $frameCount, '
      'status: $status, progress: ${(progress * 100).toStringAsFixed(0)}%)';
}

/// Estados posibles de una sesión de captura
enum CaptureSessionStatus {
  /// Sesión no iniciada
  idle,

  /// Capturando fotogramas en tiempo real
  capturing,

  /// Captura completada exitosamente
  completed,

  /// Captura cancelada por el usuario
  cancelled,

  /// Error durante la captura
  error,
}

/// Extensión para obtener descripciones legibles de los estados
extension CaptureSessionStatusExtension on CaptureSessionStatus {
  String get displayName {
    switch (this) {
      case CaptureSessionStatus.idle:
        return 'Listo para capturar';
      case CaptureSessionStatus.capturing:
        return 'Capturando...';
      case CaptureSessionStatus.completed:
        return 'Completado';
      case CaptureSessionStatus.cancelled:
        return 'Cancelado';
      case CaptureSessionStatus.error:
        return 'Error';
    }
  }
}
