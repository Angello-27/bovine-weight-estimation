/// Page: CapturePage
///
/// US-001: Captura Continua de Fotogramas
///
/// Pantalla refactorizada con Atomic Design + SOLID.
/// Single Responsibility: Coordinar componentes de captura.
///
/// Presentation Layer - Pages
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/routes/app_router.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../providers/capture_provider.dart';
import '../../widgets/molecules/cards/status_card.dart';
import '../../widgets/organisms/capture/capture_config_section.dart';
import 'widgets/capture_action_button.dart';
import 'widgets/capture_error_card.dart';
import 'widgets/capture_progress_indicator.dart';
import 'widgets/capture_results_card.dart';

/// Pantalla de captura de fotogramas
class CapturePage extends StatelessWidget {
  const CapturePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Captura de Fotogramas')),
      body: Consumer<CaptureProvider>(
        builder: (context, provider, child) {
          return SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.screenPadding),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Estado actual
                  StatusCard(
                    icon: provider.state.icon,
                    iconColor: provider.state.color,
                    title: provider.state.title,
                    description: provider.state.description,
                  ),

                  const SizedBox(height: AppSpacing.lg),

                  // Contenido principal (scrollable)
                  Expanded(
                    child: SingleChildScrollView(
                      child: Column(
                        children: [
                          // Configuración (solo si está idle)
                          if (!provider.isCapturing &&
                              provider.state == CaptureState.idle)
                            CaptureConfigSection(
                              targetFps: provider.targetFps,
                              targetDurationSeconds:
                                  provider.targetDurationSeconds,
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
                            if (provider.bestFrame != null)
                              ElevatedButton.icon(
                                onPressed: () {
                                  AppRouter.push(
                                    context,
                                    AppRoutes.weightEstimation,
                                    arguments: {
                                      'framePath':
                                          provider.bestFrame!.imagePath,
                                      'cattleId': null,
                                    },
                                  );
                                },
                                icon: const Icon(Icons.navigate_next),
                                label: const Text(
                                  'Continuar a Estimación de Peso',
                                ),
                                style: ElevatedButton.styleFrom(
                                  backgroundColor: AppColors.secondary,
                                ),
                              ),
                          ],

                          // Error (si hay error)
                          if (provider.hasError)
                            CaptureErrorCard(
                              errorMessage:
                                  provider.errorMessage ?? 'Error desconocido',
                            ),
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: AppSpacing.md),

                  // Botón de acción
                  CaptureActionButton(provider: provider),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
