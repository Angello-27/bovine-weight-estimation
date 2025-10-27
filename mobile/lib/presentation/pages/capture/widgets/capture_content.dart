/// Capture Content - Organism
///
/// Contenido principal que cambia según el estado de la captura.
/// Atomic Design: Organism
///
/// Presentation Layer - Organisms
library;

import 'package:flutter/material.dart';

import '../../../../core/routes/app_router.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../providers/capture_provider.dart';
import '../../../widgets/organisms/capture/capture_config_section.dart';
import 'capture_error_card.dart';
import 'capture_progress_indicator.dart';
import 'capture_results_card.dart';

/// Contenido principal de la página de captura
class CaptureContent extends StatelessWidget {
  /// Provider de capture
  final CaptureProvider provider;

  const CaptureContent({required this.provider, super.key});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        children: [
          // Mensaje informativo sobre la captura
          if (provider.state == CaptureState.idle)
            Card(
              color: Colors.blue.shade50,
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Row(
                  children: [
                    Icon(Icons.info_outline, color: Colors.blue.shade700),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        'La captura automática tomará fotogramas a ${provider.targetFps} FPS durante ${provider.targetDurationSeconds} segundos.',
                        style: TextStyle(
                          color: Colors.blue.shade900,
                          fontSize: 14,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),

          if (provider.state == CaptureState.idle)
            const SizedBox(height: AppSpacing.lg),

          // Configuración (solo si está idle)
          if (!provider.isCapturing && provider.state == CaptureState.idle)
            CaptureConfigSection(
              targetFps: provider.targetFps,
              targetDurationSeconds: provider.targetDurationSeconds,
              onFpsChanged: provider.setTargetFps,
              onDurationChanged: provider.setTargetDuration,
            ),

          // Progreso de captura (si está capturando)
          if (provider.isCapturing)
            CaptureProgressIndicator(
              progress: provider.progress,
              frameCount: provider.frameCount,
              expectedFrameCount: provider.expectedFrameCount,
            ),

          // Resultados (si completó)
          if (provider.state == CaptureState.completed) ...[
            CaptureResultsCard(
              totalFrames: provider.frameCount,
              optimalFrames: provider.optimalFrames.length,
              bestScore: provider.bestFrame?.globalScore,
            ),

            const SizedBox(height: AppSpacing.md),

            // Botón para continuar a estimación de peso (US-002)
            if (provider.bestFrame != null) _buildContinueButton(context),
          ],

          // Error (si hay error)
          if (provider.hasError)
            CaptureErrorCard(
              errorMessage: provider.errorMessage ?? 'Error desconocido',
            ),
        ],
      ),
    );
  }

  /// Botón para continuar a estimación de peso
  Widget _buildContinueButton(BuildContext context) {
    return ElevatedButton.icon(
      onPressed: () {
        AppRouter.push(
          context,
          AppRoutes.weightEstimation,
          arguments: {
            'framePath': provider.bestFrame!.imagePath,
            'cattleId': null,
          },
        );
      },
      icon: const Icon(Icons.navigate_next),
      label: const Text('Continuar a Estimación de Peso'),
      style: ElevatedButton.styleFrom(backgroundColor: AppColors.secondary),
    );
  }
}
