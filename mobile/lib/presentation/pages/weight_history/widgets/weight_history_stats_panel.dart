/// Widget: WeightHistoryStatsPanel
///
/// Panel con estadísticas clave del historial (peso actual, GDP, ganancia).
/// Single Responsibility: Mostrar métricas resumidas.
///
/// Page-specific Widget (Weight History)
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../domain/entities/weight_history.dart';

/// Panel de estadísticas del historial
class WeightHistoryStatsPanel extends StatelessWidget {
  /// Historial de peso
  final WeightHistory history;

  const WeightHistoryStatsPanel({required this.history, super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.lg),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [AppColors.secondaryLight, Colors.white],
        ),
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusXLarge),
        boxShadow: [
          BoxShadow(
            color: AppColors.secondary.withValues(alpha: 0.1),
            blurRadius: AppSpacing.elevationMedium,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        children: [
          // Título
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(AppSpacing.sm),
                decoration: BoxDecoration(
                  color: AppColors.secondary.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(
                    AppSpacing.borderRadiusMedium,
                  ),
                ),
                child: const Icon(
                  Icons.analytics,
                  color: AppColors.secondary,
                  size: AppSpacing.iconSizeLarge,
                ),
              ),
              const SizedBox(width: AppSpacing.md),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Análisis de Peso',
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                        fontWeight: FontWeight.bold,
                        color: AppColors.grey900,
                      ),
                    ),
                    Text(
                      '${history.totalWeighings} pesajes registrados',
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: AppColors.grey600,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),

          const SizedBox(height: AppSpacing.lg),

          // Stats grid
          Row(
            children: [
              Expanded(
                child: _buildStatCard(
                  context,
                  'Peso Actual',
                  history.currentWeight != null
                      ? '${history.currentWeight!.toStringAsFixed(1)} kg'
                      : 'N/A',
                  Icons.monitor_weight,
                  AppColors.primary,
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              Expanded(
                child: _buildStatCard(
                  context,
                  'Ganancia Total',
                  '${history.totalGain.toStringAsFixed(1)} kg',
                  Icons.trending_up,
                  AppColors.success,
                ),
              ),
            ],
          ),

          const SizedBox(height: AppSpacing.sm),

          Row(
            children: [
              Expanded(
                child: _buildStatCard(
                  context,
                  'GDP',
                  '${history.averageDailyGain.toStringAsFixed(2)} kg/día',
                  Icons.speed,
                  AppColors.secondary,
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              Expanded(
                child: _buildStatCard(
                  context,
                  'Anomalías',
                  '${history.anomalies.length}',
                  Icons.warning,
                  history.anomalies.isEmpty
                      ? AppColors.success
                      : AppColors.warning,
                ),
              ),
            ],
          ),

          // Proyección a 30 días (si existe)
          if (history.projectedWeight30Days != null) ...[
            const SizedBox(height: AppSpacing.md),
            Container(
              padding: const EdgeInsets.all(AppSpacing.md),
              decoration: BoxDecoration(
                color: AppColors.infoLight,
                borderRadius: BorderRadius.circular(
                  AppSpacing.borderRadiusMedium,
                ),
                border: Border.all(
                  color: AppColors.info.withValues(alpha: 0.3),
                  width: 1,
                ),
              ),
              child: Row(
                children: [
                  const Icon(
                    Icons.timeline,
                    color: AppColors.info,
                    size: AppSpacing.iconSize,
                  ),
                  const SizedBox(width: AppSpacing.sm),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Proyección a 30 días',
                          style: Theme.of(context).textTheme.bodySmall
                              ?.copyWith(
                                color: AppColors.grey700,
                                fontWeight: FontWeight.w500,
                              ),
                        ),
                        Text(
                          '${history.projectedWeight30Days!.toStringAsFixed(1)} kg',
                          style: Theme.of(context).textTheme.titleMedium
                              ?.copyWith(
                                color: AppColors.info,
                                fontWeight: FontWeight.bold,
                              ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  /// Card de estadística individual
  Widget _buildStatCard(
    BuildContext context,
    String label,
    String value,
    IconData icon,
    Color color,
  ) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        border: Border.all(color: color.withValues(alpha: 0.3), width: 1.5),
      ),
      child: Column(
        children: [
          Icon(icon, color: color, size: AppSpacing.iconSize),
          const SizedBox(height: AppSpacing.xs),
          Text(
            value,
            style: TextStyle(
              fontSize: AppSpacing.fontSizeLarge,
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
          Text(
            label,
            style: const TextStyle(
              fontSize: AppSpacing.fontSizeSmall,
              color: AppColors.grey600,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}
