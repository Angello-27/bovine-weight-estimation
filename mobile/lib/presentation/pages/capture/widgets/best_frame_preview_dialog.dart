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
    return Dialog(
      backgroundColor: Colors.transparent,
      insetPadding: const EdgeInsets.all(AppSpacing.md),
      child: Container(
        constraints: const BoxConstraints(maxHeight: 600),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Header
            _buildHeader(context),

            // Imagen del mejor frame
            Flexible(child: _buildImagePreview()),

            // Información detallada
            _buildFrameInfo(),

            // Botones de acción
            _buildActionButtons(context),
          ],
        ),
      ),
    );
  }

  /// Header del diálogo
  Widget _buildHeader(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.primary,
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(AppSpacing.borderRadiusLarge),
          topRight: Radius.circular(AppSpacing.borderRadiusLarge),
        ),
      ),
      child: Row(
        children: [
          const Icon(Icons.star, color: Colors.white),
          const SizedBox(width: AppSpacing.sm),
          const Expanded(
            child: Text(
              'Mejor Frame Capturado',
              style: TextStyle(
                color: Colors.white,
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.close, color: Colors.white),
            onPressed: () => Navigator.of(context).pop(),
          ),
        ],
      ),
    );
  }

  /// Preview de la imagen
  Widget _buildImagePreview() {
    return Container(
      width: double.infinity,
      constraints: const BoxConstraints(maxHeight: 300),
      child: ClipRRect(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        child: Image.file(
          File(bestFrame.imagePath),
          fit: BoxFit.contain,
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
    );
  }

  /// Información del frame
  Widget _buildFrameInfo() {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Score global
          _buildInfoRow(
            icon: Icons.star,
            label: 'Score Global',
            value: bestFrame.globalScore.toStringAsFixed(2),
            color: AppColors.accent,
          ),

          const SizedBox(height: AppSpacing.sm),

          // Estadísticas de calidad
          Row(
            children: [
              Expanded(
                child: _buildInfoCard(
                  icon: Icons.center_focus_strong,
                  label: 'Nitidez',
                  value: bestFrame.quality.sharpness.toStringAsFixed(2),
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              Expanded(
                child: _buildInfoCard(
                  icon: Icons.wb_sunny,
                  label: 'Iluminación',
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
                  icon: Icons.contrast,
                  label: 'Contraste',
                  value: bestFrame.quality.contrast.toStringAsFixed(2),
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              Expanded(
                child: _buildInfoCard(
                  icon: Icons.visibility,
                  label: 'Silueta',
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
            icon: Icons.camera,
            label: 'Total Frames',
            value: '$totalFrames',
          ),

          const SizedBox(height: 4),

          _buildInfoRow(
            icon: Icons.check_circle,
            label: 'Frames Óptimos',
            value: '$optimalFrames',
            color: AppColors.success,
          ),
        ],
      ),
    );
  }

  /// Fila de información
  Widget _buildInfoRow({
    required IconData icon,
    required String label,
    required String value,
    Color? color,
  }) {
    return Row(
      children: [
        Icon(icon, size: 20, color: color ?? AppColors.textSecondary),
        const SizedBox(width: AppSpacing.sm),
        Text(
          label,
          style: TextStyle(color: AppColors.textSecondary, fontSize: 14),
        ),
        const Spacer(),
        Text(
          value,
          style: TextStyle(
            color: color ?? AppColors.onSurface,
            fontSize: 14,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  /// Card de información
  Widget _buildInfoCard({
    required IconData icon,
    required String label,
    required String value,
  }) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.sm),
      decoration: BoxDecoration(
        color: AppColors.surfaceVariant,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
      ),
      child: Column(
        children: [
          Icon(icon, size: 24, color: AppColors.primary),
          const SizedBox(height: 4),
          Text(
            label,
            style: const TextStyle(
              fontSize: 12,
              color: AppColors.textSecondary,
            ),
          ),
          Text(
            value,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.bold,
              color: AppColors.onSurface,
            ),
          ),
        ],
      ),
    );
  }

  /// Botones de acción
  Widget _buildActionButtons(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        border: Border(top: BorderSide(color: AppColors.surfaceVariant)),
      ),
      child: Row(
        children: [
          // Botón cancelar
          Expanded(
            child: OutlinedButton(
              onPressed: () => Navigator.of(context).pop(),
              style: OutlinedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
              ),
              child: Text(AppLocalizations.of(context)!.cancel),
            ),
          ),

          const SizedBox(width: AppSpacing.md),

          // Botón confirmar y continuar
          Expanded(
            flex: 2,
            child: ElevatedButton(
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
                padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
              ),
              child: const Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.check_circle, color: Colors.white),
                  SizedBox(width: AppSpacing.sm),
                  Text(
                    'Confirmar y Continuar',
                    style: TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
