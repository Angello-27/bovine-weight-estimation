/// Atom: CameraLoadingIndicator
///
/// Indicador de carga para inicialización de cámara.
/// Single Responsibility: Mostrar estado de carga de cámara.
///
/// Atomic Design - Atoms Layer
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_spacing.dart';

/// Indicador de carga para cámara
class CameraLoadingIndicator extends StatelessWidget {
  /// Altura del contenedor
  final double height;

  const CameraLoadingIndicator({super.key, this.height = 300});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: height,
      decoration: BoxDecoration(
        color: Colors.black,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      ),
      child: const Center(
        child: CircularProgressIndicator(color: Colors.white),
      ),
    );
  }
}
