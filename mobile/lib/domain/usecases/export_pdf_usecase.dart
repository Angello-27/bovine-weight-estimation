/// UseCase: ExportPdfUseCase
///
/// US-004: Exportar historial de pesajes a PDF.
/// Single Responsibility: Coordinar generación y exportación de PDF.
///
/// Domain Layer - Use Case
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../repositories/weight_history_repository.dart';

/// Caso de uso: Exportar historial a PDF
///
/// **Contenido del PDF** (US-004 - Criterio 8):
/// - Logo de Hacienda Gamelera
/// - Datos del animal (caravana, raza, edad, categoría)
/// - Indicadores clave (peso actual, GDP, ganancia total)
/// - Gráfico de evolución de peso
/// - Tabla de pesajes (fecha, peso, método, confidence, GPS)
/// - Proyecciones a 30/60/90 días
/// - Anomalías detectadas (si las hay)
///
/// **Formato**:
/// - Tamaño: A4
/// - Orientación: Portrait
/// - Calidad: Alta (para impresión)
class ExportPdfUseCase implements UseCase<List<int>, ExportPdfParams> {
  final WeightHistoryRepository repository;

  const ExportPdfUseCase({required this.repository});

  /// Ejecuta la exportación a PDF
  ///
  /// Retorna:
  /// - [Right(List<int>)]: Bytes del PDF generado
  /// - [Left(ValidationFailure)]: Si no hay datos para exportar
  /// - [Left(StorageFailure)]: Si hay error al generar PDF
  /// - [Left(DatabaseFailure)]: Si hay error al consultar datos
  @override
  Future<Either<Failure, List<int>>> call(ExportPdfParams params) async {
    try {
      // 1. Validar parámetros
      if (params.cattleId.isEmpty) {
        return const Left(
          ValidationFailure(message: 'ID de animal no puede estar vacío'),
        );
      }

      // 2. Verificar que el animal tenga pesajes
      final history = await repository.getWeightHistory(params.cattleId);

      if (history.weighings.isEmpty) {
        return const Left(
          ValidationFailure(
            message: 'El animal no tiene pesajes para exportar',
          ),
        );
      }

      // 3. Generar PDF a través del repositorio
      // El repositorio implementa la lógica específica de generación
      final pdfBytes = await repository.exportToPdf(params.cattleId);

      // 4. Validar que se generó contenido
      if (pdfBytes.isEmpty) {
        return const Left(
          StorageFailure(message: 'Error: PDF generado está vacío'),
        );
      }

      return Right(pdfBytes);
    } on ValidationFailure catch (e) {
      return Left(e);
    } on DatabaseFailure catch (e) {
      return Left(e);
    } on StorageFailure catch (e) {
      return Left(e);
    } catch (e) {
      return Left(
        UnexpectedFailure(
          message: 'Error inesperado al exportar PDF: ${e.toString()}',
        ),
      );
    }
  }
}

/// Parámetros para exportar a PDF
class ExportPdfParams {
  /// ID del animal a exportar
  final String cattleId;

  /// Incluir gráfico de evolución (default: true)
  final bool includeChart;

  /// Incluir tabla de pesajes (default: true)
  final bool includeTable;

  /// Incluir anomalías detectadas (default: true)
  final bool includeAnomalies;

  /// Incluir proyecciones (default: true)
  final bool includeProjections;

  const ExportPdfParams({
    required this.cattleId,
    this.includeChart = true,
    this.includeTable = true,
    this.includeAnomalies = true,
    this.includeProjections = true,
  });

  @override
  String toString() =>
      'ExportPdfParams('
      'cattleId: $cattleId, '
      'includeChart: $includeChart, '
      'includeTable: $includeTable, '
      'includeAnomalies: $includeAnomalies, '
      'includeProjections: $includeProjections'
      ')';
}
