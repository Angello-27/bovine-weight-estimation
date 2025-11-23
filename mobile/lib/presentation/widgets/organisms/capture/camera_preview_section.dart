/// Organism: CameraPreviewSection
///
/// Sección completa que maneja todos los estados del preview de cámara.
/// Single Responsibility: Orquestar estados de preview (loading, error, preview, sin permiso).
///
/// Atomic Design - Organisms Layer
library;

import 'package:flutter/material.dart';
import 'package:camera/camera.dart' as camera;

import '../../atoms/indicators/camera_loading_indicator.dart';
import '../../molecules/cards/camera_error_card.dart';
import '../../molecules/cards/camera_permission_card.dart';
import '../../../pages/capture/widgets/camera_preview_widget.dart';

/// Sección de preview de cámara con manejo de estados
class CameraPreviewSection extends StatelessWidget {
  /// Controller de la cámara (null si no está inicializada)
  final camera.CameraController? cameraController;

  /// Indica si la cámara se está inicializando
  final bool isInitializing;

  /// Mensaje de error (null si no hay error)
  final String? errorMessage;

  /// Callback para solicitar permiso manualmente
  final VoidCallback onRequestPermission;

  const CameraPreviewSection({
    super.key,
    this.cameraController,
    this.isInitializing = false,
    this.errorMessage,
    required this.onRequestPermission,
  });

  @override
  Widget build(BuildContext context) {
    // Estado: Inicializando
    if (isInitializing) {
      return const CameraLoadingIndicator();
    }

    // Estado: Cámara inicializada y lista
    if (cameraController != null && cameraController!.value.isInitialized) {
      return CameraPreviewWidget(controller: cameraController!);
    }

    // Estado: Error
    if (errorMessage != null) {
      return CameraErrorCard(
        errorMessage: errorMessage!,
        onActionPressed: onRequestPermission,
        actionText: 'Solicitar Permiso',
        actionIcon: Icons.settings,
      );
    }

    // Estado: Sin permiso (estado inicial)
    return CameraPermissionCard(onRequestPermission: onRequestPermission);
  }
}
