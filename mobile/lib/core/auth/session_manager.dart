/// Session Manager
///
/// Gestiona la sesión del usuario y tokens JWT.
/// Almacena tokens de forma segura usando flutter_secure_storage.
///
/// Core Auth Layer
library;

import 'dart:convert';
import 'package:flutter/foundation.dart';
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
    try {
      await Future.wait([
        _storage.write(key: _accessTokenKey, value: accessToken),
        _storage.write(key: _userDataKey, value: jsonEncode(userData)),
        if (refreshToken != null)
          _storage.write(key: _refreshTokenKey, value: refreshToken),
      ]);
      // Verificar que se guardó correctamente
      final savedToken = await getAccessToken();
      final savedUserData = await getUserData();
      if (savedToken != null && savedUserData != null) {
        debugPrint(
          '✅ Sesión guardada correctamente: ${savedUserData['username']}',
        );
      } else {
        debugPrint('⚠️ Error: Sesión no se guardó correctamente');
      }
    } catch (e) {
      debugPrint('❌ Error al guardar sesión: $e');
      rethrow;
    }
  }

  /// Obtiene el token de acceso actual
  Future<String?> getAccessToken() async {
    return await _storage.read(key: _accessTokenKey);
  }

  /// Obtiene los datos del usuario actual
  Future<Map<String, dynamic>?> getUserData() async {
    try {
      final userDataStr = await _storage.read(key: _userDataKey);
      if (userDataStr == null) {
        debugPrint('⚠️ No hay datos de usuario guardados');
        return null;
      }

      try {
        final userData = jsonDecode(userDataStr) as Map<String, dynamic>;
        debugPrint('✅ Datos de usuario cargados: ${userData['username']}');
        return userData;
      } catch (e) {
        debugPrint('❌ Error al decodificar datos de usuario: $e');
        return null;
      }
    } catch (e) {
      debugPrint('❌ Error al leer datos de usuario: $e');
      return null;
    }
  }

  /// Verifica si hay una sesión activa
  Future<bool> hasSession() async {
    try {
      final token = await getAccessToken();
      final hasToken = token != null && token.isNotEmpty;
      debugPrint(
        '🔍 Verificando sesión: ${hasToken ? "✅ Token encontrado" : "❌ No hay token"}',
      );
      return hasToken;
    } catch (e) {
      debugPrint('❌ Error al verificar sesión: $e');
      return false;
    }
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
