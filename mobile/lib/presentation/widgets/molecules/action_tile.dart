/// Molecule: ActionTile
///
/// Tile de acción con ícono, título, subtítulo y gradiente.
/// Single Responsibility: Representar una acción rápida.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';

import '../../../core/theme/app_spacing.dart';

/// Tile de acción moderno con gradiente
class ActionTile extends StatelessWidget {
  /// Ícono de la acción
  final IconData icon;

  /// Título de la acción
  final String title;

  /// Subtítulo descriptivo
  final String? subtitle;

  /// Color de fondo (en lugar de gradiente)
  final Color color;

  /// Callback al tocar
  final VoidCallback? onTap;

  /// Tamaño del ícono
  final double? iconSize;

  const ActionTile({
    required this.icon,
    required this.title,
    required this.color,
    this.subtitle,
    this.onTap,
    this.iconSize,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      color: color,
      elevation: AppSpacing.elevationMedium,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
        child: Padding(
          padding: const EdgeInsets.all(AppSpacing.sm),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            mainAxisSize: MainAxisSize.min,
            children: [
              // Ícono
              Icon(
                icon,
                size: iconSize ?? AppSpacing.iconSizeXLarge,
                color: Colors.white,
              ),

              const SizedBox(height: AppSpacing.xs),

              // Título
              Text(
                title,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),

              // Subtítulo opcional
              if (subtitle != null) ...[
                const SizedBox(height: 2),
                Text(
                  subtitle!,
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: Colors.white.withValues(alpha: 0.9),
                  ),
                  textAlign: TextAlign.center,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
