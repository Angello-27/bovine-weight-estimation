/// UseCase: DetectAnomaliesUseCase
///
/// US-004: Detectar anomalías en el historial de pesajes.
/// Single Responsibility: Analizar historial y detectar patrones anormales.
///
/// Domain Layer - Use Case
library;

import 'package:dartz/dartz.dart';

import '../../core/constants/age_categories.dart';
import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/weight_history.dart';
import '../repositories/weight_history_repository.dart';

/// Caso de uso: Detectar anomalías en historial de peso
///
/// **Tipos de anomalías detectadas**:
/// 1. Pérdida significativa de peso (>5% entre pesajes consecutivos)
/// 2. Estancamiento en crecimiento (>15 días sin ganancia)
/// 3. GDP bajo para categoría de edad (<0.3 kg/día)
/// 4. Variación inusual (cambio >10% en <3 días)
///
/// **US-004 - Criterio de Aceptación 7**
class DetectAnomaliesUseCase
    implements UseCase<List<WeightAnomaly>, DetectAnomaliesParams> {
  final WeightHistoryRepository repository;

  const DetectAnomaliesUseCase({required this.repository});

  /// Ejecuta la detección de anomalías
  ///
  /// Retorna:
  /// - [Right(List<WeightAnomaly>)]: Lista de anomalías detectadas (puede ser vacía)
  /// - [Left(ValidationFailure)]: Si no hay suficientes datos
  /// - [Left(DatabaseFailure)]: Si hay error al consultar datos
  @override
  Future<Either<Failure, List<WeightAnomaly>>> call(
    DetectAnomaliesParams params,
  ) async {
    try {
      // 1. Validar parámetros
      if (params.cattleId.isEmpty) {
        return const Left(
          ValidationFailure(message: 'ID de animal no puede estar vacío'),
        );
      }

      // 2. Obtener historial del animal
      final history = await repository.getWeightHistory(params.cattleId);

      // 3. Validar que tenga suficientes pesajes para análisis
      if (history.weighings.length < 2) {
        // No hay anomalías si no hay datos suficientes
        return const Right([]);
      }

      final anomalies = <WeightAnomaly>[];

      // 4. Detectar pérdidas significativas de peso (>5% entre consecutivos)
      anomalies.addAll(_detectWeightLoss(history));

      // 5. Detectar estancamiento (>15 días sin ganancia)
      anomalies.addAll(_detectStagnation(history));

      // 6. Detectar GDP bajo para categoría
      final lowGdpAnomaly = _detectLowGdp(history);
      if (lowGdpAnomaly != null) {
        anomalies.add(lowGdpAnomaly);
      }

      // 7. Detectar variaciones inusuales
      anomalies.addAll(_detectUnusualVariations(history));

      // 8. Ordenar por fecha de detección (más reciente primero)
      anomalies.sort((a, b) => b.detectedAt.compareTo(a.detectedAt));

      return Right(anomalies);
    } catch (e) {
      return Left(
        UnexpectedFailure(
          message: 'Error inesperado al detectar anomalías: ${e.toString()}',
        ),
      );
    }
  }

  /// Detecta pérdidas significativas de peso (>5% entre consecutivos)
  List<WeightAnomaly> _detectWeightLoss(WeightHistory history) {
    final anomalies = <WeightAnomaly>[];

    for (int i = 1; i < history.weighings.length; i++) {
      final current = history.weighings[i];
      final previous = history.weighings[i - 1];

      final weightDiff = current.estimatedWeight - previous.estimatedWeight;
      final percentChange = (weightDiff / previous.estimatedWeight) * 100;

      // Si hay pérdida >5%
      if (percentChange < -5.0) {
        anomalies.add(
          WeightAnomaly(
            type: AnomalyType.significantWeightLoss,
            description:
                'Pérdida de ${percentChange.abs().toStringAsFixed(1)}% de peso '
                '(${weightDiff.abs().toStringAsFixed(1)} kg) '
                'entre ${_formatDate(previous.timestamp)} y ${_formatDate(current.timestamp)}',
            detectedAt: current.timestamp,
            severity: _calculateSeverity(percentChange.abs(), 5, 10, 15),
            value: weightDiff,
          ),
        );
      }
    }

    return anomalies;
  }

  /// Detecta estancamiento (>15 días sin ganancia)
  List<WeightAnomaly> _detectStagnation(WeightHistory history) {
    final anomalies = <WeightAnomaly>[];

    for (int i = 1; i < history.weighings.length; i++) {
      final current = history.weighings[i];
      final previous = history.weighings[i - 1];

      final daysBetween = current.timestamp
          .difference(previous.timestamp)
          .inDays;
      final weightGain = current.estimatedWeight - previous.estimatedWeight;

      // Si han pasado >15 días y hay ganancia ≤0 kg
      if (daysBetween > 15 && weightGain <= 0) {
        anomalies.add(
          WeightAnomaly(
            type: AnomalyType.growthStagnation,
            description:
                'Sin ganancia de peso durante $daysBetween días '
                '(${_formatDate(previous.timestamp)} - ${_formatDate(current.timestamp)}). '
                'Cambio: ${weightGain.toStringAsFixed(1)} kg',
            detectedAt: current.timestamp,
            severity: _calculateSeverity(daysBetween.toDouble(), 15, 30, 45),
            value: 0.0,
          ),
        );
      }
    }

    return anomalies;
  }

  /// Detecta GDP bajo para categoría de edad
  WeightAnomaly? _detectLowGdp(WeightHistory history) {
    // Necesitamos al menos 7 días para calcular GDP confiable
    if (!history.hasEnoughDataForAnalysis) return null;

    final gdp = history.averageDailyGain;

    // GDP mínimo esperado por categoría
    final ageCategory = history.cattle.ageCategory;
    final minGdpExpected = _getMinGdpForCategory(ageCategory);

    if (gdp < minGdpExpected) {
      return WeightAnomaly(
        type: AnomalyType.lowAverageDailyGain,
        description:
            'Ganancia diaria promedio baja: ${gdp.toStringAsFixed(2)} kg/día '
            '(esperado: ≥${minGdpExpected.toStringAsFixed(2)} kg/día para ${ageCategory.displayName})',
        detectedAt: history.weighings.last.timestamp,
        severity: _calculateGdpSeverity(gdp, minGdpExpected),
        value: gdp,
      );
    }

    return null;
  }

  /// Detecta variaciones inusuales (cambio >10% en <3 días)
  List<WeightAnomaly> _detectUnusualVariations(WeightHistory history) {
    final anomalies = <WeightAnomaly>[];

    for (int i = 1; i < history.weighings.length; i++) {
      final current = history.weighings[i];
      final previous = history.weighings[i - 1];

      final daysBetween = current.timestamp
          .difference(previous.timestamp)
          .inDays;
      final weightDiff = current.estimatedWeight - previous.estimatedWeight;
      final percentChange = (weightDiff / previous.estimatedWeight) * 100;

      // Si hay cambio >10% en menos de 3 días (probable error de medición)
      if (daysBetween < 3 && percentChange.abs() > 10.0) {
        anomalies.add(
          WeightAnomaly(
            type: AnomalyType.unusualVariation,
            description:
                'Variación inusual de ${percentChange.abs().toStringAsFixed(1)}% '
                '(${weightDiff.abs().toStringAsFixed(1)} kg) en solo $daysBetween día(s). '
                'Posible error de medición.',
            detectedAt: current.timestamp,
            severity: 3,
            value: percentChange,
          ),
        );
      }
    }

    return anomalies;
  }

  /// Obtiene el GDP mínimo esperado para una categoría de edad
  double _getMinGdpForCategory(AgeCategory category) {
    switch (category) {
      case AgeCategory.terneros:
        return 0.3; // Terneros: 0.3-0.6 kg/día
      case AgeCategory.vaquillonasTorillo:
        return 0.5; // Vaquillonas/Torillos: 0.5-0.8 kg/día
      case AgeCategory.vaquillonasToretes:
        return 0.6; // Vaquillonas/Toretes: 0.6-1.0 kg/día
      case AgeCategory.vacasToros:
        return 0.4; // Vacas/Toros: 0.4-0.7 kg/día
    }
  }

  /// Calcula severidad basada en umbrales (1-5)
  int _calculateSeverity(double value, double low, double medium, double high) {
    if (value >= high) return 5; // Crítico
    if (value >= medium) return 4; // Alto
    if (value >= low) return 3; // Medio
    return 2; // Bajo
  }

  /// Calcula severidad para GDP bajo
  int _calculateGdpSeverity(double gdp, double minExpected) {
    final diff = minExpected - gdp;
    if (diff >= 0.3) return 5; // Muy por debajo
    if (diff >= 0.2) return 4; // Significativamente bajo
    if (diff >= 0.1) return 3; // Moderadamente bajo
    return 2; // Ligeramente bajo
  }

  /// Formatea fecha para mostrar
  String _formatDate(DateTime date) {
    return '${date.day.toString().padLeft(2, '0')}/${date.month.toString().padLeft(2, '0')}/${date.year}';
  }
}

/// Parámetros para detectar anomalías
class DetectAnomaliesParams {
  /// ID del animal a analizar
  final String cattleId;

  const DetectAnomaliesParams({required this.cattleId});

  @override
  String toString() => 'DetectAnomaliesParams(cattleId: $cattleId)';
}
