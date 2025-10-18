/// Model: SyncBatchRequestModel
///
/// DTO para requests de sincronización batch al backend.
/// Mapea a CattleSyncBatchRequest y WeightEstimationSyncBatchRequest del backend.
///
/// Data Layer - Clean Architecture
library;

/// Request batch para sincronización de ganado
class CattleSyncBatchRequestModel {
  final List<CattleSyncItemModel> items;
  final String deviceId;
  final DateTime syncTimestamp;

  const CattleSyncBatchRequestModel({
    required this.items,
    required this.deviceId,
    required this.syncTimestamp,
  });

  Map<String, dynamic> toJson() => {
    'items': items.map((item) => item.toJson()).toList(),
    'device_id': deviceId,
    'sync_timestamp': syncTimestamp.toUtc().toIso8601String(),
  };
}

/// Item individual de ganado para sincronizar
class CattleSyncItemModel {
  final String id;
  final String earTag;
  final String? name;
  final String breed;
  final DateTime birthDate;
  final String gender;
  final String? color;
  final double? birthWeight;
  final String? motherId;
  final String? fatherId;
  final String? observations;
  final String status;
  final DateTime registrationDate;
  final DateTime lastUpdated;
  final String? photoPath;
  final String operation;

  const CattleSyncItemModel({
    required this.id,
    required this.earTag,
    this.name,
    required this.breed,
    required this.birthDate,
    required this.gender,
    this.color,
    this.birthWeight,
    this.motherId,
    this.fatherId,
    this.observations,
    required this.status,
    required this.registrationDate,
    required this.lastUpdated,
    this.photoPath,
    required this.operation,
  });

  Map<String, dynamic> toJson() => {
    'id': id,
    'ear_tag': earTag,
    if (name != null) 'name': name,
    'breed': breed.toLowerCase(),
    'birth_date': birthDate.toUtc().toIso8601String(),
    'gender': gender.toLowerCase(),
    if (color != null) 'color': color,
    if (birthWeight != null) 'birth_weight': birthWeight,
    if (motherId != null) 'mother_id': motherId,
    if (fatherId != null) 'father_id': fatherId,
    if (observations != null) 'observations': observations,
    'status': status.toLowerCase(),
    'registration_date': registrationDate.toUtc().toIso8601String(),
    'last_updated': lastUpdated.toUtc().toIso8601String(),
    if (photoPath != null) 'photo_path': photoPath,
    'operation': operation.toLowerCase(),
  };
}

/// Request batch para sincronización de estimaciones
class WeightEstimationSyncBatchRequestModel {
  final List<WeightEstimationSyncItemModel> items;
  final String deviceId;
  final DateTime syncTimestamp;

  const WeightEstimationSyncBatchRequestModel({
    required this.items,
    required this.deviceId,
    required this.syncTimestamp,
  });

  Map<String, dynamic> toJson() => {
    'items': items.map((item) => item.toJson()).toList(),
    'device_id': deviceId,
    'sync_timestamp': syncTimestamp.toUtc().toIso8601String(),
  };
}

/// Item individual de estimación para sincronizar
class WeightEstimationSyncItemModel {
  final String id;
  final String? cattleId;
  final String breed;
  final double estimatedWeight;
  final double confidenceScore;
  final String frameImagePath;
  final DateTime timestamp;
  final double? gpsLatitude;
  final double? gpsLongitude;
  final String method;
  final String modelVersion;
  final int processingTimeMs;
  final String operation;

  const WeightEstimationSyncItemModel({
    required this.id,
    this.cattleId,
    required this.breed,
    required this.estimatedWeight,
    required this.confidenceScore,
    required this.frameImagePath,
    required this.timestamp,
    this.gpsLatitude,
    this.gpsLongitude,
    required this.method,
    required this.modelVersion,
    required this.processingTimeMs,
    required this.operation,
  });

  Map<String, dynamic> toJson() => {
    'id': id,
    if (cattleId != null) 'cattle_id': cattleId,
    'breed': breed.toLowerCase(),
    'estimated_weight': estimatedWeight,
    'confidence_score': confidenceScore,
    'frame_image_path': frameImagePath,
    'timestamp': timestamp.toUtc().toIso8601String(),
    if (gpsLatitude != null) 'gps_latitude': gpsLatitude,
    if (gpsLongitude != null) 'gps_longitude': gpsLongitude,
    'method': method.toLowerCase(),
    'model_version': modelVersion,
    'processing_time_ms': processingTimeMs,
    'operation': operation.toLowerCase(),
  };
}

/// Response batch del backend
class SyncBatchResponseModel {
  final bool success;
  final int totalItems;
  final int syncedCount;
  final int failedCount;
  final int conflictCount;
  final List<SyncItemResponseModel> results;
  final DateTime syncTimestamp;
  final String message;

  const SyncBatchResponseModel({
    required this.success,
    required this.totalItems,
    required this.syncedCount,
    required this.failedCount,
    required this.conflictCount,
    required this.results,
    required this.syncTimestamp,
    required this.message,
  });

  factory SyncBatchResponseModel.fromJson(Map<String, dynamic> json) {
    return SyncBatchResponseModel(
      success: json['success'] as bool,
      totalItems: json['total_items'] as int,
      syncedCount: json['synced_count'] as int,
      failedCount: json['failed_count'] as int,
      conflictCount: json['conflict_count'] as int,
      results: (json['results'] as List)
          .map((item) => SyncItemResponseModel.fromJson(item))
          .toList(),
      syncTimestamp: DateTime.parse(json['sync_timestamp'] as String),
      message: json['message'] as String,
    );
  }
}

/// Response individual por item
class SyncItemResponseModel {
  final String id;
  final String status;
  final String? message;
  final Map<String, dynamic>? conflictData;
  final DateTime syncedAt;

  const SyncItemResponseModel({
    required this.id,
    required this.status,
    this.message,
    this.conflictData,
    required this.syncedAt,
  });

  factory SyncItemResponseModel.fromJson(Map<String, dynamic> json) {
    return SyncItemResponseModel(
      id: json['id'] as String,
      status: json['status'] as String,
      message: json['message'] as String?,
      conflictData: json['conflict_data'] as Map<String, dynamic>?,
      syncedAt: DateTime.parse(json['synced_at'] as String),
    );
  }
}

/// Health check response
class HealthCheckResponseModel {
  final String status;
  final String database;
  final DateTime timestamp;
  final String version;

  const HealthCheckResponseModel({
    required this.status,
    required this.database,
    required this.timestamp,
    required this.version,
  });

  factory HealthCheckResponseModel.fromJson(Map<String, dynamic> json) {
    return HealthCheckResponseModel(
      status: json['status'] as String,
      database: json['database'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      version: json['version'] as String,
    );
  }

  bool get isOnline => status.toLowerCase() == 'online';
}
