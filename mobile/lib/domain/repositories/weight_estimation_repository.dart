/// Repository Interface: WeightEstimationRepository
/// 
/// Contrato para operaciones de estimación de peso con IA.
/// Single Responsibility: Definir operaciones de estimación.
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/constants/breeds.dart';
import '../../core/errors/failures.dart';
import '../entities/weight_estimation.dart';

/// Repositorio para estimación de peso
abstract class WeightEstimationRepository {
  /// Estima el peso de un animal usando IA
  /// 
  /// Parámetros:
  /// - [imagePath]: Path de la imagen del animal
  /// - [breed]: Raza del animal (determina qué modelo TFLite usar)
  /// - [cattleId]: ID del animal (opcional, para vincular con registro)
  /// 
  /// Retorna:
  /// - [Right(WeightEstimation)]: Estimación exitosa con peso y confidence
  /// - [Left(Failure)]: Error durante la estimación
  Future<Either<Failure, WeightEstimation>> estimateWeight({
    required String imagePath,
    required BreedType breed,
    String? cattleId,
  });

  /// Guarda una estimación en almacenamiento local (SQLite)
  /// 
  /// Parámetros:
  /// - [estimation]: Estimación a guardar
  /// 
  /// Retorna:
  /// - [Right(void)]: Guardado exitoso
  /// - [Left(Failure)]: Error al guardar
  Future<Either<Failure, void>> saveEstimation(WeightEstimation estimation);

  /// Obtiene todas las estimaciones guardadas
  /// 
  /// Retorna:
  /// - [Right(List<WeightEstimation>)]: Lista de estimaciones
  /// - [Left(Failure)]: Error al obtener estimaciones
  Future<Either<Failure, List<WeightEstimation>>> getAllEstimations();

  /// Obtiene estimaciones de un animal específico
  /// 
  /// Parámetros:
  /// - [cattleId]: ID del animal
  /// 
  /// Retorna:
  /// - [Right(List<WeightEstimation>)]: Lista de estimaciones del animal
  /// - [Left(Failure)]: Error al obtener estimaciones
  Future<Either<Failure, List<WeightEstimation>>> getEstimationsByCattle(
    String cattleId,
  );

  /// Obtiene la última estimación de un animal
  /// 
  /// Parámetros:
  /// - [cattleId]: ID del animal
  /// 
  /// Retorna:
  /// - [Right(WeightEstimation?)]: Última estimación o null
  /// - [Left(Failure)]: Error al obtener estimación
  Future<Either<Failure, WeightEstimation?>> getLastEstimation(String cattleId);

  /// Elimina una estimación
  /// 
  /// Parámetros:
  /// - [estimationId]: ID de la estimación a eliminar
  /// 
  /// Retorna:
  /// - [Right(void)]: Eliminación exitosa
  /// - [Left(Failure)]: Error al eliminar
  Future<Either<Failure, void>> deleteEstimation(String estimationId);

  /// Verifica si los modelos TFLite están cargados
  /// 
  /// Retorna:
  /// - [Right(bool)]: true si los modelos están listos
  /// - [Left(Failure)]: Error al verificar modelos
  Future<Either<Failure, bool>> areModelsLoaded();

  /// Carga los modelos TFLite de las razas especificadas
  /// 
  /// Parámetros:
  /// - [breeds]: Lista de razas cuyos modelos se deben cargar
  ///            Si es null, carga todas las 7 razas
  /// 
  /// Retorna:
  /// - [Right(void)]: Modelos cargados exitosamente
  /// - [Left(Failure)]: Error al cargar modelos
  Future<Either<Failure, void>> loadModels([List<BreedType>? breeds]);
}

