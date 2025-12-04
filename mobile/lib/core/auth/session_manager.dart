/// Session Manager
///
/// Gestiona la sesión del usuario y tokens JWT.
/// Almacena tokens de forma segura usando flutter_secure_storage.
///
/// Core Auth Layer
library;

import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// Gestor de sesión de usuario
class SessionManager {
  final FlutterSecureStorage _storage;

  // Keys para almacenamiento
  static const String _accessTokenKey = 'access_token';
  static const String _userDataKey = 'user_data';
  static const String _refreshTokenKey =
      'refresh_token'; // Para futuras implementaciones

  SessionManager({FlutterSecureStorage? storage})
    : _storage =
          storage ??
          const FlutterSecureStorage(
            aOptions: AndroidOptions(encryptedSharedPreferences: true),
            iOptions: IOSOptions(
              accessibility: KeychainAccessibility.first_unlock_this_device,
            ),
          );

  /// Guarda la sesión del usuario después del login
  Future<void> saveSession({
    required String accessToken,
    required Map<String, dynamic> userData,
    String? refreshToken,
  }) async {
    await Future.wait([
      _storage.write(key: _accessTokenKey, value: accessToken),
      _storage.write(key: _userDataKey, value: jsonEncode(userData)),
      if (refreshToken != null)
        _storage.write(key: _refreshTokenKey, value: refreshToken),
    ]);
  }

  /// Obtiene el token de acceso actual
  Future<String?> getAccessToken() async {
    return await _storage.read(key: _accessTokenKey);
  }

  /// Obtiene los datos del usuario actual
  Future<Map<String, dynamic>?> getUserData() async {
    final userDataStr = await _storage.read(key: _userDataKey);
    if (userDataStr == null) return null;

    try {
      return jsonDecode(userDataStr) as Map<String, dynamic>;
    } catch (e) {
      return null;
    }
  }

  /// Verifica si hay una sesión activa
  Future<bool> hasSession() async {
    final token = await getAccessToken();
    return token != null && token.isNotEmpty;
  }

  /// Limpia la sesión (logout)
  Future<void> clearSession() async {
    await Future.wait([
      _storage.delete(key: _accessTokenKey),
      _storage.delete(key: _userDataKey),
      _storage.delete(key: _refreshTokenKey),
    ]);
  }

  /// Obtiene el refresh token (para futuras implementaciones)
  Future<String?> getRefreshToken() async {
    return await _storage.read(key: _refreshTokenKey);
  }
}
