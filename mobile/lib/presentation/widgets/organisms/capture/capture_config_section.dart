/// Organism: CaptureConfigSection
///
/// Sección de configuración de captura (FPS y duración).
/// Single Responsibility: Agrupar controles de configuración.
///
/// Atomic Design - Organisms Layer
library;

import 'package:flutter/material.dart';

import '../../../../core/config/app_config.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../molecules/sliders/configuration_slider.dart';

/// Sección de configuración de captura
class CaptureConfigSection extends StatelessWidget {
  final int targetFps;
  final int targetDurationSeconds;
  final ValueChanged<int> onFpsChanged;
  final ValueChanged<int> onDurationChanged;

  const CaptureConfigSection({
    super.key,
    required this.targetFps,
    required this.targetDurationSeconds,
    required this.onFpsChanged,
    required this.onDurationChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Configuración', style: Theme.of(context).textTheme.titleMedium),
        const SizedBox(height: AppSpacing.sm),

        // Slider de FPS
        ConfigurationSlider(
          label: 'FPS',
          value: targetFps.toDouble(),
          min: AppConfig.minFps.toDouble(),
          max: AppConfig.maxFps.toDouble(),
          divisions: AppConfig.maxFps - AppConfig.minFps,
          valueFormatter: (value) => '${value.toInt()} FPS',
          onChanged: (value) => onFpsChanged(value.toInt()),
        ),

        const SizedBox(height: AppSpacing.sm),

        // Slider de duración
        ConfigurationSlider(
          label: 'Duración',
          value: targetDurationSeconds.toDouble(),
          min: AppConfig.minCaptureDuration.toDouble(),
          max: AppConfig.maxCaptureDuration.toDouble(),
          divisions:
              AppConfig.maxCaptureDuration - AppConfig.minCaptureDuration,
          valueFormatter: (value) => '${value.toInt()}s',
          onChanged: (value) => onDurationChanged(value.toInt()),
        ),
      ],
    );
  }
}
