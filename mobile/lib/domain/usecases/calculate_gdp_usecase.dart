/// UseCase: CalculateGdpUseCase
///
/// US-004: Calcular Ganancia Diaria Promedio (GDP) de un animal.
/// Single Responsibility: Coordinar cálculo de GDP con validaciones.
///
/// Domain Layer - Use Case
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../repositories/weight_history_repository.dart';

/// Caso de uso: Calcular GDP (Ganancia Diaria Promedio)
///
/// **Fórmula GDP**:
/// GDP = (Peso Final - Peso Inicial) / Días Transcurridos
///
/// **Validaciones**:
/// - Debe haber ≥2 pesajes
/// - Debe haber ≥7 días entre primer y último pesaje
/// - Peso final debe ser > 0
/// - Peso inicial debe ser > 0
///
/// **Benchmarks GDP esperados por categoría**:
/// - Terneros (<8m): 0.3-0.6 kg/día
/// - Vaquillonas/Torillos (6-18m): 0.5-0.8 kg/día
/// - Vaquillonas/Toretes (19-30m): 0.6-1.0 kg/día
/// - Vacas/Toros (>30m): 0.4-0.7 kg/día
class CalculateGdpUseCase implements UseCase<double, CalculateGdpParams> {
  final WeightHistoryRepository repository;

  const CalculateGdpUseCase({required this.repository});

  /// Ejecuta el cálculo del GDP
  ///
  /// Retorna:
  /// - [Right(double)]: GDP en kg/día (ej: 0.52)
  /// - [Left(ValidationFailure)]: Si no hay suficientes datos
  /// - [Left(DatabaseFailure)]: Si hay error al consultar datos
  @override
  Future<Either<Failure, double>> call(CalculateGdpParams params) async {
    try {
      // 1. Validar parámetros
      if (params.cattleId.isEmpty) {
        return const Left(
          ValidationFailure(message: 'ID de animal no puede estar vacío'),
        );
      }

      // 2. Obtener historial del animal
      final history = await repository.getWeightHistory(params.cattleId);

      // 3. Validar que tenga suficientes pesajes
      if (history.weighings.length < 2) {
        return const Left(
          ValidationFailure(
            message: 'Se requieren al menos 2 pesajes para calcular GDP',
          ),
        );
      }

      // 4. Obtener primer y último pesaje (el historial ya viene ordenado)
      final firstWeighing = history.weighings.first;
      final lastWeighing = history.weighings.last;

      // 5. Calcular días transcurridos
      final daysBetween = lastWeighing.timestamp
          .difference(firstWeighing.timestamp)
          .inDays;

      // 6. Validar que haya al menos 7 días
      if (daysBetween < 7) {
        return Left(
          ValidationFailure(
            message:
                'Se requieren al menos 7 días entre pesajes (actual: $daysBetween días)',
          ),
        );
      }

      // 7. Validar pesos válidos
      if (firstWeighing.estimatedWeight <= 0 ||
          lastWeighing.estimatedWeight <= 0) {
        return const Left(
          ValidationFailure(message: 'Pesos deben ser mayores a 0 kg'),
        );
      }

      // 8. Calcular GDP
      final weightGain =
          lastWeighing.estimatedWeight - firstWeighing.estimatedWeight;
      final gdp = weightGain / daysBetween;

      // 9. Validar GDP razonable (no puede ser negativo excesivo ni muy alto)
      // Rango aceptable: -0.5 a +2.0 kg/día
      if (gdp < -0.5 || gdp > 2.0) {
        // Advertir pero no fallar
        // logger.warning('GDP fuera de rango típico: $gdp kg/día');
      }

      return Right(gdp);
    } catch (e) {
      return Left(
        UnexpectedFailure(
          message: 'Error inesperado al calcular GDP: ${e.toString()}',
        ),
      );
    }
  }
}

/// Parámetros para calcular GDP
class CalculateGdpParams {
  /// ID del animal
  final String cattleId;

  const CalculateGdpParams({required this.cattleId});

  @override
  String toString() => 'CalculateGdpParams(cattleId: $cattleId)';
}
