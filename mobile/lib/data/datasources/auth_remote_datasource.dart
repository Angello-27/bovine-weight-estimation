/// DataSource: AuthRemoteDataSource
///
/// DataSource para autenticación con backend via HTTP/REST.
/// Single Responsibility: Comunicación HTTP para operaciones de autenticación.
///
/// Data Layer - Clean Architecture
library;

import 'package:dio/dio.dart';

import '../../core/errors/exceptions.dart';
import '../../core/network/http_error_handler.dart';
import '../models/auth_models.dart';

/// DataSource para autenticación remota con backend
abstract class AuthRemoteDataSource {
  /// Autentica un usuario y obtiene token JWT
  ///
  /// Endpoint: POST /api/v1/auth/login
  Future<LoginResponseModel> login(LoginRequestModel request);
}

/// Implementación con Dio
class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final Dio dio;

  AuthRemoteDataSourceImpl({required this.dio});

  @override
  Future<LoginResponseModel> login(LoginRequestModel request) async {
    try {
      final response = await dio.post(
        '/api/v1/auth/login',
        data: request.toJson(),
      );

      if (response.statusCode == 200) {
        return LoginResponseModel.fromJson(response.data);
      } else {
        throw ServerException(
          message: 'Error al iniciar sesión: ${response.statusCode}',
          statusCode: response.statusCode,
        );
      }
    } on DioException catch (e) {
      throw HttpErrorHandler.handle(e);
    } catch (e) {
      if (e is AppException) {
        rethrow;
      }
      throw ServerException(message: 'Error inesperado al iniciar sesión: $e');
    }
  }
}
