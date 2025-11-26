/// Capture Overlay - Molecule
///
/// Overlay con información y estadísticas de captura continua.
/// Se muestra sobre la cámara a pantalla completa.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../providers/capture_provider.dart';

/// Overlay con información de captura sobre la cámara
class CaptureOverlay extends StatelessWidget {
  const CaptureOverlay({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<CaptureProvider>(
      builder: (context, provider, child) {
        return SafeArea(
          child: Column(
            children: [
              // Barra superior con información
              _buildTopBar(context, provider),

              const Spacer(),

              // Indicador de captura activa (si está capturando)
              if (provider.isCapturing) _buildCaptureIndicator(provider),
            ],
          ),
        );
      },
    );
  }

  /// Barra superior con estadísticas
  Widget _buildTopBar(BuildContext context, CaptureProvider provider) {
    return Container(
      margin: const EdgeInsets.all(AppSpacing.md),
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.md,
        vertical: AppSpacing.sm,
      ),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.7),
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          // Botón de configuración/volver
          IconButton(
            icon: const Icon(Icons.settings, color: Colors.white),
            onPressed: () {
              // TODO: Mostrar diálogo de configuración o volver
              Navigator.of(context).pop();
            },
          ),

          // Estado y contador de frames
          _buildStatusSection(provider),

          // Estadísticas adicionales
          if (provider.isCapturing) _buildStatsSection(provider),
        ],
      ),
    );
  }

  /// Sección de estado y contador
  Widget _buildStatusSection(CaptureProvider provider) {
    return Row(
      children: [
        // Indicador de estado
        Container(
          width: 12,
          height: 12,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: provider.isCapturing ? AppColors.success : AppColors.primary,
          ),
        ),
        const SizedBox(width: AppSpacing.sm),

        // Contador de frames
        Text(
          '${provider.frameCount} frames',
          style: const TextStyle(
            color: Colors.white,
            fontSize: 14,
            fontWeight: FontWeight.w600,
          ),
        ),
      ],
    );
  }

  /// Sección de estadísticas
  Widget _buildStatsSection(CaptureProvider provider) {
    final duration = provider.continuousCaptureDuration;
    final durationText = duration != null
        ? '${duration.inMinutes}:${(duration.inSeconds % 60).toString().padLeft(2, '0')}'
        : '0:00';

    return Row(
      children: [
        // Duración de captura
        _buildStatItem(icon: Icons.timer, label: durationText),
        const SizedBox(width: AppSpacing.md),

        // FPS actual
        _buildStatItem(icon: Icons.speed, label: '${provider.targetFps} FPS'),
        const SizedBox(width: AppSpacing.md),

        // Frames óptimos
        _buildStatItem(
          icon: Icons.star,
          label: '${provider.optimalFrames.length}',
        ),
      ],
    );
  }

  /// Item de estadística
  Widget _buildStatItem({required IconData icon, required String label}) {
    return Row(
      children: [
        Icon(icon, color: Colors.white70, size: 16),
        const SizedBox(width: 4),
        Text(
          label,
          style: const TextStyle(color: Colors.white70, fontSize: 12),
        ),
      ],
    );
  }

  /// Indicador de captura activa (pulso)
  Widget _buildCaptureIndicator(CaptureProvider provider) {
    return Container(
      margin: const EdgeInsets.only(bottom: AppSpacing.xl),
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.lg,
        vertical: AppSpacing.md,
      ),
      decoration: BoxDecoration(
        color: AppColors.error.withOpacity(0.9),
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Indicador pulsante
          TweenAnimationBuilder<double>(
            tween: Tween(begin: 0.0, end: 1.0),
            duration: const Duration(milliseconds: 1000),
            builder: (context, value, child) {
              return Container(
                width: 12,
                height: 12,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: Colors.white.withOpacity(0.8 + (value * 0.2)),
                ),
              );
            },
            onEnd: () {},
          ),
          const SizedBox(width: AppSpacing.sm),

          // Texto
          const Text(
            'CAPTURANDO',
            style: TextStyle(
              color: Colors.white,
              fontSize: 14,
              fontWeight: FontWeight.bold,
              letterSpacing: 1.2,
            ),
          ),
        ],
      ),
    );
  }
}
