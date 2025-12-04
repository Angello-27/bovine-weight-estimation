/// Molecule: InfoCard
///
/// Card informativa genérica con ícono, título y descripción.
/// Single Responsibility: Mostrar información destacada.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';

/// Tarjeta informativa genérica
class InfoCard extends StatelessWidget {
  /// Ícono representativo
  final IconData icon;

  /// Título de la información
  final String title;

  /// Descripción o contenido
  final String description;

  /// Color del ícono y acento
  final Color? color;

  /// Color de fondo
  final Color? backgroundColor;

  /// Callback al tocar
  final VoidCallback? onTap;

  /// Mostrar como destacado (con gradiente)
  final bool highlighted;

  const InfoCard({
    required this.icon,
    required this.title,
    required this.description,
    this.color,
    this.backgroundColor,
    this.onTap,
    this.highlighted = false,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final effectiveColor = color ?? AppColors.info;

    if (highlighted) {
      return _buildHighlightedCard(context, effectiveColor);
    }

    return _buildStandardCard(context, effectiveColor);
  }

  /// Card estándar con fondo sólido
  Widget _buildStandardCard(BuildContext context, Color effectiveColor) {
    return Card(
      elevation: AppSpacing.elevationMedium,
      color: backgroundColor ?? effectiveColor.withValues(alpha: 0.1),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
        side: BorderSide(
          color: effectiveColor.withValues(alpha: 0.3),
          width: 1,
        ),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: _buildContent(context, effectiveColor),
        ),
      ),
    );
  }

  /// Card destacado con gradiente
  Widget _buildHighlightedCard(BuildContext context, Color effectiveColor) {
    return Card(
      elevation: AppSpacing.elevationHigh,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
        child: Ink(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [
                effectiveColor,
                effectiveColor.withValues(
                  red: (effectiveColor.r * 0.8).clamp(0, 1),
                  green: (effectiveColor.g * 0.8).clamp(0, 1),
                  blue: (effectiveColor.b * 0.8).clamp(0, 1),
                ),
              ],
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
            ),
            borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
          ),
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.lg),
            child: _buildContent(context, Colors.white),
          ),
        ),
      ),
    );
  }

  /// Contenido de la card
  Widget _buildContent(BuildContext context, Color contentColor) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Ícono
        Container(
          padding: const EdgeInsets.all(AppSpacing.sm),
          decoration: BoxDecoration(
            color: highlighted
                ? Colors.white.withValues(alpha: 0.2)
                : contentColor.withValues(alpha: 0.15),
            borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
          ),
          child: Icon(
            icon,
            color: Colors.white,
            size: AppSpacing.iconSizeLarge,
          ),
        ),
        const SizedBox(width: AppSpacing.md),

        // Texto
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                title,
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: Theme.of(context).colorScheme.onSurface,
                ),
              ),
              const SizedBox(height: AppSpacing.xs),
              Text(
                description,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: Theme.of(context).colorScheme.onSurfaceVariant,
                ),
              ),
            ],
          ),
        ),

        // Flecha (si es interactiva)
        if (onTap != null)
          Icon(
            Icons.chevron_right,
            color: highlighted ? Colors.white : contentColor,
            size: AppSpacing.iconSize,
          ),
      ],
    );
  }
}
