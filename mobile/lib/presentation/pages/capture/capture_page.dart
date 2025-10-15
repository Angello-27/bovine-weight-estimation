/// Page: CapturePage
/// 
/// US-001: Captura Continua de Fotogramas
/// 
/// Pantalla principal para capturar fotogramas continuos (10-15 FPS, 3-5 seg)
/// con evaluación automática de calidad y selección del mejor fotograma.
///
/// Presentation Layer - Clean Architecture
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/ui/theme/app_colors.dart';
import '../../../core/ui/theme/app_spacing.dart';
import '../../providers/capture_provider.dart';

/// Pantalla de captura de fotogramas
class CapturePage extends StatefulWidget {
  const CapturePage({super.key});

  @override
  State<CapturePage> createState() => _CapturePageState();
}

class _CapturePageState extends State<CapturePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Captura de Fotogramas'),
        backgroundColor: AppColors.primary,
        foregroundColor: AppColors.onPrimary,
      ),
      body: Consumer<CaptureProvider>(
        builder: (context, captureProvider, child) {
          return SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.screenPadding),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Estado actual
                  _buildStatusCard(captureProvider),
                  
                  const SizedBox(height: AppSpacing.lg),

                  // Configuración (FPS y duración)
                  if (!captureProvider.isCapturing)
                    _buildConfigurationSection(captureProvider),

                  const SizedBox(height: AppSpacing.lg),

                  // Progreso de captura
                  if (captureProvider.isCapturing)
                    _buildCaptureProgress(captureProvider),

                  // Resultados
                  if (captureProvider.state == CaptureState.completed)
                    _buildResults(captureProvider),

                  // Error
                  if (captureProvider.hasError)
                    _buildError(captureProvider),

                  const Spacer(),

                  // Botón de acción principal
                  _buildActionButton(context, captureProvider),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  /// Card de estado actual
  Widget _buildStatusCard(CaptureProvider provider) {
    final status = _getStatusInfo(provider.state);
    
    return Card(
      elevation: AppSpacing.elevationMedium,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
      ),
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.cardPadding),
        child: Row(
          children: [
            Icon(
              status.icon,
              size: AppSpacing.iconSizeLarge,
              color: status.color,
            ),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    status.title,
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  Text(
                    status.description,
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Sección de configuración (FPS y duración)
  Widget _buildConfigurationSection(CaptureProvider provider) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Configuración',
          style: Theme.of(context).textTheme.titleMedium,
        ),
        const SizedBox(height: AppSpacing.sm),
        
        // FPS Slider
        Card(
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.md),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('FPS: ${provider.targetFps}'),
                Slider(
                  value: provider.targetFps.toDouble(),
                  min: 10,
                  max: 15,
                  divisions: 5,
                  label: '${provider.targetFps} FPS',
                  onChanged: (value) => provider.setTargetFps(value.toInt()),
                ),
              ],
            ),
          ),
        ),
        
        const SizedBox(height: AppSpacing.sm),
        
        // Duración Slider
        Card(
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.md),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Duración: ${provider.targetDurationSeconds}s'),
                Slider(
                  value: provider.targetDurationSeconds.toDouble(),
                  min: 3,
                  max: 5,
                  divisions: 2,
                  label: '${provider.targetDurationSeconds}s',
                  onChanged: (value) =>
                      provider.setTargetDuration(value.toInt()),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  /// Indicador de progreso durante la captura
  Widget _buildCaptureProgress(CaptureProvider provider) {
    return Column(
      children: [
        Text(
          'Capturando fotogramas...',
          style: Theme.of(context).textTheme.titleMedium,
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: AppSpacing.md),
        
        LinearProgressIndicator(
          value: provider.progress,
          minHeight: 8,
          backgroundColor: AppColors.surfaceVariant,
          valueColor: const AlwaysStoppedAnimation<Color>(AppColors.primary),
        ),
        
        const SizedBox(height: AppSpacing.sm),
        
        Text(
          '${provider.frameCount} / ${provider.expectedFrameCount} fotogramas',
          style: Theme.of(context).textTheme.bodySmall,
        ),
        
        const SizedBox(height: AppSpacing.lg),
        
        const CircularProgressIndicator(),
      ],
    );
  }

  /// Resultados de la captura completada
  Widget _buildResults(CaptureProvider provider) {
    return Column(
      children: [
        Text(
          '¡Captura completada!',
          style: Theme.of(context).textTheme.titleLarge?.copyWith(
            color: AppColors.success,
          ),
          textAlign: TextAlign.center,
        ),
        
        const SizedBox(height: AppSpacing.md),
        
        Card(
          elevation: AppSpacing.elevationMedium,
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.cardPadding),
            child: Column(
              children: [
                _buildResultRow(
                  'Total de fotogramas',
                  '${provider.frameCount}',
                  Icons.photo_library,
                ),
                
                const Divider(height: AppSpacing.md),
                
                _buildResultRow(
                  'Fotogramas óptimos',
                  '${provider.optimalFrames.length}',
                  Icons.check_circle,
                ),
                
                const Divider(height: AppSpacing.md),
                
                _buildResultRow(
                  'Mejor score',
                  provider.bestFrame != null
                      ? '${(provider.bestFrame!.globalScore * 100).toStringAsFixed(0)}%'
                      : 'N/A',
                  Icons.star,
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  /// Fila de resultado
  Widget _buildResultRow(String label, String value, IconData icon) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Row(
          children: [
            Icon(icon, size: AppSpacing.iconSize, color: AppColors.primary),
            const SizedBox(width: AppSpacing.sm),
            Text(label),
          ],
        ),
        Text(
          value,
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
            fontWeight: FontWeight.bold,
            color: AppColors.primary,
          ),
        ),
      ],
    );
  }

  /// Widget de error
  Widget _buildError(CaptureProvider provider) {
    return Card(
      color: AppColors.error.withOpacity(0.1),
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.cardPadding),
        child: Row(
          children: [
            const Icon(Icons.error, color: AppColors.error),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Error',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      color: AppColors.error,
                    ),
                  ),
                  const SizedBox(height: AppSpacing.xs),
                  Text(
                    provider.errorMessage ?? 'Error desconocido',
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// Botón de acción principal
  Widget _buildActionButton(BuildContext context, CaptureProvider provider) {
    if (provider.isCapturing) {
      return const SizedBox.shrink(); // No mostrar botón durante captura
    }

    final isIdle = provider.state == CaptureState.idle;
    final buttonText = isIdle ? 'Iniciar Captura' : 'Capturar de Nuevo';
    final buttonIcon = isIdle ? Icons.camera_alt : Icons.refresh;

    return ElevatedButton.icon(
      onPressed: () async {
        if (!isIdle) {
          provider.reset();
        } else {
          await provider.startCapture();
        }
      },
      icon: Icon(buttonIcon),
      label: Text(buttonText),
      style: ElevatedButton.styleFrom(
        minimumSize: const Size.fromHeight(AppSpacing.minButtonHeight),
        backgroundColor: AppColors.primary,
        foregroundColor: AppColors.onPrimary,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        ),
      ),
    );
  }

  /// Obtiene información de estado
  _StatusInfo _getStatusInfo(CaptureState state) {
    switch (state) {
      case CaptureState.idle:
        return _StatusInfo(
          icon: Icons.camera_alt,
          color: AppColors.primary,
          title: 'Listo para capturar',
          description: 'Configura los parámetros y presiona "Iniciar Captura"',
        );
      case CaptureState.capturing:
        return _StatusInfo(
          icon: Icons.camera,
          color: AppColors.info,
          title: 'Capturando...',
          description: 'Capturando fotogramas continuos',
        );
      case CaptureState.completed:
        return _StatusInfo(
          icon: Icons.check_circle,
          color: AppColors.success,
          title: 'Completado',
          description: 'Captura finalizada exitosamente',
        );
      case CaptureState.error:
        return _StatusInfo(
          icon: Icons.error,
          color: AppColors.error,
          title: 'Error',
          description: 'Ocurrió un error durante la captura',
        );
    }
  }
}

/// Información de estado para UI
class _StatusInfo {
  final IconData icon;
  final Color color;
  final String title;
  final String description;

  _StatusInfo({
    required this.icon,
    required this.color,
    required this.title,
    required this.description,
  });
}

