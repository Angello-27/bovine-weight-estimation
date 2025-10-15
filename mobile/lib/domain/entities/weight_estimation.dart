/// Entity: WeightEstimation
/// 
/// Resultado de estimación de peso usando IA.
/// Single Responsibility: Representar estimación de peso con metadatos.
///
/// Domain Layer - Clean Architecture
library;

import 'package:equatable/equatable.dart';

import '../../core/constants/breeds.dart';

/// Estimación de peso con IA
class WeightEstimation extends Equatable {
  /// ID único de la estimación
  final String id;

  /// ID del animal (si está vinculado)
  final String? cattleId;

  /// Raza del animal (una de las 7 exactas)
  final BreedType breed;

  /// Peso estimado en kilogramos
  final double estimatedWeight;

  /// Confidence score de la estimación (0.0 - 1.0)
  /// >0.90 = Verde (Alta confianza)
  /// 0.80-0.90 = Amarillo (Media confianza)
  /// <0.80 = Rojo (Baja confianza)
  final double confidenceScore;

  /// Path del fotograma usado para la estimación
  final String frameImagePath;

  /// Timestamp de la estimación
  final DateTime timestamp;

  /// Coordenadas GPS (si disponibles)
  final GpsCoordinates? gpsCoordinates;

  /// Método de estimación usado
  final EstimationMethod method;

  /// Versión del modelo TFLite usado
  final String modelVersion;

  /// Tiempo de procesamiento en milisegundos
  final int processingTimeMs;

  const WeightEstimation({
    required this.id,
    this.cattleId,
    required this.breed,
    required this.estimatedWeight,
    required this.confidenceScore,
    required this.frameImagePath,
    required this.timestamp,
    this.gpsCoordinates,
    this.method = EstimationMethod.tflite,
    this.modelVersion = '1.0.0',
    required this.processingTimeMs,
  });

  /// Nivel de confianza basado en confidence score
  ConfidenceLevel get confidenceLevel {
    if (confidenceScore >= 0.90) return ConfidenceLevel.high;
    if (confidenceScore >= 0.80) return ConfidenceLevel.medium;
    return ConfidenceLevel.low;
  }

  /// Verifica si la estimación cumple criterios de calidad
  /// Criterio: Confidence >80% y procesamiento <3s
  bool get meetsQualityCriteria =>
      confidenceScore >= 0.80 && processingTimeMs < 3000;

  @override
  List<Object?> get props => [
        id,
        cattleId,
        breed,
        estimatedWeight,
        confidenceScore,
        frameImagePath,
        timestamp,
        gpsCoordinates,
        method,
        modelVersion,
        processingTimeMs,
      ];

  @override
  String toString() =>
      'WeightEstimation(id: $id, breed: ${breed.displayName}, '
      'weight: ${estimatedWeight.toStringAsFixed(1)}kg, '
      'confidence: ${(confidenceScore * 100).toStringAsFixed(0)}%)';
}

/// Coordenadas GPS
class GpsCoordinates extends Equatable {
  final double latitude;
  final double longitude;

  const GpsCoordinates({
    required this.latitude,
    required this.longitude,
  });

  @override
  List<Object?> get props => [latitude, longitude];

  @override
  String toString() => 'GPS($latitude, $longitude)';
}

/// Método de estimación
enum EstimationMethod {
  /// TensorFlow Lite (método principal)
  tflite,

  /// Fórmula Schaeffer (método tradicional, backup)
  schaeffer,

  /// Manual (ingreso manual por usuario)
  manual,
}

/// Nivel de confianza de la estimación
enum ConfidenceLevel {
  /// Alta confianza (≥90%) - Verde
  high,

  /// Media confianza (80-90%) - Amarillo
  medium,

  /// Baja confianza (<80%) - Rojo
  low,
}

/// Extensión para obtener colores y textos
extension ConfidenceLevelExtension on ConfidenceLevel {
  String get displayName {
    switch (this) {
      case ConfidenceLevel.high:
        return 'Alta';
      case ConfidenceLevel.medium:
        return 'Media';
      case ConfidenceLevel.low:
        return 'Baja';
    }
  }

  String get colorHex {
    switch (this) {
      case ConfidenceLevel.high:
        return '#4CAF50'; // Verde
      case ConfidenceLevel.medium:
        return '#FFA726'; // Amarillo/Naranja
      case ConfidenceLevel.low:
        return '#D32F2F'; // Rojo
    }
  }
}

