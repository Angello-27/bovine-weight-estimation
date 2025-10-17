/// Molecule: StatCard
///
/// Card de estadística con ícono, valor y etiqueta.
/// Single Responsibility: Mostrar una métrica estadística.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../atoms/glass_card.dart';

/// Card de estadística moderno
class StatCard extends StatelessWidget {
  /// Ícono representativo
  final IconData icon;

  /// Valor de la estadística
  final String value;

  /// Etiqueta descriptiva
  final String label;

  /// Color del ícono
  final Color? iconColor;

  /// Color del fondo
  final Color? backgroundColor;

  /// Callback al tocar
  final VoidCallback? onTap;

  const StatCard({
    required this.icon,
    required this.value,
    required this.label,
    this.iconColor,
    this.backgroundColor,
    this.onTap,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return GlassCard(
      backgroundColor: backgroundColor ?? AppColors.primary,
      backgroundOpacity: 0.1,
      onTap: onTap,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Ícono
          Container(
            padding: const EdgeInsets.all(AppSpacing.sm),
            decoration: BoxDecoration(
              color: (iconColor ?? AppColors.primary).withValues(alpha: 0.15),
              borderRadius: BorderRadius.circular(
                AppSpacing.borderRadiusMedium,
              ),
            ),
            child: Icon(
              icon,
              color: iconColor ?? AppColors.primary,
              size: AppSpacing.iconSizeLarge,
            ),
          ),

          const SizedBox(height: AppSpacing.sm),

          // Valor
          Text(
            value,
            style: Theme.of(context).textTheme.headlineSmall?.copyWith(
              fontWeight: FontWeight.bold,
              color: AppColors.grey900,
            ),
          ),

          const SizedBox(height: AppSpacing.xs),

          // Etiqueta
          Text(
            label,
            style: Theme.of(
              context,
            ).textTheme.bodyMedium?.copyWith(color: AppColors.grey600),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}
