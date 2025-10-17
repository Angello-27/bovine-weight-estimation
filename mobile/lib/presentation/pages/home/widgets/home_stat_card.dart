/// Molecule: HomeStatCard
///
/// Card de estadística para el header del home.
/// Single Responsibility: Mostrar métrica en header con glassmorphism.
///
/// Page-specific Widget (Home)
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_spacing.dart';

/// Card de estadística en header con efecto glass
class HomeStatCard extends StatelessWidget {
  /// Ícono representativo
  final IconData icon;

  /// Valor de la estadística
  final String value;

  /// Etiqueta descriptiva
  final String label;

  const HomeStatCard({
    required this.icon,
    required this.value,
    required this.label,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.2),
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
        border: Border.all(
          color: Colors.white.withValues(alpha: 0.3),
          width: 1,
        ),
      ),
      child: Column(
        children: [
          Icon(icon, color: Colors.white, size: AppSpacing.iconSize),
          const SizedBox(height: AppSpacing.xs),
          Text(
            value,
            style: const TextStyle(
              color: Colors.white,
              fontSize: AppSpacing.fontSizeLarge,
              fontWeight: FontWeight.bold,
            ),
          ),
          Text(
            label,
            style: TextStyle(
              color: Colors.white.withValues(alpha: 0.8),
              fontSize: AppSpacing.fontSizeSmall,
            ),
          ),
        ],
      ),
    );
  }
}
