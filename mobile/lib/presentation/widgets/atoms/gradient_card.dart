/// Atom: GradientCard
///
/// Card moderno con gradiente de fondo.
/// Single Responsibility: Proporcionar un contenedor con gradiente.
///
/// Presentation Layer - Atoms
library;

import 'package:flutter/material.dart';

import '../../../core/theme/app_spacing.dart';

/// Card con gradiente moderno
class GradientCard extends StatelessWidget {
  /// Gradiente de fondo
  final Gradient gradient;

  /// Contenido del card
  final Widget child;

  /// Padding interno
  final EdgeInsetsGeometry? padding;

  /// Border radius
  final double? borderRadius;

  /// Elevación
  final double? elevation;

  /// Callback al tocar
  final VoidCallback? onTap;

  const GradientCard({
    required this.gradient,
    required this.child,
    this.padding,
    this.borderRadius,
    this.elevation,
    this.onTap,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final effectiveBorderRadius = borderRadius ?? AppSpacing.borderRadiusLarge;
    final effectivePadding = padding ?? const EdgeInsets.all(AppSpacing.md);

    return Card(
      elevation: elevation ?? AppSpacing.elevationMedium,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(effectiveBorderRadius),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(effectiveBorderRadius),
        child: Ink(
          decoration: BoxDecoration(
            gradient: gradient,
            borderRadius: BorderRadius.circular(effectiveBorderRadius),
          ),
          child: Padding(padding: effectivePadding, child: child),
        ),
      ),
    );
  }
}
