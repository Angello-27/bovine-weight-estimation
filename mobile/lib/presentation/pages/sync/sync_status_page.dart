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
import '../../widgets/molecules/sync_progress_card.dart';
import 'widgets/sync_main_status_card.dart';
import 'widgets/sync_info_card.dart';

/// Página de estado de sincronización
class SyncStatusPage extends StatelessWidget {
  const SyncStatusPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Estado de Sincronización'),
        flexibleSpace: Container(
          decoration: const BoxDecoration(color: AppColors.primary),
        ),
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
                  SyncMainStatusCard(syncProvider: syncProvider),

                  const SizedBox(height: AppSpacing.lg),

                  // Card de progreso
                  SyncProgressCard(
                    syncResult: syncProvider.lastSyncResult,
                    pendingCount: syncProvider.pendingCount,
                    lastSyncTime: syncProvider.lastSyncTime,
                  ),

                  const SizedBox(height: AppSpacing.lg),

                  // Botón de sincronización manual
                  SyncButton(
                    onPressed: syncProvider.isOffline
                        ? null
                        : () => syncProvider.triggerManualSync(),
                    isLoading: syncProvider.isSyncing,
                  ),

                  const SizedBox(height: AppSpacing.lg),

                  // Info adicional
                  SyncInfoCard(syncProvider: syncProvider),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
