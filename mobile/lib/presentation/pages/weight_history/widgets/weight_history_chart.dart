/// Widget: WeightHistoryChart
///
/// Gráfico de línea con evolución de peso y línea de tendencia.
/// Single Responsibility: Visualizar evolución temporal de peso.
///
/// Page-specific Widget (Weight History)
library;

import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../domain/entities/weight_history.dart';

/// Gráfico de evolución de peso
class WeightHistoryChart extends StatelessWidget {
  /// Historial de peso
  final WeightHistory history;

  const WeightHistoryChart({required this.history, super.key});

  @override
  Widget build(BuildContext context) {
    // Si no hay suficientes datos, mostrar mensaje
    if (!history.hasEnoughDataForAnalysis) {
      return _buildInsufficientDataCard(context);
    }

    return Card(
      elevation: AppSpacing.elevationMedium,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      ),
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.lg),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Título
            Row(
              children: [
                const Icon(
                  Icons.show_chart,
                  color: AppColors.secondary,
                  size: AppSpacing.iconSize,
                ),
                const SizedBox(width: AppSpacing.sm),
                Text(
                  'Evolución de Peso',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),

            const SizedBox(height: AppSpacing.lg),

            // Gráfico
            SizedBox(
              height: 250,
              child: LineChart(
                _buildLineChartData(),
                duration: const Duration(milliseconds: 300),
                curve: Curves.easeInOut,
              ),
            ),

            const SizedBox(height: AppSpacing.md),

            // Leyenda
            _buildLegend(context),
          ],
        ),
      ),
    );
  }

  /// Construye los datos del gráfico
  LineChartData _buildLineChartData() {
    // Ordenar pesajes por fecha (más antiguos primero para el gráfico)
    final sortedWeighings = [...history.weighings]
      ..sort((a, b) => a.timestamp.compareTo(b.timestamp));

    // Crear spots del gráfico
    final spots = <FlSpot>[];
    for (var i = 0; i < sortedWeighings.length; i++) {
      spots.add(FlSpot(i.toDouble(), sortedWeighings[i].estimatedWeight));
    }

    // Calcular límites Y
    final weights = sortedWeighings.map((w) => w.estimatedWeight).toList();
    final minWeight = weights.reduce((a, b) => a < b ? a : b);
    final maxWeight = weights.reduce((a, b) => a > b ? a : b);
    final padding = (maxWeight - minWeight) * 0.1; // 10% padding

    return LineChartData(
      gridData: FlGridData(
        show: true,
        drawVerticalLine: false,
        horizontalInterval: 50,
        getDrawingHorizontalLine: (value) {
          return FlLine(
            color: AppColors.grey300,
            strokeWidth: 1,
            dashArray: [5, 5],
          );
        },
      ),
      titlesData: FlTitlesData(
        show: true,
        rightTitles: const AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
        topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        bottomTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            reservedSize: 30,
            interval: 1,
            getTitlesWidget: (value, meta) {
              final index = value.toInt();
              if (index < 0 || index >= sortedWeighings.length) {
                return const Text('');
              }

              final date = sortedWeighings[index].timestamp;
              final formatter = DateFormat('dd/MM');

              return Padding(
                padding: const EdgeInsets.only(top: 8.0),
                child: Text(
                  formatter.format(date),
                  style: const TextStyle(
                    color: AppColors.grey600,
                    fontSize: 10,
                  ),
                ),
              );
            },
          ),
        ),
        leftTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            reservedSize: 50,
            interval: 50,
            getTitlesWidget: (value, meta) {
              return Text(
                '${value.toInt()} kg',
                style: const TextStyle(color: AppColors.grey600, fontSize: 10),
              );
            },
          ),
        ),
      ),
      borderData: FlBorderData(
        show: true,
        border: Border.all(color: AppColors.grey300, width: 1),
      ),
      minX: 0,
      maxX: (sortedWeighings.length - 1).toDouble(),
      minY: minWeight - padding,
      maxY: maxWeight + padding,
      lineBarsData: [
        // Línea de datos reales
        LineChartBarData(
          spots: spots,
          isCurved: true,
          gradient: AppColors.primaryGradient,
          barWidth: 4,
          isStrokeCapRound: true,
          dotData: FlDotData(
            show: true,
            getDotPainter: (spot, percent, barData, index) {
              return FlDotCirclePainter(
                radius: 5,
                color: AppColors.primary,
                strokeWidth: 2,
                strokeColor: Colors.white,
              );
            },
          ),
          belowBarData: BarAreaData(
            show: true,
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                AppColors.primary.withValues(alpha: 0.3),
                AppColors.primary.withValues(alpha: 0.05),
              ],
            ),
          ),
        ),

        // Línea de tendencia (proyección lineal)
        if (history.hasEnoughDataForAnalysis) _buildTrendLine(sortedWeighings),
      ],
    );
  }

  /// Construye línea de tendencia
  LineChartBarData _buildTrendLine(List<dynamic> weighings) {
    // Calcular regresión lineal simple
    final n = weighings.length;
    double sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;

    for (var i = 0; i < n; i++) {
      final x = i.toDouble();
      final y = weighings[i].estimatedWeight;
      sumX += x;
      sumY += y;
      sumXY += x * y;
      sumX2 += x * x;
    }

    final slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
    final intercept = (sumY - slope * sumX) / n;

    // Crear spots de tendencia
    final trendSpots = [
      FlSpot(0, intercept),
      FlSpot((n - 1).toDouble(), slope * (n - 1) + intercept),
    ];

    return LineChartBarData(
      spots: trendSpots,
      isCurved: false,
      color: AppColors.secondary,
      barWidth: 2,
      isStrokeCapRound: true,
      dotData: const FlDotData(show: false),
      dashArray: [5, 5],
    );
  }

  /// Leyenda del gráfico
  Widget _buildLegend(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        _buildLegendItem('Peso Real', AppColors.primary, solid: true),
        const SizedBox(width: AppSpacing.md),
        _buildLegendItem('Tendencia', AppColors.secondary, solid: false),
      ],
    );
  }

  /// Item de leyenda
  Widget _buildLegendItem(String label, Color color, {required bool solid}) {
    return Row(
      children: [
        Container(
          width: 20,
          height: 3,
          decoration: BoxDecoration(
            color: solid ? color : Colors.transparent,
            border: solid ? null : Border.all(color: color, width: 2),
          ),
          child: solid
              ? null
              : CustomPaint(painter: _DashLinePainter(color: color)),
        ),
        const SizedBox(width: AppSpacing.xs),
        Text(
          label,
          style: const TextStyle(
            fontSize: AppSpacing.fontSizeSmall,
            color: AppColors.grey700,
          ),
        ),
      ],
    );
  }

  /// Card para cuando no hay suficientes datos
  Widget _buildInsufficientDataCard(BuildContext context) {
    return Card(
      color: AppColors.warningLight,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      ),
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.lg),
        child: Row(
          children: [
            const Icon(
              Icons.info_outline,
              color: AppColors.warning,
              size: AppSpacing.iconSizeLarge,
            ),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Datos Insuficientes',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: AppColors.warning,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  Text(
                    'Se necesitan al menos 2 pesajes para generar gráficos de tendencia',
                    style: Theme.of(
                      context,
                    ).textTheme.bodySmall?.copyWith(color: AppColors.grey700),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

/// Painter para líneas punteadas
class _DashLinePainter extends CustomPainter {
  final Color color;

  _DashLinePainter({required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = 2;

    const dashWidth = 3.0;
    const dashSpace = 3.0;
    double startX = 0;

    while (startX < size.width) {
      canvas.drawLine(
        Offset(startX, size.height / 2),
        Offset(startX + dashWidth, size.height / 2),
        paint,
      );
      startX += dashWidth + dashSpace;
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
