/// Sync Result Localizer
///
/// Helper para localizar mensajes de SyncResult.
/// Single Responsibility: Convertir mensajes de SyncResult a texto localizado.
///
/// Presentation Layer - Utils
library;

import 'package:flutter/material.dart';

import '../../../../domain/entities/sync_result.dart';
import '../../../../l10n/app_localizations.dart';

/// Helper para localizar mensajes de SyncResult
class SyncResultLocalizer {
  /// Obtiene el mensaje localizado de un SyncResult
  static String getLocalizedMessage(BuildContext context, SyncResult result) {
    final localizations = AppLocalizations.of(context)!;

    // Si el resultado tiene un mensaje personalizado, usarlo
    // (pero normalmente los mensajes vienen hardcodeados del dominio)
    // Por ahora, generamos mensajes localizados basados en el estado

    if (result.totalItems == 0) {
      return localizations.syncResultEmpty;
    }

    if (result.isCompleteSuccess) {
      return localizations.syncResultSuccess(result.syncedCount);
    }

    if (result.conflictCount > 0) {
      return localizations.syncResultConflicts(
        result.conflictCount,
        result.syncedCount,
      );
    }

    if (result.failedCount > 0) {
      return localizations.syncResultPartial(
        result.syncedCount,
        result.totalItems,
        result.failedCount,
      );
    }

    // Fallback
    return localizations.syncResultSuccess(result.syncedCount);
  }

  /// Obtiene el resumen corto localizado de un SyncResult
  static String getLocalizedShortSummary(
    BuildContext context,
    SyncResult result,
  ) {
    final localizations = AppLocalizations.of(context)!;

    if (result.totalItems == 0) {
      return localizations.syncResultNoChanges;
    }

    if (result.isCompleteSuccess) {
      return localizations.syncResultSynced(result.syncedCount);
    }

    if (result.isPartialSync) {
      return localizations.syncResultPartialSummary(
        result.syncedCount,
        result.totalItems,
      );
    }

    return localizations.syncResultError(result.failedCount);
  }
}
