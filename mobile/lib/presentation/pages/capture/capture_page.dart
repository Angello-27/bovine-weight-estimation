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
import 'package:permission_handler/permission_handler.dart';
import 'package:provider/provider.dart';

import '../../../core/config/dependency_injection.dart';
import '../../../core/routes/app_router.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../providers/capture_provider.dart';
import '../../widgets/molecules/dialogs/permission_rationale_dialog.dart';
import '../../widgets/atoms/buttons/primary_button.dart';
import '../../widgets/atoms/indicators/loading_indicator.dart';
import '../../widgets/molecules/cards/status_card.dart';
import '../../widgets/organisms/capture/capture_config_section.dart';
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
          // Solicitar permiso de cámara just-in-time
          await _handleCaptureWithPermissions(context, provider);
        }
      },
    );
  }

  /// Maneja la captura con verificación de permisos
  Future<void> _handleCaptureWithPermissions(
    BuildContext context,
    CaptureProvider provider,
  ) async {
    final di = DependencyInjection();

    // 1. Verificar si ya tiene permiso
    final hasPermission = await di.permissionService.isPermissionGranted(
      Permission.camera,
    );

    if (hasPermission) {
      // Ya tiene permiso, iniciar captura
      await provider.startCapture();
      return;
    }

    // 2. Mostrar diálogo explicativo
    if (!context.mounted) return;

    final shouldRequest = await PermissionRationaleDialog.showCameraPermission(
      context,
    );

    if (shouldRequest != true) {
      // Usuario canceló
      return;
    }

    // 3. Solicitar permiso
    final status = await di.permissionService.requestPermission(
      Permission.camera,
    );

    if (status.isGranted) {
      // Permiso otorgado, iniciar captura
      await provider.startCapture();
    } else if (status.isPermanentlyDenied) {
      // Permiso denegado permanentemente
      if (!context.mounted) return;

      final openSettings =
          await PermissionRationaleDialog.showPermissionDeniedDialog(
            context,
            'Cámara',
          );

      if (openSettings == true) {
        await di.permissionService.openAppSettings();
      }
    } else {
      // Permiso denegado temporalmente
      if (!context.mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            'Se necesita permiso de cámara para capturar fotogramas',
          ),
          backgroundColor: AppColors.warning,
        ),
      );
    }
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
