/// App Router
/// 
/// Gestión de rutas de navegación de la aplicación.
/// Single Responsibility: Definir y gestionar todas las rutas.
///
/// Core Routes Layer
library;

import 'package:flutter/material.dart';

import '../../presentation/pages/capture/capture_page.dart';
import '../../presentation/pages/home/home_page.dart';

/// Nombres de rutas
class AppRoutes {
  static const String home = '/';
  static const String capture = '/capture';
  
  // TODO: Agregar rutas para US-002, US-003, etc.
  // static const String frameSelection = '/frame-selection';
  // static const String weightEstimation = '/weight-estimation';
  // static const String cattleList = '/cattle-list';
  // static const String cattleDetail = '/cattle-detail';
  // static const String analysis = '/analysis';
  // static const String settings = '/settings';
}

/// Router de la aplicación
class AppRouter {
  /// Genera rutas de la aplicación
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case AppRoutes.home:
        return MaterialPageRoute(
          builder: (_) => const HomePage(),
          settings: settings,
        );

      case AppRoutes.capture:
        return MaterialPageRoute(
          builder: (_) => const CapturePage(),
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
        appBar: AppBar(
          title: const Text('Error'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(
                Icons.error_outline,
                size: 80,
                color: Colors.red,
              ),
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
    return Navigator.pushNamed<T>(
      context,
      routeName,
      arguments: arguments,
    );
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
}

