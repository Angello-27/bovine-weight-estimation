/// UseCase: GetWeightHistoryUseCase
///
/// US-004: Obtener historial de pesajes con análisis.
/// Single Responsibility: Coordinar obtención de historial.
///
/// Domain Layer - Use Case
library;

import '../entities/weight_history.dart';
import '../repositories/weight_history_repository.dart';

/// Parámetros para obtener historial
class WeightHistoryParams {
  /// ID del animal
  final String cattleId;

  /// Fecha inicio (opcional, para filtrado por período)
  final DateTime? startDate;

  /// Fecha fin (opcional, para filtrado por período)
  final DateTime? endDate;

  const WeightHistoryParams({
    required this.cattleId,
    this.startDate,
    this.endDate,
  });
}

/// Caso de uso: Obtener historial de pesajes
class GetWeightHistoryUseCase {
  final WeightHistoryRepository repository;

  const GetWeightHistoryUseCase({required this.repository});

  /// Ejecuta el caso de uso
  ///
  /// Retorna [WeightHistory] con:
  /// - Lista de pesajes cronológica
  /// - GDP (Ganancia Diaria Promedio)
  /// - Proyecciones a 30/60/90 días
  /// - Anomalías detectadas
  Future<WeightHistory> call(WeightHistoryParams params) async {
    // Si hay filtro de período, usar método específico
    if (params.startDate != null && params.endDate != null) {
      return repository.getWeightHistoryByPeriod(
        cattleId: params.cattleId,
        startDate: params.startDate!,
        endDate: params.endDate!,
      );
    }

    // Si no, obtener historial completo
    return repository.getWeightHistory(params.cattleId);
  }
}
