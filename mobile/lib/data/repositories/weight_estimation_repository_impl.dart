/// Repository Implementation: WeightEstimationRepositoryImpl
///
/// Implementación del repositorio de estimación de peso.
/// Single Responsibility: Coordinar TFLite y almacenamiento local.
///
/// Data Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';
import 'package:flutter/foundation.dart';

import '../../core/constants/breeds.dart';
import '../../core/errors/exceptions.dart';
import '../../core/errors/failures.dart';
import '../../domain/entities/weight_estimation.dart';
import '../../domain/repositories/weight_estimation_repository.dart';
import '../datasources/tflite_datasource.dart';
import '../datasources/weight_estimation_local_datasource.dart';
import '../models/weight_estimation_model.dart';

/// Implementación del repositorio de estimación de peso
class WeightEstimationRepositoryImpl implements WeightEstimationRepository {
  final TFLiteDataSource tfliteDataSource;
  final WeightEstimationLocalDataSource localDataSource;

  WeightEstimationRepositoryImpl({
    required this.tfliteDataSource,
    required this.localDataSource,
  });

  @override
  Future<Either<Failure, WeightEstimation>> estimateWeight({
    required String imagePath,
    required BreedType breed,
    String? cattleId,
  }) async {
    try {
      // Ejecutar inferencia con TFLite
      final estimation = await tfliteDataSource.runInference(
        imagePath: imagePath,
        breed: breed,
        cattleId: cattleId,
      );

      // Validar que el tiempo de procesamiento sea <3s
      if (estimation.processingTimeMs >= 3000) {
        debugPrint(
          '⚠️ Procesamiento lento: ${estimation.processingTimeMs}ms (objetivo: <3000ms)',
        );
      }

      return Right(estimation);
    } on ModelException catch (e) {
      return Left(InferenceFailure(message: e.message));
    } on StorageException catch (e) {
      return Left(StorageFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error en estimación: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> saveEstimation(
    WeightEstimation estimation,
  ) async {
    try {
      final estimationModel = WeightEstimationModel.fromEntity(estimation);
      await localDataSource.saveEstimation(estimationModel);
      return const Right(null);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al guardar: $e'));
    }
  }

  @override
  Future<Either<Failure, List<WeightEstimation>>> getAllEstimations() async {
    try {
      final estimations = await localDataSource.getAllEstimations();
      return Right(estimations);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al obtener estimaciones: $e'));
    }
  }

  @override
  Future<Either<Failure, List<WeightEstimation>>> getEstimationsByCattle(
    String cattleId,
  ) async {
    try {
      final estimations = await localDataSource.getEstimationsByCattle(
        cattleId,
      );
      return Right(estimations);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(
        UnknownFailure(message: 'Error al obtener estimaciones del animal: $e'),
      );
    }
  }

  @override
  Future<Either<Failure, WeightEstimation?>> getLastEstimation(
    String cattleId,
  ) async {
    try {
      final estimation = await localDataSource.getLastEstimation(cattleId);
      return Right(estimation);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(
        UnknownFailure(message: 'Error al obtener última estimación: $e'),
      );
    }
  }

  @override
  Future<Either<Failure, void>> deleteEstimation(String estimationId) async {
    try {
      await localDataSource.deleteEstimation(estimationId);
      return const Right(null);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al eliminar estimación: $e'));
    }
  }

  @override
  Future<Either<Failure, bool>> areModelsLoaded() async {
    try {
      final loaded = await tfliteDataSource.areModelsLoaded();
      return Right(loaded);
    } on ModelException catch (e) {
      return Left(ModelLoadFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al verificar modelos: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> loadModels([List<BreedType>? breeds]) async {
    try {
      // Si no se especifican razas, cargar todas las 7
      final breedsList = breeds ?? BreedType.values;

      await tfliteDataSource.loadModels(breedsList);

      return const Right(null);
    } on ModelException catch (e) {
      return Left(ModelLoadFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al cargar modelos: $e'));
    }
  }
}
