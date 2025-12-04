/// Repository Interface: AuthRepository
///
/// Contrato para operaciones de autenticación.
/// Single Responsibility: Definir operaciones de autenticación.
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../entities/user.dart';

/// Repositorio para autenticación
abstract class AuthRepository {
  /// Autentica un usuario con username y password
  ///
  /// Parámetros:
  /// - [username]: Nombre de usuario
  /// - [password]: Contraseña
  ///
  /// Retorna:
  /// - [Right(User)]: Usuario autenticado
  /// - [Left(Failure)]: Error de autenticación (credenciales inválidas, red, etc.)
  Future<Either<Failure, User>> login({
    required String username,
    required String password,
  });

  /// Cierra la sesión del usuario actual
  ///
  /// Retorna:
  /// - [Right(void)]: Sesión cerrada exitosamente
  /// - [Left(Failure)]: Error al cerrar sesión
  Future<Either<Failure, void>> logout();

  /// Verifica si hay una sesión activa
  ///
  /// Retorna:
  /// - [Right(bool)]: true si hay sesión activa, false si no
  /// - [Left(Failure)]: Error al verificar sesión
  Future<Either<Failure, bool>> hasSession();

  /// Obtiene el usuario actual de la sesión
  ///
  /// Retorna:
  /// - [Right(User?)]: Usuario actual o null si no hay sesión
  /// - [Left(Failure)]: Error al obtener usuario
  Future<Either<Failure, User?>> getCurrentUser();
}
