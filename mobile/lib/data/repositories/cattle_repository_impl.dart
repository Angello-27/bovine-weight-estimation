/// Repository Implementation: CattleRepositoryImpl
/// 
/// Implementación del repositorio de ganado.
/// Single Responsibility: Coordinar operaciones CRUD de ganado.
///
/// Data Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/exceptions.dart';
import '../../core/errors/failures.dart';
import '../../domain/entities/cattle.dart';
import '../../domain/repositories/cattle_repository.dart';
import '../datasources/cattle_local_datasource.dart';
import '../models/cattle_model.dart';

/// Implementación del repositorio de ganado
class CattleRepositoryImpl implements CattleRepository {
  final CattleLocalDataSource localDataSource;

  CattleRepositoryImpl({
    required this.localDataSource,
  });

  @override
  Future<Either<Failure, Cattle>> registerCattle(Cattle cattle) async {
    try {
      final cattleModel = CattleModel.fromEntity(cattle);
      await localDataSource.saveCattle(cattleModel);
      return Right(cattle);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al registrar ganado: $e'));
    }
  }

  @override
  Future<Either<Failure, Cattle?>> getCattleById(String id) async {
    try {
      final cattle = await localDataSource.getCattleById(id);
      return Right(cattle);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al obtener ganado: $e'));
    }
  }

  @override
  Future<Either<Failure, Cattle?>> getCattleByEarTag(String earTag) async {
    try {
      final cattle = await localDataSource.getCattleByEarTag(earTag);
      return Right(cattle);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al buscar por caravana: $e'));
    }
  }

  @override
  Future<Either<Failure, List<Cattle>>> getAllCattle() async {
    try {
      final cattle = await localDataSource.getAllCattle();
      return Right(cattle);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al obtener ganado: $e'));
    }
  }

  @override
  Future<Either<Failure, List<Cattle>>> getActiveCattle() async {
    try {
      final cattle = await localDataSource.getActiveCattle();
      return Right(cattle);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al obtener ganado activo: $e'));
    }
  }

  @override
  Future<Either<Failure, List<Cattle>>> searchCattle(String searchTerm) async {
    try {
      final cattle = await localDataSource.searchCattle(searchTerm);
      return Right(cattle);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error en búsqueda: $e'));
    }
  }

  @override
  Future<Either<Failure, Cattle>> updateCattle(Cattle cattle) async {
    try {
      final cattleModel = CattleModel.fromEntity(cattle);
      final updatedCattle = cattleModel.copyWith(
        lastUpdated: DateTime.now(),
      );
      await localDataSource.updateCattle(updatedCattle);
      return Right(updatedCattle);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al actualizar ganado: $e'));
    }
  }

  @override
  Future<Either<Failure, Cattle>> updateCattleStatus(
    String id,
    CattleStatus status,
  ) async {
    try {
      final cattleResult = await getCattleById(id);
      
      return cattleResult.fold(
        (failure) => Left(failure),
        (cattle) async {
          if (cattle == null) {
            return const Left(ValidationFailure(message: 'Animal no encontrado'));
          }

          final updated = cattle.copyWith(status: status);
          return updateCattle(updated);
        },
      );
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al actualizar estado: $e'));
    }
  }

  @override
  Future<Either<Failure, void>> deleteCattle(String id) async {
    try {
      // Soft delete: cambiar estado a deceased
      await updateCattleStatus(id, CattleStatus.deceased);
      return const Right(null);
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al eliminar ganado: $e'));
    }
  }

  @override
  Future<Either<Failure, bool>> earTagExists(
    String earTag, {
    String? excludeId,
  }) async {
    try {
      final exists = await localDataSource.earTagExists(
        earTag,
        excludeId: excludeId,
      );
      return Right(exists);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al verificar caravana: $e'));
    }
  }

  @override
  Future<Either<Failure, Map<CattleStatus, int>>> getCattleCountByStatus() async {
    try {
      final counts = await localDataSource.getCattleCountByStatus();
      return Right(counts);
    } on DatabaseException catch (e) {
      return Left(DatabaseFailure(message: e.message));
    } catch (e) {
      return Left(UnknownFailure(message: 'Error al contar ganado: $e'));
    }
  }
}

