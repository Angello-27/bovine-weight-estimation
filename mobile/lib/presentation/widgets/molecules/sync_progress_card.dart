/// Molecule: SyncProgressCard
///
/// Card con progreso y estadísticas de sincronización.
/// Single Responsibility: Mostrar detalle de última sincronización.
///
/// Atomic Design - Presentation Layer
library;

import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../../domain/entities/sync_result.dart';
import '../../../l10n/app_localizations.dart';
import '../../pages/sync/utils/sync_result_localizer.dart';

/// Card de progreso de sincronización
class SyncProgressCard extends StatelessWidget {
  /// Resultado de sincronización
  final SyncResult? syncResult;

  /// Items pendientes
  final int pendingCount;

  /// Timestamp de última sincronización
  final DateTime? lastSyncTime;

  const SyncProgressCard({
    super.key,
    this.syncResult,
    required this.pendingCount,
    this.lastSyncTime,
  });

  @override
  Widget build(BuildContext context) {
    final hasResult = syncResult != null;

    return Card(
      elevation: AppSpacing.elevationMedium,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
      ),
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.md),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  AppLocalizations.of(context)!.syncStatusTitle,
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
                ),
                if (lastSyncTime != null)
                  Text(
                    _formatLastSyncTime(context, lastSyncTime!),
                    style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      color: Colors.grey.shade600,
                    ),
                  ),
              ],
            ),
            const SizedBox(height: AppSpacing.md),

            // Estadísticas
            if (hasResult) ...[
              _buildStatRow(
                context: context,
                icon: Icons.check_circle_outline_rounded,
                label: AppLocalizations.of(context)!.synced,
                value: '${syncResult!.syncedCount}',
                color: AppColors.primary,
              ),
              const SizedBox(height: AppSpacing.sm),
              _buildStatRow(
                context: context,
                icon: Icons.schedule_rounded,
                label: AppLocalizations.of(context)!.pending,
                value: '$pendingCount',
                color: Colors.grey.shade600,
              ),
              if (syncResult!.failedCount > 0) ...[
                const SizedBox(height: AppSpacing.sm),
                _buildStatRow(
                  context: context,
                  icon: Icons.error_outline_rounded,
                  label: AppLocalizations.of(context)!.errors,
                  value: '${syncResult!.failedCount}',
                  color: Colors.orange.shade700,
                ),
              ],
              if (syncResult!.conflictCount > 0) ...[
                const SizedBox(height: AppSpacing.sm),
                _buildStatRow(
                  context: context,
                  icon: Icons.warning_amber_rounded,
                  label: AppLocalizations.of(context)!.conflicts,
                  value: '${syncResult!.conflictCount}',
                  color: Colors.amber.shade700,
                ),
              ],
              const SizedBox(height: AppSpacing.md),

              // Barra de progreso
              ClipRRect(
                borderRadius: BorderRadius.circular(
                  AppSpacing.borderRadiusSmall,
                ),
                child: LinearProgressIndicator(
                  value: syncResult!.successRate / 100,
                  minHeight: 8.0,
                  backgroundColor: Colors.grey.shade200,
                  valueColor: AlwaysStoppedAnimation<Color>(
                    syncResult!.isCompleteSuccess
                        ? AppColors.primary
                        : Colors.orange.shade600,
                  ),
                ),
              ),
              const SizedBox(height: AppSpacing.sm),

              // Mensaje localizado
              Text(
                SyncResultLocalizer.getLocalizedMessage(context, syncResult!),
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  color: Colors.grey.shade700,
                  fontStyle: FontStyle.italic,
                ),
              ),
            ] else ...[
              Center(
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: AppSpacing.lg),
                  child: Column(
                    children: [
                      Icon(
                        Icons.cloud_off_rounded,
                        size: 48,
                        color: Colors.grey.shade400,
                      ),
                      const SizedBox(height: AppSpacing.sm),
                      Text(
                        AppLocalizations.of(context)!.noSyncHistory,
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: Colors.grey.shade600,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildStatRow({
    required IconData icon,
    required String label,
    required String value,
    required Color color,
    required BuildContext context,
  }) {
    return Row(
      children: [
        Icon(icon, size: 20, color: color),
        const SizedBox(width: AppSpacing.sm),
        Text(
          label,
          style: Theme.of(
            context,
          ).textTheme.bodyMedium?.copyWith(color: Colors.grey.shade700),
        ),
        const Spacer(),
        Text(
          value,
          style: Theme.of(context).textTheme.bodyLarge?.copyWith(
            fontWeight: FontWeight.w600,
            color: color,
          ),
        ),
      ],
    );
  }

  String _formatLastSyncTime(BuildContext context, DateTime time) {
    final now = DateTime.now();
    final diff = now.difference(time);
    final localizations = AppLocalizations.of(context)!;

    if (diff.inMinutes < 1) {
      return localizations.agoSeconds;
    } else if (diff.inMinutes < 60) {
      return localizations.agoMinutes(diff.inMinutes);
    } else if (diff.inHours < 24) {
      return localizations.agoHours(diff.inHours);
    } else {
      return localizations.agoDays(diff.inDays);
    }
  }
}
