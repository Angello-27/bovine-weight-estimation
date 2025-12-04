/// Best Frame Preview Dialog - Organism
///
/// Diálogo de vista previa del mejor frame con información detallada
/// y opción para confirmar y guardar como resultado final.
///
/// Presentation Layer - Organisms
library;

import 'dart:io';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../l10n/app_localizations.dart';
import '../../../providers/capture_provider.dart';
import '../../../../core/routes/app_router.dart';

/// Diálogo de vista previa del mejor frame
class BestFramePreviewDialog extends StatelessWidget {
  /// Mejor frame a mostrar
  final dynamic bestFrame; // Frame entity

  /// Total de frames capturados
  final int totalFrames;

  /// Frames óptimos
  final int optimalFrames;

  const BestFramePreviewDialog({
    required this.bestFrame,
    required this.totalFrames,
    required this.optimalFrames,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Dialog(
      backgroundColor: Colors.transparent,
      insetPadding: const EdgeInsets.all(AppSpacing.md),
      child: Container(
        constraints: BoxConstraints(
          maxHeight: MediaQuery.of(context).size.height * 0.9,
        ),
        decoration: BoxDecoration(
          color: colorScheme.surface,
          borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Header (fijo)
            _buildHeader(context, theme, colorScheme),

            // Contenido scrolleable
            Flexible(
              child: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    // Imagen del mejor frame
                    _buildImagePreview(),

                    // Información detallada
                    _buildFrameInfo(context, theme, colorScheme),
                  ],
                ),
              ),
            ),

            // Botones de acción (fijos en la parte inferior)
            _buildActionButtons(context, theme, colorScheme),
          ],
        ),
      ),
    );
  }

  /// Header del diálogo
  Widget _buildHeader(
    BuildContext context,
    ThemeData theme,
    ColorScheme colorScheme,
  ) {
    final l10n = AppLocalizations.of(context)!;

    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: colorScheme.primary,
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(AppSpacing.borderRadiusLarge),
          topRight: Radius.circular(AppSpacing.borderRadiusLarge),
        ),
      ),
      child: Row(
        children: [
          Icon(Icons.star, color: colorScheme.onPrimary),
          const SizedBox(width: AppSpacing.sm),
          Expanded(
            child: Text(
              l10n.bestFrameCaptured,
              style: theme.textTheme.titleLarge?.copyWith(
                color: colorScheme.onPrimary,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          IconButton(
            icon: Icon(Icons.close, color: colorScheme.onPrimary),
            onPressed: () => Navigator.of(context).pop(),
          ),
        ],
      ),
    );
  }

  /// Preview de la imagen
  Widget _buildImagePreview() {
    return Padding(
      padding: const EdgeInsets.all(AppSpacing.md),
      child: Container(
        width: double.infinity,
        constraints: const BoxConstraints(minHeight: 200, maxHeight: 250),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
          child: Image.file(
            File(bestFrame.imagePath),
            fit: BoxFit.cover,
            alignment: Alignment.center,
            errorBuilder: (context, error, stackTrace) {
              return Container(
                height: 200,
                color: Colors.grey[200],
                child: const Center(
                  child: Icon(Icons.image, size: 64, color: Colors.grey),
                ),
              );
            },
          ),
        ),
      ),
    );
  }

  /// Información del frame
  Widget _buildFrameInfo(
    BuildContext context,
    ThemeData theme,
    ColorScheme colorScheme,
  ) {
    final l10n = AppLocalizations.of(context)!;

    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Score global
          _buildInfoRow(
            context: context,
            theme: theme,
            colorScheme: colorScheme,
            icon: Icons.star,
            label: l10n.globalScore,
            value: bestFrame.globalScore.toStringAsFixed(2),
            color: colorScheme.primary,
          ),

          const SizedBox(height: AppSpacing.sm),

          // Estadísticas de calidad
          Row(
            children: [
              Expanded(
                child: _buildInfoCard(
                  context: context,
                  theme: theme,
                  colorScheme: colorScheme,
                  icon: Icons.center_focus_strong,
                  label: l10n.sharpness,
                  value: bestFrame.quality.sharpness.toStringAsFixed(2),
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              Expanded(
                child: _buildInfoCard(
                  context: context,
                  theme: theme,
                  colorScheme: colorScheme,
                  icon: Icons.wb_sunny,
                  label: l10n.illumination,
                  value: bestFrame.quality.brightness.toStringAsFixed(2),
                ),
              ),
            ],
          ),

          const SizedBox(height: AppSpacing.sm),

          Row(
            children: [
              Expanded(
                child: _buildInfoCard(
                  context: context,
                  theme: theme,
                  colorScheme: colorScheme,
                  icon: Icons.contrast,
                  label: l10n.contrast,
                  value: bestFrame.quality.contrast.toStringAsFixed(2),
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              Expanded(
                child: _buildInfoCard(
                  context: context,
                  theme: theme,
                  colorScheme: colorScheme,
                  icon: Icons.visibility,
                  label: l10n.silhouette,
                  value: bestFrame.quality.silhouetteVisibility.toStringAsFixed(
                    2,
                  ),
                ),
              ),
            ],
          ),

          const SizedBox(height: AppSpacing.sm),

          // Estadísticas de captura
          _buildInfoRow(
            context: context,
            theme: theme,
            colorScheme: colorScheme,
            icon: Icons.camera,
            label: l10n.totalFrames,
            value: '$totalFrames',
          ),

          const SizedBox(height: 4),

          _buildInfoRow(
            context: context,
            theme: theme,
            colorScheme: colorScheme,
            icon: Icons.check_circle,
            label: l10n.optimalFrames,
            value: '$optimalFrames',
            color: AppColors.success,
          ),
        ],
      ),
    );
  }

  /// Fila de información
  Widget _buildInfoRow({
    required BuildContext context,
    required ThemeData theme,
    required ColorScheme colorScheme,
    required IconData icon,
    required String label,
    required String value,
    Color? color,
  }) {
    return Row(
      children: [
        Icon(icon, size: 20, color: color ?? colorScheme.onSurfaceVariant),
        const SizedBox(width: AppSpacing.sm),
        Text(
          label,
          style: theme.textTheme.bodyMedium?.copyWith(
            color: colorScheme.onSurfaceVariant,
          ),
        ),
        const Spacer(),
        Text(
          value,
          style: theme.textTheme.bodyMedium?.copyWith(
            color: color ?? colorScheme.onSurface,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  /// Card de información
  Widget _buildInfoCard({
    required BuildContext context,
    required ThemeData theme,
    required ColorScheme colorScheme,
    required IconData icon,
    required String label,
    required String value,
  }) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.sm),
      decoration: BoxDecoration(
        color: colorScheme.surfaceContainerHighest,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
      ),
      child: Column(
        children: [
          Icon(icon, size: 24, color: colorScheme.primary),
          const SizedBox(height: 4),
          Text(
            label,
            style: theme.textTheme.bodySmall?.copyWith(
              color: colorScheme.onSurfaceVariant,
            ),
          ),
          Text(
            value,
            style: theme.textTheme.bodyLarge?.copyWith(
              fontWeight: FontWeight.bold,
              color: colorScheme.onSurface,
            ),
          ),
        ],
      ),
    );
  }

  /// Botones de acción
  Widget _buildActionButtons(
    BuildContext context,
    ThemeData theme,
    ColorScheme colorScheme,
  ) {
    final l10n = AppLocalizations.of(context)!;

    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        border: Border(top: BorderSide(color: colorScheme.outlineVariant)),
      ),
      child: Row(
        children: [
          // Botón eliminar
          Expanded(
            child: OutlinedButton.icon(
              onPressed: () {
                // Mostrar diálogo de confirmación
                showDialog(
                  context: context,
                  builder: (dialogContext) => AlertDialog(
                    title: Text(l10n.deleteFrame),
                    content: Text(l10n.deleteFrameConfirmation),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.of(dialogContext).pop(),
                        child: Text(l10n.cancel),
                      ),
                      TextButton(
                        onPressed: () {
                          // Eliminar el frame primero
                          final provider = Provider.of<CaptureProvider>(
                            context,
                            listen: false,
                          );
                          provider.removeFrame(bestFrame);

                          // Cerrar diálogo de confirmación
                          Navigator.of(dialogContext).pop();

                          // Cerrar diálogo principal después de un pequeño delay
                          // para que la UI se actualice
                          Future.microtask(() {
                            if (context.mounted) {
                              Navigator.of(context).pop();
                            }
                          });
                        },
                        style: TextButton.styleFrom(
                          foregroundColor: AppColors.error,
                        ),
                        child: Text(l10n.deleteFrame),
                      ),
                    ],
                  ),
                );
              },
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
                foregroundColor: AppColors.error,
                side: BorderSide(color: AppColors.error),
              ),
              icon: const Icon(Icons.delete_outline, size: 20),
              label: Text(l10n.deleteFrame),
            ),
          ),

          const SizedBox(width: AppSpacing.md),

          // Botón cancelar
          Expanded(
            child: OutlinedButton(
              onPressed: () => Navigator.of(context).pop(),
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
              ),
              child: Text(l10n.cancel),
            ),
          ),

          const SizedBox(width: AppSpacing.md),

          // Botón confirmar y continuar
          Expanded(
            flex: 2,
            child: ElevatedButton.icon(
              onPressed: () {
                // Cerrar diálogo
                Navigator.of(context).pop();

                // Navegar a estimación de peso con el mejor frame
                final provider = Provider.of<CaptureProvider>(
                  context,
                  listen: false,
                );

                if (provider.bestFrame != null) {
                  AppRouter.push(
                    context,
                    AppRoutes.weightEstimation,
                    arguments: {
                      'framePath': provider.bestFrame!.imagePath,
                      'cattleId': null,
                    },
                  );
                }
              },
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.success,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
              ),
              icon: const Icon(Icons.check_circle, size: 20),
              label: Text(
                l10n.confirmAndContinue,
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
