/// Repository Implementation: WeightHistoryRepositoryImpl
///
/// Implementación del repositorio de historial de pesajes.
/// Single Responsibility: Obtener y analizar historial desde SQLite.
///
/// Data Layer - Repository Implementation
library;

import 'package:flutter/foundation.dart';

import '../../core/errors/exceptions.dart';
import '../../domain/entities/cattle.dart';
import '../../domain/entities/weight_history.dart';
import '../../domain/entities/weight_estimation.dart';
import '../../domain/repositories/weight_history_repository.dart';
import '../datasources/cattle_local_datasource.dart';
import '../datasources/weight_estimation_local_datasource.dart';

/// Implementación del repositorio de historial
class WeightHistoryRepositoryImpl implements WeightHistoryRepository {
  final WeightEstimationLocalDataSource weightEstimationDataSource;
  final CattleLocalDataSource cattleDataSource;

  const WeightHistoryRepositoryImpl({
    required this.weightEstimationDataSource,
    required this.cattleDataSource,
  });

  @override
  Future<WeightHistory> getWeightHistory(String cattleId) async {
    try {
      // 1. Obtener información del animal
      final cattleModel = await cattleDataSource.getCattleById(cattleId);

      if (cattleModel == null) {
        throw DatabaseException(
          message: 'Animal no encontrado con ID: $cattleId',
        );
      }

      // 2. Obtener todos los pesajes del animal
      final weighings = await weightEstimationDataSource.getEstimationsByCattle(
        cattleId,
      );

      // 3. Ordenar por fecha (más reciente primero)
      weighings.sort((a, b) => b.timestamp.compareTo(a.timestamp));

      // 4. Calcular análisis
      return _calculateAnalysis(cattleModel, weighings);
    } on DatabaseException {
      rethrow;
    } catch (e) {
      debugPrint('Error al obtener historial: $e');
      throw DatabaseException(message: 'Error al cargar historial de peso');
    }
  }

  @override
  Future<WeightHistory> getWeightHistoryByPeriod({
    required String cattleId,
    required DateTime startDate,
    required DateTime endDate,
  }) async {
    try {
      // 1. Obtener información del animal
      final cattleModel = await cattleDataSource.getCattleById(cattleId);

      if (cattleModel == null) {
        throw DatabaseException(
          message: 'Animal no encontrado con ID: $cattleId',
        );
      }

      // 2. Obtener pesajes del período
      final allWeighings = await weightEstimationDataSource
          .getEstimationsByCattle(cattleId);

      // 3. Filtrar por período
      final filteredWeighings = allWeighings.where((w) {
        return w.timestamp.isAfter(startDate) &&
            w.timestamp.isBefore(endDate.add(const Duration(days: 1)));
      }).toList();

      // 4. Ordenar por fecha
      filteredWeighings.sort((a, b) => b.timestamp.compareTo(a.timestamp));

      // 5. Calcular análisis
      return _calculateAnalysis(cattleModel, filteredWeighings);
    } catch (e) {
      debugPrint('Error al obtener historial por período: $e');
      throw DatabaseException(message: 'Error al cargar historial de peso');
    }
  }

  @override
  Future<Map<String, WeightHistory>> getComparativeHistory(
    List<String> cattleIds,
  ) async {
    final result = <String, WeightHistory>{};

    for (final cattleId in cattleIds) {
      try {
        result[cattleId] = await getWeightHistory(cattleId);
      } catch (e) {
        debugPrint('Error al obtener historial de $cattleId: $e');
        // Continuar con los demás
      }
    }

    return result;
  }

  @override
  Future<List<int>> exportToPdf(String cattleId) async {
    // TODO: Implementar exportación PDF con package:pdf
    throw UnimplementedError('Exportación PDF en desarrollo');
  }

  @override
  Future<String> exportToCsv({String? cattleId}) async {
    // TODO: Implementar exportación CSV
    throw UnimplementedError('Exportación CSV en desarrollo');
  }

