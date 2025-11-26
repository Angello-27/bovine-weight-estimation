/// Registration Snackbar Handler - Helper
///
/// Maneja la lógica de mostrar snackbars de éxito y error.
/// Single Responsibility: Gestionar notificaciones de la página de registro.
///
/// Presentation Layer - Helpers
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../providers/cattle_provider.dart';

/// Helper para manejar snackbars de registro
class RegistrationSnackbarHandler {
  /// Muestra snackbar de éxito
  static void showSuccessSnackbar(
    BuildContext context,
    String message,
    VoidCallback? onComplete,
  ) {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Row(
            children: [
              const Icon(Icons.check_circle, color: Colors.white),
              const SizedBox(width: AppSpacing.sm),
              Expanded(child: Text(message)),
            ],
          ),
          backgroundColor: AppColors.success,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
          ),
        ),
      );
      onComplete?.call();
    });
  }

  /// Muestra snackbar de error
  static void showErrorSnackbar(
    BuildContext context,
    String message,
    VoidCallback? onComplete,
  ) {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Row(
            children: [
              const Icon(Icons.error, color: Colors.white),
              const SizedBox(width: AppSpacing.sm),
              Expanded(child: Text(message)),
            ],
          ),
          backgroundColor: AppColors.error,
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
          ),
        ),
      );
      onComplete?.call();
    });
  }

  /// Maneja los snackbars según el estado del provider
  static void handleProviderState(
    BuildContext context,
    CattleProvider provider,
    VoidCallback? onSuccess,
  ) {
    // Snackbar de éxito
    if (provider.state == CattleState.success &&
        provider.successMessage != null) {
      showSuccessSnackbar(context, provider.successMessage!, () {
        provider.clearMessages();
        onSuccess?.call();
      });
    }

    // Snackbar de error
    if (provider.hasError && provider.errorMessage != null) {
      showErrorSnackbar(context, provider.errorMessage!, () {
        provider.clearMessages();
      });
    }
  }
}
