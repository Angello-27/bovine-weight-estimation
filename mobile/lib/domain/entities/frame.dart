/// Entity: Frame (Fotograma capturado)
/// 
/// Representa un fotograma individual capturado durante la sesión de captura continua.
/// Incluye la imagen y las métricas de calidad evaluadas.
///
/// Domain Layer - Clean Architecture
library;

import 'package:equatable/equatable.dart';

/// Fotograma capturado con métricas de calidad
class Frame extends Equatable {
  /// Identificador único del fotograma
  final String id;

  /// Timestamp de captura
  final DateTime timestamp;

  /// Path o datos de la imagen (puede ser path local o bytes)
  final String imagePath;

  /// Métricas de calidad del fotograma
  final FrameQuality quality;

  /// Score global ponderado (0.0 - 1.0)
  /// Score = Silueta(40%) + Nitidez(30%) + Iluminación(20%) + Ángulo(10%)
  final double globalScore;

  const Frame({
    required this.id,
    required this.timestamp,
    required this.imagePath,
    required this.quality,
    required this.globalScore,
  });

  /// Verifica si el fotograma es óptimo según criterios mínimos
  bool get isOptimal =>
      quality.sharpness > 0.7 &&
      quality.brightness >= 0.4 &&
      quality.brightness <= 0.8 &&
      quality.contrast > 0.5 &&
      quality.silhouetteVisibility > 0.8 &&
      quality.angleScore > 0.6;

  /// Calcula el score global ponderado
  /// Silueta 40%, Nitidez 30%, Iluminación 20%, Ángulo 10%
  static double calculateGlobalScore(FrameQuality quality) {
    return (quality.silhouetteVisibility * 0.40) +
        (quality.sharpness * 0.30) +
        (quality.brightness * 0.20) +
        (quality.angleScore * 0.10);
  }

  @override
  List<Object?> get props => [
        id,
        timestamp,
        imagePath,
        quality,
        globalScore,
      ];

  @override
  String toString() =>
      'Frame(id: $id, score: ${globalScore.toStringAsFixed(2)}, optimal: $isOptimal)';
}

/// Métricas de calidad del fotograma
class FrameQuality extends Equatable {
  /// Nitidez/sharpness (0.0 - 1.0) - Objetivo: >0.7
  final double sharpness;

  /// Iluminación/brightness (0.0 - 1.0) - Objetivo: 0.4-0.8
  final double brightness;

  /// Contraste (0.0 - 1.0) - Objetivo: >0.5
  final double contrast;

  /// Visibilidad de silueta (0.0 - 1.0) - Objetivo: >0.8
  final double silhouetteVisibility;

  /// Score de ángulo apropiado (0.0 - 1.0) - Objetivo: >0.6
  final double angleScore;

  const FrameQuality({
    required this.sharpness,
    required this.brightness,
    required this.contrast,
    required this.silhouetteVisibility,
    required this.angleScore,
  });

  /// Verifica si todas las métricas cumplen los criterios mínimos
  bool get meetsMinimumCriteria =>
      sharpness > 0.7 &&
      brightness >= 0.4 &&
      brightness <= 0.8 &&
      contrast > 0.5 &&
      silhouetteVisibility > 0.8 &&
      angleScore > 0.6;

  @override
  List<Object?> get props => [
        sharpness,
        brightness,
        contrast,
        silhouetteVisibility,
        angleScore,
      ];

  @override
  String toString() =>
      'FrameQuality(sharpness: ${sharpness.toStringAsFixed(2)}, '
      'brightness: ${brightness.toStringAsFixed(2)}, '
      'contrast: ${contrast.toStringAsFixed(2)}, '
      'silhouette: ${silhouetteVisibility.toStringAsFixed(2)}, '
      'angle: ${angleScore.toStringAsFixed(2)})';
}

