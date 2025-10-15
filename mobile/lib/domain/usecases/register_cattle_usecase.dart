/// UseCase: RegisterCattleUseCase
/// 
/// US-003: Registro Automático de Animales
/// 
/// Caso de uso para registrar un nuevo animal con validaciones de negocio.
/// Single Responsibility: Lógica de registro con validaciones.
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/constants/age_categories.dart';
import '../../core/constants/breeds.dart';
import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/cattle.dart';
import '../repositories/cattle_repository.dart';

/// Caso de uso para registro de ganado (US-003)
class RegisterCattleUseCase implements UseCase<Cattle, RegisterCattleParams> {
  final CattleRepository repository;

  RegisterCattleUseCase(this.repository);

  /// Ejecuta el registro de un animal
  /// 
  /// Proceso:
  /// 1. Validar campos obligatorios
  /// 2. Verificar que la caravana no esté duplicada
  /// 3. Validar fecha de nacimiento (no futura)
  /// 4. Registrar animal en SQLite
  /// 
  /// Parámetros:
  /// - [params]: Datos del animal a registrar
  /// 
  /// Retorna:
  /// - [Right(Cattle)]: Animal registrado exitosamente
  /// - [Left(Failure)]: Error durante el registro
  @override
  Future<Either<Failure, Cattle>> call(RegisterCattleParams params) async {
    // 1. Validar campos obligatorios
    final validation = _validateParams(params);
    if (validation != null) {
      return Left(ValidationFailure(message: validation));
    }

    // 2. Verificar que la caravana no exista
    final existsResult = await repository.earTagExists(params.earTag);

    final exists = existsResult.fold(
      (failure) => false,
      (exists) => exists,
    );

    if (exists) {
      return const Left(ValidationFailure(
        message: 'El número de caravana ya existe en el sistema',
      ));
    }

    // 3. Crear entidad Cattle
    final cattle = Cattle(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      earTag: params.earTag,
      name: params.name,
      breed: params.breed,
      birthDate: params.birthDate,
      gender: params.gender,
      color: params.color,
      birthWeight: params.birthWeight,
      motherId: params.motherId,
      fatherId: params.fatherId,
      observations: params.observations,
      status: CattleStatus.active,
      registrationDate: DateTime.now(),
      lastUpdated: DateTime.now(),
      photoPath: params.photoPath,
    );

    // 4. Registrar en repositorio
    return repository.registerCattle(cattle);
  }

  /// Valida los parámetros de registro
  String? _validateParams(RegisterCattleParams params) {
    // Caravana obligatoria
    if (params.earTag.trim().isEmpty) {
      return 'El número de caravana es obligatorio';
    }

    // Caravana con formato válido (alfanumérico)
    final earTagRegex = RegExp(r'^[A-Za-z0-9\-]+$');
    if (!earTagRegex.hasMatch(params.earTag)) {
      return 'Número de caravana inválido (solo alfanumérico y guiones)';
    }

    // Fecha de nacimiento no futura
    if (params.birthDate.isAfter(DateTime.now())) {
      return 'La fecha de nacimiento no puede ser futura';
    }

    // Fecha de nacimiento razonable (no más de 20 años atrás)
    final twentyYearsAgo = DateTime.now().subtract(const Duration(days: 365 * 20));
    if (params.birthDate.isBefore(twentyYearsAgo)) {
      return 'La fecha de nacimiento es demasiado antigua';
    }

    // Peso al nacer razonable (si se proporciona)
    if (params.birthWeight != null) {
      if (params.birthWeight! < 10 || params.birthWeight! > 100) {
        return 'Peso al nacer debe estar entre 10-100 kg';
      }
    }

    return null; // Sin errores
  }
}

/// Parámetros para registro de ganado
class RegisterCattleParams {
  /// Número de caravana (obligatorio, único)
  final String earTag;

  /// Nombre del animal (opcional)
  final String? name;

  /// Raza (obligatorio)
  final BreedType breed;

  /// Fecha de nacimiento (obligatorio)
  final DateTime birthDate;

  /// Género (obligatorio)
  final Gender gender;

  /// Color del pelaje (opcional)
  final String? color;

  /// Peso al nacer en kg (opcional)
  final double? birthWeight;

  /// ID de la madre (opcional)
  final String? motherId;

  /// ID del padre (opcional)
  final String? fatherId;

  /// Observaciones (opcional)
  final String? observations;

  /// Foto del animal (opcional)
  final String? photoPath;

  const RegisterCattleParams({
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
    this.photoPath,
  });

  @override
  String toString() => 'RegisterCattleParams(earTag: $earTag, breed: ${breed.displayName})';
}

