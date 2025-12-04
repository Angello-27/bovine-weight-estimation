/// Best Frame Thumbnail - Molecule
///
/// Muestra una miniatura del mejor frame capturado durante la captura continua.
/// Al presionar, abre la vista previa detallada.
///
/// Presentation Layer - Molecules
library;

import 'dart:io';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../l10n/app_localizations.dart';
import '../../../providers/capture_provider.dart';
import 'best_frame_preview_dialog.dart';

/// Miniatura flotante del mejor frame
class BestFrameThumbnail extends StatelessWidget {
  const BestFrameThumbnail({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<CaptureProvider>(
      builder: (context, provider, child) {
        // Solo mostrar si hay frames capturados
        if (provider.frameCount == 0 || provider.bestFrame == null) {
          return const SizedBox.shrink();
        }

        return Positioned(
          top: 100, // Debajo del overlay superior
          right: AppSpacing.md,
          child: GestureDetector(
            onTap: () {
              // Abrir vista previa detallada
              showDialog(
                context: context,
                barrierColor: Colors.black87,
                builder: (context) => BestFramePreviewDialog(
                  bestFrame: provider.bestFrame!,
                  totalFrames: provider.frameCount,
                  optimalFrames: provider.optimalFrames.length,
                ),
              );
            },
            child: Container(
              width: 100,
              height: 100,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(
                  AppSpacing.borderRadiusMedium,
                ),
                border: Border.all(color: AppColors.success, width: 3),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withValues(alpha: 0.5),
                    blurRadius: 10,
                    spreadRadius: 2,
                  ),
                ],
              ),
              child: Stack(
                children: [
                  // Imagen del mejor frame
                  ClipRRect(
                    borderRadius: BorderRadius.circular(
                      AppSpacing.borderRadiusMedium - 3,
                    ),
                    child: Image.file(
                      File(provider.bestFrame!.imagePath),
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) {
                        return Container(
                          color: Colors.grey[800],
                          child: const Icon(Icons.image, color: Colors.white70),
                        );
                      },
                    ),
                  ),

                  // Badge "MEJOR" en la esquina con animación
                  Positioned(
                    top: 4,
                    right: 4,
                    child: TweenAnimationBuilder<double>(
                      tween: Tween(begin: 0.0, end: 1.0),
                      duration: const Duration(milliseconds: 500),
                      builder: (context, value, child) {
                        return Transform.scale(
                          scale: 0.8 + (value * 0.2),
                          child: Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 6,
                              vertical: 2,
                            ),
                            decoration: BoxDecoration(
                              color: AppColors.success,
                              borderRadius: BorderRadius.circular(4),
                              boxShadow: [
                                BoxShadow(
                                  color: AppColors.success.withValues(
                                    alpha: 0.5 * value,
                                  ),
                                  blurRadius: 8,
                                  spreadRadius: 2,
                                ),
                              ],
                            ),
                            child: const Text(
                              'MEJOR',
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 8,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                  ),

                  // Score en la parte inferior
                  Positioned(
                    bottom: 0,
                    left: 0,
                    right: 0,
                    child: Container(
                      padding: const EdgeInsets.symmetric(vertical: 2),
                      decoration: BoxDecoration(
                        color: Colors.black.withValues(alpha: 0.7),
                        borderRadius: const BorderRadius.only(
                          bottomLeft: Radius.circular(
                            AppSpacing.borderRadiusMedium - 3,
                          ),
                          bottomRight: Radius.circular(
                            AppSpacing.borderRadiusMedium - 3,
                          ),
                        ),
                      ),
                      child: Text(
                        'Score: ${provider.bestFrame!.globalScore.toStringAsFixed(1)}',
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 10,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ),

                  // Botón de eliminar en la esquina superior izquierda
                  Positioned(
                    top: 4,
                    left: 4,
                    child: GestureDetector(
                      onTap: () {
                        // Mostrar diálogo de confirmación
                        showDialog(
                          context: context,
                          builder: (dialogContext) => AlertDialog(
                            title: Text(
                              AppLocalizations.of(context)!.deleteFrame,
                            ),
                            content: Text(
                              AppLocalizations.of(
                                context,
                              )!.deleteFrameConfirmation,
                            ),
                            actions: [
                              TextButton(
                                onPressed: () =>
                                    Navigator.of(dialogContext).pop(),
                                child: Text(
                                  AppLocalizations.of(context)!.cancel,
                                ),
                              ),
                              TextButton(
                                onPressed: () {
                                  // Guardar referencia al frame antes de eliminar
                                  final frameToDelete = provider.bestFrame!;

                                  // Eliminar el frame
                                  provider.removeFrame(frameToDelete);

                                  // Cerrar diálogo
                                  if (dialogContext.mounted) {
                                    Navigator.of(dialogContext).pop();
                                  }
                                },
                                style: TextButton.styleFrom(
                                  foregroundColor: AppColors.error,
                                ),
                                child: Text(
                                  AppLocalizations.of(context)!.deleteFrame,
                                ),
                              ),
                            ],
                          ),
                        );
                      },
                      child: Container(
                        padding: const EdgeInsets.all(4),
                        decoration: BoxDecoration(
                          color: AppColors.error,
                          shape: BoxShape.circle,
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withValues(alpha: 0.3),
                              blurRadius: 4,
                              spreadRadius: 1,
                            ),
                          ],
                        ),
                        child: const Icon(
                          Icons.close,
                          color: Colors.white,
                          size: 16,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}
