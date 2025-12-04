/// Dio Client
///
/// Cliente HTTP centralizado con configuración y interceptors.
/// Single Responsibility: Crear instancias de Dio configuradas.
///
/// Core Network Layer
library;

import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

import '../auth/session_manager.dart';
import '../config/api_config.dart';
import '../errors/exceptions.dart';
import 'auth_interceptor.dart';
import 'http_error_handler.dart';

/// Factory para crear instancias de Dio configuradas
class DioClient {
  final String baseUrl;
  final SessionManager sessionManager;

  DioClient({required this.baseUrl, required this.sessionManager});

  /// Crea una instancia de Dio configurada
  Dio create() {
    final dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: ApiConfig.connectTimeout,
        receiveTimeout: ApiConfig.receiveTimeout,
        headers: ApiConfig.defaultHeaders,
      ),
    );

    // Interceptor de autenticación
    dio.interceptors.add(
      AuthInterceptor(
        sessionManager,
        publicPaths: AuthInterceptor.defaultPublicPaths,
      ),
    );

    // Interceptor de logging (solo en debug)
    if (kDebugMode) {
      dio.interceptors.add(
        LogInterceptor(requestBody: true, responseBody: true, error: true),
      );
    }

    return dio;
  }

  /// Crea una instancia de Dio sin autenticación (para endpoints públicos)
  Dio createPublic() {
    final dio = Dio(
      BaseOptions(
        baseUrl: baseUrl,
        connectTimeout: ApiConfig.connectTimeout,
        receiveTimeout: ApiConfig.receiveTimeout,
        headers: ApiConfig.defaultHeaders,
      ),
    );

    // Solo logging en debug
    if (kDebugMode) {
      dio.interceptors.add(
        LogInterceptor(requestBody: true, responseBody: true, error: true),
      );
    }

    return dio;
  }

  /// Maneja errores de Dio y los convierte a Exceptions
  static AppException handleError(DioException error) {
    return HttpErrorHandler.handle(error);
  }
}
