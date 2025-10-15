/// Dependency Injection
/// 
/// Configuración de inyección de dependencias.
/// Single Responsibility: Crear y proveer instancias de servicios.
///
/// Core Config Layer
library;

import '../../data/datasources/camera_datasource.dart';
import '../../data/datasources/frame_local_datasource.dart';
import '../../data/repositories/frame_repository_impl.dart';
import '../../domain/repositories/frame_repository.dart';
import '../../domain/usecases/capture_frames_usecase.dart';

/// Contenedor de dependencias
/// 
/// TODO: Migrar a GetIt para DI más robusto en producción
class DependencyInjection {
  // Singleton
  static final DependencyInjection _instance = DependencyInjection._internal();
  factory DependencyInjection() => _instance;
  DependencyInjection._internal();

  // DataSources
  late final CameraDataSource _cameraDataSource;
  late final FrameLocalDataSource _localDataSource;

  // Repositories
  late final FrameRepository _frameRepository;

  // UseCases
  late final CaptureFramesUseCase _captureFramesUseCase;

  /// Inicializa todas las dependencias
  void init() {
    // DataSources
    _cameraDataSource = CameraDataSourceImpl();
    _localDataSource = FrameLocalDataSourceImpl();

    // Repositories
    _frameRepository = FrameRepositoryImpl(
      cameraDataSource: _cameraDataSource,
      localDataSource: _localDataSource,
    );

    // UseCases
    _captureFramesUseCase = CaptureFramesUseCase(_frameRepository);
  }

  // Getters
  CameraDataSource get cameraDataSource => _cameraDataSource;
  FrameLocalDataSource get localDataSource => _localDataSource;
  FrameRepository get frameRepository => _frameRepository;
  CaptureFramesUseCase get captureFramesUseCase => _captureFramesUseCase;

  /// Libera recursos
  Future<void> dispose() async {
    await _localDataSource.close();
  }
}

