/// Model: WeightEstimationModel
/// 
/// Modelo de datos para WeightEstimation con serialización JSON y SQLite.
/// Single Responsibility: Serialización y deserialización de estimaciones.
///
/// Data Layer - Clean Architecture
library;

import '../../core/constants/breeds.dart';
import '../../domain/entities/weight_estimation.dart';

/// Modelo de WeightEstimation con serialización
class WeightEstimationModel extends WeightEstimation {
  const WeightEstimationModel({
    required super.id,
    super.cattleId,
    required super.breed,
    required super.estimatedWeight,
    required super.confidenceScore,
    required super.frameImagePath,
    required super.timestamp,
    super.gpsCoordinates,
    super.method,
    super.modelVersion,
    required super.processingTimeMs,
  });

  /// Crea un modelo desde una entidad
  factory WeightEstimationModel.fromEntity(WeightEstimation estimation) {
    return WeightEstimationModel(
      id: estimation.id,
      cattleId: estimation.cattleId,
      breed: estimation.breed,
      estimatedWeight: estimation.estimatedWeight,
      confidenceScore: estimation.confidenceScore,
      frameImagePath: estimation.frameImagePath,
      timestamp: estimation.timestamp,
      gpsCoordinates: estimation.gpsCoordinates,
      method: estimation.method,
      modelVersion: estimation.modelVersion,
      processingTimeMs: estimation.processingTimeMs,
    );
  }

  /// Crea un modelo desde JSON
  factory WeightEstimationModel.fromJson(Map<String, dynamic> json) {
    return WeightEstimationModel(
      id: json['id'] as String,
      cattleId: json['cattle_id'] as String?,
      breed: BreedType.fromValue(json['breed'] as String),
      estimatedWeight: (json['estimated_weight'] as num).toDouble(),
      confidenceScore: (json['confidence_score'] as num).toDouble(),
      frameImagePath: json['frame_image_path'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      gpsCoordinates: json['gps_coordinates'] != null
          ? GpsCoordinatesModel.fromJson(
              json['gps_coordinates'] as Map<String, dynamic>)
          : null,
      method: EstimationMethod.values.firstWhere(
        (m) => m.name == json['method'],
        orElse: () => EstimationMethod.tflite,
      ),
      modelVersion: json['model_version'] as String? ?? '1.0.0',
      processingTimeMs: json['processing_time_ms'] as int,
    );
  }

  /// Convierte el modelo a JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'cattle_id': cattleId,
      'breed': breed.value,
      'estimated_weight': estimatedWeight,
      'confidence_score': confidenceScore,
      'frame_image_path': frameImagePath,
      'timestamp': timestamp.toIso8601String(),
      'gps_coordinates': gpsCoordinates != null
          ? GpsCoordinatesModel.fromEntity(gpsCoordinates!).toJson()
          : null,
      'method': method.name,
      'model_version': modelVersion,
      'processing_time_ms': processingTimeMs,
    };
  }

  /// Crea un modelo desde SQLite Map
  factory WeightEstimationModel.fromSQLite(Map<String, dynamic> map) {
    return WeightEstimationModel(
      id: map['id'] as String,
      cattleId: map['cattle_id'] as String?,
      breed: BreedType.fromValue(map['breed'] as String),
      estimatedWeight: (map['estimated_weight'] as num).toDouble(),
      confidenceScore: (map['confidence_score'] as num).toDouble(),
      frameImagePath: map['frame_image_path'] as String,
      timestamp: DateTime.fromMillisecondsSinceEpoch(map['timestamp'] as int),
      gpsCoordinates: map['gps_latitude'] != null && map['gps_longitude'] != null
          ? GpsCoordinates(
              latitude: (map['gps_latitude'] as num).toDouble(),
              longitude: (map['gps_longitude'] as num).toDouble(),
            )
          : null,
      method: EstimationMethod.values.firstWhere(
        (m) => m.name == map['method'],
        orElse: () => EstimationMethod.tflite,
      ),
      modelVersion: map['model_version'] as String? ?? '1.0.0',
      processingTimeMs: map['processing_time_ms'] as int,
    );
  }

  /// Convierte el modelo a SQLite Map
  Map<String, dynamic> toSQLite() {
    return {
      'id': id,
      'cattle_id': cattleId,
      'breed': breed.value,
      'estimated_weight': estimatedWeight,
      'confidence_score': confidenceScore,
      'frame_image_path': frameImagePath,
      'timestamp': timestamp.millisecondsSinceEpoch,
      'gps_latitude': gpsCoordinates?.latitude,
      'gps_longitude': gpsCoordinates?.longitude,
      'method': method.name,
      'model_version': modelVersion,
      'processing_time_ms': processingTimeMs,
    };
  }
}

/// Modelo de GpsCoordinates con serialización
class GpsCoordinatesModel extends GpsCoordinates {
  const GpsCoordinatesModel({
    required super.latitude,
    required super.longitude,
  });

  factory GpsCoordinatesModel.fromEntity(GpsCoordinates coords) {
    return GpsCoordinatesModel(
      latitude: coords.latitude,
      longitude: coords.longitude,
    );
  }

  factory GpsCoordinatesModel.fromJson(Map<String, dynamic> json) {
    return GpsCoordinatesModel(
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'latitude': latitude,
      'longitude': longitude,
    };
  }
}

