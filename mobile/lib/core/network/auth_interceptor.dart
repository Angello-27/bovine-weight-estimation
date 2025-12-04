/// Auth Interceptor
///
/// Interceptor de Dio para agregar automáticamente el token JWT
/// a todas las requests que requieren autenticación.
///
/// Core Network Layer
library;

import 'package:dio/dio.dart';

import '../auth/session_manager.dart';

/// Interceptor para agregar token de autenticación a las requests
class AuthInterceptor extends Interceptor {
  final SessionManager _sessionManager;
  final List<String> _publicPaths;

  /// Paths que no requieren autenticación
  static const List<String> defaultPublicPaths = [
    '/api/v1/auth/login',
    '/api/v1/sync/health',
    '/api/v1/ml/models/status',
  ];

  AuthInterceptor(this._sessionManager, {List<String>? publicPaths})
    : _publicPaths = publicPaths ?? defaultPublicPaths;

  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    // Verificar si el path requiere autenticación
    final requiresAuth = !_publicPaths.any(
      (path) => options.path.startsWith(path),
    );

    if (requiresAuth) {
      // Obtener token del session manager
      final token = await _sessionManager.getAccessToken();

      if (token != null && token.isNotEmpty) {
        // Agregar token al header
        options.headers['Authorization'] = 'Bearer $token';
      }
    }

    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    // Si recibimos un 401, limpiar la sesión
    if (err.response?.statusCode == 401) {
      await _sessionManager.clearSession();
    }

    handler.next(err);
  }
}
