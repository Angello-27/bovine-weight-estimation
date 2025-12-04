/// HTTP Error Handler
///
/// Manejo centralizado de errores HTTP.
/// Convierte DioException a AppException del dominio.
///
/// Core Network Layer
library;

import 'package:dio/dio.dart';

import '../errors/exceptions.dart';

/// Maneja errores de Dio y los convierte a Exceptions del dominio
class HttpErrorHandler {
  /// Convierte una DioException a una AppException
  static AppException handle(DioException error) {
    switch (error.type) {
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
              'Verifica tu conexión e intenta nuevamente.',
        );

      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode ?? 0;
        final message = _extractErrorMessage(error.response?.data);

        if (statusCode >= 500) {
          return ServerException(
            message: 'Error del servidor: $message',
            statusCode: statusCode,
          );
        } else if (statusCode == 400) {
          return ValidationException(message: 'Datos inválidos: $message');
        } else if (statusCode == 401) {
          return AuthException(message: 'No autorizado: $message');
        } else if (statusCode == 403) {
          return AuthException(message: 'Sin permisos: $message');
        } else if (statusCode == 404) {
          return ServerException(
            message: 'Recurso no encontrado: $message',
            statusCode: statusCode,
          );
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
          message: 'Error de red desconocido: ${error.message}',
        );
    }
  }

  /// Extrae el mensaje de error de la respuesta
  static String _extractErrorMessage(dynamic data) {
    if (data == null) return 'Error desconocido';

    if (data is Map<String, dynamic>) {
      // FastAPI devuelve errores en formato {"detail": "mensaje"}
      if (data.containsKey('detail')) {
        final detail = data['detail'];
        if (detail is String) {
          return detail;
        } else if (detail is List && detail.isNotEmpty) {
          return detail[0].toString();
        }
      }

      // Otros formatos posibles
      if (data.containsKey('message')) {
        return data['message'].toString();
      }

      if (data.containsKey('error')) {
        return data['error'].toString();
      }
    }

    return data.toString();
  }
}
