/// Repository Implementation: WeightHistoryRepositoryImpl
///
/// Implementación del repositorio de historial de pesajes.
/// Single Responsibility: Obtener y analizar historial desde SQLite.
///
/// Data Layer - Repository Implementation
library;

import 'package:csv/csv.dart';
import 'package:flutter/foundation.dart';
import 'package:intl/intl.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;

import '../../core/constants/breeds.dart';
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
        // Si no existe el animal, retornar historial vacío en lugar de error
        // Esto puede pasar si es la primera vez que se usa la app
        return WeightHistory(
          cattleId: cattleId,
          cattle: Cattle(
            id: cattleId,
            earTag: 'N/A',
            breed: BreedType.nelore, // Valor por defecto
            birthDate: DateTime.now(),
            gender: Gender.male,
            registrationDate: DateTime.now(),
            lastUpdated: DateTime.now(),
          ),
          weighings: [],
          totalGain: 0.0,
          averageDailyGain: 0.0,
          anomalies: [],
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
    } on DatabaseException catch (e) {
      // Detectar errores específicos y convertirlos en mensajes amigables
      final errorMessage = e.message.toLowerCase();
      if (errorMessage.contains('no such table') ||
          errorMessage.contains('table') &&
              errorMessage.contains('not exist')) {
        // Si la tabla no existe, retornar historial vacío
        debugPrint('Tabla no encontrada, retornando historial vacío: $e');
        return WeightHistory(
          cattleId: cattleId,
          cattle: Cattle(
            id: cattleId,
            earTag: 'N/A',
            breed: BreedType.nelore, // Valor por defecto
            birthDate: DateTime.now(),
            gender: Gender.male,
            registrationDate: DateTime.now(),
            lastUpdated: DateTime.now(),
          ),
          weighings: [],
          totalGain: 0.0,
          averageDailyGain: 0.0,
          anomalies: [],
        );
      }
      rethrow;
    } catch (e) {
      debugPrint('Error al obtener historial: $e');
      // Si es un error desconocido, retornar historial vacío en lugar de lanzar error
      final errorMessage = e.toString().toLowerCase();
      if (errorMessage.contains('no such table') ||
          errorMessage.contains('table') &&
              errorMessage.contains('not exist')) {
        return WeightHistory(
          cattleId: cattleId,
          cattle: Cattle(
            id: cattleId,
            earTag: 'N/A',
            breed: BreedType.nelore, // Valor por defecto
            birthDate: DateTime.now(),
            gender: Gender.male,
            registrationDate: DateTime.now(),
            lastUpdated: DateTime.now(),
          ),
          weighings: [],
          totalGain: 0.0,
          averageDailyGain: 0.0,
          anomalies: [],
        );
      }
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
    try {
      // 1. Obtener historial completo del animal
      final history = await getWeightHistory(cattleId);

      if (history.weighings.isEmpty) {
        throw ValidationException(
          message: 'No hay datos de pesajes para exportar',
        );
      }

      // 2. Crear documento PDF
      final pdf = pw.Document();

      // 3. Formatear fechas
      final dateFormatter = DateFormat('dd/MM/yyyy HH:mm');
      final now = DateTime.now();

      // 4. Agregar página con contenido
      pdf.addPage(
        pw.MultiPage(
          pageFormat: PdfPageFormat.a4,
          margin: const pw.EdgeInsets.all(40),
          build: (context) => [
            // Header
            pw.Header(
              level: 0,
              child: pw.Column(
                crossAxisAlignment: pw.CrossAxisAlignment.start,
                children: [
                  pw.Text(
                    'Hacienda Gamelera',
                    style: pw.TextStyle(
                      fontSize: 24,
                      fontWeight: pw.FontWeight.bold,
                    ),
                  ),
                  pw.SizedBox(height: 5),
                  pw.Text(
                    'San Ignacio de Velasco, Bolivia',
                    style: const pw.TextStyle(fontSize: 12),
                  ),
                  pw.Text(
                    'GPS: 15°51\'34.2"S, 60°47\'52.4"W',
                    style: const pw.TextStyle(fontSize: 10),
                  ),
                  pw.SizedBox(height: 20),
                  pw.Divider(),
                ],
              ),
            ),

            // Título
            pw.SizedBox(height: 10),
            pw.Text(
              'Historial de Pesajes',
              style: pw.TextStyle(fontSize: 20, fontWeight: pw.FontWeight.bold),
            ),
            pw.Text(
              'Generado: ${dateFormatter.format(now)}',
              style: const pw.TextStyle(fontSize: 10),
            ),
            pw.SizedBox(height: 20),

            // Información del animal
            pw.Container(
              padding: const pw.EdgeInsets.all(10),
              decoration: pw.BoxDecoration(
                border: pw.Border.all(color: PdfColors.grey400),
                borderRadius: const pw.BorderRadius.all(pw.Radius.circular(5)),
              ),
              child: pw.Column(
                crossAxisAlignment: pw.CrossAxisAlignment.start,
                children: [
                  pw.Text(
                    'Datos del Animal',
                    style: pw.TextStyle(
                      fontSize: 14,
                      fontWeight: pw.FontWeight.bold,
                    ),
                  ),
                  pw.SizedBox(height: 10),
                  _buildPdfInfoRow('Caravana:', history.cattle.earTag),
                  _buildPdfInfoRow(
                    'Nombre:',
                    history.cattle.name ?? 'Sin nombre',
                  ),
                  _buildPdfInfoRow('Raza:', history.cattle.breed.displayName),
                  _buildPdfInfoRow('Sexo:', history.cattle.gender.displayName),
                  _buildPdfInfoRow(
                    'Edad:',
                    '${history.cattle.ageInMonths} meses',
                  ),
                  _buildPdfInfoRow(
                    'Categoría:',
                    history.cattle.ageCategory.displayName,
                  ),
                ],
              ),
            ),
            pw.SizedBox(height: 20),

            // Indicadores clave
            pw.Text(
              'Indicadores Clave',
              style: pw.TextStyle(fontSize: 14, fontWeight: pw.FontWeight.bold),
            ),
            pw.SizedBox(height: 10),
            pw.Row(
              mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
              children: [
                _buildPdfStatCard(
                  'Peso Actual',
                  '${history.currentWeight?.toStringAsFixed(1) ?? "N/A"} kg',
                ),
                _buildPdfStatCard(
                  'Peso Inicial',
                  '${history.initialWeight?.toStringAsFixed(1) ?? "N/A"} kg',
                ),
                _buildPdfStatCard(
                  'Ganancia Total',
                  '${history.totalGain.toStringAsFixed(1)} kg',
                ),
                _buildPdfStatCard(
                  'GDP',
                  '${history.averageDailyGain.toStringAsFixed(2)} kg/día',
                ),
              ],
            ),
            pw.SizedBox(height: 20),

            // Proyecciones (si hay datos suficientes)
            if (history.projectedWeight30Days != null) ...[
              pw.Text(
                'Proyecciones de Peso',
                style: pw.TextStyle(
                  fontSize: 14,
                  fontWeight: pw.FontWeight.bold,
                ),
              ),
              pw.SizedBox(height: 10),
              pw.Row(
                mainAxisAlignment: pw.MainAxisAlignment.spaceAround,
                children: [
                  _buildPdfStatCard(
                    '30 días',
                    '${history.projectedWeight30Days!.toStringAsFixed(1)} kg',
                  ),
                  _buildPdfStatCard(
                    '60 días',
                    '${history.projectedWeight60Days!.toStringAsFixed(1)} kg',
                  ),
                  _buildPdfStatCard(
                    '90 días',
                    '${history.projectedWeight90Days!.toStringAsFixed(1)} kg',
                  ),
                ],
              ),
              pw.SizedBox(height: 20),
            ],

            // Anomalías detectadas
            if (history.anomalies.isNotEmpty) ...[
              pw.Text(
                'Anomalías Detectadas',
                style: pw.TextStyle(
                  fontSize: 14,
                  fontWeight: pw.FontWeight.bold,
                  color: PdfColors.red700,
                ),
              ),
              pw.SizedBox(height: 10),
              ...history.anomalies.map(
                (anomaly) => pw.Container(
                  margin: const pw.EdgeInsets.only(bottom: 5),
                  padding: const pw.EdgeInsets.all(8),
                  decoration: pw.BoxDecoration(
                    color: PdfColors.red50,
                    border: pw.Border.all(color: PdfColors.red200),
                    borderRadius: const pw.BorderRadius.all(
                      pw.Radius.circular(3),
                    ),
                  ),
                  child: pw.Text(
                    '⚠️ ${anomaly.description}',
                    style: const pw.TextStyle(fontSize: 10),
                  ),
                ),
              ),
              pw.SizedBox(height: 20),
            ],

            // Tabla de pesajes
            pw.Text(
              'Registro de Pesajes',
              style: pw.TextStyle(fontSize: 14, fontWeight: pw.FontWeight.bold),
            ),
            pw.SizedBox(height: 10),
            _buildPdfWeighingsTable(history.weighings, dateFormatter),
          ],
        ),
      );

      // 5. Generar bytes del PDF
      return pdf.save();
    } on ValidationException {
      rethrow;
    } on DatabaseException {
      rethrow;
    } catch (e) {
      debugPrint('Error al generar PDF: $e');
      throw StorageException(
        message: 'Error al generar archivo PDF: ${e.toString()}',
      );
    }
  }

  @override
  Future<String> exportToCsv({String? cattleId}) async {
    try {
      List<List<dynamic>> rows = [];

      // 1. Header CSV
      rows.add([
        'animal_id',
        'caravana',
        'nombre',
        'raza',
        'edad_meses',
        'categoria',
        'fecha',
        'hora',
        'peso_kg',
        'metodo',
        'confidence',
        'latitud',
        'longitud',
        'model_version',
      ]);

      // 2. Si es un solo animal, obtener sus datos
      if (cattleId != null) {
        final history = await getWeightHistory(cattleId);

        for (final weighing in history.weighings) {
          rows.add(_buildCsvRow(history.cattle, weighing));
        }
      } else {
        // 3. Si es para todos los animales, obtener todos
        final allEstimations = await weightEstimationDataSource
            .getAllEstimations();

        // Agrupar por animal y obtener datos de cada uno
        final animalIds = <String>{};
        for (final estimation in allEstimations) {
          if (estimation.cattleId != null) {
            animalIds.add(estimation.cattleId!);
          }
        }

        // Obtener datos completos de cada animal
        for (final animalId in animalIds) {
          try {
            final history = await getWeightHistory(animalId);

            for (final weighing in history.weighings) {
              rows.add(_buildCsvRow(history.cattle, weighing));
            }
          } catch (e) {
            debugPrint('Error al exportar animal $animalId: $e');
            // Continuar con los demás
          }
        }
      }

      // 4. Validar que haya datos
      if (rows.length < 2) {
        throw ValidationException(
          message: 'No hay datos de pesajes para exportar',
        );
      }

      // 5. Convertir a CSV
      final csvConverter = const ListToCsvConverter();
      return csvConverter.convert(rows);
    } on ValidationException {
      rethrow;
    } on DatabaseException {
      rethrow;
    } catch (e) {
      debugPrint('Error al generar CSV: $e');
      throw StorageException(
        message: 'Error al generar archivo CSV: ${e.toString()}',
      );
    }
  }

  /// Construye una fila de información para PDF
  pw.Widget _buildPdfInfoRow(String label, String value) {
    return pw.Padding(
      padding: const pw.EdgeInsets.only(bottom: 5),
      child: pw.Row(
        children: [
          pw.SizedBox(
            width: 100,
            child: pw.Text(
              label,
              style: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 11),
            ),
          ),
          pw.Text(value, style: const pw.TextStyle(fontSize: 11)),
        ],
      ),
    );
  }

  /// Construye una tarjeta de estadística para PDF
  pw.Widget _buildPdfStatCard(String label, String value) {
    return pw.Container(
      padding: const pw.EdgeInsets.all(10),
      decoration: pw.BoxDecoration(
        color: PdfColors.blue50,
        border: pw.Border.all(color: PdfColors.blue200),
        borderRadius: const pw.BorderRadius.all(pw.Radius.circular(5)),
      ),
      child: pw.Column(
        children: [
          pw.Text(label, style: const pw.TextStyle(fontSize: 10)),
          pw.SizedBox(height: 5),
          pw.Text(
            value,
            style: pw.TextStyle(fontSize: 14, fontWeight: pw.FontWeight.bold),
          ),
        ],
      ),
    );
  }

  /// Construye la tabla de pesajes para PDF
  pw.Widget _buildPdfWeighingsTable(
    List<WeightEstimation> weighings,
    DateFormat dateFormatter,
  ) {
    return pw.Table(
      border: pw.TableBorder.all(color: PdfColors.grey400),
      columnWidths: {
        0: const pw.FlexColumnWidth(2),
        1: const pw.FlexColumnWidth(1),
        2: const pw.FlexColumnWidth(1),
        3: const pw.FlexColumnWidth(1),
      },
      children: [
        // Header
        pw.TableRow(
          decoration: const pw.BoxDecoration(color: PdfColors.grey300),
          children: [
            _buildPdfTableCell('Fecha/Hora', isHeader: true),
            _buildPdfTableCell('Peso (kg)', isHeader: true),
            _buildPdfTableCell('Método', isHeader: true),
            _buildPdfTableCell('Confidence', isHeader: true),
          ],
        ),
        // Datos (limitado a 50 registros más recientes)
        ...weighings
            .take(50)
            .map(
              (w) => pw.TableRow(
                children: [
                  _buildPdfTableCell(dateFormatter.format(w.timestamp)),
                  _buildPdfTableCell(w.estimatedWeight.toStringAsFixed(1)),
                  _buildPdfTableCell(_getMethodLabel(w.method)),
                  _buildPdfTableCell(
                    '${(w.confidenceScore * 100).toStringAsFixed(0)}%',
                  ),
                ],
              ),
            ),
      ],
    );
  }

  /// Construye una celda de tabla para PDF
  pw.Widget _buildPdfTableCell(String text, {bool isHeader = false}) {
    return pw.Padding(
      padding: const pw.EdgeInsets.all(5),
      child: pw.Text(
        text,
        style: pw.TextStyle(
          fontSize: 9,
          fontWeight: isHeader ? pw.FontWeight.bold : null,
        ),
      ),
    );
  }

  /// Construye una fila CSV para un pesaje
  List<dynamic> _buildCsvRow(Cattle cattle, WeightEstimation weighing) {
    final dateFormatter = DateFormat('yyyy-MM-dd');
    final timeFormatter = DateFormat('HH:mm:ss');

    return [
      cattle.id,
      cattle.earTag,
      cattle.name ?? '',
      cattle.breed.value,
      cattle.ageInMonths,
      cattle.ageCategory.value,
      dateFormatter.format(weighing.timestamp),
      timeFormatter.format(weighing.timestamp),
      weighing.estimatedWeight.toStringAsFixed(2),
      _getMethodLabel(weighing.method),
      weighing.confidenceScore.toStringAsFixed(4),
      weighing.gpsCoordinates?.latitude.toStringAsFixed(6) ?? '',
      weighing.gpsCoordinates?.longitude.toStringAsFixed(6) ?? '',
      weighing.modelVersion,
    ];
  }

  /// Obtiene etiqueta del método de estimación
  String _getMethodLabel(EstimationMethod method) {
    switch (method) {
      case EstimationMethod.tflite:
        return 'ia';
      case EstimationMethod.schaeffer:
        return 'formula';
      case EstimationMethod.manual:
        return 'manual';
    }
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
