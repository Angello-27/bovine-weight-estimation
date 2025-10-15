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
import 'core/ui/theme/app_theme.dart';
import 'presentation/providers/capture_provider.dart';

void main() async {
  // Asegurar inicialización de Flutter
  WidgetsFlutterBinding.ensureInitialized();

  // Inicializar Dependency Injection
  final di = DependencyInjection();
  di.init();

  // Ejecutar app
  runApp(MyApp(di: di));
}

/// App principal
class MyApp extends StatelessWidget {
  final DependencyInjection di;

  const MyApp({
    super.key,
    required this.di,
  });

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        // Provider para captura de fotogramas (US-001)
        ChangeNotifierProvider(
          create: (_) => CaptureProvider(
            captureFramesUseCase: di.captureFramesUseCase,
          ),
        ),
        
        // TODO: Agregar más providers según se implementen US
        // US-002: SelectionProvider
        // US-003: WeightEstimationProvider
        // US-004: AnalysisProvider
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
