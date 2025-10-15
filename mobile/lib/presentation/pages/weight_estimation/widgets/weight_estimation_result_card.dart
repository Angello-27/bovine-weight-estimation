/// Widget: WeightEstimationResultCard
///
/// Card con resultado de estimación de peso.
/// Single Responsibility: Mostrar resultado con peso, confidence y metadatos.
///
/// Page-specific Widget
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../domain/entities/weight_estimation.dart';

/// Card de resultado de estimación
class WeightEstimationResultCard extends StatelessWidget {
  final WeightEstimation estimation;

  const WeightEstimationResultCard({super.key, required this.estimation});

  @override
  Widget build(BuildContext context) {
    final confidenceColor = _getConfidenceColor(estimation.confidenceLevel);

    return Card(
      elevation: AppSpacing.elevationHigh,
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.cardPadding * 1.5),
        child: Column(
          children: [
            // Título
            Text(
              '¡Estimación Completada!',
              style: Theme.of(
                context,
              ).textTheme.titleLarge?.copyWith(color: AppColors.success),
              textAlign: TextAlign.center,
            ),

            const SizedBox(height: AppSpacing.lg),

            // Peso estimado (grande y prominente)
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.baseline,
              textBaseline: TextBaseline.alphabetic,
              children: [
                Text(
                  estimation.estimatedWeight.toStringAsFixed(1),
                  style: Theme.of(context).textTheme.displayLarge?.copyWith(
                    color: AppColors.primary,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(width: AppSpacing.sm),
                Text(
                  'kg',
                  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                    color: AppColors.primary,
                  ),
                ),
              ],
            ),

            const SizedBox(height: AppSpacing.md),

            // Confidence score con color
            Container(
              padding: const EdgeInsets.symmetric(
                horizontal: AppSpacing.md,
                vertical: AppSpacing.sm,
              ),
              decoration: BoxDecoration(
                color: confidenceColor.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(
                  AppSpacing.borderRadiusLarge,
                ),
                border: Border.all(color: confidenceColor, width: 2),
              ),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Icon(
                    _getConfidenceIcon(estimation.confidenceLevel),
                    color: confidenceColor,
                  ),
                  const SizedBox(width: AppSpacing.sm),
                  Text(
                    'Confianza: ${(estimation.confidenceScore * 100).toStringAsFixed(0)}%',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: confidenceColor,
                    ),
                  ),
                ],
              ),
            ),

            const SizedBox(height: AppSpacing.lg),

            const Divider(),

            const SizedBox(height: AppSpacing.md),

            // Metadatos
            _buildMetadataRow(
              context,
              'Raza',
              estimation.breed.displayName,
              Icons.category,
            ),

            const SizedBox(height: AppSpacing.sm),

            _buildMetadataRow(
              context,
              'Método',
              estimation.method.name.toUpperCase(),
              Icons.psychology,
            ),

            const SizedBox(height: AppSpacing.sm),

            _buildMetadataRow(
              context,
              'Tiempo procesamiento',
              '${(estimation.processingTimeMs / 1000).toStringAsFixed(2)}s',
              Icons.timer,
            ),

            const SizedBox(height: AppSpacing.sm),

            _buildMetadataRow(
              context,
              'Modelo',
              'v${estimation.modelVersion}',
              Icons.model_training,
            ),
          ],
        ),
      ),
    );
  }

  /// Fila de metadato
  Widget _buildMetadataRow(
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
            Icon(
              icon,
              size: AppSpacing.iconSizeSmall,
              color: AppColors.grey600,
            ),
            const SizedBox(width: AppSpacing.sm),
            Text(
              label,
              style: Theme.of(
                context,
              ).textTheme.bodyMedium?.copyWith(color: AppColors.grey700),
            ),
          ],
        ),
        Text(
          value,
          style: Theme.of(
            context,
          ).textTheme.bodyMedium?.copyWith(fontWeight: FontWeight.bold),
        ),
      ],
    );
  }

  /// Obtiene color según nivel de confianza
  Color _getConfidenceColor(ConfidenceLevel level) {
    switch (level) {
      case ConfidenceLevel.high:
        return AppColors.success; // Verde ≥90%
      case ConfidenceLevel.medium:
        return AppColors.warning; // Amarillo 80-90%
      case ConfidenceLevel.low:
        return AppColors.error; // Rojo <80%
    }
  }

  /// Obtiene icono según nivel de confianza
  IconData _getConfidenceIcon(ConfidenceLevel level) {
    switch (level) {
      case ConfidenceLevel.high:
        return Icons.check_circle;
      case ConfidenceLevel.medium:
        return Icons.warning;
      case ConfidenceLevel.low:
        return Icons.error;
    }
  }
}
