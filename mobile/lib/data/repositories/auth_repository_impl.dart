/// Repository Implementation: AuthRepositoryImpl
///
/// Implementa operaciones de autenticación.
/// Coordina entre AuthRemoteDataSource y SessionManager.
///
/// Data Layer - Clean Architecture
library;

import 'package:dartz/dartz.dart';

import '../../core/auth/session_manager.dart';
import '../../core/errors/exceptions.dart';
import '../../core/errors/failures.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_remote_datasource.dart';
import '../models/auth_models.dart';

/// Implementación de AuthRepository
class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final SessionManager sessionManager;

  AuthRepositoryImpl({
    required this.remoteDataSource,
    required this.sessionManager,
  });

  @override
  Future<Either<Failure, User>> login({
    required String username,
    required String password,
  }) async {
    try {
      final request = LoginRequestModel(username: username, password: password);

      final response = await remoteDataSource.login(request);

      // Guardar sesión
      await sessionManager.saveSession(
        accessToken: response.accessToken,
        userData: response.toUserData(),
      );

      // Convertir a entidad User
      final user = _mapToUser(response);

      return Right(user);
    } on AuthException catch (e) {
      return Left(AuthFailure(message: e.message));
    } on NetworkException catch (e) {
      return Left(NetworkFailure(message: e.message));
    } on ServerException catch (e) {
      return Left(ServerFailure(message: e.message));
    } on AppException catch (e) {
      return Left(ServerFailure(message: e.message));
    } catch (e) {
      return Left(
        ServerFailure(message: 'Error inesperado al iniciar sesión: $e'),
      );
    }
  }

  @override
  Future<Either<Failure, void>> logout() async {
    try {
      await sessionManager.clearSession();
      return const Right(null);
    } catch (e) {
      return Left(ServerFailure(message: 'Error al cerrar sesión: $e'));
    }
  }

  @override
  Future<Either<Failure, bool>> hasSession() async {
    try {
      final hasSession = await sessionManager.hasSession();
      return Right(hasSession);
    } catch (e) {
      return Left(ServerFailure(message: 'Error al verificar sesión: $e'));
    }
  }

  @override
  Future<Either<Failure, User?>> getCurrentUser() async {
    try {
      final userData = await sessionManager.getUserData();
      if (userData == null) {
        return const Right(null);
      }

      final user = UserModel.fromJson(userData);
      return Right(_mapToUserFromModel(user));
    } catch (e) {
      return Left(ServerFailure(message: 'Error al obtener usuario: $e'));
    }
  }

  /// Mapea LoginResponseModel a User entity
  User _mapToUser(LoginResponseModel response) {
    return User(
      id: response.id,
      username: response.username,
      email: '', // El backend no devuelve email en el login
      role: UserRole(
        id: response.roleId,
        name: response.role,
        priority: response.rolePriority,
      ),
      roleId: response.roleId,
      farmId: response.farmId,
    );
  }

  /// Mapea UserModel a User entity
  User _mapToUserFromModel(UserModel model) {
    return User(
      id: model.id,
      username: model.username,
      email: '', // El backend no devuelve email en el login
      role: UserRole(
        id: model.roleId,
        name: model.role,
        priority: model.rolePriority,
      ),
      roleId: model.roleId,
      farmId: model.farmId,
    );
  }
}
