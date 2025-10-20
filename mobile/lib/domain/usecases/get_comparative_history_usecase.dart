/// UseCase: GetComparativeHistoryUseCase
///
/// US-004: Obtener historial comparativo de múltiples animales.
/// Single Responsibility: Coordinar obtención de historiales para comparación.
///
/// Domain Layer - Use Case
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/weight_history.dart';
import '../repositories/weight_history_repository.dart';

/// Caso de uso: Obtener historial comparativo de múltiples animales
///
/// **US-004 - Criterio de Aceptación 6**:
/// Comparar 2-5 animales en mismo gráfico con colores diferenciados.
///
/// **Validaciones**:
/// - Mínimo 2 animales
/// - Máximo 5 animales (legibilidad del gráfico)
/// - Todos los IDs deben existir
class GetComparativeHistoryUseCase
    implements UseCase<Map<String, WeightHistory>, ComparativeHistoryParams> {
  final WeightHistoryRepository repository;

  const GetComparativeHistoryUseCase({required this.repository});

  /// Ejecuta la obtención de historiales comparativos
  ///
  /// Retorna:
  /// - [Right(Map<String, WeightHistory>)]: Mapa de ID → WeightHistory
  /// - [Left(ValidationFailure)]: Si los parámetros son inválidos
  /// - [Left(DatabaseFailure)]: Si hay error al consultar datos
  @override
  Future<Either<Failure, Map<String, WeightHistory>>> call(
    ComparativeHistoryParams params,
  ) async {
    try {
      // 1. Validar cantidad de animales (2-5)
      if (params.cattleIds.isEmpty) {
        return const Left(
          ValidationFailure(
            message: 'Debe proporcionar al menos 1 ID de animal',
          ),
        );
      }

      if (params.cattleIds.length < 2) {
        return const Left(
          ValidationFailure(
            message: 'Comparación requiere al menos 2 animales',
          ),
        );
      }

      if (params.cattleIds.length > 5) {
        return const Left(
          ValidationFailure(
            message: 'Máximo 5 animales para comparación (legibilidad)',
          ),
        );
      }

      // 2. Validar que no haya IDs duplicados
      final uniqueIds = params.cattleIds.toSet();
      if (uniqueIds.length != params.cattleIds.length) {
        return const Left(
          ValidationFailure(
            message: 'No se permiten IDs de animales duplicados',
          ),
        );
      }

      // 3. Obtener historiales a través del repositorio
      final comparativeHistory = await repository.getComparativeHistory(
        params.cattleIds,
      );

      // 4. Validar que se obtuvieron todos los historiales
      if (comparativeHistory.length != params.cattleIds.length) {
        final missingIds = params.cattleIds
            .where((id) => !comparativeHistory.containsKey(id))
            .toList();

        return Left(
          DatabaseFailure(
            message:
                'No se encontraron datos para los animales: ${missingIds.join(", ")}',
          ),
        );
      }

      // 5. Validar que todos tengan al menos 2 pesajes
      final animalsWithoutData = <String>[];
      for (final entry in comparativeHistory.entries) {
        if (entry.value.weighings.length < 2) {
          animalsWithoutData.add(entry.key);
        }
      }

      if (animalsWithoutData.isNotEmpty) {
        return Left(
          ValidationFailure(
            message:
                'Los siguientes animales no tienen suficientes pesajes para comparar: '
                '${animalsWithoutData.join(", ")} (mínimo 2)',
          ),
        );
      }

      return Right(comparativeHistory);
    } on ValidationFailure catch (e) {
      return Left(e);
    } on DatabaseFailure catch (e) {
      return Left(e);
    } catch (e) {
      return Left(
        UnexpectedFailure(
          message:
              'Error inesperado al obtener historiales comparativos: ${e.toString()}',
        ),
      );
    }
  }
}

/// Parámetros para obtener historial comparativo
class ComparativeHistoryParams {
  /// Lista de IDs de animales a comparar (2-5 animales)
  final List<String> cattleIds;

  /// Filtro de período (opcional)
  final DateTime? startDate;

  /// Filtro de período (opcional)
  final DateTime? endDate;

  const ComparativeHistoryParams({
    required this.cattleIds,
    this.startDate,
    this.endDate,
  });

  @override
  String toString() =>
      'ComparativeHistoryParams('
      'cattleIds: ${cattleIds.join(", ")}, '
      'startDate: $startDate, '
      'endDate: $endDate'
      ')';
}
