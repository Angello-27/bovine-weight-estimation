/// Atom: SyncButton
///
/// Botón para sincronización manual.
/// Single Responsibility: Trigger manual de sincronización.
///
/// Atomic Design - Presentation Layer
library;

import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';

/// Botón de sincronización manual
class SyncButton extends StatelessWidget {
  /// Callback al presionar
  final VoidCallback? onPressed;

  /// Estado de carga
  final bool isLoading;

  /// Texto del botón
  final String label;

  /// Mostrar ícono
  final bool showIcon;

  /// Estilo compacto
  final bool compact;

  const SyncButton({
    super.key,
    required this.onPressed,
    this.isLoading = false,
    this.label = 'Sincronizar ahora',
    this.showIcon = true,
    this.compact = false,
  });

  @override
  Widget build(BuildContext context) {
    if (compact) {
      return IconButton(
        onPressed: isLoading ? null : onPressed,
        icon: isLoading
            ? const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(strokeWidth: 2.0),
              )
            : const Icon(Icons.sync_rounded),
        tooltip: label,
        style: IconButton.styleFrom(foregroundColor: AppColors.primary),
      );
    }

    return ElevatedButton.icon(
      onPressed: isLoading ? null : onPressed,
      icon: isLoading
          ? const SizedBox(
              width: 18,
              height: 18,
              child: CircularProgressIndicator(
                strokeWidth: 2.0,
                valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
              ),
            )
          : showIcon
          ? const Icon(Icons.sync_rounded, size: 20)
          : const SizedBox.shrink(),
      label: Text(
        isLoading ? 'Sincronizando...' : label,
        style: const TextStyle(fontSize: 14.0, fontWeight: FontWeight.w600),
      ),
      style: ElevatedButton.styleFrom(
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(
          horizontal: AppSpacing.lg,
          vertical: AppSpacing.md,
        ),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        ),
      ),
    );
  }
}
