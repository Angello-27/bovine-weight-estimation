/// Widget: WeightEstimationResultCard
///
/// Card con resultado de estimación de peso.
/// Single Responsibility: Mostrar resultado con peso, confidence y metadatos.
///
/// Page-specific Widget
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/utils/weight_converter.dart';
import '../../../../domain/entities/app_settings.dart';
import '../../../../domain/entities/weight_estimation.dart';
import '../../../../l10n/app_localizations.dart';
import '../../../providers/settings_provider.dart';

/// Card de resultado de estimación
class WeightEstimationResultCard extends StatelessWidget {
  final WeightEstimation estimation;

  const WeightEstimationResultCard({super.key, required this.estimation});

  @override
  Widget build(BuildContext context) {
    final confidenceColor = _getConfidenceColor(estimation.confidenceLevel);
    final settingsProvider = Provider.of<SettingsProvider>(
      context,
      listen: false,
    );
    final weightUnit = settingsProvider.settings.weightUnit;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        // Card principal con resultado
        Card(
          elevation: AppSpacing.elevationMedium,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
          ),
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.cardPadding),
            child: Column(
              children: [
                // Header con título e ícono
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(AppSpacing.sm),
                      decoration: BoxDecoration(
                        color: Theme.of(
                          context,
                        ).colorScheme.primary.withValues(alpha: 0.1),
                        borderRadius: BorderRadius.circular(
                          AppSpacing.borderRadiusMedium,
                        ),
                      ),
                      child: Icon(
                        Icons.check_circle,
                        color: Theme.of(context).colorScheme.primary,
                        size: AppSpacing.iconSize,
                      ),
                    ),
                    const SizedBox(width: AppSpacing.md),
                    Expanded(
                      child: Text(
                        AppLocalizations.of(context)!.estimationCompleted,
                        style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: AppSpacing.lg),

                // Peso estimado destacado
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.symmetric(
                    horizontal: AppSpacing.lg,
                    vertical: AppSpacing.xl,
                  ),
                  decoration: BoxDecoration(
                    color: Theme.of(context).colorScheme.primaryContainer,
                    borderRadius: BorderRadius.circular(
                      AppSpacing.borderRadiusLarge,
                    ),
                  ),
                  child: Column(
                    children: [
                      Text(
                        AppLocalizations.of(context)!.estimatedWeight,
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: Theme.of(context)
                              .colorScheme
                              .onPrimaryContainer
                              .withValues(alpha: 0.7),
                        ),
                      ),
                      const SizedBox(height: AppSpacing.xs),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.baseline,
                        textBaseline: TextBaseline.alphabetic,
                        children: [
                          Text(
                            WeightConverter.getWeightInUnit(
                              estimation.estimatedWeight,
                              weightUnit,
                            ).toStringAsFixed(1),
                            style: Theme.of(context).textTheme.displayMedium
                                ?.copyWith(
                                  fontWeight: FontWeight.bold,
                                  color: Theme.of(
                                    context,
                                  ).colorScheme.onPrimaryContainer,
                                ),
                          ),
                          const SizedBox(width: AppSpacing.xs),
                          Text(
                            weightUnit == WeightUnit.kilograms ? 'kg' : 'lb',
                            style: Theme.of(context).textTheme.titleLarge
                                ?.copyWith(
                                  color: Theme.of(context)
                                      .colorScheme
                                      .onPrimaryContainer
                                      .withValues(alpha: 0.8),
                                ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // Confidence score
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: AppSpacing.md,
                    vertical: AppSpacing.sm,
                  ),
                  decoration: BoxDecoration(
                    color: confidenceColor.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(
                      AppSpacing.borderRadiusMedium,
                    ),
                    border: Border.all(
                      color: confidenceColor.withValues(alpha: 0.3),
                      width: 1,
                    ),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        _getConfidenceIcon(estimation.confidenceLevel),
                        color: confidenceColor,
                        size: AppSpacing.iconSizeSmall,
                      ),
                      const SizedBox(width: AppSpacing.sm),
                      Text(
                        AppLocalizations.of(context)!.confidence(
                          (estimation.confidenceScore * 100).toStringAsFixed(0),
                        ),
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          fontWeight: FontWeight.w600,
                          color: confidenceColor,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),

        const SizedBox(height: AppSpacing.md),

        // Card de información detallada
        Card(
          elevation: AppSpacing.elevationLow,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
          ),
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.cardPadding),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  AppLocalizations.of(context)!.information,
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: AppSpacing.md),
                _buildMetadataRow(
                  context,
                  AppLocalizations.of(context)!.breed,
                  estimation.breed.displayName,
                  Icons.category,
                ),
                const SizedBox(height: AppSpacing.sm),
                _buildMetadataRow(
                  context,
                  AppLocalizations.of(context)!.method,
                  estimation.method.name.toUpperCase(),
                  Icons.psychology,
                ),
                const SizedBox(height: AppSpacing.sm),
                _buildMetadataRow(
                  context,
                  AppLocalizations.of(context)!.processingTime,
                  '${(estimation.processingTimeMs / 1000).toStringAsFixed(2)}s',
                  Icons.timer,
                ),
                const SizedBox(height: AppSpacing.sm),
                _buildMetadataRow(
                  context,
                  AppLocalizations.of(context)!.model,
                  'v${estimation.modelVersion}',
                  Icons.model_training,
                ),
              ],
            ),
          ),
        ),
      ],
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
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
            const SizedBox(width: AppSpacing.sm),
            Text(
              label,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
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
