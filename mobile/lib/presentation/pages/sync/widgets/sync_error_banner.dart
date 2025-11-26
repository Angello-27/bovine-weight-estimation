/// Sync Error Banner - Molecule
///
/// Banner que muestra mensajes de error de sincronización.
/// Usa colores de marca para mantener consistencia visual.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';

/// Banner de error para sincronización
class SyncErrorBanner extends StatelessWidget {
  final String message;

  const SyncErrorBanner({required this.message, super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.warningLight,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        border: Border.all(
          color: AppColors.accent.withValues(alpha: 0.4),
          width: 1.5,
        ),
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(AppSpacing.xs),
            decoration: BoxDecoration(
              color: AppColors.accent,
              shape: BoxShape.circle,
            ),
            child: const Icon(
              Icons.info_outline_rounded,
              size: 18,
              color: AppColors.onAccent,
            ),
          ),
          const SizedBox(width: AppSpacing.md),
          Expanded(
            child: Text(
              message,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: AppColors.grey900,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
