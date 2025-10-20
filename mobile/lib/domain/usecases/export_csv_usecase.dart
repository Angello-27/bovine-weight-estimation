/// UseCase: ExportCsvUseCase
///
/// US-004: Exportar historial de pesajes a CSV.
/// Single Responsibility: Coordinar generación y exportación de CSV.
///
/// Domain Layer - Use Case
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../repositories/weight_history_repository.dart';

/// Caso de uso: Exportar historial a CSV
///
/// **Formato CSV** (US-004 - Criterio 9):
/// ```
/// animal_id,fecha,hora,peso_kg,metodo,confidence,latitud,longitud,raza,edad_meses,categoria
/// C001,2024-10-20,14:30:00,480.5,ia,0.95,-15.859500,-60.797889,Brahman,24,vaquillonas_toretes
/// ```
///
/// **Separador**: Coma (,)
/// **Encoding**: UTF-8
/// **Compatible con**: Excel, Google Sheets, R, Python pandas
class ExportCsvUseCase implements UseCase<String, ExportCsvParams> {
  final WeightHistoryRepository repository;

  const ExportCsvUseCase({required this.repository});

  /// Ejecuta la exportación a CSV
  ///
  /// Retorna:
  /// - [Right(String)]: Contenido CSV como string
  /// - [Left(ValidationFailure)]: Si no hay datos para exportar
  /// - [Left(DatabaseFailure)]: Si hay error al consultar datos
  @override
  Future<Either<Failure, String>> call(ExportCsvParams params) async {
    try {
      // 1. Si se especifica un animal, validar ID
      if (params.cattleId != null && params.cattleId!.isEmpty) {
        return const Left(
          ValidationFailure(message: 'ID de animal no puede estar vacío'),
        );
      }

      // 2. Si es un solo animal, verificar que tenga pesajes
      if (params.cattleId != null) {
        final history = await repository.getWeightHistory(params.cattleId!);

        if (history.weighings.isEmpty) {
          return const Left(
            ValidationFailure(
              message: 'El animal no tiene pesajes para exportar',
            ),
          );
        }
      }

      // 3. Generar CSV a través del repositorio
      // Si cattleId es null, exporta todos los animales
      final csvContent = await repository.exportToCsv(
        cattleId: params.cattleId,
      );

      // 4. Validar que se generó contenido (al menos header)
      if (csvContent.isEmpty || csvContent.split('\n').length < 2) {
        return const Left(
          ValidationFailure(message: 'No hay datos para exportar a CSV'),
        );
      }

      return Right(csvContent);
    } on ValidationFailure catch (e) {
      return Left(e);
    } on DatabaseFailure catch (e) {
      return Left(e);
    } catch (e) {
      return Left(
        UnexpectedFailure(
          message: 'Error inesperado al exportar CSV: ${e.toString()}',
        ),
      );
    }
  }
}

/// Parámetros para exportar a CSV
class ExportCsvParams {
  /// ID del animal a exportar (si null, exporta todos)
  final String? cattleId;

  /// Incluir header con nombres de columnas (default: true)
  final bool includeHeader;

  /// Formato de fecha (default: 'yyyy-MM-dd')
  final String dateFormat;

  /// Separador de decimales (default: '.')
  final String decimalSeparator;

  const ExportCsvParams({
    this.cattleId,
    this.includeHeader = true,
    this.dateFormat = 'yyyy-MM-dd',
    this.decimalSeparator = '.',
  });

  @override
  String toString() =>
      'ExportCsvParams('
      'cattleId: $cattleId, '
      'includeHeader: $includeHeader, '
      'dateFormat: $dateFormat, '
      'decimalSeparator: $decimalSeparator'
      ')';
}
