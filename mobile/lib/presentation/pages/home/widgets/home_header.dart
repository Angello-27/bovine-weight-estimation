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
      decoration: BoxDecoration(
        color: AppColors.primary,
        borderRadius: const BorderRadius.only(
          bottomLeft: Radius.circular(AppSpacing.borderRadiusXLarge),
          bottomRight: Radius.circular(AppSpacing.borderRadiusXLarge),
        ),
        boxShadow: [
          BoxShadow(
            color: AppColors.primary.withValues(alpha: 0.3),
            blurRadius: 20,
            offset: const Offset(0, 4),
          ),
        ],
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
      padding: const EdgeInsets.all(AppSpacing.md),
      decoration: BoxDecoration(
        color: AppColors.accent,
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.2),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: const Icon(
        Icons.pets,
        color: AppColors.onAccent,
        size: AppSpacing.iconSizeXLarge,
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
        final isOnline = !syncProvider.isOffline;
        final hasPending = syncProvider.hasPendingItems;
        final isSyncing = syncProvider.isSyncing;

        return GestureDetector(
          onTap: () => AppRouter.push(context, AppRoutes.sync),
          child: Container(
            padding: const EdgeInsets.symmetric(
              horizontal: AppSpacing.md,
              vertical: AppSpacing.sm,
            ),
            decoration: BoxDecoration(
              color: isOnline
                  ? AppColors.success.withValues(alpha: 0.2)
                  : AppColors.error.withValues(alpha: 0.2),
              borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
              border: Border.all(
                color: isOnline ? AppColors.success : AppColors.error,
                width: 1.5,
              ),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                if (isSyncing)
                  const SizedBox(
                    width: 16,
                    height: 16,
                    child: CircularProgressIndicator(
                      strokeWidth: 2,
                      valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                    ),
                  )
                else
                  Icon(
                    isOnline
                        ? Icons.cloud_done_rounded
                        : Icons.cloud_off_rounded,
                    color: Colors.white,
                    size: 18,
                  ),
                if (hasPending) ...[
                  const SizedBox(width: AppSpacing.xs),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 6,
                      vertical: 2,
                    ),
                    decoration: BoxDecoration(
                      color: AppColors.accent,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      '${syncProvider.pendingCount}',
                      style: const TextStyle(
                        color: AppColors.onAccent,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
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
