/// Entity: SyncStatus
///
/// Estado de sincronización de una entidad.
/// Single Responsibility: Representar estado de sync en arquitectura offline-first.
///
/// Domain Layer - Clean Architecture
library;

/// Estado de sincronización de una entidad
enum SyncStatus {
  /// No sincronizado (cambios locales pendientes)
  pending,

  /// En proceso de sincronización
  syncing,

  /// Sincronizado exitosamente con backend
  synced,

  /// Error al sincronizar (requiere reintento)
  error,

  /// Conflicto detectado (requiere resolución)
  conflict;

  /// Crea desde string (para deserialización desde SQLite)
  static SyncStatus fromString(String value) {
    return SyncStatus.values.firstWhere(
      (status) => status.name == value,
      orElse: () => SyncStatus.pending,
    );
  }

  /// Convierte a string (para serialización a SQLite)
  String toSqlite() => name;

  /// Indica si requiere acción (no sincronizado completamente)
  bool get requiresAction =>
      this == SyncStatus.pending ||
      this == SyncStatus.error ||
      this == SyncStatus.conflict;

  /// Indica si está en un estado final exitoso
  bool get isSynced => this == SyncStatus.synced;

  /// Indica si hay un problema que requiere atención
  bool get hasIssue => this == SyncStatus.error || this == SyncStatus.conflict;
}

/// Tipo de operación de sincronización
enum SyncOperation {
  /// Crear nueva entidad en backend
  create,

  /// Actualizar entidad existente en backend
  update,

  /// Eliminar entidad en backend
  delete;

  /// Crea desde string
  static SyncOperation fromString(String value) {
    return SyncOperation.values.firstWhere(
      (op) => op.name == value,
      orElse: () => SyncOperation.create,
    );
  }

  /// Convierte a string
  String toSqlite() => name;
}

/// Tipo de entidad sincronizable
enum SyncEntityType {
  /// Animal registrado
  cattle,

  /// Estimación de peso
  weightEstimation,

  /// Fotograma capturado
  frame;

  /// Crea desde string
  static SyncEntityType fromString(String value) {
    return SyncEntityType.values.firstWhere(
      (type) => type.name == value,
      orElse: () => SyncEntityType.cattle,
    );
  }

  /// Convierte a string
  String toSqlite() => name;

  /// Nombre legible para UI
  String get displayName {
    switch (this) {
      case SyncEntityType.cattle:
        return 'Animal';
      case SyncEntityType.weightEstimation:
        return 'Pesaje';
      case SyncEntityType.frame:
        return 'Fotograma';
    }
  }

  /// Nombre plural para UI
  String get displayNamePlural {
    switch (this) {
      case SyncEntityType.cattle:
        return 'Animales';
      case SyncEntityType.weightEstimation:
        return 'Pesajes';
      case SyncEntityType.frame:
        return 'Fotogramas';
    }
  }
}
