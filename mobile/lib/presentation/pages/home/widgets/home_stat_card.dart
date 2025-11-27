/// Molecule: HomeStatCard
///
/// Card de estadística para el header del home.
/// Single Responsibility: Mostrar métrica en header con glassmorphism.
///
/// Page-specific Widget (Home)
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../core/theme/app_spacing.dart';
import '../../../../core/theme/app_theme.dart';
import '../../../providers/settings_provider.dart';

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
    // Obtener el tamaño de fuente actual desde el provider
    final settingsProvider = Provider.of<SettingsProvider>(
      context,
      listen: false,
    );
    final textSize = settingsProvider.settings.textSize;
    // Usar la función pública de AppTheme para mantener consistencia
    final scaleFactor = AppTheme.getTextScaleFactor(textSize);

    // Altura base que se escala según el tamaño de fuente
    const double baseHeight = 120.0;
    const double baseMinHeight = 100.0;
    final double maxHeight = baseHeight * scaleFactor;
    final double minHeight = baseMinHeight * scaleFactor;

    return ConstrainedBox(
      constraints: BoxConstraints(maxHeight: maxHeight, minHeight: minHeight),
      child: Container(
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
          mainAxisSize: MainAxisSize.min,
          children: [
            // Ícono con tamaño fijo
            Container(
              padding: const EdgeInsets.all(AppSpacing.xs),
              decoration: BoxDecoration(
                color: Colors.white.withValues(alpha: 0.2),
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: Colors.white, size: AppSpacing.iconSize),
            ),
            const SizedBox(height: AppSpacing.sm),
            // Valor - usa el tema pero se ajusta dentro del espacio
            Flexible(
              child: Text(
                value,
                style: Theme.of(context).textTheme.titleLarge?.copyWith(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  height: 1.2,
                ),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                textAlign: TextAlign.center,
              ),
            ),
            const SizedBox(height: AppSpacing.xs),
            // Etiqueta - usa el tema pero se ajusta dentro del espacio
            Flexible(
              child: Text(
                label,
                textAlign: TextAlign.center,
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  color: Colors.white.withValues(alpha: 0.9),
                  fontWeight: FontWeight.w500,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
