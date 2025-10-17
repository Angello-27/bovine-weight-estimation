/// Main App - Sistema de Estimación de Peso Bovino
///
/// Hacienda Gamelera - Bruno Brito Macedo
/// Clean Architecture + Provider + Material Design 3
///
/// Single Responsibility: Inicializar app y configurar providers
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'core/config/app_config.dart';
import 'core/config/dependency_injection.dart';
import 'core/routes/app_router.dart';
import 'core/theme/app_theme.dart';
import 'presentation/providers/capture_provider.dart';
import 'presentation/providers/cattle_provider.dart';
import 'presentation/providers/weight_estimation_provider.dart';
import 'presentation/providers/weight_history_provider.dart';

void main() async {
  // Asegurar inicialización de Flutter
  WidgetsFlutterBinding.ensureInitialized();

  // Inicializar Dependency Injection
  final di = DependencyInjection();
  di.init();

  // Ejecutar app (permisos se solicitan just-in-time en cada feature)
  runApp(MyApp(di: di));
}

/// App principal
class MyApp extends StatelessWidget {
  final DependencyInjection di;

  const MyApp({super.key, required this.di});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        // Provider para captura de fotogramas (US-001)
        ChangeNotifierProvider(
          create: (_) =>
              CaptureProvider(captureFramesUseCase: di.captureFramesUseCase),
        ),

        // Provider para estimación de peso (US-002)
        ChangeNotifierProvider(
          create: (_) => WeightEstimationProvider(
            estimateWeightUseCase: di.estimateWeightUseCase,
          ),
        ),

        // Provider para registro de ganado (US-003)
        ChangeNotifierProvider(
          create: (_) =>
              CattleProvider(registerCattleUseCase: di.registerCattleUseCase),
        ),

        // Provider para historial de peso (US-004)
        ChangeNotifierProvider(
          create: (_) => WeightHistoryProvider(
            getWeightHistoryUseCase: di.getWeightHistoryUseCase,
          ),
        ),

        // TODO: Agregar más providers según se implementen US
        // US-005: SyncProvider
        // US-006: SearchProvider
      ],
      child: MaterialApp(
        // Configuración básica
        title: AppConfig.appName,
        debugShowCheckedModeBanner: AppConfig.showDebugBanner,

        // Tema Material Design 3
        theme: AppTheme.lightTheme,

        // Sistema de rutas
        initialRoute: AppRoutes.home,
        onGenerateRoute: AppRouter.generateRoute,
      ),
    );
  }
}
