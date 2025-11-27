/// Widget: WeightHistoryList
///
/// Lista cronológica de todos los pesajes.
/// Single Responsibility: Mostrar lista detallada de pesajes.
///
/// Page-specific Widget (Weight History)
library;

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../domain/entities/weight_estimation.dart';

/// Lista de pesajes históricos
class WeightHistoryList extends StatelessWidget {
  /// Lista de pesajes (ordenados cronológicamente)
  final List<WeightEstimation> weighings;

  const WeightHistoryList({required this.weighings, super.key});

  @override
  Widget build(BuildContext context) {
    return SliverList(
      delegate: SliverChildBuilderDelegate((context, index) {
        final weighing = weighings[index];
        final dateFormatter = DateFormat('dd/MM/yyyy HH:mm');

        return Card(
          margin: const EdgeInsets.only(bottom: AppSpacing.sm),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
          ),
          child: ListTile(
            contentPadding: const EdgeInsets.all(AppSpacing.md),
            leading: Container(
              padding: const EdgeInsets.all(AppSpacing.sm),
              decoration: BoxDecoration(
                gradient: AppColors.primaryGradient,
                borderRadius: BorderRadius.circular(
                  AppSpacing.borderRadiusSmall,
                ),
              ),
              child: const Icon(
                Icons.monitor_weight,
                color: Colors.white,
                size: AppSpacing.iconSize,
              ),
            ),
            title: Text(
              '${weighing.estimatedWeight.toStringAsFixed(1)} kg',
              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                fontWeight: FontWeight.bold,
                color: AppColors.grey900,
              ),
            ),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: AppSpacing.xs),
                Row(
                  children: [
                    Icon(
                      Icons.calendar_today,
                      size: AppSpacing.iconSizeSmall,
                      color: AppColors.grey600,
                    ),
                    const SizedBox(width: AppSpacing.xs),
                    Text(
                      dateFormatter.format(weighing.timestamp),
                      style: Theme.of(
                        context,
                      ).textTheme.bodySmall?.copyWith(color: AppColors.grey700),
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.xs),
                Row(
                  children: [
                    Icon(
                      _getConfidenceIcon(weighing.confidenceLevel),
                      size: AppSpacing.iconSizeSmall,
                      color: _getConfidenceColor(weighing.confidenceLevel),
                    ),
                    const SizedBox(width: AppSpacing.xs),
                    Text(
                      'Confianza: ${(weighing.confidenceScore * 100).toStringAsFixed(0)}%',
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: _getConfidenceColor(weighing.confidenceLevel),
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ],
            ),
            trailing: Container(
              padding: const EdgeInsets.symmetric(
                horizontal: AppSpacing.sm,
                vertical: AppSpacing.xs,
              ),
              decoration: BoxDecoration(
                color: AppColors.infoLight,
                borderRadius: BorderRadius.circular(
                  AppSpacing.borderRadiusSmall,
                ),
              ),
              child: Text(
                weighing.method.name.toUpperCase(),
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  color: AppColors.info,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        );
      }, childCount: weighings.length),
    );
  }

  /// Ícono según nivel de confianza
  IconData _getConfidenceIcon(ConfidenceLevel level) {
    switch (level) {
      case ConfidenceLevel.high:
        return Icons.verified;
      case ConfidenceLevel.medium:
        return Icons.check_circle_outline;
      case ConfidenceLevel.low:
        return Icons.warning_amber;
    }
  }

  /// Color según nivel de confianza
  Color _getConfidenceColor(ConfidenceLevel level) {
    switch (level) {
      case ConfidenceLevel.high:
        return AppColors.success;
      case ConfidenceLevel.medium:
        return AppColors.warning;
      case ConfidenceLevel.low:
        return AppColors.error;
    }
  }
}
