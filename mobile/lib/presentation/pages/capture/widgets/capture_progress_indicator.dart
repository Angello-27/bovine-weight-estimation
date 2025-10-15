/// Widget: CaptureProgressIndicator
///
/// Indicador de progreso durante la captura.
/// Single Responsibility: Mostrar progreso de captura en tiempo real.
///
/// Page-specific Widget
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';

/// Indicador de progreso de captura
class CaptureProgressIndicator extends StatelessWidget {
  final double progress;
  final int frameCount;
  final int expectedFrameCount;

  const CaptureProgressIndicator({
    super.key,
    required this.progress,
    required this.frameCount,
    required this.expectedFrameCount,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          'Capturando fotogramas...',
          style: Theme.of(context).textTheme.titleMedium,
          textAlign: TextAlign.center,
        ),

        const SizedBox(height: AppSpacing.md),

        LinearProgressIndicator(
          value: progress,
          minHeight: 8,
          backgroundColor: AppColors.surfaceVariant,
          valueColor: const AlwaysStoppedAnimation<Color>(AppColors.primary),
        ),

        const SizedBox(height: AppSpacing.sm),

        Text(
          '$frameCount / $expectedFrameCount fotogramas',
          style: Theme.of(context).textTheme.bodySmall,
        ),

        const SizedBox(height: AppSpacing.lg),

        const CircularProgressIndicator(),
      ],
    );
  }
}
