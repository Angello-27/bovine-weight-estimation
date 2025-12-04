/// Repository Implementation: WeightEstimationRepositoryImpl
///
/// Implementación del repositorio de estimación de peso.
/// Single Responsibility: Coordinar TFLite y almacenamiento local.
///
/// Data Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';
import 'package:flutter/foundation.dart';

import 'dart:io';

import '../../core/constants/breeds.dart';
import '../../core/errors/exceptions.dart';
import '../../core/errors/failures.dart';
import '../../domain/entities/weight_estimation.dart';
import '../../domain/repositories/weight_estimation_repository.dart';
import '../datasources/ml_remote_datasource.dart';
import '../datasources/tflite_datasource.dart';
import '../datasources/weight_estimation_local_datasource.dart';
import '../models/weight_estimation_model.dart';

/// Implementación del repositorio de estimación de peso
class WeightEstimationRepositoryImpl implements WeightEstimationRepository {
  final TFLiteDataSource tfliteDataSource;
  final WeightEstimationLocalDataSource localDataSource;
  final MLRemoteDataSource? mlRemoteDataSource; // Opcional para fallback

  WeightEstimationRepositoryImpl({
    required this.tfliteDataSource,
    required this.localDataSource,
    this.mlRemoteDataSource,
  });

  @override
  Future<Either<Failure, WeightEstimation>> estimateWeight({
    required String imagePath,
    required BreedType breed,
    String? cattleId,
  }) async {
    // Intentar primero con el servidor (si está disponible)
    if (mlRemoteDataSource != null) {
      try {
        final imageFile = File(imagePath);
        if (await imageFile.exists()) {
          final prediction = await mlRemoteDataSource!.predictWeight(
            imageFile: imageFile,
            breed: breed.value,
            animalId: cattleId,
          );

          // Convertir respuesta del servidor a WeightEstimation entity
          final estimation = WeightEstimation(
            id: prediction.id,
            cattleId: prediction.animalId,
            breed: breed,
            estimatedWeight: prediction.estimatedWeightKg,
            confidenceScore: prediction.confidence,
            frameImagePath: imagePath,
            timestamp: prediction.timestamp,
            method: EstimationMethod.tflite, // El servidor usa TFLite
            modelVersion: prediction.mlModelVersion,
            processingTimeMs: prediction.processingTimeMs,
          );

          return Right(estimation);
        }
      } on NetworkException catch (e) {
        // Si no hay conexión, usar TFLite local como fallback
        debugPrint('⚠️ Sin conexión, usando TFLite local: ${e.message}');
      } on ServerException catch (e) {
        // Si el servidor falla, usar TFLite local como fallback
        debugPrint('⚠️ Error del servidor, usando TFLite local: ${e.message}');
      } catch (e) {
        // Cualquier otro error, usar TFLite local como fallback
        debugPrint('⚠️ Error con servidor, usando TFLite local: $e');
      }
    }

    // Fallback: Ejecutar inferencia con TFLite local
    try {
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
