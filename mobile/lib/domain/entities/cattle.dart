/// Entity: Cattle (Ganado)
/// 
/// Representa un animal bovino registrado en el sistema.
/// Single Responsibility: Modelar datos de un animal con reglas de negocio.
///
/// Domain Layer - Clean Architecture
library;

import 'package:equatable/equatable.dart';

import '../../core/constants/age_categories.dart';
import '../../core/constants/breeds.dart';

/// Animal bovino registrado
class Cattle extends Equatable {
  /// ID único del animal
  final String id;

  /// Número de caravana/arete (único, obligatorio)
  final String earTag;

  /// Nombre del animal (opcional)
  final String? name;

  /// Raza (una de las 7 exactas)
  final BreedType breed;

  /// Fecha de nacimiento
  final DateTime birthDate;

  /// Género del animal
  final Gender gender;

  /// Color del pelaje (opcional)
  final String? color;

  /// Peso al nacer en kg (opcional)
  final double? birthWeight;

  /// ID de la madre (opcional)
  final String? motherId;

  /// ID del padre (opcional)
  final String? fatherId;

  /// Observaciones adicionales (opcional)
  final String? observations;

  /// Estado actual del animal
  final CattleStatus status;

  /// Fecha de registro en el sistema
  final DateTime registrationDate;

  /// Última actualización
  final DateTime lastUpdated;

  /// Foto del animal (path local, opcional)
  final String? photoPath;

  const Cattle({
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
    this.status = CattleStatus.active,
    required this.registrationDate,
    required this.lastUpdated,
    this.photoPath,
  });

  /// Calcula la edad en meses
  int get ageInMonths {
    final now = DateTime.now();
    final difference = now.difference(birthDate);
    return (difference.inDays / 30).floor();
  }

  /// Calcula la categoría de edad automáticamente
  AgeCategory get ageCategory {
    return AgeCategory.fromAgeInMonths(ageInMonths);
  }

  /// Verifica si el animal está activo
  bool get isActive => status == CattleStatus.active;

  /// Obtiene el display name (caravana + nombre)
  String get displayName {
    if (name != null && name!.isNotEmpty) {
      return '$earTag - $name';
    }
    return earTag;
  }

  /// Copia el cattle con nuevos valores
  Cattle copyWith({
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
    return Cattle(
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

  @override
  List<Object?> get props => [
        id,
        earTag,
        name,
        breed,
        birthDate,
        gender,
        color,
        birthWeight,
        motherId,
        fatherId,
        observations,
        status,
        registrationDate,
        lastUpdated,
        photoPath,
      ];

  @override
  String toString() => 'Cattle(earTag: $earTag, name: $name, breed: ${breed.displayName})';
}

/// Género del animal
enum Gender {
  /// Macho
  male,

  /// Hembra
  female,
}

/// Extensión para Gender
extension GenderExtension on Gender {
  String get displayName {
    switch (this) {
      case Gender.male:
        return 'Macho';
      case Gender.female:
        return 'Hembra';
    }
  }

  String get value {
    switch (this) {
      case Gender.male:
        return 'male';
      case Gender.female:
        return 'female';
    }
  }

  static Gender fromValue(String value) {
    switch (value) {
      case 'male':
        return Gender.male;
      case 'female':
        return Gender.female;
      default:
        throw ArgumentError('Género inválido: $value');
    }
  }
}

/// Estado del animal
enum CattleStatus {
  /// Activo en el hato
  active,

  /// Inactivo (temporal)
  inactive,

  /// Vendido
  sold,

  /// Muerto
  deceased,
}

/// Extensión para CattleStatus
extension CattleStatusExtension on CattleStatus {
  String get displayName {
    switch (this) {
      case CattleStatus.active:
        return 'Activo';
      case CattleStatus.inactive:
        return 'Inactivo';
      case CattleStatus.sold:
        return 'Vendido';
      case CattleStatus.deceased:
        return 'Muerto';
    }
  }

  String get value {
    return name;
  }

  /// Color asociado al estado (según criterio US-003)
  String get colorHex {
    switch (this) {
      case CattleStatus.active:
        return '#4CAF50'; // Verde
      case CattleStatus.inactive:
        return '#9E9E9E'; // Gris
      case CattleStatus.sold:
        return '#2196F3'; // Azul
      case CattleStatus.deceased:
        return '#D32F2F'; // Rojo
    }
  }

  static CattleStatus fromValue(String value) {
    return CattleStatus.values.firstWhere(
      (status) => status.name == value,
      orElse: () => CattleStatus.active,
    );
  }
}

