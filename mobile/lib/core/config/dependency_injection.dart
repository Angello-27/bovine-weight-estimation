/// Dependency Injection
///
/// Configuración de inyección de dependencias.
/// Single Responsibility: Crear y proveer instancias de servicios.
///
/// Core Config Layer
library;

import '../services/permission_service.dart';
import '../../data/datasources/camera_datasource.dart';
import '../../data/datasources/cattle_local_datasource.dart';
import '../../data/datasources/frame_local_datasource.dart';
import '../../data/datasources/tflite_datasource.dart';
import '../../data/datasources/weight_estimation_local_datasource.dart';
import '../../data/repositories/cattle_repository_impl.dart';
import '../../data/repositories/frame_repository_impl.dart';
import '../../data/repositories/weight_estimation_repository_impl.dart';
import '../../data/repositories/weight_history_repository_impl.dart';
import '../../domain/repositories/cattle_repository.dart';
import '../../domain/repositories/frame_repository.dart';
import '../../domain/repositories/weight_estimation_repository.dart';
import '../../domain/repositories/weight_history_repository.dart';
import '../../data/datasources/sync_queue_local_datasource.dart';
import '../../data/datasources/sync_remote_datasource.dart';
import '../../data/repositories/sync_repository_impl.dart';
import '../../domain/repositories/sync_repository.dart';
import '../../domain/usecases/capture_frames_usecase.dart';
import '../../domain/usecases/check_connectivity_usecase.dart';
import '../../domain/usecases/estimate_weight_usecase.dart';
import '../../domain/usecases/get_pending_count_usecase.dart';
import '../../domain/usecases/get_weight_history_usecase.dart';
import '../../domain/usecases/register_cattle_usecase.dart';
import '../../domain/usecases/sync_pending_items_usecase.dart';
import '../../domain/usecases/trigger_manual_sync_usecase.dart';

/// Contenedor de dependencias
///
/// TODO: Migrar a GetIt para DI más robusto en producción
class DependencyInjection {
  // Singleton
  static final DependencyInjection _instance = DependencyInjection._internal();
  factory DependencyInjection() => _instance;
  DependencyInjection._internal();

  // Services
  late final PermissionService _permissionService;

  // DataSources - US-001
  late final CameraDataSource _cameraDataSource;
  late final FrameLocalDataSource _frameLocalDataSource;

  // DataSources - US-002
  late final TFLiteDataSource _tfliteDataSource;
  late final WeightEstimationLocalDataSource _weightEstimationLocalDataSource;

  // DataSources - US-003
  late final CattleLocalDataSource _cattleLocalDataSource;

  // DataSources - US-005
  late final SyncQueueLocalDataSource _syncQueueLocalDataSource;
  late final SyncRemoteDataSource _syncRemoteDataSource;

  // Repositories
  late final FrameRepository _frameRepository;
  late final WeightEstimationRepository _weightEstimationRepository;
  late final CattleRepository _cattleRepository;
  late final WeightHistoryRepository _weightHistoryRepository;
  late final SyncRepository _syncRepository;

  // UseCases
  late final CaptureFramesUseCase _captureFramesUseCase;
  late final EstimateWeightUseCase _estimateWeightUseCase;
  late final RegisterCattleUseCase _registerCattleUseCase;
  late final GetWeightHistoryUseCase _getWeightHistoryUseCase;
  late final SyncPendingItemsUseCase _syncPendingItemsUseCase;
  late final GetPendingCountUseCase _getPendingCountUseCase;
  late final TriggerManualSyncUseCase _triggerManualSyncUseCase;
  late final CheckConnectivityUseCase _checkConnectivityUseCase;

  /// Inicializa todas las dependencias
  void init() {
    // Services
    _permissionService = PermissionService();

    // DataSources - US-001
    _cameraDataSource = CameraDataSourceImpl();
    _frameLocalDataSource = FrameLocalDataSourceImpl();

    // DataSources - US-002
    _tfliteDataSource = TFLiteDataSourceImpl();
    _weightEstimationLocalDataSource = WeightEstimationLocalDataSourceImpl();

    // DataSources - US-003
    _cattleLocalDataSource = CattleLocalDataSourceImpl();

    // DataSources - US-005
    _syncQueueLocalDataSource = SyncQueueLocalDataSourceImpl();
    _syncRemoteDataSource = SyncRemoteDataSourceFactory.create(
      // TODO: Cargar baseUrl desde .env en producción
      baseUrl: 'http://localhost:8000',
    );

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

    // Repositories - US-003
    _cattleRepository = CattleRepositoryImpl(
      localDataSource: _cattleLocalDataSource,
    );

    // Repositories - US-004
    _weightHistoryRepository = WeightHistoryRepositoryImpl(
      weightEstimationDataSource: _weightEstimationLocalDataSource,
      cattleDataSource: _cattleLocalDataSource,
    );

    // Repositories - US-005
    _syncRepository = SyncRepositoryImpl(
      syncQueueLocal: _syncQueueLocalDataSource,
      cattleLocal: _cattleLocalDataSource,
      weightEstimationLocal: _weightEstimationLocalDataSource,
      syncRemote: _syncRemoteDataSource,
      // TODO: Generar deviceId único al instalar la app
      deviceId: 'dev-device-001',
    );

    // UseCases - US-001
    _captureFramesUseCase = CaptureFramesUseCase(_frameRepository);

    // UseCases - US-002
    _estimateWeightUseCase = EstimateWeightUseCase(_weightEstimationRepository);

    // UseCases - US-003
    _registerCattleUseCase = RegisterCattleUseCase(_cattleRepository);

    // UseCases - US-004
    _getWeightHistoryUseCase = GetWeightHistoryUseCase(
      repository: _weightHistoryRepository,
    );

    // UseCases - US-005
    _syncPendingItemsUseCase = SyncPendingItemsUseCase(_syncRepository);
    _getPendingCountUseCase = GetPendingCountUseCase(_syncRepository);
    _triggerManualSyncUseCase = TriggerManualSyncUseCase(_syncRepository);
    _checkConnectivityUseCase = CheckConnectivityUseCase(_syncRepository);
  }

  // Getters - Services
  PermissionService get permissionService => _permissionService;

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

  // Getters - US-003
  CattleLocalDataSource get cattleLocalDataSource => _cattleLocalDataSource;
  CattleRepository get cattleRepository => _cattleRepository;
  RegisterCattleUseCase get registerCattleUseCase => _registerCattleUseCase;

  // Getters - US-004
  WeightHistoryRepository get weightHistoryRepository =>
      _weightHistoryRepository;
  GetWeightHistoryUseCase get getWeightHistoryUseCase =>
      _getWeightHistoryUseCase;

  // Getters - US-005
  SyncRepository get syncRepository => _syncRepository;
  SyncPendingItemsUseCase get syncPendingItemsUseCase =>
      _syncPendingItemsUseCase;
  GetPendingCountUseCase get getPendingCountUseCase => _getPendingCountUseCase;
  TriggerManualSyncUseCase get triggerManualSyncUseCase =>
      _triggerManualSyncUseCase;
  CheckConnectivityUseCase get checkConnectivityUseCase =>
      _checkConnectivityUseCase;

  /// Libera recursos
  Future<void> dispose() async {
    await _frameLocalDataSource.close();
    await _weightEstimationLocalDataSource.close();
    await _cattleLocalDataSource.close();
    await _syncQueueLocalDataSource.close();
    await _tfliteDataSource.dispose();
    await _syncRepository.stopAutoSyncListener();
  }
}
