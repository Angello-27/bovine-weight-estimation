/// Provider: CaptureProvider
///
/// Provider para gestionar el estado de captura continua de fotogramas (US-001).
/// Implementa la lógica de UI y comunica con el UseCase.
///
/// Presentation Layer - Clean Architecture + Provider Pattern
library;

import 'dart:async';

import 'package:camera/camera.dart' as camera;
import 'package:flutter/material.dart';

import '../../core/config/dependency_injection.dart';
import '../../core/constants/breeds.dart';
import '../../core/theme/app_colors.dart';
import '../../domain/entities/capture_session.dart';
import '../../domain/entities/frame.dart';
import '../../domain/entities/weight_estimation.dart';
import '../../domain/usecases/capture_frames_usecase.dart';
import '../../domain/usecases/estimate_weight_usecase.dart';

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
  final EstimateWeightUseCase?
  estimateWeightUseCase; // Opcional para estimación

  /// Estado actual
  CaptureState _state = CaptureState.idle;

  /// Sesión de captura actual
  CaptureSession? _session;

  /// Mensaje de error (si existe)
  String? _errorMessage;

  /// Fotogramas capturados en la sesión actual
  List<Frame> _frames = [];

  /// FPS objetivo (se lee desde settings, default: 5)
  int _targetFps = 5;

  /// Duración objetivo en segundos (3-5)
  int _targetDurationSeconds = 4;

  /// Timer para captura continua
  Timer? _continuousCaptureTimer;

  /// Timestamp de inicio de captura continua
  DateTime? _continuousCaptureStartTime;

  /// Controller de la cámara (se establece desde CapturePage)
  camera.CameraController? _cameraController;

  /// Flag para evitar capturas simultáneas
  bool _isCapturingFrame = false;

  /// Última estimación de peso (resultado del servidor)
  WeightEstimation? _lastEstimation;

  /// Estado de estimación
  bool _isEstimating = false;
  String? _estimationError;

  CaptureProvider({
    required this.captureFramesUseCase,
    this.estimateWeightUseCase,
  });

  /// Establece el controller de la cámara (llamado desde CapturePage)
  void setCameraController(camera.CameraController? controller) {
    _cameraController = controller;
  }

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

  /// Última estimación de peso
  WeightEstimation? get lastEstimation => _lastEstimation;

  /// Elimina un frame específico de la lista
  /// Si se elimina el mejor frame, se recalcula automáticamente
  void removeFrame(Frame frame) {
    _frames.removeWhere((f) => f.id == frame.id);
    notifyListeners();
  }

  /// Indica si está estimando peso
  bool get isEstimating => _isEstimating;

  /// Error de estimación (si existe)
  String? get estimationError => _estimationError;

  /// Configura FPS objetivo (1-10)
  void setTargetFps(int fps) {
    final clampedFps = fps.clamp(1, 10);
    _targetFps = clampedFps;
    notifyListeners();
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
      // Usar FPS configurado (ya está validado en 1-10)
      final msPerFrame = (1000 / _targetFps).round();
      _continuousCaptureTimer = Timer.periodic(
        Duration(milliseconds: msPerFrame),
        (timer) {
          // Capturar frame en segundo plano sin bloquear
          _captureSingleFrame();
        },
      );
    } catch (e) {
      _state = CaptureState.error;
      _errorMessage = 'Error iniciando captura continua: $e';
      notifyListeners();
    }
  }

  /// Detiene la captura continua
  Future<void> stopContinuousCapture() async {
    _continuousCaptureTimer?.cancel();
    _continuousCaptureTimer = null;

    if (_frames.isNotEmpty) {
      _state = CaptureState.completed;

      // Enviar el mejor frame al servidor para estimación
      if (bestFrame != null && estimateWeightUseCase != null) {
        await _estimateBestFrame();
      }
    } else {
      _state = CaptureState.idle;
    }

    _continuousCaptureStartTime = null;
    notifyListeners();
  }

  /// Estima el peso del mejor frame usando el servidor
  Future<void> _estimateBestFrame() async {
    if (bestFrame == null || estimateWeightUseCase == null) return;

    try {
      _isEstimating = true;
      _estimationError = null;
      notifyListeners();

      // Usar una raza por defecto (el usuario puede cambiarla después)
      // Por ahora usamos nelore como default
      final params = EstimateWeightParams(
        imagePath: bestFrame!.imagePath,
        breed: BreedType.nelore, // Default, el usuario puede cambiar
        cattleId: null,
      );

      final result = await estimateWeightUseCase!.call(params);

      result.fold(
        (failure) {
          _estimationError = failure.message;
          _lastEstimation = null;
        },
        (estimation) {
          _lastEstimation = estimation;
          _estimationError = null;
        },
      );
    } catch (e) {
      _estimationError = 'Error al estimar peso: $e';
      _lastEstimation = null;
    } finally {
      _isEstimating = false;
      notifyListeners();
    }
  }

  /// Captura un solo frame (usado en captura continua)
  ///
  /// Captura directamente desde la cámara sin usar el use case,
  /// para evitar validaciones de duración mínima.
  /// Se ejecuta en segundo plano para no bloquear la UI.
  void _captureSingleFrame() {
    // Evitar capturas simultáneas
    if (_isCapturingFrame) {
      return;
    }

    // Ejecutar en segundo plano sin bloquear
    Future.microtask(() async {
      try {
        // Verificar que la cámara esté disponible
        if (_cameraController == null ||
            !_cameraController!.value.isInitialized) {
          return;
        }

        // Marcar como capturando
        _isCapturingFrame = true;

        // Capturar frame directamente de la cámara usando CameraDataSource
        // Esto evita usar captureFramesUseCase que requiere duración mínima de 3-5 segundos
        final di = DependencyInjection();
        final frame = await di.cameraDataSource.captureFrame(
          _cameraController!,
        );

        // Agregar frame a la lista
        _frames.add(frame);

        // Notificar cambios en el siguiente frame para no bloquear
        WidgetsBinding.instance.addPostFrameCallback((_) {
          notifyListeners();
        });
      } catch (e) {
        // Solo loguear errores críticos, ignorar errores de "Previous capture"
        if (e.toString().contains('Previous capture')) {
          // Error esperado cuando la cámara está ocupada, ignorar silenciosamente
        } else {
          debugPrint('Error capturando frame: $e');
        }
      } finally {
        // Liberar flag
        _isCapturingFrame = false;
      }
    });
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
