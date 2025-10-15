/// Dependency Injection
/// 
/// Configuración de inyección de dependencias.
/// Single Responsibility: Crear y proveer instancias de servicios.
///
/// Core Config Layer
library;

import '../../data/datasources/camera_datasource.dart';
import '../../data/datasources/frame_local_datasource.dart';
import '../../data/datasources/tflite_datasource.dart';
import '../../data/datasources/weight_estimation_local_datasource.dart';
import '../../data/repositories/frame_repository_impl.dart';
import '../../data/repositories/weight_estimation_repository_impl.dart';
import '../../domain/repositories/frame_repository.dart';
import '../../domain/repositories/weight_estimation_repository.dart';
import '../../domain/usecases/capture_frames_usecase.dart';
import '../../domain/usecases/estimate_weight_usecase.dart';

/// Contenedor de dependencias
/// 
/// TODO: Migrar a GetIt para DI más robusto en producción
class DependencyInjection {
  // Singleton
  static final DependencyInjection _instance = DependencyInjection._internal();
  factory DependencyInjection() => _instance;
  DependencyInjection._internal();

  // DataSources - US-001
  late final CameraDataSource _cameraDataSource;
  late final FrameLocalDataSource _frameLocalDataSource;

  // DataSources - US-002
  late final TFLiteDataSource _tfliteDataSource;
  late final WeightEstimationLocalDataSource _weightEstimationLocalDataSource;

  // Repositories
  late final FrameRepository _frameRepository;
  late final WeightEstimationRepository _weightEstimationRepository;

  // UseCases
  late final CaptureFramesUseCase _captureFramesUseCase;
  late final EstimateWeightUseCase _estimateWeightUseCase;

  /// Inicializa todas las dependencias
  void init() {
    // DataSources - US-001
    _cameraDataSource = CameraDataSourceImpl();
    _frameLocalDataSource = FrameLocalDataSourceImpl();

    // DataSources - US-002
    _tfliteDataSource = TFLiteDataSourceImpl();
    _weightEstimationLocalDataSource = WeightEstimationLocalDataSourceImpl();

    // Repositories - US-001
    _frameRepository = FrameRepositoryImpl(
      cameraDataSource: _cameraDataSource,
      localDataSource: _frameLocalDataSource,
    );

    // Repositories - US-002
    _weightEstimationRepository = WeightEstimationRepositoryImpl(
      tfliteDataSource: _tfliteDataSource,
      localDataSource: _weightEstimationLocalDataSource,
    );

    // UseCases - US-001
    _captureFramesUseCase = CaptureFramesUseCase(_frameRepository);

    // UseCases - US-002
    _estimateWeightUseCase = EstimateWeightUseCase(_weightEstimationRepository);
  }

  // Getters - US-001
  CameraDataSource get cameraDataSource => _cameraDataSource;
  FrameLocalDataSource get frameLocalDataSource => _frameLocalDataSource;
  FrameRepository get frameRepository => _frameRepository;
  CaptureFramesUseCase get captureFramesUseCase => _captureFramesUseCase;

  // Getters - US-002
  TFLiteDataSource get tfliteDataSource => _tfliteDataSource;
  WeightEstimationLocalDataSource get weightEstimationLocalDataSource =>
      _weightEstimationLocalDataSource;
  WeightEstimationRepository get weightEstimationRepository =>
      _weightEstimationRepository;
  EstimateWeightUseCase get estimateWeightUseCase => _estimateWeightUseCase;

  /// Libera recursos
  Future<void> dispose() async {
    await _frameLocalDataSource.close();
    await _weightEstimationLocalDataSource.close();
    await _tfliteDataSource.dispose();
  }
}

