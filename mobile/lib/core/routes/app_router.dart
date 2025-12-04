/// App Router
///
/// Gestión de rutas de navegación de la aplicación.
/// Single Responsibility: Definir y gestionar todas las rutas.
///
/// Core Routes Layer
library;

import 'package:flutter/material.dart';

import 'package:provider/provider.dart';

import '../../presentation/pages/auth/login_page.dart';
import '../../presentation/pages/capture/capture_page.dart';
import '../../presentation/pages/cattle_registration/cattle_registration_page.dart';
import '../../presentation/pages/home/home_page.dart';
import '../../presentation/pages/settings/settings_page.dart';
import '../../presentation/pages/sync/sync_status_page.dart';
import '../../presentation/pages/weight_estimation/weight_estimation_page.dart';
import '../../presentation/pages/weight_history/weight_history_page.dart';
import '../../presentation/providers/auth_provider.dart';

/// Nombres de rutas
class AppRoutes {
  static const String login = '/login';
  static const String home = '/';
  static const String capture = '/capture';
  static const String weightEstimation = '/weight-estimation';
  static const String cattleRegistration = '/cattle-registration';
  static const String weightHistory = '/weight-history';
  static const String sync = '/sync'; // US-005
  static const String settings = '/settings';

  // TODO: Agregar rutas para US-006, etc.
  // static const String cattleList = '/cattle-list';
  // static const String cattleDetail = '/cattle-detail';
}

/// Router de la aplicación
class AppRouter {
  /// Genera rutas de la aplicación
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case AppRoutes.login:
        return MaterialPageRoute(
          builder: (_) => const LoginPage(),
          settings: settings,
        );

      case AppRoutes.home:
        return _protectedRoute(
          builder: (_) => const HomePage(),
          settings: settings,
        );

      case AppRoutes.capture:
        return _protectedRoute(
          builder: (_) => const CapturePage(),
          settings: settings,
        );

      case AppRoutes.weightEstimation:
        // Espera argumentos: { 'framePath': String, 'cattleId': String? }
        final args = settings.arguments as Map<String, dynamic>?;
        final framePath = args?['framePath'] as String? ?? '';
        final cattleId = args?['cattleId'] as String?;

        return _protectedRoute(
          builder: (_) =>
              WeightEstimationPage(framePath: framePath, cattleId: cattleId),
          settings: settings,
        );

      case AppRoutes.cattleRegistration:
        return _protectedRoute(
          builder: (_) => const CattleRegistrationPage(),
          settings: settings,
        );

      case AppRoutes.weightHistory:
        // Espera argumentos: { 'cattleId': String, 'cattleName': String }
        final args = settings.arguments as Map<String, dynamic>?;
        final cattleId = args?['cattleId'] as String? ?? '';
        final cattleName = args?['cattleName'] as String? ?? 'Animal';

        return _protectedRoute(
          builder: (_) =>
              WeightHistoryPage(cattleId: cattleId, cattleName: cattleName),
          settings: settings,
        );

      case AppRoutes.sync:
        return _protectedRoute(
          builder: (_) => const SyncStatusPage(),
          settings: settings,
        );

      case AppRoutes.settings:
        return _protectedRoute(
          builder: (_) => const SettingsPage(),
          settings: settings,
        );

      // TODO: Agregar más rutas según se implementen

      default:
        return _errorRoute(settings.name);
    }
  }

  /// Ruta de error para rutas no definidas
  static Route<dynamic> _errorRoute(String? routeName) {
    return MaterialPageRoute(
      builder: (_) => Scaffold(
        appBar: AppBar(title: const Text('Error')),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 80, color: Colors.red),
              const SizedBox(height: 16),
              Text(
                'Ruta no encontrada: $routeName',
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 18),
              ),
            ],
          ),
        ),
      ),
    );
  }

  /// Navegación programática con tipo seguro
  static Future<T?> push<T>(
    BuildContext context,
    String routeName, {
    Object? arguments,
  }) {
    return Navigator.pushNamed<T>(context, routeName, arguments: arguments);
  }

  /// Navegación con reemplazo de ruta actual
  static Future<T?> pushReplacement<T>(
    BuildContext context,
    String routeName, {
    Object? arguments,
  }) {
    return Navigator.pushReplacementNamed<T, dynamic>(
      context,
      routeName,
      arguments: arguments,
    );
  }

  /// Navegación con limpieza de stack
  static Future<T?> pushAndRemoveUntil<T>(
    BuildContext context,
    String routeName, {
    Object? arguments,
  }) {
    return Navigator.pushNamedAndRemoveUntil<T>(
      context,
      routeName,
      (route) => false,
      arguments: arguments,
    );
  }

  /// Pop con resultado
  static void pop<T>(BuildContext context, [T? result]) {
    Navigator.pop(context, result);
  }

  /// Crea una ruta protegida que verifica autenticación
  static Route<dynamic> _protectedRoute({
    required Widget Function(BuildContext) builder,
    required RouteSettings settings,
  }) {
    return MaterialPageRoute(
      builder: (context) {
        final authProvider = Provider.of<AuthProvider>(context, listen: false);

        // Si no está autenticado, redirigir a login
        if (!authProvider.isAuthenticated) {
          // Usar un Future.microtask para evitar problemas de navegación
          WidgetsBinding.instance.addPostFrameCallback((_) {
            if (context.mounted) {
              Navigator.of(context).pushReplacementNamed(AppRoutes.login);
            }
          });
          // Retornar un widget temporal mientras redirige
          return const Scaffold(
            body: Center(child: CircularProgressIndicator()),
          );
        }

        return builder(context);
      },
      settings: settings,
    );
  }
}
