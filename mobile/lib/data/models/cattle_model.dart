/// Model: CattleModel
///
/// Modelo de datos para Cattle con serialización JSON y SQLite.
/// Single Responsibility: Serialización de datos de ganado.
///
/// Data Layer - Clean Architecture
library;

import '../../core/constants/breeds.dart';
import '../../domain/entities/cattle.dart';

/// Modelo de Cattle con serialización
class CattleModel extends Cattle {
  const CattleModel({
    required super.id,
    required super.earTag,
    super.name,
    required super.breed,
    required super.birthDate,
    required super.gender,
    super.color,
    super.birthWeight,
    super.motherId,
    super.fatherId,
    super.observations,
    super.status,
    required super.registrationDate,
    required super.lastUpdated,
    super.photoPath,
  });

  /// Crea un modelo desde una entidad
  factory CattleModel.fromEntity(Cattle cattle) {
    return CattleModel(
      id: cattle.id,
      earTag: cattle.earTag,
      name: cattle.name,
      breed: cattle.breed,
      birthDate: cattle.birthDate,
      gender: cattle.gender,
      color: cattle.color,
      birthWeight: cattle.birthWeight,
      motherId: cattle.motherId,
      fatherId: cattle.fatherId,
      observations: cattle.observations,
      status: cattle.status,
      registrationDate: cattle.registrationDate,
      lastUpdated: cattle.lastUpdated,
      photoPath: cattle.photoPath,
    );
  }

  /// Crea un modelo desde JSON
  factory CattleModel.fromJson(Map<String, dynamic> json) {
    return CattleModel(
      id: json['id'] as String,
      earTag: json['ear_tag'] as String,
      name: json['name'] as String?,
      breed: BreedType.fromValue(json['breed'] as String),
      birthDate: DateTime.parse(json['birth_date'] as String),
      gender: GenderExtension.fromValue(json['gender'] as String),
      color: json['color'] as String?,
      birthWeight: json['birth_weight'] != null
          ? (json['birth_weight'] as num).toDouble()
          : null,
      motherId: json['mother_id'] as String?,
      fatherId: json['father_id'] as String?,
      observations: json['observations'] as String?,
      status: CattleStatusExtension.fromValue(json['status'] as String),
      registrationDate: DateTime.parse(json['registration_date'] as String),
      lastUpdated: DateTime.parse(json['last_updated'] as String),
      photoPath: json['photo_path'] as String?,
    );
  }

  /// Convierte el modelo a JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'ear_tag': earTag,
      'name': name,
      'breed': breed.value,
      'birth_date': birthDate.toIso8601String(),
      'gender': gender.value,
      'color': color,
      'birth_weight': birthWeight,
      'mother_id': motherId,
      'father_id': fatherId,
      'observations': observations,
      'status': status.value,
      'registration_date': registrationDate.toIso8601String(),
      'last_updated': lastUpdated.toIso8601String(),
      'photo_path': photoPath,
    };
  }

  /// Crea un modelo desde SQLite Map
  factory CattleModel.fromSQLite(Map<String, dynamic> map) {
    return CattleModel(
      id: map['id'] as String,
      earTag: map['ear_tag'] as String,
      name: map['name'] as String?,
      breed: BreedType.fromValue(map['breed'] as String),
      birthDate: DateTime.fromMillisecondsSinceEpoch(map['birth_date'] as int),
      gender: GenderExtension.fromValue(map['gender'] as String),
      color: map['color'] as String?,
      birthWeight: map['birth_weight'] != null
          ? (map['birth_weight'] as num).toDouble()
          : null,
      motherId: map['mother_id'] as String?,
      fatherId: map['father_id'] as String?,
      observations: map['observations'] as String?,
      status: CattleStatusExtension.fromValue(map['status'] as String),
      registrationDate: DateTime.fromMillisecondsSinceEpoch(
        map['registration_date'] as int,
      ),
      lastUpdated: DateTime.fromMillisecondsSinceEpoch(
        map['last_updated'] as int,
      ),
      photoPath: map['photo_path'] as String?,
    );
  }

  /// Convierte el modelo a SQLite Map
  Map<String, dynamic> toSQLite() {
    return {
      'id': id,
      'ear_tag': earTag,
      'name': name,
      'breed': breed.value,
      'birth_date': birthDate.millisecondsSinceEpoch,
      'gender': gender.value,
      'color': color,
      'birth_weight': birthWeight,
      'mother_id': motherId,
      'father_id': fatherId,
      'observations': observations,
      'status': status.value,
      'registration_date': registrationDate.millisecondsSinceEpoch,
      'last_updated': lastUpdated.millisecondsSinceEpoch,
      'photo_path': photoPath,
    };
  }

  @override
  CattleModel copyWith({
    String? id,
    String? earTag,
    String? name,
    BreedType? breed,
    DateTime? birthDate,
    Gender? gender,
    String? color,
    double? birthWeight,
    String? motherId,
    String? fatherId,
    String? observations,
    CattleStatus? status,
    DateTime? registrationDate,
    DateTime? lastUpdated,
    String? photoPath,
  }) {
    return CattleModel(
      id: id ?? this.id,
      earTag: earTag ?? this.earTag,
      name: name ?? this.name,
      breed: breed ?? this.breed,
      birthDate: birthDate ?? this.birthDate,
      gender: gender ?? this.gender,
      color: color ?? this.color,
      birthWeight: birthWeight ?? this.birthWeight,
      motherId: motherId ?? this.motherId,
      fatherId: fatherId ?? this.fatherId,
      observations: observations ?? this.observations,
      status: status ?? this.status,
      registrationDate: registrationDate ?? this.registrationDate,
      lastUpdated: lastUpdated ?? this.lastUpdated,
      photoPath: photoPath ?? this.photoPath,
    );
  }
}
