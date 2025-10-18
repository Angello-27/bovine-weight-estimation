/// DataSource: SyncRemoteDataSource
///
/// DataSource para sincronización con backend via HTTP/REST.
/// Single Responsibility: Comunicación HTTP para operaciones de sync.
///
/// Data Layer - Clean Architecture
library;

import 'package:dio/dio.dart';

import '../../core/errors/exceptions.dart';
import '../models/sync_batch_request_model.dart';

/// DataSource para sincronización remota con backend
abstract class SyncRemoteDataSource {
  /// Sincroniza batch de ganado al backend
  ///
  /// Endpoint: POST /api/v1/sync/cattle
  Future<SyncBatchResponseModel> syncCattleBatch(
    CattleSyncBatchRequestModel request,
  );

  /// Sincroniza batch de estimaciones al backend
  ///
  /// Endpoint: POST /api/v1/sync/weight-estimations
  Future<SyncBatchResponseModel> syncWeightEstimationsBatch(
    WeightEstimationSyncBatchRequestModel request,
  );

  /// Verifica salud del servicio de sincronización
  ///
  /// Endpoint: GET /api/v1/sync/health
  Future<HealthCheckResponseModel> healthCheck();
}

/// Implementación con Dio
class SyncRemoteDataSourceImpl implements SyncRemoteDataSource {
  final Dio dio;
  final String baseUrl;

  /// Timeout para operaciones de sincronización (30 segundos según US-005)
  static const syncTimeout = Duration(seconds: 30);

  /// Timeout corto para health check (2-3 segundos para detección rápida)
  static const healthCheckTimeout = Duration(seconds: 3);

  SyncRemoteDataSourceImpl({required this.dio, required this.baseUrl}) {
    // Configurar Dio
    dio.options.baseUrl = baseUrl;
    dio.options.connectTimeout = syncTimeout;
    dio.options.receiveTimeout = syncTimeout;
    dio.options.headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
  }

  @override
  Future<SyncBatchResponseModel> syncCattleBatch(
    CattleSyncBatchRequestModel request,
  ) async {
    try {
      final response = await dio.post(
        '/api/v1/sync/cattle',
        data: request.toJson(),
      );

      if (response.statusCode == 200) {
        return SyncBatchResponseModel.fromJson(response.data);
      } else {
        throw ServerException(
          message: 'Error al sincronizar ganado: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } on DioException catch (e) {
      throw _handleDioError(e);
    } catch (e) {
      throw ServerException(
        message: 'Error inesperado al sincronizar ganado: $e',
      );
    }
  }

  @override
  Future<SyncBatchResponseModel> syncWeightEstimationsBatch(
    WeightEstimationSyncBatchRequestModel request,
  ) async {
    try {
      final response = await dio.post(
        '/api/v1/sync/weight-estimations',
        data: request.toJson(),
      );

      if (response.statusCode == 200) {
        return SyncBatchResponseModel.fromJson(response.data);
      } else {
        throw ServerException(
          message: 'Error al sincronizar estimaciones: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } on DioException catch (e) {
      throw _handleDioError(e);
    } catch (e) {
      throw ServerException(
        message: 'Error inesperado al sincronizar estimaciones: $e',
      );
    }
  }

  @override
  Future<HealthCheckResponseModel> healthCheck() async {
    try {
      final response = await dio.get(
        '/api/v1/sync/health',
        options: Options(
          sendTimeout: healthCheckTimeout,
          receiveTimeout: healthCheckTimeout,
        ),
      );

      if (response.statusCode == 200) {
        return HealthCheckResponseModel.fromJson(response.data);
      } else {
        throw ServerException(
          message: 'Error en health check: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } on DioException catch (e) {
      throw _handleDioError(e);
    } catch (e) {
      throw ServerException(message: 'Error inesperado en health check: $e');
    }
  }

  /// Maneja errores de Dio y los convierte a Exceptions del dominio
  Exception _handleDioError(DioException e) {
    switch (e.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return TimeoutException(
          message:
              'La conexión tardó demasiado. '
              'Verifica tu conectividad e intenta nuevamente.',
        );

      case DioExceptionType.connectionError:
        return NetworkException(
          message:
              'Sin conexión a internet. '
              'La sincronización se ejecutará automáticamente cuando '
              'se detecte conexión.',
        );

      case DioExceptionType.badResponse:
        final statusCode = e.response?.statusCode ?? 0;
        final message =
            e.response?.data['message'] ??
            e.response?.data['detail'] ??
            'Error del servidor';

        if (statusCode >= 500) {
          return ServerException(
            message: 'Error del servidor: $message',
            statusCode: statusCode,
          );
        } else if (statusCode == 400) {
          return ValidationException(message: 'Datos inválidos: $message');
        } else if (statusCode == 401 || statusCode == 403) {
          return AuthException(message: 'No autorizado: $message');
        } else {
          return ServerException(
            message: 'Error: $message',
            statusCode: statusCode,
          );
        }

      case DioExceptionType.cancel:
        return CancelledException(
          message: 'Operación cancelada por el usuario',
        );

      case DioExceptionType.badCertificate:
        return ServerException(
          message:
              'Error de certificado SSL. '
              'Verifica la configuración del servidor.',
        );

      default:
        return NetworkException(
          message: 'Error de red desconocido: ${e.message}',
        );
    }
  }
}

/// Factory para crear instancia configurada
class SyncRemoteDataSourceFactory {
  static SyncRemoteDataSource create({String? baseUrl}) {
    final dio = Dio();

    // URL del backend (en producción viene de .env)
    // Para desarrollo local:
    final url = baseUrl ?? 'http://localhost:8000';

    return SyncRemoteDataSourceImpl(dio: dio, baseUrl: url);
  }
}