  /// Calcula análisis completo del historial
  WeightHistory _calculateAnalysis(
    Cattle cattle,
    List<WeightEstimation> weighings,
  ) {
    // Si no hay pesajes, retornar historial vacío
    if (weighings.isEmpty) {
      return WeightHistory(
        cattleId: cattle.id,
        cattle: cattle,
        weighings: [],
        totalGain: 0.0,
        averageDailyGain: 0.0,
        anomalies: [],
      );
    }

    // Pesos (ordenados cronológicamente: más antiguo primero para cálculos)
    final sortedWeighings = [...weighings]
      ..sort((a, b) => a.timestamp.compareTo(b.timestamp));

    final currentWeight = sortedWeighings.last.estimatedWeight;
    final initialWeight = sortedWeighings.first.estimatedWeight;
    final totalGain = currentWeight - initialWeight;

    // Calcular GDP (Ganancia Diaria Promedio)
    final daysBetween = sortedWeighings.last.timestamp
        .difference(sortedWeighings.first.timestamp)
        .inDays;
    final gdp = daysBetween > 0 ? totalGain / daysBetween : 0.0;

    // Proyecciones (basadas en GDP)
    final projected30 = daysBetween > 7 ? currentWeight + (gdp * 30) : null;
    final projected60 = daysBetween > 7 ? currentWeight + (gdp * 60) : null;
    final projected90 = daysBetween > 7 ? currentWeight + (gdp * 90) : null;

    // Detectar anomalías
    final anomalies = _detectAnomalies(sortedWeighings, gdp);

    return WeightHistory(
      cattleId: cattle.id,
      cattle: cattle,
      weighings: weighings, // Mantener orden original (más reciente primero)
      currentWeight: currentWeight,
      initialWeight: initialWeight,
      totalGain: totalGain,
      averageDailyGain: gdp,
      projectedWeight30Days: projected30,
      projectedWeight60Days: projected60,
      projectedWeight90Days: projected90,
      anomalies: anomalies,
    );
  }

  /// Detecta anomalías en el historial
  ///
  /// Criterios según US-004:
  /// - Pérdida >5% en 7 días
  /// - Estancamiento >15 días sin ganancia
  /// - GDP bajo para categoría
  List<WeightAnomaly> _detectAnomalies(
    List<WeightEstimation> weighings,
    double averageGdp,
  ) {
    final anomalies = <WeightAnomaly>[];

    // Necesita al menos 2 pesajes
    if (weighings.length < 2) return anomalies;

    // Recorrer pesajes consecutivos
    for (var i = 1; i < weighings.length; i++) {
      final current = weighings[i];
      final previous = weighings[i - 1];

      final weightChange = current.estimatedWeight - previous.estimatedWeight;
      final percentChange = (weightChange / previous.estimatedWeight) * 100;
      final daysBetween = current.timestamp
          .difference(previous.timestamp)
          .inDays;

      // 1. Pérdida significativa (>5% en 7 días)
      if (percentChange < -5.0 && daysBetween <= 7) {
        anomalies.add(
          WeightAnomaly(
            type: AnomalyType.significantWeightLoss,
            description:
                'Pérdida de ${percentChange.abs().toStringAsFixed(1)}% en $daysBetween días',
            detectedAt: current.timestamp,
            severity: 5, // Crítico
            value: percentChange,
          ),
        );
      }

      // 2. Estancamiento (>15 días sin ganancia significativa)
      if (daysBetween > 15 && weightChange.abs() < 2.0) {
        anomalies.add(
          WeightAnomaly(
            type: AnomalyType.growthStagnation,
            description: 'Sin ganancia significativa en $daysBetween días',
            detectedAt: current.timestamp,
            severity: 3, // Importante
            value: weightChange,
          ),
        );
      }

      // 3. Variación inusual (>20 kg entre pesajes consecutivos)
      if (weightChange.abs() > 20.0 && daysBetween < 7) {
        anomalies.add(
          WeightAnomaly(
            type: AnomalyType.unusualVariation,
            description:
                'Variación de ${weightChange.toStringAsFixed(1)} kg en $daysBetween días',
            detectedAt: current.timestamp,
            severity: 2, // Advertencia
            value: weightChange,
          ),
        );
      }
    }

    // 4. GDP bajo (< 0.5 kg/día para animales en crecimiento)
    if (averageGdp < 0.5 && averageGdp > 0) {
      anomalies.add(
        WeightAnomaly(
          type: AnomalyType.lowAverageDailyGain,
          description: 'GDP de ${averageGdp.toStringAsFixed(2)} kg/día es bajo',
          detectedAt: DateTime.now(),
          severity: 3,
          value: averageGdp,
        ),
      );
    }

    return anomalies;
  }
}
