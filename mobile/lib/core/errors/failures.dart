/// Failures (Errores de Dominio)
/// 
/// Define todos los posibles fallos que pueden ocurrir en la aplicación.
/// Siguiendo Clean Architecture, los Failures son para el Domain Layer.
///
/// Core Layer - Clean Architecture
library;

import 'package:equatable/equatable.dart';

/// Clase base abstracta para todos los fallos
abstract class Failure extends Equatable {
  final String message;
  final String? code;

  const Failure({
    required this.message,
    this.code,
  });

  @override
  List<Object?> get props => [message, code];

  @override
  String toString() => 'Failure(message: $message, code: $code)';
}

/// Fallo al capturar fotograma
class CameraFailure extends Failure {
  const CameraFailure({
    required super.message,
    super.code = 'CAMERA_ERROR',
  });
}

/// Fallo al acceder a la cámara (permisos)
class CameraPermissionFailure extends Failure {
  const CameraPermissionFailure({
    super.message = 'Permiso de cámara denegado',
    super.code = 'CAMERA_PERMISSION_DENIED',
  });
}

/// Fallo al inicializar cámara
class CameraInitializationFailure extends Failure {
  const CameraInitializationFailure({
    super.message = 'Error al inicializar cámara',
    super.code = 'CAMERA_INIT_ERROR',
  });
}

/// Fallo al guardar fotograma
class StorageFailure extends Failure {
  const StorageFailure({
    required super.message,
    super.code = 'STORAGE_ERROR',
  });
}

/// Fallo al acceder a SQLite
class DatabaseFailure extends Failure {
  const DatabaseFailure({
    required super.message,
    super.code = 'DATABASE_ERROR',
  });
}

/// Fallo al evaluar calidad del fotograma
class FrameQualityFailure extends Failure {
  const FrameQualityFailure({
    super.message = 'Error al evaluar calidad del fotograma',
    super.code = 'FRAME_QUALITY_ERROR',
  });
}

/// Fallo de validación (datos inválidos)
class ValidationFailure extends Failure {
  const ValidationFailure({
    required super.message,
    super.code = 'VALIDATION_ERROR',
  });
}

/// Fallo de red (sin conexión)
class NetworkFailure extends Failure {
  const NetworkFailure({
    super.message = 'Sin conexión a internet',
    super.code = 'NETWORK_ERROR',
  });
}

/// Fallo del servidor (Backend API)
class ServerFailure extends Failure {
  const ServerFailure({
    required super.message,
    super.code = 'SERVER_ERROR',
  });
}

/// Fallo desconocido o inesperado
class UnknownFailure extends Failure {
  const UnknownFailure({
    super.message = 'Error desconocido',
    super.code = 'UNKNOWN_ERROR',
  });
}

/// Fallo al cargar modelo TFLite
class ModelLoadFailure extends Failure {
  const ModelLoadFailure({
    super.message = 'Error al cargar modelo TFLite',
    super.code = 'MODEL_LOAD_ERROR',
  });
}

/// Fallo al ejecutar inferencia ML
class InferenceFailure extends Failure {
  const InferenceFailure({
    super.message = 'Error al ejecutar inferencia',
    super.code = 'INFERENCE_ERROR',
  });
}

/// Fallo al sincronizar con backend
class SyncFailure extends Failure {
  const SyncFailure({
    required super.message,
    super.code = 'SYNC_ERROR',
  });
}

