/// Molecule: PermissionRationaleDialog
///
/// Diálogo para explicar por qué se necesita un permiso.
/// Single Responsibility: Mostrar justificación clara antes de solicitar permiso.
///
/// Atomic Design - Molecules Layer
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';

/// Diálogo de justificación de permisos
class PermissionRationaleDialog extends StatelessWidget {
  final String title;
  final String description;
  final IconData icon;
  final VoidCallback onAccept;
  final VoidCallback? onDeny;

  const PermissionRationaleDialog({
    super.key,
    required this.title,
    required this.description,
    required this.icon,
    required this.onAccept,
    this.onDeny,
  });

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      icon: Icon(
        icon,
        size: AppSpacing.iconSizeXXLarge,
        color: AppColors.primary,
      ),
      title: Text(title),
      content: Text(description),
      actions: [
        if (onDeny != null)
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              onDeny?.call();
            },
            child: const Text('Cancelar'),
          ),
        ElevatedButton(
          onPressed: () {
            Navigator.of(context).pop();
            onAccept();
          },
          child: const Text('Permitir'),
        ),
      ],
    );
  }

  /// Muestra diálogo de permiso de cámara
  static Future<bool?> showCameraPermission(BuildContext context) {
    return showDialog<bool>(
      context: context,
      builder: (context) => PermissionRationaleDialog(
        title: 'Permiso de Cámara',
        description:
            'Necesitamos acceso a la cámara para capturar fotogramas del ganado y estimar su peso.\n\n'
            'La captura continua a 10-15 FPS durante 3-5 segundos permite obtener el mejor fotograma para la estimación.',
        icon: Icons.camera_alt,
        onAccept: () => Navigator.of(context).pop(true),
        onDeny: () => Navigator.of(context).pop(false),
      ),
    );
  }

  /// Muestra diálogo de permiso de ubicación
  static Future<bool?> showLocationPermission(BuildContext context) {
    return showDialog<bool>(
      context: context,
      builder: (context) => PermissionRationaleDialog(
        title: 'Permiso de Ubicación',
        description:
            'Necesitamos acceso a tu ubicación para registrar la geolocalización de los pesajes.\n\n'
            'Esto ayuda a mantener trazabilidad y cumplir con requisitos de SENASAG.',
        icon: Icons.location_on,
        onAccept: () => Navigator.of(context).pop(true),
        onDeny: () => Navigator.of(context).pop(false),
      ),
    );
  }

  /// Muestra diálogo cuando permiso está denegado permanentemente
  static Future<bool?> showPermissionDeniedDialog(
    BuildContext context,
    String permissionName,
  ) {
    return showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        icon: const Icon(
          Icons.warning,
          size: AppSpacing.iconSizeXXLarge,
          color: AppColors.warning,
        ),
        title: const Text('Permiso Denegado'),
        content: Text(
          'El permiso de $permissionName está desactivado.\n\n'
          'Para usar esta función, debes habilitarlo en la configuración de la app.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.of(context).pop(true),
            child: const Text('Abrir Configuración'),
          ),
        ],
      ),
    );
  }
}
