/// Entity: SyncResult
///
/// Resultado de una operación de sincronización.
/// Single Responsibility: Representar resultado de sync con métricas y errores.
///
/// Domain Layer - Clean Architecture
library;

import 'sync_queue_item.dart';
import 'sync_status.dart';

/// Resultado de una operación de sincronización
class SyncResult {
  /// Indica si la sincronización fue exitosa
  final bool success;

  /// Total de items procesados
  final int totalItems;

  /// Items sincronizados exitosamente
  final int syncedCount;

  /// Items con error
  final int failedCount;

  /// Items con conflicto detectado
  final int conflictCount;

  /// Duración de la sincronización
  final Duration duration;

  /// Timestamp de inicio de la sincronización
  final DateTime startedAt;

  /// Timestamp de finalización de la sincronización
  final DateTime completedAt;

  /// Lista de items que fallaron (para detalle en UI)
  final List<SyncQueueItem> failedItems;

  /// Lista de items con conflicto (para resolución manual)
  final List<SyncQueueItem> conflictItems;

  /// Mensaje general de resultado
  final String? message;

  /// Detalles de errores específicos
  final List<String> errors;

  const SyncResult({
    required this.success,
    required this.totalItems,
    required this.syncedCount,
    required this.failedCount,
    required this.conflictCount,
    required this.duration,
    required this.startedAt,
    required this.completedAt,
    this.failedItems = const [],
    this.conflictItems = const [],
    this.message,
    this.errors = const [],
  });

  /// Crea un resultado exitoso
  factory SyncResult.success({
    required int totalItems,
    required int syncedCount,
    required Duration duration,
    required DateTime startedAt,
    required DateTime completedAt,
    String? message,
  }) {
    return SyncResult(
      success: true,
      totalItems: totalItems,
      syncedCount: syncedCount,
      failedCount: 0,
      conflictCount: 0,
      duration: duration,
      startedAt: startedAt,
      completedAt: completedAt,
      message: message ?? '$syncedCount items sincronizados exitosamente',
    );
  }

  /// Crea un resultado con errores
  factory SyncResult.withErrors({
    required int totalItems,
    required int syncedCount,
    required int failedCount,
    required Duration duration,
    required DateTime startedAt,
    required DateTime completedAt,
    List<SyncQueueItem> failedItems = const [],
    List<String> errors = const [],
    String? message,
  }) {
    return SyncResult(
      success: false,
      totalItems: totalItems,
      syncedCount: syncedCount,
      failedCount: failedCount,
      conflictCount: 0,
      duration: duration,
      startedAt: startedAt,
      completedAt: completedAt,
      failedItems: failedItems,
      message:
          message ??
          '$syncedCount de $totalItems sincronizados. $failedCount errores.',
      errors: errors,
    );
  }

  /// Crea un resultado con conflictos
  factory SyncResult.withConflicts({
    required int totalItems,
    required int syncedCount,
    required int conflictCount,
    required Duration duration,
    required DateTime startedAt,
    required DateTime completedAt,
    List<SyncQueueItem> conflictItems = const [],
    String? message,
  }) {
    return SyncResult(
      success: false,
      totalItems: totalItems,
      syncedCount: syncedCount,
      failedCount: 0,
      conflictCount: conflictCount,
      duration: duration,
      startedAt: startedAt,
      completedAt: completedAt,
      conflictItems: conflictItems,
      message:
          message ??
          '$conflictCount conflictos detectados. $syncedCount sincronizados.',
    );
  }

  /// Crea un resultado vacío (sin items para sincronizar)
  factory SyncResult.empty({DateTime? startedAt, DateTime? completedAt}) {
    final start = startedAt ?? DateTime.now();
    final complete = completedAt ?? DateTime.now();

    return SyncResult(
      success: true,
      totalItems: 0,
      syncedCount: 0,
      failedCount: 0,
      conflictCount: 0,
      duration: complete.difference(start),
      startedAt: start,
      completedAt: complete,
      message: 'No hay items pendientes de sincronización',
    );
  }

  /// Porcentaje de éxito (0-100)
  double get successRate {
    if (totalItems == 0) return 100.0;
    return (syncedCount / totalItems) * 100;
  }

  /// Indica si hay items pendientes (errores o conflictos)
  bool get hasPendingItems => failedCount > 0 || conflictCount > 0;

  /// Indica si la sincronización fue parcial
  bool get isPartialSync => syncedCount > 0 && hasPendingItems;

  /// Indica si fue una sincronización completa y exitosa
  bool get isCompleteSuccess => success && syncedCount == totalItems;

  /// Resumen corto para UI
  String get shortSummary {
    if (totalItems == 0) return 'Sin cambios';
    if (isCompleteSuccess) return '$syncedCount sincronizados';
    if (isPartialSync) {
      return '$syncedCount de $totalItems sincronizados';
    }
    return 'Error: $failedCount fallidos';
  }

  /// Resumen detallado para logs
  String get detailedSummary {
    final buffer = StringBuffer();
    buffer.writeln('Sincronización completada en ${duration.inSeconds}s');
    buffer.writeln('Total items: $totalItems');
    buffer.writeln('✓ Sincronizados: $syncedCount');
    if (failedCount > 0) {
      buffer.writeln('✗ Errores: $failedCount');
    }
    if (conflictCount > 0) {
      buffer.writeln('⚠ Conflictos: $conflictCount');
    }
    buffer.writeln('Tasa de éxito: ${successRate.toStringAsFixed(1)}%');
    return buffer.toString();
  }

  /// Agrupa items fallidos por tipo de entidad
  Map<SyncEntityType, List<SyncQueueItem>> get failedItemsByType {
    final map = <SyncEntityType, List<SyncQueueItem>>{};
    for (final item in failedItems) {
      map.putIfAbsent(item.entityType, () => []).add(item);
    }
    return map;
  }

  @override
  String toString() {
    return 'SyncResult(success: $success, totalItems: $totalItems, '
        'syncedCount: $syncedCount, failedCount: $failedCount, '
        'conflictCount: $conflictCount, duration: ${duration.inSeconds}s)';
  }
}
