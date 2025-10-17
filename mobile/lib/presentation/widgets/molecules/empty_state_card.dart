/// Molecule: EmptyStateCard
///
/// Card de estado vacío con ícono y mensaje.
/// Single Responsibility: Mostrar estado vacío consistente.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';

/// Card de estado vacío
class EmptyStateCard extends StatelessWidget {
  /// Ícono a mostrar
  final IconData icon;

  /// Título
  final String title;

  /// Mensaje descriptivo
  final String message;

  const EmptyStateCard({
    required this.icon,
    required this.title,
    required this.message,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.screenPadding),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(AppSpacing.xl),
              decoration: BoxDecoration(
                color: AppColors.grey200,
                borderRadius: BorderRadius.circular(
                  AppSpacing.borderRadiusLarge,
                ),
              ),
              child: Icon(
                icon,
                size: AppSpacing.iconSizeXXLarge * 1.5,
                color: AppColors.grey500,
              ),
            ),
            const SizedBox(height: AppSpacing.lg),
            Text(title, style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: AppSpacing.sm),
            Text(
              message,
              style: const TextStyle(color: AppColors.grey600),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
