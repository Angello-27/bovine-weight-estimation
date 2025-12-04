/// Model: MLModels
///
/// DTOs para predicciones de Machine Learning.
/// Mapea a los schemas del backend FastAPI.
///
/// Data Layer - Clean Architecture
library;

/// Response de predicción de peso desde el servidor
class WeightPredictionResponseModel {
  final String id;
  final String? animalId;
  final String breed;
  final double estimatedWeightKg;
  final double confidence;
  final String confidenceLevel;
  final int processingTimeMs;
  final String mlModelVersion;
  final String method;
  final bool meetsQualityCriteria;
  final DateTime timestamp;

  const WeightPredictionResponseModel({
    required this.id,
    this.animalId,
    required this.breed,
    required this.estimatedWeightKg,
    required this.confidence,
    required this.confidenceLevel,
    required this.processingTimeMs,
    required this.mlModelVersion,
    required this.method,
    required this.meetsQualityCriteria,
    required this.timestamp,
  });

  factory WeightPredictionResponseModel.fromJson(Map<String, dynamic> json) {
    return WeightPredictionResponseModel(
      id: json['id'] as String,
      animalId: json['animal_id'] as String?,
      breed: json['breed'] as String,
      estimatedWeightKg: (json['estimated_weight_kg'] as num).toDouble(),
      confidence: (json['confidence'] as num).toDouble(),
      confidenceLevel: json['confidence_level'] as String,
      processingTimeMs: json['processing_time_ms'] as int,
      mlModelVersion: json['ml_model_version'] as String,
      method: json['method'] as String,
      meetsQualityCriteria: json['meets_quality_criteria'] as bool,
      timestamp: DateTime.parse(json['timestamp'] as String),
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    if (animalId != null) 'animal_id': animalId,
    'breed': breed,
    'estimated_weight_kg': estimatedWeightKg,
    'confidence': confidence,
    'confidence_level': confidenceLevel,
    'processing_time_ms': processingTimeMs,
    'ml_model_version': mlModelVersion,
    'method': method,
    'meets_quality_criteria': meetsQualityCriteria,
    'timestamp': timestamp.toIso8601String(),
  };
}

/// Response del estado de modelos ML
class MLModelsStatusResponseModel {
  final String status;
  final int totalLoaded;
  final List<String> breedsLoaded;
  final List<String> allBreeds;
  final List<String> missingBreeds;
  final MLStrategiesInfo strategies;
  final List<String> availableStrategies;
  final String? note;
  final String method;

  const MLModelsStatusResponseModel({
    required this.status,
    required this.totalLoaded,
    required this.breedsLoaded,
    required this.allBreeds,
    required this.missingBreeds,
    required this.strategies,
    required this.availableStrategies,
    this.note,
    required this.method,
  });

  factory MLModelsStatusResponseModel.fromJson(Map<String, dynamic> json) {
    return MLModelsStatusResponseModel(
      status: json['status'] as String,
      totalLoaded: json['total_loaded'] as int,
      breedsLoaded: (json['breeds_loaded'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      allBreeds: (json['all_breeds'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      missingBreeds: (json['missing_breeds'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      strategies: MLStrategiesInfo.fromJson(
        json['strategies'] as Map<String, dynamic>,
      ),
      availableStrategies: (json['available_strategies'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      note: json['note'] as String?,
      method: json['method'] as String,
    );
  }

  Map<String, dynamic> toJson() => {
    'status': status,
    'total_loaded': totalLoaded,
    'breeds_loaded': breedsLoaded,
    'all_breeds': allBreeds,
    'missing_breeds': missingBreeds,
    'strategies': strategies.toJson(),
    'available_strategies': availableStrategies,
    if (note != null) 'note': note,
    'method': method,
  };
}

/// Información de estrategias ML
class MLStrategiesInfo {
  final int totalStrategies;
  final List<String> availableStrategies;
  final List<StrategyDetail> strategyDetails;

  const MLStrategiesInfo({
    required this.totalStrategies,
    required this.availableStrategies,
    required this.strategyDetails,
  });

  factory MLStrategiesInfo.fromJson(Map<String, dynamic> json) {
    return MLStrategiesInfo(
      totalStrategies: json['total_strategies'] as int,
      availableStrategies: (json['available_strategies'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      strategyDetails: (json['strategy_details'] as List<dynamic>)
          .map((e) => StrategyDetail.fromJson(e as Map<String, dynamic>))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() => {
    'total_strategies': totalStrategies,
    'available_strategies': availableStrategies,
    'strategy_details': strategyDetails.map((e) => e.toJson()).toList(),
  };
}

/// Detalle de una estrategia
class StrategyDetail {
  final String strategyName;
  final bool available;

  const StrategyDetail({required this.strategyName, required this.available});

  factory StrategyDetail.fromJson(Map<String, dynamic> json) {
    return StrategyDetail(
      strategyName: json['strategy_name'] as String,
      available: json['available'] as bool,
    );
  }

  Map<String, dynamic> toJson() => {
    'strategy_name': strategyName,
    'available': available,
  };
}
