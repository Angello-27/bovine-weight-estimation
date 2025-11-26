/// Provider: CaptureProvider
///
/// Provider para gestionar el estado de captura continua de fotogramas (US-001).
/// Implementa la lógica de UI y comunica con el UseCase.
///
/// Presentation Layer - Clean Architecture + Provider Pattern
library;

import 'dart:async';

import 'package:flutter/material.dart';

import '../../core/theme/app_colors.dart';
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

/// Extensión para mapear estados a propiedades de UI
extension CaptureStateUI on CaptureState {
  /// Ícono representativo del estado
  IconData get icon {
    switch (this) {
      case CaptureState.idle:
        return Icons.camera_alt;
      case CaptureState.capturing:
        return Icons.camera;
      case CaptureState.completed:
        return Icons.check_circle;
      case CaptureState.error:
        return Icons.error;
    }
  }

  /// Color del estado
  Color get color {
    switch (this) {
      case CaptureState.idle:
        return AppColors.primary;
      case CaptureState.capturing:
        return AppColors.info;
      case CaptureState.completed:
        return AppColors.success;
      case CaptureState.error:
        return AppColors.error;
    }
  }

  /// Título del estado
  String get title {
    switch (this) {
      case CaptureState.idle:
        return 'Listo para capturar';
      case CaptureState.capturing:
        return 'Capturando...';
      case CaptureState.completed:
        return 'Completado';
      case CaptureState.error:
        return 'Error';
    }
  }

  /// Descripción del estado
  String get description {
    switch (this) {
      case CaptureState.idle:
        return 'Configura los parámetros y presiona "Iniciar Captura"';
      case CaptureState.capturing:
        return 'Capturando fotogramas continuos';
      case CaptureState.completed:
        return 'Captura finalizada exitosamente';
      case CaptureState.error:
        return 'Ocurrió un error durante la captura';
    }
  }
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

  /// Timer para captura continua
  Timer? _continuousCaptureTimer;

  /// Timestamp de inicio de captura continua
  DateTime? _continuousCaptureStartTime;

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

  /// Inicia captura continua ilimitada (hasta que se detenga manualmente)
  Future<void> startContinuousCapture() async {
    if (_state == CaptureState.capturing) {
      return; // Ya está capturando
    }

    try {
      _state = CaptureState.capturing;
      _errorMessage = null;
      _frames = [];
      _continuousCaptureStartTime = DateTime.now();
      notifyListeners();

      // Iniciar timer para captura continua
      final msPerFrame = (1000 / _targetFps).round();
      _continuousCaptureTimer = Timer.periodic(
        Duration(milliseconds: msPerFrame),
        (timer) async {
          // Capturar frame
          await _captureSingleFrame();
        },
      );
    } catch (e) {
      _state = CaptureState.error;
      _errorMessage = 'Error iniciando captura continua: $e';
      notifyListeners();
    }
  }

  /// Detiene la captura continua
  void stopContinuousCapture() {
    _continuousCaptureTimer?.cancel();
    _continuousCaptureTimer = null;

    if (_frames.isNotEmpty) {
      _state = CaptureState.completed;
    } else {
      _state = CaptureState.idle;
    }

    _continuousCaptureStartTime = null;
    notifyListeners();
  }

  /// Captura un solo frame (usado en captura continua)
  Future<void> _captureSingleFrame() async {
    try {
      // Crear parámetros para un solo frame
      final params = CaptureParams(
        targetFps: _targetFps,
        durationSeconds: 1, // Solo necesitamos 1 segundo para 1 frame
      );

      // Ejecutar caso de uso (capturará 1 frame)
      final result = await captureFramesUseCase.call(params);

      result.fold(
        (failure) {
          // Error en frame individual, continuar con siguiente
          debugPrint('Error capturando frame: ${failure.message}');
        },
        (session) {
          // Agregar frames a la lista
          if (session.frames.isNotEmpty) {
            _frames.addAll(session.frames);
            notifyListeners();
          }
        },
      );
    } catch (e) {
      debugPrint('Error capturando frame: $e');
      // Continuar capturando aunque haya error en un frame
    }
  }

  /// Duración de captura continua (en segundos)
  Duration? get continuousCaptureDuration {
    if (_continuousCaptureStartTime == null) return null;
    return DateTime.now().difference(_continuousCaptureStartTime!);
  }

  /// Libera recursos
  @override
  void dispose() {
    _continuousCaptureTimer?.cancel();
    _frames = [];
    _session = null;
    super.dispose();
  }
}
