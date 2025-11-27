/// Main App - Sistema de Estimación de Peso Bovino
///
/// Hacienda Gamelera - Bruno Brito Macedo
/// Clean Architecture + Provider + Material Design 3
///
/// Single Responsibility: Inicializar app
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'core/config/app_config.dart';
import 'core/config/dependency_injection.dart';
import 'core/config/provider_configuration.dart';
import 'core/routes/app_router.dart';
import 'core/theme/app_theme.dart';
import 'domain/entities/app_settings.dart';
import 'presentation/providers/settings_provider.dart';

void main() async {
  // Asegurar inicialización de Flutter
  WidgetsFlutterBinding.ensureInitialized();

  // Inicializar SharedPreferences para settings
  final prefs = await SharedPreferences.getInstance();

  // Inicializar Dependency Injection
  final di = DependencyInjection();
  di.init(prefs: prefs);

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
      child: Consumer<SettingsProvider>(
        builder: (context, settingsProvider, _) {
          // Obtener ThemeMode desde settings
          final themeMode = switch (settingsProvider.settings.themeMode) {
            AppThemeMode.light => ThemeMode.light,
            AppThemeMode.dark => ThemeMode.dark,
            AppThemeMode.system => ThemeMode.system,
          };

          return MaterialApp(
            // Configuración básica
            title: AppConfig.appName,
            debugShowCheckedModeBanner: AppConfig.showDebugBanner,

            // Tema Material Design 3 con tamaño de texto
            theme: AppTheme.lightTheme(
              textSize: settingsProvider.settings.textSize,
            ),
            darkTheme: AppTheme.darkTheme(
              textSize: settingsProvider.settings.textSize,
            ),
            themeMode: themeMode, // Usa la preferencia del usuario
            // Sistema de rutas
            initialRoute: AppRoutes.home,
            onGenerateRoute: AppRouter.generateRoute,
          );
        },
      ),
    );
  }
}
