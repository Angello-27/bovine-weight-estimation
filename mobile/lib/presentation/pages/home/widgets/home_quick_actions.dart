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
import '../../../widgets/molecules/action_tile.dart';

/// Grid de acciones rápidas del home
class HomeQuickActions extends StatelessWidget {
  const HomeQuickActions({super.key});

  @override
  Widget build(BuildContext context) {
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
          title: 'Capturar',
          subtitle: 'Fotogramas',
          gradient: AppColors.primaryGradient,
          onTap: () => AppRouter.push(context, AppRoutes.capture),
        ),

        // US-002: Estimación de peso
        ActionTile(
          icon: Icons.monitor_weight,
          title: 'Estimar',
          subtitle: 'Peso IA',
          gradient: AppColors.secondaryGradient,
          onTap: () => AppRouter.push(
            context,
            AppRoutes.weightEstimation,
            arguments: {
              'framePath': '/mock/frame.jpg',
              'cattleId': null,
            },
          ),
        ),

        // US-003: Registro de ganado
        ActionTile(
          icon: Icons.add_circle,
          title: 'Registrar',
          subtitle: 'Animal',
          gradient: AppColors.accentGradient,
          onTap: () => AppRouter.push(context, AppRoutes.cattleRegistration),
        ),

        // US-004: Historial de peso
        ActionTile(
          icon: Icons.history,
          title: 'Historial',
          subtitle: 'Pesajes',
          gradient: AppColors.infoGradient,
          onTap: () => AppRouter.push(context, AppRoutes.weightHistory),
        ),
      ],
    );
  }
}

