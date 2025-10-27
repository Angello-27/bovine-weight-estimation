/// Home Header - Organism
///
/// Header con gradiente que muestra nombre de la app y sincronización.
/// Atomic Design: Organism (componente complejo con estado)
///
/// Presentation Layer - Organisms
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../core/config/app_config.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../core/routes/app_router.dart';
import '../../../providers/sync_provider.dart';
import 'home_stats.dart';

/// Header principal del home con indicador de sincronización
class HomeHeader extends StatelessWidget {
  const HomeHeader({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: const BoxDecoration(
        gradient: AppColors.primaryGradient,
        borderRadius: BorderRadius.only(
          bottomLeft: Radius.circular(AppSpacing.borderRadiusXLarge),
          bottomRight: Radius.circular(AppSpacing.borderRadiusXLarge),
        ),
      ),
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Título con logo + indicador de sincronización
          Row(
            children: [
              _buildLogo(),
              const SizedBox(width: AppSpacing.md),
              Expanded(child: _buildTitle()),
              _buildSyncIndicator(context),
            ],
          ),

          const SizedBox(height: AppSpacing.lg),

          // Estadísticas rápidas
          const HomeStats(),
        ],
      ),
    );
  }

  /// Logo de la aplicación
  Widget _buildLogo() {
    return Container(
      padding: const EdgeInsets.all(AppSpacing.sm),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.2),
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
      ),
      child: const Icon(
        Icons.pets,
        color: Colors.white,
        size: AppSpacing.iconSizeLarge,
      ),
    );
  }

  /// Título y subtítulo
  Widget _buildTitle() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Agrocom',
          style: TextStyle(
            color: Colors.white,
            fontSize: AppSpacing.fontSizeLarge,
            fontWeight: FontWeight.bold,
          ),
        ),
        Text(
          AppConfig.haciendaName,
          style: TextStyle(
            color: Colors.white.withValues(alpha: 0.9),
            fontSize: AppSpacing.fontSizeMedium,
          ),
        ),
      ],
    );
  }

  /// Indicador de sincronización interactivo
  Widget _buildSyncIndicator(BuildContext context) {
    return Consumer<SyncProvider>(
      builder: (context, syncProvider, _) {
        return GestureDetector(
          onTap: () => AppRouter.push(context, AppRoutes.sync),
          child: Container(
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.sm,
              vertical: AppSpacing.xs,
            ),
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.2),
              borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  syncProvider.isSyncing
                      ? Icons.sync_rounded
                      : syncProvider.isOffline
                      ? Icons.cloud_off_rounded
                      : Icons.cloud_done_rounded,
                  color: Colors.white,
                  size: 16,
                ),
                if (syncProvider.hasPendingItems) ...[
                  const SizedBox(width: 4),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 6,
                      vertical: 2,
                    ),
                    decoration: BoxDecoration(
                      color: Colors.amber.shade600,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      '${syncProvider.pendingCount}',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 10,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),
        );
      },
    );
  }
}
