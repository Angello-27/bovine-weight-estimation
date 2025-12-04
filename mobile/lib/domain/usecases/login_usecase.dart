/// UseCase: LoginUseCase
///
/// Caso de uso para autenticación de usuario.
/// Autentica un usuario con username y password, guarda la sesión y retorna el usuario.
///
/// Domain Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../entities/user.dart';
import '../repositories/auth_repository.dart';

/// Caso de uso para login
class LoginUseCase implements UseCase<User, LoginParams> {
  final AuthRepository repository;

  LoginUseCase(this.repository);

  /// Ejecuta el login
  ///
  /// Parámetros:
  /// - [params]: Credenciales (username, password)
  ///
  /// Retorna:
  /// - [Right(User)]: Usuario autenticado
  /// - [Left(Failure)]: Error de autenticación
  @override
  Future<Either<Failure, User>> call(LoginParams params) async {
    return await repository.login(
      username: params.username,
      password: params.password,
    );
  }
}

/// Parámetros para login
class LoginParams {
  final String username;
  final String password;

  const LoginParams({required this.username, required this.password});
}
