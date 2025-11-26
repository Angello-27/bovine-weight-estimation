/// Capture Floating Controls - Molecule
///
/// Controles flotantes para iniciar/detener captura continua.
/// Se muestra en la parte inferior sobre la cámara.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

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
      onTap: () {
        if (isCapturing) {
          // Detener captura
          provider.stopContinuousCapture();
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
              color: Colors.black.withOpacity(0.3),
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
