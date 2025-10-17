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
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusXLarge),
      ),
      child: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [AppColors.successLight, Colors.white],
          ),
          borderRadius: BorderRadius.circular(AppSpacing.borderRadiusXLarge),
        ),
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.cardPadding * 1.5),
          child: Column(
            children: [
              // Ícono de éxito
              Container(
                padding: const EdgeInsets.all(AppSpacing.md),
                decoration: BoxDecoration(
                  color: AppColors.success.withValues(alpha: 0.15),
                  shape: BoxShape.circle,
                ),
                child: const Icon(
                  Icons.check_circle,
                  size: AppSpacing.iconSizeXXLarge,
                  color: AppColors.success,
                ),
              ),

              const SizedBox(height: AppSpacing.md),

              // Título
              Text(
                '¡Estimación Completada!',
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: AppColors.success,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),

              const SizedBox(height: AppSpacing.lg),

              // Peso estimado en card destacado
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.xl,
                  vertical: AppSpacing.lg,
                ),
                decoration: BoxDecoration(
                  gradient: AppColors.primaryGradient,
                  borderRadius: BorderRadius.circular(
                    AppSpacing.borderRadiusLarge,
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: AppColors.primary.withValues(alpha: 0.3),
                      blurRadius: AppSpacing.elevationHigh,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.baseline,
                  textBaseline: TextBaseline.alphabetic,
                  children: [
                    Text(
                      estimation.estimatedWeight.toStringAsFixed(1),
                      style: const TextStyle(
                        fontSize: 56,
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(width: AppSpacing.sm),
                    const Text(
                      'kg',
                      style: TextStyle(
                        fontSize: 28,
                        color: Colors.white,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              // Confidence score con color
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: AppSpacing.lg,
                  vertical: AppSpacing.md,
                ),
                decoration: BoxDecoration(
                  color: confidenceColor.withValues(alpha: 0.15),
                  borderRadius: BorderRadius.circular(
                    AppSpacing.borderRadiusLarge,
                  ),
                  border: Border.all(
                    color: confidenceColor.withValues(alpha: 0.5),
                    width: 1.5,
                  ),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      _getConfidenceIcon(estimation.confidenceLevel),
                      color: confidenceColor,
                      size: AppSpacing.iconSize,
                    ),
                    const SizedBox(width: AppSpacing.sm),
                    Text(
                      'Confianza: ${(estimation.confidenceScore * 100).toStringAsFixed(0)}%',
                      style: TextStyle(
                        fontSize: AppSpacing.fontSizeNormal,
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
