/// Model: CaptureSessionModel
/// 
/// Modelo de datos para CaptureSession con serialización JSON y SQLite.
/// Extiende la entidad CaptureSession del dominio.
///
/// Data Layer - Clean Architecture
library;

import '../../domain/entities/capture_session.dart';
import '../../domain/entities/frame.dart';
import 'frame_model.dart';

/// Modelo de CaptureSession con serialización
class CaptureSessionModel extends CaptureSession {
  const CaptureSessionModel({
    required super.id,
    required super.startTime,
    super.endTime,
    required super.frames,
    required super.status,
    super.selectedFrame,
    super.targetFps,
    super.targetDurationSeconds,
  });

  /// Crea un CaptureSessionModel desde una entidad CaptureSession
  factory CaptureSessionModel.fromEntity(CaptureSession session) {
    return CaptureSessionModel(
      id: session.id,
      startTime: session.startTime,
      endTime: session.endTime,
      frames: session.frames,
      status: session.status,
      selectedFrame: session.selectedFrame,
      targetFps: session.targetFps,
      targetDurationSeconds: session.targetDurationSeconds,
    );
  }

  /// Crea un CaptureSessionModel desde JSON
  factory CaptureSessionModel.fromJson(Map<String, dynamic> json) {
    return CaptureSessionModel(
      id: json['id'] as String,
      startTime: DateTime.parse(json['start_time'] as String),
      endTime: json['end_time'] != null
          ? DateTime.parse(json['end_time'] as String)
          : null,
      frames: (json['frames'] as List<dynamic>)
          .map((frameJson) =>
              FrameModel.fromJson(frameJson as Map<String, dynamic>))
          .toList(),
      status: CaptureSessionStatus.values.firstWhere(
        (status) => status.name == json['status'],
      ),
      selectedFrame: json['selected_frame'] != null
          ? FrameModel.fromJson(json['selected_frame'] as Map<String, dynamic>)
          : null,
      targetFps: json['target_fps'] as int? ?? 12,
      targetDurationSeconds: json['target_duration_seconds'] as int? ?? 4,
    );
  }

  /// Convierte el modelo a JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'start_time': startTime.toIso8601String(),
      'end_time': endTime?.toIso8601String(),
      'frames': frames
          .map((frame) => FrameModel.fromEntity(frame).toJson())
          .toList(),
      'status': status.name,
      'selected_frame': selectedFrame != null
          ? FrameModel.fromEntity(selectedFrame!).toJson()
          : null,
      'target_fps': targetFps,
      'target_duration_seconds': targetDurationSeconds,
    };
  }

  /// Crea un CaptureSessionModel desde SQLite Map
  factory CaptureSessionModel.fromSQLite(Map<String, dynamic> map) {
    return CaptureSessionModel(
      id: map['id'] as String,
      startTime: DateTime.fromMillisecondsSinceEpoch(map['start_time'] as int),
      endTime: map['end_time'] != null
          ? DateTime.fromMillisecondsSinceEpoch(map['end_time'] as int)
          : null,
      frames: const [], // Los frames se cargan por separado con JOIN
      status: CaptureSessionStatus.values.firstWhere(
        (status) => status.name == map['status'],
      ),
      selectedFrame: null, // Se carga por separado si existe
      targetFps: map['target_fps'] as int,
      targetDurationSeconds: map['target_duration_seconds'] as int,
    );
  }

  /// Convierte el modelo a SQLite Map
  Map<String, dynamic> toSQLite() {
    return {
      'id': id,
      'start_time': startTime.millisecondsSinceEpoch,
      'end_time': endTime?.millisecondsSinceEpoch,
      'status': status.name,
      'selected_frame_id': selectedFrame?.id,
      'target_fps': targetFps,
      'target_duration_seconds': targetDurationSeconds,
    };
  }

  @override
  CaptureSessionModel copyWith({
    String? id,
    DateTime? startTime,
    DateTime? endTime,
    List<Frame>? frames,
    CaptureSessionStatus? status,
    Frame? selectedFrame,
    int? targetFps,
    int? targetDurationSeconds,
  }) {
    return CaptureSessionModel(
      id: id ?? this.id,
      startTime: startTime ?? this.startTime,
      endTime: endTime ?? this.endTime,
      frames: frames ?? this.frames,
      status: status ?? this.status,
      selectedFrame: selectedFrame ?? this.selectedFrame,
      targetFps: targetFps ?? this.targetFps,
      targetDurationSeconds: targetDurationSeconds ?? this.targetDurationSeconds,
    );
  }

  @override
  String toString() => 'CaptureSessionModel(${super.toString()})';
}

