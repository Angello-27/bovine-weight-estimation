/// Repository Interface: WeightHistoryRepository
///
/// Contrato para acceso a historial de pesajes.
/// Single Responsibility: Definir operaciones de historial.
///
/// Domain Layer - Repository Interface
library;

import '../entities/weight_history.dart';

/// Repository para gestión de historial de pesajes
abstract class WeightHistoryRepository {
  /// Obtiene el historial completo de un animal
  ///
  /// [cattleId] ID del animal
  /// Retorna [WeightHistory] con análisis calculado (GDP, anomalías, proyecciones)
  Future<WeightHistory> getWeightHistory(String cattleId);

  /// Obtiene historial filtrado por período
  ///
  /// [cattleId] ID del animal
  /// [startDate] Fecha inicio del período
  /// [endDate] Fecha fin del período
  Future<WeightHistory> getWeightHistoryByPeriod({
    required String cattleId,
    required DateTime startDate,
    required DateTime endDate,
  });

  /// Obtiene historial comparativo de múltiples animales
  ///
  /// [cattleIds] Lista de IDs de animales (2-5 animales)
  /// Retorna mapa de ID → WeightHistory para comparación
  Future<Map<String, WeightHistory>> getComparativeHistory(
    List<String> cattleIds,
  );

  /// Exporta historial individual a PDF
  ///
  /// [cattleId] ID del animal
  /// Retorna bytes del PDF generado
  Future<List<int>> exportToPdf(String cattleId);

  /// Exporta historial a CSV
  ///
  /// [cattleId] ID del animal (si null, exporta todos)
  /// Retorna string CSV
  Future<String> exportToCsv({String? cattleId});
}
