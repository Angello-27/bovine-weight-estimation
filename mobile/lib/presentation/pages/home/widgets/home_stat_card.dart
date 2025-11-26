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
        color: Colors.white.withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
        border: Border.all(
          color: Colors.white.withValues(alpha: 0.3),
          width: 1.5,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.1),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            padding: const EdgeInsets.all(AppSpacing.xs),
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.2),
              shape: BoxShape.circle,
            ),
            child: Icon(icon, color: Colors.white, size: AppSpacing.iconSize),
          ),
          const SizedBox(height: AppSpacing.sm),
          Text(
            value,
            style: const TextStyle(
              color: Colors.white,
              fontSize: AppSpacing.fontSizeTitle,
              fontWeight: FontWeight.bold,
              height: 1.2,
            ),
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(
            label,
            textAlign: TextAlign.center,
            style: TextStyle(
              color: Colors.white.withValues(alpha: 0.9),
              fontSize: AppSpacing.fontSizeSmall,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}
