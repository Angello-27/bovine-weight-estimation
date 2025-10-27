/// Widget: CameraPreviewWidget
///
/// Preview en vivo de la cámara.
/// Single Responsibility: Mostrar vista previa de la cámara.
///
/// Page-specific Widget (Capture) - Atom
library;

import 'package:flutter/material.dart';
import 'package:camera/camera.dart' as camera;

import '../../../../core/theme/app_spacing.dart';

/// Widget para mostrar preview de la cámara
class CameraPreviewWidget extends StatelessWidget {
  /// Controller de la cámara
  final camera.CameraController controller;

  const CameraPreviewWidget({required this.controller, super.key});

  @override
  Widget build(BuildContext context) {
    if (!controller.value.isInitialized) {
      return Container(
        height: 300,
        decoration: BoxDecoration(
          color: Colors.black,
          borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
        ),
        child: const Center(
          child: CircularProgressIndicator(color: Colors.white),
        ),
      );
    }

    return ClipRRect(
      borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      child: AspectRatio(
        aspectRatio: controller.value.aspectRatio,
        child: OverflowBox(
          alignment: Alignment.center,
          child: FittedBox(
            fit: BoxFit.fitWidth,
            child: SizedBox(
              width: MediaQuery.of(context).size.width,
              height:
                  MediaQuery.of(context).size.width /
                  controller.value.aspectRatio,
              child: camera.CameraPreview(controller),
            ),
          ),
        ),
      ),
    );
  }
}
