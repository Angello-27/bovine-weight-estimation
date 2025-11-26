/// Main App - Sistema de Estimación de Peso Bovino
///
/// Hacienda Gamelera - Bruno Brito Macedo
/// Clean Architecture + Provider + Material Design 3
///
/// Single Responsibility: Inicializar app
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'core/config/app_config.dart';
import 'core/config/dependency_injection.dart';
import 'core/config/provider_configuration.dart';
import 'core/routes/app_router.dart';
import 'core/theme/app_theme.dart';

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
///
/// Single Responsibility: Construir el árbol de widgets de la app
/// Dependency Inversion: Depende de abstracción (ProviderConfiguration)
class MyApp extends StatelessWidget {
  final DependencyInjection di;

  const MyApp({super.key, required this.di});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      // Usa ProviderConfiguration para crear todos los providers
      // Siguiendo principios SOLID: Open/Closed, Single Responsibility
      providers: ProviderConfiguration.createProviders(di),
      child: MaterialApp(
        // Configuración básica
        title: AppConfig.appName,
        debugShowCheckedModeBanner: AppConfig.showDebugBanner,

        // Tema Material Design 3
        theme: AppTheme.lightTheme,
        darkTheme: AppTheme.darkTheme,
        themeMode: ThemeMode.system, // Sigue la preferencia del sistema
        // Sistema de rutas
        initialRoute: AppRoutes.home,
        onGenerateRoute: AppRouter.generateRoute,
      ),
    );
  }
}
