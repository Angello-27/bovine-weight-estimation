/// Provider: CaptureProvider
///
/// Provider para gestionar el estado de captura continua de fotogramas (US-001).
/// Implementa la lógica de UI y comunica con el UseCase.
///
/// Presentation Layer - Clean Architecture + Provider Pattern
library;

import 'package:flutter/foundation.dart';

import '../../domain/entities/capture_session.dart';
import '../../domain/entities/frame.dart';
import '../../domain/usecases/capture_frames_usecase.dart';

/// Estados posibles de la captura
enum CaptureState {
  /// Estado inicial, listo para capturar
  idle,

  /// Capturando fotogramas
  capturing,

  /// Captura completada exitosamente
  completed,

  /// Error durante la captura
  error,
}

/// Provider para gestionar el estado de captura de fotogramas
class CaptureProvider with ChangeNotifier {
  final CaptureFramesUseCase captureFramesUseCase;

  /// Estado actual
  CaptureState _state = CaptureState.idle;

  /// Sesión de captura actual
  CaptureSession? _session;

  /// Mensaje de error (si existe)
  String? _errorMessage;

  /// Fotogramas capturados en la sesión actual
  List<Frame> _frames = [];

  /// FPS objetivo (10-15)
  int _targetFps = 12;

  /// Duración objetivo en segundos (3-5)
  int _targetDurationSeconds = 4;

  CaptureProvider({required this.captureFramesUseCase});

  // Getters
  CaptureState get state => _state;
  CaptureSession? get session => _session;
  String? get errorMessage => _errorMessage;
  List<Frame> get frames => _frames;
  int get targetFps => _targetFps;
  int get targetDurationSeconds => _targetDurationSeconds;

  /// Progreso de captura (0.0 - 1.0)
  double get progress {
    if (_session == null) return 0.0;
    return _session!.progress;
  }

  /// Número de fotogramas capturados
  int get frameCount => _frames.length;

  /// Número esperado de fotogramas
  int get expectedFrameCount => _targetFps * _targetDurationSeconds;

  /// Fotogramas óptimos (cumplen criterios)
  List<Frame> get optimalFrames =>
      _frames.where((frame) => frame.isOptimal).toList();

  /// Mejor fotograma por score global
  Frame? get bestFrame {
    if (_frames.isEmpty) return null;
    return _frames.reduce(
      (current, next) =>
          next.globalScore > current.globalScore ? next : current,
    );
  }

  /// Indica si la captura está en progreso
  bool get isCapturing => _state == CaptureState.capturing;

  /// Indica si hay un error
  bool get hasError => _state == CaptureState.error;

  /// Configura FPS objetivo
  void setTargetFps(int fps) {
    if (fps >= 10 && fps <= 15) {
      _targetFps = fps;
      notifyListeners();
    }
  }

  /// Configura duración objetivo
  void setTargetDuration(int seconds) {
    if (seconds >= 3 && seconds <= 5) {
      _targetDurationSeconds = seconds;
      notifyListeners();
    }
  }

  /// Inicia la captura continua de fotogramas
  Future<void> startCapture() async {
    try {
      // Cambiar estado a capturing
      _state = CaptureState.capturing;
      _errorMessage = null;
      _frames = [];
      notifyListeners();

      // Crear parámetros de captura
      final params = CaptureParams(
        targetFps: _targetFps,
        durationSeconds: _targetDurationSeconds,
      );

      // Ejecutar caso de uso
      final result = await captureFramesUseCase.call(params);

      result.fold(
        // Error
        (failure) {
          _state = CaptureState.error;
          _errorMessage = failure.message;
          _session = null;
          _frames = [];
          notifyListeners();
        },
        // Éxito
        (session) {
          _state = CaptureState.completed;
          _session = session;
          _frames = session.frames;
          _errorMessage = null;
          notifyListeners();
        },
      );
    } catch (e) {
      _state = CaptureState.error;
      _errorMessage = 'Error inesperado: $e';
      _session = null;
      _frames = [];
      notifyListeners();
    }
  }

  /// Reinicia el provider a estado inicial
  void reset() {
    _state = CaptureState.idle;
    _session = null;
    _errorMessage = null;
    _frames = [];
    notifyListeners();
  }

  /// Libera recursos
  @override
  void dispose() {
    _frames = [];
    _session = null;
    super.dispose();
  }
}
