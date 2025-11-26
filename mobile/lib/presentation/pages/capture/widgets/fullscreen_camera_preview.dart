/// Full Screen Camera Preview - Atom
///
/// Preview de cámara a pantalla completa (como app nativa).
/// Single Responsibility: Mostrar cámara ocupando toda la pantalla.
///
/// Presentation Layer - Atoms
library;

import 'package:flutter/material.dart';
import 'package:camera/camera.dart' as camera;

/// Preview de cámara a pantalla completa
class FullScreenCameraPreview extends StatelessWidget {
  /// Controller de la cámara
  final camera.CameraController controller;

  const FullScreenCameraPreview({required this.controller, super.key});

  @override
  Widget build(BuildContext context) {
    if (!controller.value.isInitialized) {
      return Container(
        color: Colors.black,
        child: const Center(
          child: CircularProgressIndicator(color: Colors.white),
        ),
      );
    }

    // Obtener tamaño de pantalla
    final screenSize = MediaQuery.of(context).size;
    final aspectRatio = controller.value.aspectRatio;

    return SizedBox(
      width: screenSize.width,
      height: screenSize.height,
      child: FittedBox(
        fit: BoxFit.cover,
        child: SizedBox(
          width: screenSize.width,
          height: screenSize.width / aspectRatio,
          child: camera.CameraPreview(controller),
        ),
      ),
    );
  }
}
