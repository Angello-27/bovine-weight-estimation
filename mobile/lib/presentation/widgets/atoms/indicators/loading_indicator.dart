/// Atom: LoadingIndicator
///
/// Indicador de carga circular.
/// Single Responsibility: Mostrar progreso indeterminado.
///
/// Atomic Design - Atoms Layer
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';

/// Indicador de carga
class LoadingIndicator extends StatelessWidget {
  final double size;
  final Color? color;

  const LoadingIndicator({super.key, this.size = 48.0, this.color});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: SizedBox(
        width: size,
        height: size,
        child: CircularProgressIndicator(
          valueColor: AlwaysStoppedAnimation<Color>(color ?? AppColors.primary),
        ),
      ),
    );
  }
}
