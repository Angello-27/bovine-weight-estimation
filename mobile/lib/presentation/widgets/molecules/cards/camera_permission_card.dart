/// Molecule: CameraPermissionCard
///
/// Card para solicitar permiso de cámara.
/// Single Responsibility: Mostrar UI para solicitar permisos de cámara.
///
/// Atomic Design - Molecules Layer
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_spacing.dart';

/// Card para solicitar permiso de cámara
class CameraPermissionCard extends StatelessWidget {
  /// Callback cuando se presiona el botón de solicitar permiso
  final VoidCallback onRequestPermission;

  /// Mensaje personalizado (opcional)
  final String? message;

  const CameraPermissionCard({
    super.key,
    required this.onRequestPermission,
    this.message,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.blue.shade50,
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.md),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.camera_alt, color: Colors.blue.shade700, size: 48),
            const SizedBox(height: AppSpacing.md),
            Text(
              message ??
                  'Se necesita permiso de cámara para mostrar el preview.',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: AppSpacing.md),
            ElevatedButton.icon(
              onPressed: onRequestPermission,
              icon: const Icon(Icons.camera_alt),
              label: const Text('Solicitar Permiso'),
            ),
          ],
        ),
      ),
    );
  }
}
