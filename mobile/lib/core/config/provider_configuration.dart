/// Provider Configuration
///
/// Gestión centralizada de providers siguiendo SOLID principles.
/// Single Responsibility: Configurar providers de la aplicación
/// Open/Closed: Fácil agregar nuevos providers sin modificar código existente
///
/// Core Config Layer
library;

import 'package:provider/provider.dart';

import '../../presentation/providers/capture_provider.dart';
import '../../presentation/providers/cattle_provider.dart';
import '../../presentation/providers/settings_provider.dart';
import '../../presentation/providers/sync_provider.dart';
import '../../presentation/providers/weight_estimation_provider.dart';
import '../../presentation/providers/weight_history_provider.dart';
import 'dependency_injection.dart';

/// Configurador de providers de la aplicación
///
/// Sigue el principio de Single Responsibility: solo se encarga
/// de crear y configurar los providers necesarios para la app.
class ProviderConfiguration {
  /// Crea todos los providers necesarios para la aplicación
  ///
  /// Retorna una lista de providers configurados con sus dependencias.
  /// Este método centraliza la creación de providers, facilitando
  /// el mantenimiento y la adición de nuevos providers.
  static List<ChangeNotifierProvider> createProviders(DependencyInjection di) {
    return [
      // US-001: Captura de fotogramas
      _createCaptureProvider(di),

      // US-002: Estimación de peso
      _createWeightEstimationProvider(di),

      // US-003: Registro de ganado
      _createCattleProvider(di),

      // US-004: Historial de peso
      _createWeightHistoryProvider(di),

      // US-005: Sincronización
      _createSyncProvider(di),

      // Settings
      _createSettingsProvider(di),

      // Agregar más providers aquí según se implementen nuevas US
      // US-006: SearchProvider
      // US-007: ReportProvider
    ];
  }

  /// Crea el provider de captura (US-001)
  static ChangeNotifierProvider<CaptureProvider> _createCaptureProvider(
    DependencyInjection di,
  ) {
    return ChangeNotifierProvider(
      create: (_) =>
          CaptureProvider(captureFramesUseCase: di.captureFramesUseCase),
    );
  }

  /// Crea el provider de estimación de peso (US-002)
  static ChangeNotifierProvider<WeightEstimationProvider>
  _createWeightEstimationProvider(DependencyInjection di) {
    return ChangeNotifierProvider(
      create: (_) => WeightEstimationProvider(
        estimateWeightUseCase: di.estimateWeightUseCase,
      ),
    );
  }

  /// Crea el provider de ganado (US-003)
  static ChangeNotifierProvider<CattleProvider> _createCattleProvider(
    DependencyInjection di,
  ) {
    return ChangeNotifierProvider(
      create: (_) =>
          CattleProvider(registerCattleUseCase: di.registerCattleUseCase),
    );
  }

  /// Crea el provider de historial de peso (US-004)
  static ChangeNotifierProvider<WeightHistoryProvider>
  _createWeightHistoryProvider(DependencyInjection di) {
    return ChangeNotifierProvider(
      create: (_) => WeightHistoryProvider(
        getWeightHistoryUseCase: di.getWeightHistoryUseCase,
      ),
    );
  }

  /// Crea el provider de sincronización (US-005)
  static ChangeNotifierProvider<SyncProvider> _createSyncProvider(
    DependencyInjection di,
  ) {
    return ChangeNotifierProvider(
      create: (_) => SyncProvider(
        syncPendingItemsUseCase: di.syncPendingItemsUseCase,
        getPendingCountUseCase: di.getPendingCountUseCase,
        triggerManualSyncUseCase: di.triggerManualSyncUseCase,
        checkConnectivityUseCase: di.checkConnectivityUseCase,
      ),
    );
  }

  /// Crea el provider de configuración
  static ChangeNotifierProvider<SettingsProvider> _createSettingsProvider(
    DependencyInjection di,
  ) {
    return ChangeNotifierProvider(
      create: (_) => SettingsProvider(
        getSettingsUseCase: di.getSettingsUseCase,
        saveSettingsUseCase: di.saveSettingsUseCase,
      ),
    );
  }
}
