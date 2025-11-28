/// Sync Main Status Card - Molecule
///
/// Card principal que muestra el estado de sincronización.
/// Incluye indicador de estado, texto descriptivo y banner de error opcional.
///
/// Presentation Layer - Molecules
library;

import 'package:flutter/material.dart';

import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_spacing.dart';
import '../../../../l10n/app_localizations.dart';
import '../../../providers/sync_provider.dart';
import '../../../widgets/atoms/sync_status_indicator.dart';
import '../utils/sync_result_localizer.dart';
import 'sync_error_banner.dart';

/// Card principal de estado de sincronización
class SyncMainStatusCard extends StatelessWidget {
  final SyncProvider syncProvider;

  const SyncMainStatusCard({required this.syncProvider, super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: AppSpacing.elevationMedium,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
      ),
      child: Container(
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.surface,
          borderRadius: BorderRadius.circular(AppSpacing.borderRadiusLarge),
          border: Border.all(
            color: AppColors.primary.withValues(alpha: 0.15),
            width: 1.5,
          ),
        ),
        padding: const EdgeInsets.all(AppSpacing.xl),
        child: Column(
          children: [
            // Indicador principal de estado
            SyncStatusIndicator(
              status: syncProvider.syncState.name,
              label: _getStateText(context, syncProvider),
              size: 20.0,
            ),

            const SizedBox(height: AppSpacing.lg),

            // Texto detallado del estado
            Text(
              _getDetailedStatusText(context, syncProvider),
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                color: Theme.of(
                  context,
                ).colorScheme.onSurface.withValues(alpha: 0.8),
                height: 1.5,
              ),
            ),

            // Banner de error si existe
            if (syncProvider.hasError && syncProvider.errorMessage != null) ...[
              const SizedBox(height: AppSpacing.md),
              SyncErrorBanner(message: syncProvider.errorMessage!),
            ],
          ],
        ),
      ),
    );
  }

  /// Obtiene el texto del estado localizado
  String _getStateText(BuildContext context, SyncProvider provider) {
    final localizations = AppLocalizations.of(context)!;
    switch (provider.syncState) {
      case GlobalSyncState.offline:
        return localizations.noConnection;
      case GlobalSyncState.syncing:
        return localizations.syncing;
      case GlobalSyncState.synced:
        return localizations.syncedStatus;
      case GlobalSyncState.error:
        return localizations.syncError;
      case GlobalSyncState.idle:
        return provider.pendingCount > 0
            ? localizations.pendingCount(provider.pendingCount)
            : localizations.allSynced;
    }
  }

  /// Obtiene el texto detallado del estado localizado
  String _getDetailedStatusText(BuildContext context, SyncProvider provider) {
    final localizations = AppLocalizations.of(context)!;
    if (provider.lastSyncResult != null) {
      // Usar el helper para localizar el mensaje
      return SyncResultLocalizer.getLocalizedMessage(
        context,
        provider.lastSyncResult!,
      );
    }
    if (provider.errorMessage != null) {
      return provider.errorMessage!;
    }
    if (provider.pendingCount > 0) {
      return localizations.itemsWaitingSync(provider.pendingCount);
    }
    return localizations.noPendingChanges;
  }
}
