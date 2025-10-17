/// Atom: GlassCard
///
/// Card con efecto glassmorphism (vidrio esmerilado).
/// Single Responsibility: Proporcionar un contenedor con efecto de vidrio.
///
/// Presentation Layer - Atoms
library;

import 'dart:ui';

import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';

/// Card con efecto glassmorphism moderno
class GlassCard extends StatelessWidget {
  /// Contenido del card
  final Widget child;

  /// Padding interno
  final EdgeInsetsGeometry? padding;

  /// Border radius
  final double? borderRadius;

  /// Opacidad del fondo
  final double backgroundOpacity;

  /// Blur radius
  final double blurRadius;

  /// Color del fondo
  final Color? backgroundColor;

  /// Callback al tocar
  final VoidCallback? onTap;

  const GlassCard({
    required this.child,
    this.padding,
    this.borderRadius,
    this.backgroundOpacity = 0.15,
    this.blurRadius = 10.0,
    this.backgroundColor,
    this.onTap,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final effectiveBorderRadius = borderRadius ?? AppSpacing.borderRadiusLarge;
    final effectivePadding = padding ?? const EdgeInsets.all(AppSpacing.md);
    final effectiveBackgroundColor = backgroundColor ?? Colors.white;

    return ClipRRect(
      borderRadius: BorderRadius.circular(effectiveBorderRadius),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: blurRadius, sigmaY: blurRadius),
        child: Container(
          decoration: BoxDecoration(
            color: effectiveBackgroundColor.withValues(
              alpha: backgroundOpacity,
            ),
            borderRadius: BorderRadius.circular(effectiveBorderRadius),
            border: Border.all(
              color: Colors.white.withValues(alpha: 0.2),
              width: 1.5,
            ),
            boxShadow: [
              BoxShadow(
                color: AppColors.primary.withValues(alpha: 0.1),
                blurRadius: AppSpacing.elevationMedium,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Material(
            color: Colors.transparent,
            child: InkWell(
              onTap: onTap,
              borderRadius: BorderRadius.circular(effectiveBorderRadius),
              child: Padding(padding: effectivePadding, child: child),
            ),
          ),
        ),
      ),
    );
  }
}
