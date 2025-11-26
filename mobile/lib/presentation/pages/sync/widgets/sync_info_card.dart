/// Sync Info Card - Molecule
///
/// Card que muestra información detallada sobre el estado de sincronización.
/// Incluye conectividad, items pendientes y configuración automática.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../providers/sync_provider.dart';
import 'sync_info_row.dart';

/// Card de información de sincronización
class SyncInfoCard extends StatelessWidget {
  final SyncProvider syncProvider;

  const SyncInfoCard({required this.syncProvider, super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: AppSpacing.elevationLow,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      ),
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.lg),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Título
            Row(
              children: [
                Icon(
                  Icons.info_outline_rounded,
                  size: 20,
                  color: AppColors.primary,
                ),
                const SizedBox(width: AppSpacing.sm),
                Text(
                  'Información',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: Theme.of(context).colorScheme.onSurface,
                  ),
                ),
              ],
            ),

            const SizedBox(height: AppSpacing.md),

            // Conectividad
            SyncInfoRow(
              icon: Icons.wifi_rounded,
              label: 'Conectividad',
              value: syncProvider.isConnected ? 'Online' : 'Offline',
              valueColor: syncProvider.isConnected
                  ? AppColors.success
                  : AppColors.error,
            ),

            const Divider(height: AppSpacing.xl),

            // Items pendientes
            SyncInfoRow(
              icon: Icons.schedule_rounded,
              label: 'Items pendientes',
              value: '${syncProvider.pendingCount}',
              valueColor: syncProvider.pendingCount > 0
                  ? AppColors.warning
                  : AppColors.success,
            ),

            const Divider(height: AppSpacing.xl),

            // Sincronización automática
            SyncInfoRow(
              icon: Icons.sync_rounded,
              label: 'Sincronización automática',
              value: 'Activa',
              valueColor: AppColors.primary,
            ),

            const SizedBox(height: AppSpacing.md),

            // Descripción
            Container(
              padding: const EdgeInsets.all(AppSpacing.md),
              decoration: BoxDecoration(
                color: AppColors.primary.withValues(alpha: 0.05),
                borderRadius: BorderRadius.circular(
                  AppSpacing.borderRadiusMedium,
                ),
                border: Border.all(
                  color: AppColors.primary.withValues(alpha: 0.1),
                  width: 1,
                ),
              ),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Icon(
                    Icons.lightbulb_outline_rounded,
                    size: 18,
                    color: AppColors.primary,
                  ),
                  const SizedBox(width: AppSpacing.sm),
                  Expanded(
                    child: Text(
                      'La sincronización se ejecuta automáticamente cada 60 segundos '
                      'cuando hay conexión y items pendientes.',
                      style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: Theme.of(
                          context,
                        ).colorScheme.onSurface.withValues(alpha: 0.7),
                        height: 1.4,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
