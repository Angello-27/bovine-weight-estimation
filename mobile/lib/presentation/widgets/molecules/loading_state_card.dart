/// Molecule: LoadingStateCard
///
/// Card de estado de carga con spinner y mensaje.
/// Single Responsibility: Mostrar estado de carga consistente.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';

/// Card de estado de carga moderno
class LoadingStateCard extends StatelessWidget {
  /// Mensaje a mostrar
  final String message;

  /// Color del spinner
  final Color? color;

  const LoadingStateCard({required this.message, this.color, super.key});

  @override
  Widget build(BuildContext context) {
    final spinnerColor = color ?? AppColors.primary;

    return Center(
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.xl),
        decoration: BoxDecoration(
          color: spinnerColor.withValues(alpha: 0.05),
          borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            SizedBox(
              width: 60,
              height: 60,
              child: CircularProgressIndicator(
                strokeWidth: 6,
                color: spinnerColor,
              ),
            ),
            const SizedBox(height: AppSpacing.lg),
            Text(
              message,
              style: const TextStyle(
                fontSize: AppSpacing.fontSizeNormal,
                fontWeight: FontWeight.w500,
                color: AppColors.grey800,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
