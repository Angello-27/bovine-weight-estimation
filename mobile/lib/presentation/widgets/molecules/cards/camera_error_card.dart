/// Molecule: CameraErrorCard
///
/// Card para mostrar errores relacionados con la cámara.
/// Single Responsibility: Mostrar mensajes de error de cámara.
///
/// Atomic Design - Molecules Layer
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';

/// Card para mostrar errores de cámara
class CameraErrorCard extends StatelessWidget {
  /// Mensaje de error
  final String errorMessage;

  /// Callback cuando se presiona el botón de acción
  final VoidCallback? onActionPressed;

  /// Texto del botón de acción
  final String? actionText;

  /// Ícono del botón de acción
  final IconData? actionIcon;

  const CameraErrorCard({
    super.key,
    required this.errorMessage,
    this.onActionPressed,
    this.actionText,
    this.actionIcon,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: AppColors.error.withValues(alpha: 0.1),
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.md),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.error_outline, color: AppColors.error, size: 48),
            const SizedBox(height: AppSpacing.md),
            Text(
              errorMessage,
              textAlign: TextAlign.center,
              style: TextStyle(color: AppColors.error),
            ),
            if (onActionPressed != null) ...[
              const SizedBox(height: AppSpacing.md),
              ElevatedButton.icon(
                onPressed: onActionPressed,
                icon: Icon(actionIcon ?? Icons.settings),
                label: Text(actionText ?? 'Solicitar Permiso'),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
