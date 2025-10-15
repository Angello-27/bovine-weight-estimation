/// Model: FrameModel
/// 
/// Modelo de datos para Frame con serialización JSON y SQLite.
/// Extiende la entidad Frame del dominio agregando funcionalidad de persistencia.
///
/// Data Layer - Clean Architecture
library;

import '../../domain/entities/frame.dart';

/// Modelo de Frame con serialización
class FrameModel extends Frame {
  const FrameModel({
    required super.id,
    required super.timestamp,
    required super.imagePath,
    required super.quality,
    required super.globalScore,
  });

  /// Crea un FrameModel desde una entidad Frame
  factory FrameModel.fromEntity(Frame frame) {
    return FrameModel(
      id: frame.id,
      timestamp: frame.timestamp,
      imagePath: frame.imagePath,
      quality: frame.quality,
      globalScore: frame.globalScore,
    );
  }

  /// Crea un FrameModel desde JSON
  factory FrameModel.fromJson(Map<String, dynamic> json) {
    return FrameModel(
      id: json['id'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      imagePath: json['image_path'] as String,
      quality: FrameQualityModel.fromJson(json['quality'] as Map<String, dynamic>),
      globalScore: (json['global_score'] as num).toDouble(),
    );
  }

  /// Convierte el modelo a JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'timestamp': timestamp.toIso8601String(),
      'image_path': imagePath,
      'quality': FrameQualityModel.fromEntity(quality).toJson(),
      'global_score': globalScore,
    };
  }

  /// Crea un FrameModel desde SQLite Map
  factory FrameModel.fromSQLite(Map<String, dynamic> map) {
    return FrameModel(
      id: map['id'] as String,
      timestamp: DateTime.fromMillisecondsSinceEpoch(map['timestamp'] as int),
      imagePath: map['image_path'] as String,
      quality: FrameQuality(
        sharpness: (map['sharpness'] as num).toDouble(),
        brightness: (map['brightness'] as num).toDouble(),
        contrast: (map['contrast'] as num).toDouble(),
        silhouetteVisibility: (map['silhouette_visibility'] as num).toDouble(),
        angleScore: (map['angle_score'] as num).toDouble(),
      ),
      globalScore: (map['global_score'] as num).toDouble(),
    );
  }

  /// Convierte el modelo a SQLite Map
  Map<String, dynamic> toSQLite() {
    return {
      'id': id,
      'timestamp': timestamp.millisecondsSinceEpoch,
      'image_path': imagePath,
      'sharpness': quality.sharpness,
      'brightness': quality.brightness,
      'contrast': quality.contrast,
      'silhouette_visibility': quality.silhouetteVisibility,
      'angle_score': quality.angleScore,
      'global_score': globalScore,
    };
  }

  @override
  String toString() => 'FrameModel(${super.toString()})';
}

/// Modelo de FrameQuality con serialización
class FrameQualityModel extends FrameQuality {
  const FrameQualityModel({
    required super.sharpness,
    required super.brightness,
    required super.contrast,
    required super.silhouetteVisibility,
    required super.angleScore,
  });

  /// Crea un FrameQualityModel desde una entidad FrameQuality
  factory FrameQualityModel.fromEntity(FrameQuality quality) {
    return FrameQualityModel(
      sharpness: quality.sharpness,
      brightness: quality.brightness,
      contrast: quality.contrast,
      silhouetteVisibility: quality.silhouetteVisibility,
      angleScore: quality.angleScore,
    );
  }

  /// Crea un FrameQualityModel desde JSON
  factory FrameQualityModel.fromJson(Map<String, dynamic> json) {
    return FrameQualityModel(
      sharpness: (json['sharpness'] as num).toDouble(),
      brightness: (json['brightness'] as num).toDouble(),
      contrast: (json['contrast'] as num).toDouble(),
      silhouetteVisibility: (json['silhouette_visibility'] as num).toDouble(),
      angleScore: (json['angle_score'] as num).toDouble(),
    );
  }

  /// Convierte el modelo a JSON
  Map<String, dynamic> toJson() {
    return {
      'sharpness': sharpness,
      'brightness': brightness,
      'contrast': contrast,
      'silhouette_visibility': silhouetteVisibility,
      'angle_score': angleScore,
    };
  }
}

