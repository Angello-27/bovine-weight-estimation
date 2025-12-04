/// Provider: AuthProvider
///
/// State management para autenticación.
/// Gestiona login, logout y estado de sesión.
///
/// Presentation Layer - Providers
library;

import 'package:flutter/foundation.dart';

import '../../core/errors/failures.dart';
import '../../core/usecases/usecase.dart';
import '../../domain/entities/user.dart';
import '../../domain/usecases/get_current_user_usecase.dart';
import '../../domain/usecases/has_session_usecase.dart';
import '../../domain/usecases/login_usecase.dart';
import '../../domain/usecases/logout_usecase.dart';

/// Provider para autenticación
class AuthProvider extends ChangeNotifier {
  final LoginUseCase loginUseCase;
  final HasSessionUseCase hasSessionUseCase;
  final GetCurrentUserUseCase getCurrentUserUseCase;
  final LogoutUseCase logoutUseCase;

  User? _currentUser;
  bool _isLoading = false;
  Failure? _error;

  AuthProvider({
    required this.loginUseCase,
    required this.hasSessionUseCase,
    required this.getCurrentUserUseCase,
    required this.logoutUseCase,
  });

  /// Usuario actual
  User? get currentUser => _currentUser;

  /// Estado de carga
  bool get isLoading => _isLoading;

  /// Error actual
  Failure? get error => _error;

  /// Verifica si hay una sesión activa
  bool get isAuthenticated => _currentUser != null;

  /// Inicializa el provider (verifica sesión existente)
  /// [silent] si es true, no llama a notifyListeners() para evitar rebuilds durante la inicialización
  Future<void> initialize({bool silent = false}) async {
    _isLoading = true;
    if (!silent) {
      notifyListeners();
    }

    try {
      final hasSessionResult = await hasSessionUseCase(const NoParams());
      hasSessionResult.fold(
        (failure) {
          _error = failure;
          _currentUser = null;
        },
        (hasSession) async {
          if (hasSession) {
            final userResult = await getCurrentUserUseCase(const NoParams());
            userResult.fold(
              (failure) {
                _error = failure;
                _currentUser = null;
              },
              (user) {
                _currentUser = user;
                _error = null;
              },
            );
          } else {
            _currentUser = null;
            _error = null;
          }
        },
      );
    } catch (e) {
      _error = ServerFailure(message: 'Error al inicializar: $e');
      _currentUser = null;
    } finally {
      _isLoading = false;
      if (!silent) {
        notifyListeners();
      }
    }
  }

  /// Inicia sesión
  Future<bool> login({
    required String username,
    required String password,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final result = await loginUseCase(
        LoginParams(username: username, password: password),
      );

      return result.fold(
        (failure) {
          _error = failure;
          _currentUser = null;
          _isLoading = false;
          notifyListeners();
          return false;
        },
        (user) {
          _currentUser = user;
          _error = null;
          _isLoading = false;
          notifyListeners();
          return true;
        },
      );
    } catch (e) {
      _error = ServerFailure(message: 'Error inesperado: $e');
      _currentUser = null;
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  /// Cierra sesión
  Future<void> logout() async {
    _isLoading = true;
    notifyListeners();

    try {
      final result = await logoutUseCase(const NoParams());
      result.fold(
        (failure) {
          _error = failure;
        },
        (_) {
          _currentUser = null;
          _error = null;
        },
      );
    } catch (e) {
      _error = ServerFailure(message: 'Error al cerrar sesión: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Limpia el error
  void clearError() {
    _error = null;
    notifyListeners();
  }
}
