/// Widget: CaptureResultsCard
///
/// Card con resultados de la captura completada.
/// Single Responsibility: Mostrar resumen de resultados.
///
/// Page-specific Widget
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';

/// Card de resultados de captura
class CaptureResultsCard extends StatelessWidget {
  final int totalFrames;
  final int optimalFrames;
  final double? bestScore;

  const CaptureResultsCard({
    super.key,
    required this.totalFrames,
    required this.optimalFrames,
    this.bestScore,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          '¡Captura completada!',
          style: Theme.of(
            context,
          ).textTheme.titleLarge?.copyWith(color: AppColors.success),
          textAlign: TextAlign.center,
        ),

        const SizedBox(height: AppSpacing.md),

        Card(
          elevation: AppSpacing.elevationMedium,
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.cardPadding),
            child: Column(
              children: [
                _buildResultRow(
                  context,
                  'Total de fotogramas',
                  '$totalFrames',
                  Icons.photo_library,
                ),

                const Divider(height: AppSpacing.md),

                _buildResultRow(
                  context,
                  'Fotogramas óptimos',
                  '$optimalFrames',
                  Icons.check_circle,
                ),

                const Divider(height: AppSpacing.md),

                _buildResultRow(
                  context,
                  'Mejor score',
                  bestScore != null
                      ? '${(bestScore! * 100).toStringAsFixed(0)}%'
                      : 'N/A',
                  Icons.star,
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  /// Fila de resultado
  Widget _buildResultRow(
    BuildContext context,
    String label,
    String value,
    IconData icon,
  ) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Row(
          children: [
            Icon(icon, size: AppSpacing.iconSize, color: AppColors.primary),
            const SizedBox(width: AppSpacing.sm),
            Text(label),
          ],
        ),
        Text(
          value,
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.bold,
            color: AppColors.primary,
          ),
        ),
      ],
    );
  }
}
