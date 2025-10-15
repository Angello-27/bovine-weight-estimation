/// Exceptions (Excepciones Técnicas)
/// 
/// Define todas las excepciones que pueden ocurrir en Data Layer.
/// Siguiendo Clean Architecture, las Exceptions son para Data Layer
/// y luego se convierten en Failures en Domain Layer.
///
/// Core Layer - Clean Architecture
library;

/// Clase base para todas las excepciones de la aplicación
class AppException implements Exception {
  final String message;
  final String? code;

  const AppException({
    required this.message,
    this.code,
  });

  @override
  String toString() => 'AppException(message: $message, code: $code)';
}

/// Excepción de cámara
class CameraException extends AppException {
  const CameraException({
    required super.message,
    super.code = 'CAMERA_EXCEPTION',
  });
}

/// Excepción de permisos de cámara
class CameraPermissionException extends AppException {
  const CameraPermissionException({
    super.message = 'Permiso de cámara denegado',
    super.code = 'CAMERA_PERMISSION_EXCEPTION',
  });
}

/// Excepción de almacenamiento
class StorageException extends AppException {
  const StorageException({
    required super.message,
    super.code = 'STORAGE_EXCEPTION',
  });
}

/// Excepción de base de datos
class DatabaseException extends AppException {
  const DatabaseException({
    required super.message,
    super.code = 'DATABASE_EXCEPTION',
  });
}

/// Excepción de caché
class CacheException extends AppException {
  const CacheException({
    required super.message,
    super.code = 'CACHE_EXCEPTION',
  });
}

/// Excepción de red
class NetworkException extends AppException {
  const NetworkException({
    super.message = 'Sin conexión a internet',
    super.code = 'NETWORK_EXCEPTION',
  });
}

/// Excepción del servidor
class ServerException extends AppException {
  final int? statusCode;

  const ServerException({
    required super.message,
    super.code = 'SERVER_EXCEPTION',
    this.statusCode,
  });

  @override
  String toString() =>
      'ServerException(message: $message, code: $code, statusCode: $statusCode)';
}

/// Excepción de validación
class ValidationException extends AppException {
  const ValidationException({
    required super.message,
    super.code = 'VALIDATION_EXCEPTION',
  });
}

/// Excepción de formato
class FormatException extends AppException {
  const FormatException({
    required super.message,
    super.code = 'FORMAT_EXCEPTION',
  });
}

/// Excepción de modelo ML
class ModelException extends AppException {
  const ModelException({
    required super.message,
    super.code = 'MODEL_EXCEPTION',
  });
}

