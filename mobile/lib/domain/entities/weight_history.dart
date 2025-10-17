/// Entity: WeightHistory
///
/// Historial de pesajes de un animal con análisis.
/// Single Responsibility: Representar datos de historial de peso.
///
/// Domain Layer - Entity
library;

import 'package:equatable/equatable.dart';

import 'cattle.dart';
import 'weight_estimation.dart';

/// Historial de pesajes con análisis
class WeightHistory extends Equatable {
  /// ID del animal
  final String cattleId;

  /// Información del animal
  final Cattle cattle;

  /// Lista de pesajes ordenados cronológicamente (más reciente primero)
  final List<WeightEstimation> weighings;

  /// Peso actual (kg) - último pesaje
  final double? currentWeight;

  /// Peso inicial (kg) - primer pesaje
  final double? initialWeight;

  /// Ganancia total de peso (kg)
  final double totalGain;

  /// Ganancia diaria promedio - GDP (kg/día)
  final double averageDailyGain;

  /// Proyección de peso a 30 días (kg)
  final double? projectedWeight30Days;

  /// Proyección de peso a 60 días (kg)
  final double? projectedWeight60Days;

  /// Proyección de peso a 90 días (kg)
  final double? projectedWeight90Days;

  /// Anomalías detectadas
  final List<WeightAnomaly> anomalies;

  const WeightHistory({
    required this.cattleId,
    required this.cattle,
    required this.weighings,
    this.currentWeight,
    this.initialWeight,
    required this.totalGain,
    required this.averageDailyGain,
    this.projectedWeight30Days,
    this.projectedWeight60Days,
    this.projectedWeight90Days,
    required this.anomalies,
  });

  /// Verifica si tiene al menos 2 pesajes para análisis
  bool get hasEnoughDataForAnalysis => weighings.length >= 2;

  /// Número total de pesajes
  int get totalWeighings => weighings.length;

  @override
  List<Object?> get props => [
        cattleId,
        cattle,
        weighings,
        currentWeight,
        initialWeight,
        totalGain,
        averageDailyGain,
        projectedWeight30Days,
        projectedWeight60Days,
        projectedWeight90Days,
        anomalies,
      ];
}

/// Anomalía detectada en el historial de peso
class WeightAnomaly extends Equatable {
  /// Tipo de anomalía
  final AnomalyType type;

  /// Descripción de la anomalía
  final String description;

  /// Fecha de detección
  final DateTime detectedAt;

  /// Severidad (1-5, siendo 5 crítico)
  final int severity;

  /// Valor que disparó la alerta
  final double? value;

  const WeightAnomaly({
    required this.type,
    required this.description,
    required this.detectedAt,
    required this.severity,
    this.value,
  });

  @override
  List<Object?> get props => [
        type,
        description,
        detectedAt,
        severity,
        value,
      ];
}

/// Tipos de anomalías detectables
enum AnomalyType {
  /// Pérdida significativa de peso (>5% en 7 días)
  significantWeightLoss,

  /// Estancamiento en crecimiento (>15 días sin ganancia)
  growthStagnation,

  /// GDP bajo para categoría de edad
  lowAverageDailyGain,

  /// Variación inusual entre pesajes consecutivos
  unusualVariation,
}

/// Extension para anomaly types
extension AnomalyTypeExtension on AnomalyType {
  /// Nombre para mostrar en UI
  String get displayName {
    switch (this) {
      case AnomalyType.significantWeightLoss:
        return 'Pérdida Significativa de Peso';
      case AnomalyType.growthStagnation:
        return 'Estancamiento en Crecimiento';
      case AnomalyType.lowAverageDailyGain:
        return 'Ganancia Diaria Baja';
      case AnomalyType.unusualVariation:
        return 'Variación Inusual';
    }
  }

  /// Ícono representativo
  String get icon {
    switch (this) {
      case AnomalyType.significantWeightLoss:
        return '⚠️';
      case AnomalyType.growthStagnation:
        return '📉';
      case AnomalyType.lowAverageDailyGain:
        return '🐢';
      case AnomalyType.unusualVariation:
        return '❓';
    }
  }
}

