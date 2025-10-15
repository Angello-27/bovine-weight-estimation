/// Provider: WeightEstimationProvider
/// 
/// Provider para gestionar el estado de estimación de peso (US-002).
/// Single Responsibility: State management de estimación de peso.
///
/// Presentation Layer - Provider Pattern
library;

import 'package:flutter/foundation.dart';

import '../../core/constants/breeds.dart';
import '../../domain/entities/weight_estimation.dart';
import '../../domain/usecases/estimate_weight_usecase.dart';

/// Estados de estimación
enum WeightEstimationState {
  /// Estado inicial, esperando selección de raza
  idle,

  /// Cargando modelos TFLite
  loadingModels,

  /// Ejecutando inferencia
  estimating,

  /// Estimación completada
  completed,

  /// Error durante estimación
  error,
}

/// Provider para estimación de peso
class WeightEstimationProvider with ChangeNotifier {
  final EstimateWeightUseCase estimateWeightUseCase;

  /// Estado actual
  WeightEstimationState _state = WeightEstimationState.idle;

  /// Raza seleccionada (requerida para estimación)
  BreedType? _selectedBreed;

  /// Última estimación realizada
  WeightEstimation? _estimation;

  /// Mensaje de error (si existe)
  String? _errorMessage;

  /// Path de la imagen a estimar
  String? _imagePath;

  WeightEstimationProvider({
    required this.estimateWeightUseCase,
  });

  // Getters
  WeightEstimationState get state => _state;
  BreedType? get selectedBreed => _selectedBreed;
  WeightEstimation? get estimation => _estimation;
  String? get errorMessage => _errorMessage;
  String? get imagePath => _imagePath;

  /// Indica si está estimando
  bool get isEstimating => _state == WeightEstimationState.estimating;

  /// Indica si hay error
  bool get hasError => _state == WeightEstimationState.error;

  /// Indica si hay resultado
  bool get hasResult =>
      _state == WeightEstimationState.completed && _estimation != null;

  /// Selecciona la raza para estimación
  void selectBreed(BreedType breed) {
    _selectedBreed = breed;
    notifyListeners();
  }

  /// Establece la imagen para estimación
  void setImagePath(String path) {
    _imagePath = path;
    notifyListeners();
  }

  /// Estima el peso del animal
  Future<void> estimateWeight({
    String? imagePath,
    BreedType? breed,
    String? cattleId,
  }) async {
    try {
      // Usar parámetros o valores guardados
      final finalImagePath = imagePath ?? _imagePath;
      final finalBreed = breed ?? _selectedBreed;

      // Validar parámetros requeridos
      if (finalImagePath == null) {
        _state = WeightEstimationState.error;
        _errorMessage = 'No hay imagen para estimar';
        notifyListeners();
        return;
      }

      if (finalBreed == null) {
        _state = WeightEstimationState.error;
        _errorMessage = 'Debe seleccionar la raza del animal';
        notifyListeners();
        return;
      }

      // Cambiar estado a estimando
      _state = WeightEstimationState.estimating;
      _errorMessage = null;
      notifyListeners();

      // Ejecutar estimación
      final params = EstimateWeightParams(
        imagePath: finalImagePath,
        breed: finalBreed,
        cattleId: cattleId,
      );

      final result = await estimateWeightUseCase.call(params);

      result.fold(
        // Error
        (failure) {
          _state = WeightEstimationState.error;
          _errorMessage = failure.message;
          _estimation = null;
          notifyListeners();
        },
        // Éxito
        (estimation) {
          _state = WeightEstimationState.completed;
          _estimation = estimation;
          _errorMessage = null;
          notifyListeners();
        },
      );
    } catch (e) {
      _state = WeightEstimationState.error;
      _errorMessage = 'Error inesperado: $e';
      _estimation = null;
      notifyListeners();
    }
  }

  /// Reinicia el provider a estado inicial
  void reset() {
    _state = WeightEstimationState.idle;
    _selectedBreed = null;
    _estimation = null;
    _errorMessage = null;
    _imagePath = null;
    notifyListeners();
  }

  @override
  void dispose() {
    _estimation = null;
    super.dispose();
  }
}

