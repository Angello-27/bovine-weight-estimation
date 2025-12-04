/// Capture Floating Controls - Molecule
///
/// Controles flotantes para iniciar/detener captura continua.
/// Se muestra en la parte inferior sobre la cámara.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../core/routes/app_router.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../providers/capture_provider.dart';

/// Controles flotantes de captura
class CaptureFloatingControls extends StatelessWidget {
  const CaptureFloatingControls({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<CaptureProvider>(
      builder: (context, provider, child) {
        return SafeArea(
          child: Container(
            margin: const EdgeInsets.all(AppSpacing.lg),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Botón principal de captura (grande, circular)
                _buildCaptureButton(context, provider),
              ],
            ),
          ),
        );
      },
    );
  }

  /// Botón principal de captura
  Widget _buildCaptureButton(BuildContext context, CaptureProvider provider) {
    final isCapturing = provider.isCapturing;

    return GestureDetector(
      onTap: () async {
        if (isCapturing) {
          // Detener captura (ahora es async)
          await provider.stopContinuousCapture();

          // Navegar a estimación de peso si hay frames capturados
          if (provider.bestFrame != null && provider.frameCount > 0) {
            // Esperar un momento para que la UI se actualice
            await Future.delayed(const Duration(milliseconds: 300));

            if (context.mounted) {
              AppRouter.push(
                context,
                AppRoutes.weightEstimation,
                arguments: {
                  'framePath': provider.bestFrame!.imagePath,
                  'cattleId':
                      null, // Se puede pasar si hay un animal seleccionado
                },
              );
            }
          }
        } else {
          // Iniciar captura continua
          provider.startContinuousCapture();
        }
      },
      child: Container(
        width: 80,
        height: 80,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: isCapturing ? AppColors.error : AppColors.primary,
          border: Border.all(color: Colors.white, width: 4),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.3),
              blurRadius: 10,
              spreadRadius: 2,
            ),
          ],
        ),
        child: Center(
          child: Icon(
            isCapturing ? Icons.stop : Icons.camera_alt,
            color: Colors.white,
            size: 40,
          ),
        ),
      ),
    );
  }
}
