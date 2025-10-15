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
import '../../../core/ui/atoms/buttons/primary_button.dart';
import '../../../core/ui/atoms/indicators/loading_indicator.dart';
import '../../../core/ui/molecules/cards/status_card.dart';
import '../../../core/ui/organisms/capture/capture_config_section.dart';
import '../../../core/ui/theme/app_colors.dart';
import '../../../core/ui/theme/app_spacing.dart';
import '../../providers/capture_provider.dart';
import 'widgets/capture_error_card.dart';
import 'widgets/capture_progress_indicator.dart';
import 'widgets/capture_results_card.dart';

/// Pantalla de captura de fotogramas
class CapturePage extends StatelessWidget {
  const CapturePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Captura de Fotogramas'),
      ),
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
                    icon: _getStatusIcon(provider.state),
                    iconColor: _getStatusColor(provider.state),
                    title: _getStatusTitle(provider.state),
                    description: _getStatusDescription(provider.state),
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
                    if (provider.bestFrame != null)
                      ElevatedButton.icon(
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
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.secondary,
                        ),
                      ),
                  ],

                          // Error (si hay error)
                          if (provider.hasError)
                            CaptureErrorCard(
                              errorMessage: provider.errorMessage ?? 'Error desconocido',
                            ),
                        ],
                      ),
                    ),
                  ),

                  const SizedBox(height: AppSpacing.md),

                  // Botón de acción
                  _buildActionButton(context, provider),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  /// Construye el botón de acción según el estado
  Widget _buildActionButton(BuildContext context, CaptureProvider provider) {
    if (provider.isCapturing) {
      // Durante captura, mostrar indicador de carga
      return const LoadingIndicator();
    }

    final isIdle = provider.state == CaptureState.idle;
    final buttonText = isIdle ? 'Iniciar Captura' : 'Capturar de Nuevo';
    final buttonIcon = isIdle ? Icons.camera_alt : Icons.refresh;

    return PrimaryButton(
      text: buttonText,
      icon: buttonIcon,
      onPressed: () async {
        if (!isIdle) {
          provider.reset();
        } else {
          await provider.startCapture();
        }
      },
    );
  }

  // Métodos helper para obtener información de estado
  IconData _getStatusIcon(CaptureState state) {
    switch (state) {
      case CaptureState.idle:
        return Icons.camera_alt;
      case CaptureState.capturing:
        return Icons.camera;
      case CaptureState.completed:
        return Icons.check_circle;
      case CaptureState.error:
        return Icons.error;
    }
  }

  Color _getStatusColor(CaptureState state) {
    switch (state) {
      case CaptureState.idle:
        return AppColors.primary;
      case CaptureState.capturing:
        return AppColors.info;
      case CaptureState.completed:
        return AppColors.success;
      case CaptureState.error:
        return AppColors.error;
    }
  }

  String _getStatusTitle(CaptureState state) {
    switch (state) {
      case CaptureState.idle:
        return 'Listo para capturar';
      case CaptureState.capturing:
        return 'Capturando...';
      case CaptureState.completed:
        return 'Completado';
      case CaptureState.error:
        return 'Error';
    }
  }

  String _getStatusDescription(CaptureState state) {
    switch (state) {
      case CaptureState.idle:
        return 'Configura los parámetros y presiona "Iniciar Captura"';
      case CaptureState.capturing:
        return 'Capturando fotogramas continuos';
      case CaptureState.completed:
        return 'Captura finalizada exitosamente';
      case CaptureState.error:
        return 'Ocurrió un error durante la captura';
    }
  }
}
