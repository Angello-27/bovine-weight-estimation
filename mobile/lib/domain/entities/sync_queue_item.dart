/// Entity: SyncQueueItem
///
/// Item en la cola de sincronización.
/// Single Responsibility: Representar un item pendiente de sincronizar.
///
/// Domain Layer - Clean Architecture
library;

import 'sync_status.dart';

/// Item en la cola de sincronización
class SyncQueueItem {
  /// ID único del item en la cola
  final String id;

  /// Tipo de entidad a sincronizar
  final SyncEntityType entityType;

  /// ID de la entidad a sincronizar
  final String entityId;

  /// Operación a realizar
  final SyncOperation operation;

  /// Datos de la entidad (JSON serializado)
  final String data;

  /// Estado actual de sincronización
  final SyncStatus status;

  /// Número de reintentos realizados
  final int retryCount;

  /// Fecha del último reintento
  final DateTime? lastRetryAt;

  /// Fecha de creación del item
  final DateTime createdAt;

  /// Último mensaje de error (si existe)
  final String? errorMessage;

  const SyncQueueItem({
    required this.id,
    required this.entityType,
    required this.entityId,
    required this.operation,
    required this.data,
    this.status = SyncStatus.pending,
    this.retryCount = 0,
    this.lastRetryAt,
    required this.createdAt,
    this.errorMessage,
  });

  /// Crea una copia con campos modificados
  SyncQueueItem copyWith({
    String? id,
    SyncEntityType? entityType,
    String? entityId,
    SyncOperation? operation,
    String? data,
    SyncStatus? status,
    int? retryCount,
    DateTime? lastRetryAt,
    DateTime? createdAt,
    String? errorMessage,
  }) {
    return SyncQueueItem(
      id: id ?? this.id,
      entityType: entityType ?? this.entityType,
      entityId: entityId ?? this.entityId,
      operation: operation ?? this.operation,
      data: data ?? this.data,
      status: status ?? this.status,
      retryCount: retryCount ?? this.retryCount,
      lastRetryAt: lastRetryAt ?? this.lastRetryAt,
      createdAt: createdAt ?? this.createdAt,
      errorMessage: errorMessage ?? this.errorMessage,
    );
  }

  /// Calcula el tiempo de espera antes del próximo reintento (backoff exponencial)
  ///
  /// Estrategia según US-005:
  /// - Intento 0: inmediato
  /// - Intento 1: 5 segundos
  /// - Intento 2: 15 segundos
  /// - Intento 3: 30 segundos
  /// - Intento 4: 1 minuto
  /// - Intento 5+: 5 minutos
  Duration get nextRetryDelay {
    switch (retryCount) {
      case 0:
        return Duration.zero;
      case 1:
        return const Duration(seconds: 5);
      case 2:
        return const Duration(seconds: 15);
      case 3:
        return const Duration(seconds: 30);
      case 4:
        return const Duration(minutes: 1);
      default:
        return const Duration(minutes: 5);
    }
  }

  /// Indica si debe reintentar ahora
  bool get shouldRetry {
    if (status != SyncStatus.error) return false;
    if (lastRetryAt == null) return true;

    final timeSinceLastRetry = DateTime.now().difference(lastRetryAt!);
    return timeSinceLastRetry >= nextRetryDelay;
  }

  /// Indica si alcanzó el límite de reintentos
  bool get hasExceededRetryLimit => retryCount >= 10;

  /// Prioridad del item (menor número = mayor prioridad)
  ///
  /// Criterios:
  /// - create > update > delete
  /// - cattle > weightEstimation > frame
  /// - más antiguo > más reciente
  int get priority {
    int operationPriority = operation == SyncOperation.create
        ? 0
        : operation == SyncOperation.update
        ? 10
        : 20;

    int entityPriority = entityType == SyncEntityType.cattle
        ? 0
        : entityType == SyncEntityType.weightEstimation
        ? 3
        : 6;

    return operationPriority + entityPriority;
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is SyncQueueItem &&
        other.id == id &&
        other.entityType == entityType &&
        other.entityId == entityId &&
        other.operation == operation;
  }

  @override
  int get hashCode {
    return id.hashCode ^
        entityType.hashCode ^
        entityId.hashCode ^
        operation.hashCode;
  }

  @override
  String toString() {
    return 'SyncQueueItem(id: $id, entityType: ${entityType.name}, '
        'entityId: $entityId, operation: ${operation.name}, '
        'status: ${status.name}, retryCount: $retryCount)';
  }
}
