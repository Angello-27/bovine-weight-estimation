/// Repository Interface: CattleRepository
/// 
/// Contrato para operaciones CRUD de ganado.
/// Single Responsibility: Definir operaciones de gestión de ganado.
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../entities/cattle.dart';

/// Repositorio para gestión de ganado
abstract class CattleRepository {
  /// Registra un nuevo animal
  /// 
  /// Parámetros:
  /// - [cattle]: Animal a registrar
  /// 
  /// Retorna:
  /// - [Right(Cattle)]: Animal registrado exitosamente
  /// - [Left(Failure)]: Error (ej: caravana duplicada)
  Future<Either<Failure, Cattle>> registerCattle(Cattle cattle);

  /// Obtiene un animal por ID
  /// 
  /// Parámetros:
  /// - [id]: ID del animal
  /// 
  /// Retorna:
  /// - [Right(Cattle?)]: Animal encontrado o null
  /// - [Left(Failure)]: Error al buscar
  Future<Either<Failure, Cattle?>> getCattleById(String id);

  /// Obtiene un animal por número de caravana
  /// 
  /// Parámetros:
  /// - [earTag]: Número de caravana
  /// 
  /// Retorna:
  /// - [Right(Cattle?)]: Animal encontrado o null
  /// - [Left(Failure)]: Error al buscar
  Future<Either<Failure, Cattle?>> getCattleByEarTag(String earTag);

  /// Obtiene todos los animales
  /// 
  /// Retorna:
  /// - [Right(List<Cattle>)]: Lista de animales (ordenada por fecha desc)
  /// - [Left(Failure)]: Error al obtener lista
  Future<Either<Failure, List<Cattle>>> getAllCattle();

  /// Obtiene animales activos
  /// 
  /// Retorna:
  /// - [Right(List<Cattle>)]: Lista de animales activos
  /// - [Left(Failure)]: Error al obtener lista
  Future<Either<Failure, List<Cattle>>> getActiveCattle();

  /// Busca animales por término (caravana, nombre)
  /// 
  /// Parámetros:
  /// - [searchTerm]: Término de búsqueda
  /// 
  /// Retorna:
  /// - [Right(List<Cattle>)]: Animales que coinciden
  /// - [Left(Failure)]: Error en búsqueda
  Future<Either<Failure, List<Cattle>>> searchCattle(String searchTerm);

  /// Actualiza un animal
  /// 
  /// Parámetros:
  /// - [cattle]: Animal con datos actualizados
  /// 
  /// Retorna:
  /// - [Right(Cattle)]: Animal actualizado
  /// - [Left(Failure)]: Error al actualizar
  Future<Either<Failure, Cattle>> updateCattle(Cattle cattle);

  /// Cambia el estado de un animal
  /// 
  /// Parámetros:
  /// - [id]: ID del animal
  /// - [status]: Nuevo estado
  /// 
  /// Retorna:
  /// - [Right(Cattle)]: Animal con estado actualizado
  /// - [Left(Failure)]: Error al actualizar
  Future<Either<Failure, Cattle>> updateCattleStatus(
    String id,
    CattleStatus status,
  );

  /// Elimina un animal (soft delete - cambia a deceased)
  /// 
  /// Parámetros:
  /// - [id]: ID del animal
  /// 
  /// Retorna:
  /// - [Right(void)]: Animal eliminado (soft delete)
  /// - [Left(Failure)]: Error al eliminar
  Future<Either<Failure, void>> deleteCattle(String id);

  /// Verifica si una caravana ya existe
  /// 
  /// Parámetros:
  /// - [earTag]: Número de caravana a verificar
  /// - [excludeId]: ID a excluir (para edición)
  /// 
  /// Retorna:
  /// - [Right(bool)]: true si existe, false si no
  /// - [Left(Failure)]: Error al verificar
  Future<Either<Failure, bool>> earTagExists(String earTag, {String? excludeId});

  /// Obtiene el conteo total de animales por estado
  /// 
  /// Retorna:
  /// - [Right(Map<CattleStatus, int>)]: Conteo por estado
  /// - [Left(Failure)]: Error al contar
  Future<Either<Failure, Map<CattleStatus, int>>> getCattleCountByStatus();
}

