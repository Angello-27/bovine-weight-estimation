/// Page: SyncStatusPage
///
/// US-005: Sincronización Offline
///
/// Página de estado y control de sincronización offline-first.
/// Composición pura siguiendo Atomic Design 100%.
///
/// Presentation Layer - Clean Architecture
library;

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_spacing.dart';
import '../../providers/sync_provider.dart';
import '../../widgets/atoms/sync_button.dart';
import '../../widgets/atoms/sync_status_indicator.dart';
import '../../widgets/molecules/sync_progress_card.dart';

/// Página de estado de sincronización
class SyncStatusPage extends StatelessWidget {
  const SyncStatusPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Estado de Sincronización'),
        backgroundColor: AppColors.primary,
        foregroundColor: Colors.white,
      ),
      body: Consumer<SyncProvider>(
        builder: (context, syncProvider, child) {
          return RefreshIndicator(
            onRefresh: () => syncProvider.refreshPendingCount(),
            child: SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: const EdgeInsets.all(AppSpacing.md),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Indicador de estado principal
                  _buildMainStatusCard(context, syncProvider),

                  const SizedBox(height: AppSpacing.md),

                  // Card de progreso
                  SyncProgressCard(
                    syncResult: syncProvider.lastSyncResult,
                    pendingCount: syncProvider.pendingCount,
                    lastSyncTime: syncProvider.lastSyncTime,
                  ),

                  const SizedBox(height: AppSpacing.md),

                  // Botón de sincronización manual
                  SyncButton(
                    onPressed: syncProvider.isOffline
                        ? null
                        : () => syncProvider.triggerManualSync(),
                    isLoading: syncProvider.isSyncing,
                  ),

                  const SizedBox(height: AppSpacing.lg),

                  // Info adicional
                  _buildInfoSection(context, syncProvider),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildMainStatusCard(BuildContext context, SyncProvider syncProvider) {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [AppColors.primary.withValues(alpha: 0.1), Colors.white],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
        border: Border.all(
          color: AppColors.primary.withValues(alpha: 0.2),
          width: 1.0,
        ),
      ),
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        children: [
          // Indicador principal
          SyncStatusIndicator(
            status: syncProvider.syncState.name,
            label: syncProvider.stateText,
            size: 16.0,
          ),

          const SizedBox(height: AppSpacing.md),

          // Texto detallado
          Text(
            syncProvider.detailedStatusText,
            textAlign: TextAlign.center,
            style: Theme.of(
              context,
            ).textTheme.bodyMedium?.copyWith(color: Colors.grey.shade700),
          ),

          // Mensaje de error si existe
          if (syncProvider.hasError && syncProvider.errorMessage != null) ...[
            const SizedBox(height: AppSpacing.sm),
            Container(
              padding: const EdgeInsets.all(AppSpacing.sm),
              decoration: BoxDecoration(
                color: Colors.orange.shade50,
                borderRadius: BorderRadius.circular(
                  AppSpacing.borderRadiusSmall,
                ),
                border: Border.all(color: Colors.orange.shade200, width: 1.0),
              ),
              child: Row(
                children: [
                  Icon(
                    Icons.info_outline_rounded,
                    size: 18,
                    color: Colors.orange.shade700,
                  ),
                  const SizedBox(width: AppSpacing.sm),
                  Expanded(
                    child: Text(
                      syncProvider.errorMessage!,
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.orange.shade900,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildInfoSection(BuildContext context, SyncProvider syncProvider) {
    return Card(
      elevation: AppSpacing.elevationLow,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusMedium),
      ),
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.md),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Información',
              style: Theme.of(
                context,
              ).textTheme.titleSmall?.copyWith(fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: AppSpacing.sm),
            _buildInfoRow(
              icon: Icons.wifi_rounded,
              label: 'Conectividad',
              value: syncProvider.isConnected ? 'Online' : 'Offline',
              valueColor: syncProvider.isConnected
                  ? AppColors.primary
                  : Colors.red.shade600,
            ),
            const Divider(height: AppSpacing.md),
            _buildInfoRow(
              icon: Icons.schedule_rounded,
              label: 'Items pendientes',
              value: '${syncProvider.pendingCount}',
              valueColor: syncProvider.pendingCount > 0
                  ? Colors.amber.shade700
                  : AppColors.primary,
            ),
            const Divider(height: AppSpacing.md),
            _buildInfoRow(
              icon: Icons.sync_rounded,
              label: 'Sincronización automática',
              value: 'Activa',
              valueColor: AppColors.primary,
            ),
            const SizedBox(height: AppSpacing.sm),
            Text(
              'La sincronización se ejecuta automáticamente cada 60 segundos '
              'cuando hay conexión y items pendientes.',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                color: Colors.grey.shade600,
                fontSize: 11,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoRow({
    required IconData icon,
    required String label,
    required String value,
    required Color valueColor,
  }) {
    return Row(
      children: [
        Icon(icon, size: 20, color: Colors.grey.shade600),
        const SizedBox(width: AppSpacing.sm),
        Text(
          label,
          style: TextStyle(fontSize: 14, color: Colors.grey.shade700),
        ),
        const Spacer(),
        Text(
          value,
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
            color: valueColor,
          ),
        ),
      ],
    );
  }
}
