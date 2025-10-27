/// Widget: CaptureActionButton
///
/// Botón de acción para iniciar/reiniciar captura.
/// Single Responsibility: Manejar acción de captura con permisos.
///
/// Page-specific Widget (Capture)
library;

import 'package:flutter/material.dart';
import 'package:permission_handler/permission_handler.dart'
    as permission_handler;

import '../../../../core/config/dependency_injection.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../providers/capture_provider.dart';
import '../../../widgets/atoms/buttons/primary_button.dart';
import '../../../widgets/atoms/indicators/loading_indicator.dart';
import '../../../widgets/molecules/dialogs/permission_rationale_dialog.dart';

/// Botón de acción para captura
class CaptureActionButton extends StatelessWidget {
  /// Provider de capture
  final CaptureProvider provider;

  const CaptureActionButton({required this.provider, super.key});

  @override
  Widget build(BuildContext context) {
    // Durante captura, mostrar indicador de carga
    if (provider.isCapturing) {
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
      permission_handler.Permission.camera,
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
      permission_handler.Permission.camera,
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
}
