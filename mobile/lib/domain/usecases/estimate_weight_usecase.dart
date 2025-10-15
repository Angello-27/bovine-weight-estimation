/// UseCase: EstimateWeightUseCase
///
/// US-002: Estimación de Peso por Raza con IA
///
/// Caso de uso que implementa la estimación de peso usando modelos TFLite
/// específicos por raza, logrando precisión >95% (R² ≥0.95, MAE <5kg).
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';
import 'package:flutter/foundation.dart';

import '../../core/constants/breeds.dart';
import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/weight_estimation.dart';
import '../repositories/weight_estimation_repository.dart';

/// Caso de uso para estimación de peso con IA (US-002)
class EstimateWeightUseCase
    implements UseCase<WeightEstimation, EstimateWeightParams> {
  final WeightEstimationRepository repository;

  EstimateWeightUseCase(this.repository);

  /// Ejecuta la estimación de peso
  ///
  /// Proceso:
  /// 1. Validar que los modelos TFLite estén cargados
  /// 2. Ejecutar inferencia con el modelo de la raza específica
  /// 3. Validar que el tiempo de procesamiento sea <3s
  /// 4. Guardar estimación en SQLite
  ///
  /// Parámetros:
  /// - [params]: Parámetros de estimación (imagen, raza, cattleId)
  ///
  /// Retorna:
  /// - [Right(WeightEstimation)]: Estimación exitosa
  /// - [Left(Failure)]: Error durante la estimación
  @override
  Future<Either<Failure, WeightEstimation>> call(
    EstimateWeightParams params,
  ) async {
    // 1. Verificar que los modelos estén cargados
    final modelsLoadedResult = await repository.areModelsLoaded();

    final modelsLoaded = modelsLoadedResult.fold(
      (failure) => false,
      (loaded) => loaded,
    );

    // Si los modelos no están cargados, intentar cargarlos
    if (!modelsLoaded) {
      final loadResult = await repository.loadModels([params.breed]);
      if (loadResult.isLeft()) {
        return loadResult.fold(
          (failure) => Left(failure),
          (_) => const Left(
            ModelLoadFailure(
              message: 'No se pudieron cargar los modelos TFLite',
            ),
          ),
        );
      }
    }

    // 2. Ejecutar estimación
    final startTime = DateTime.now();

    final estimationResult = await repository.estimateWeight(
      imagePath: params.imagePath,
      breed: params.breed,
      cattleId: params.cattleId,
    );

    return estimationResult.fold((failure) => Left(failure), (
      estimation,
    ) async {
      // 3. Validar tiempo de procesamiento <3 segundos
      final processingTime = DateTime.now().difference(startTime);
      if (processingTime.inMilliseconds >= 3000) {
        // Advertir pero no fallar (métrica de performance)
        debugPrint(
          '⚠️ Procesamiento tomó ${processingTime.inMilliseconds}ms (>3000ms)',
        );
      }

      // 4. Validar métricas de calidad
      if (estimation.confidenceScore < 0.80) {
        debugPrint(
          '⚠️ Confianza baja: ${(estimation.confidenceScore * 100).toStringAsFixed(0)}%',
        );
      }

      // 5. Guardar estimación en SQLite
      final saveResult = await repository.saveEstimation(estimation);

      return saveResult.fold((failure) {
        // Error al guardar, pero retornar estimación
        debugPrint('⚠️ Error al guardar estimación: $failure');
        return Right(estimation);
      }, (_) => Right(estimation));
    });
  }
}

/// Parámetros para estimación de peso
class EstimateWeightParams {
  /// Path de la imagen del fotograma
  final String imagePath;

  /// Raza del animal (determina qué modelo usar)
  final BreedType breed;

  /// ID del animal (opcional, para vincular con registro)
  final String? cattleId;

  const EstimateWeightParams({
    required this.imagePath,
    required this.breed,
    this.cattleId,
  });

  @override
  String toString() =>
      'EstimateWeightParams(breed: ${breed.displayName}, cattleId: $cattleId)';
}
