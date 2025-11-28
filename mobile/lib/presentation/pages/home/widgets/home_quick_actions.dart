/// Home Quick Actions - Organism
///
/// Grid de accesos rápidos a funcionalidades principales.
/// Atomic Design: Organism
///
/// Presentation Layer - Organisms
library;

import 'package:flutter/material.dart';

import '../../../../core/routes/app_router.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../l10n/app_localizations.dart';
import '../../../widgets/molecules/action_tile.dart';

/// Grid de acciones rápidas del home
class HomeQuickActions extends StatelessWidget {
  const HomeQuickActions({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      mainAxisSpacing: AppSpacing.md,
      crossAxisSpacing: AppSpacing.md,
      childAspectRatio: 1.2,
      children: [
        // US-001: Captura de fotogramas
        ActionTile(
          icon: Icons.camera_alt,
          title: l10n.captureAction,
          subtitle: l10n.captureSubtitle,
          color: AppColors.primary,
          onTap: () => AppRouter.push(context, AppRoutes.capture),
        ),

        // US-002: Estimación de peso
        ActionTile(
          icon: Icons.monitor_weight,
          title: l10n.estimateAction,
          subtitle: l10n.estimateSubtitle,
          color: AppColors.secondary,
          onTap: () => AppRouter.push(
            context,
            AppRoutes.weightEstimation,
            arguments: {'framePath': '/mock/frame.jpg', 'cattleId': null},
          ),
        ),

        // US-003: Registro de ganado
        ActionTile(
          icon: Icons.add_circle,
          title: l10n.registerAction,
          subtitle: l10n.registerSubtitle,
          color: AppColors.accent,
          onTap: () => AppRouter.push(context, AppRoutes.cattleRegistration),
        ),

        // US-004: Historial de peso
        ActionTile(
          icon: Icons.history,
          title: l10n.historyAction,
          subtitle: l10n.historySubtitle,
          color: AppColors.info,
          onTap: () => AppRouter.push(context, AppRoutes.weightHistory),
        ),
      ],
    );
  }
}
