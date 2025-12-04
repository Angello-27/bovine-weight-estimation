/// Model: AuthModels
///
/// DTOs para autenticación (login request/response).
/// Mapea a los schemas del backend FastAPI.
///
/// Data Layer - Clean Architecture
library;

/// Request de login
class LoginRequestModel {
  final String username;
  final String password;

  const LoginRequestModel({required this.username, required this.password});

  Map<String, dynamic> toJson() => {'username': username, 'password': password};
}

/// Response de login
class LoginResponseModel {
  final String id;
  final String username;
  final String role; // Nombre del rol (string, no objeto)
  final String rolePriority; // Prioridad del rol
  final String roleId;
  final String? farmId;
  final String accessToken;
  final String tokenType;

  const LoginResponseModel({
    required this.id,
    required this.username,
    required this.role,
    required this.rolePriority,
    required this.roleId,
    this.farmId,
    required this.accessToken,
    this.tokenType = 'bearer',
  });

  factory LoginResponseModel.fromJson(Map<String, dynamic> json) {
    return LoginResponseModel(
      id: json['id'] as String,
      username: json['username'] as String,
      role: json['role'] as String,
      rolePriority: json['role_priority'] as String,
      roleId: json['role_id'] as String,
      farmId: json['farm_id'] as String?,
      accessToken: json['access_token'] as String,
      tokenType: json['token_type'] as String? ?? 'bearer',
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'username': username,
    'role': role,
    'role_priority': rolePriority,
    'role_id': roleId,
    if (farmId != null) 'farm_id': farmId,
    'access_token': accessToken,
    'token_type': tokenType,
  };

  /// Convierte a formato de datos de usuario para almacenamiento
  Map<String, dynamic> toUserData() => {
    'id': id,
    'username': username,
    'role': role,
    'role_priority': rolePriority,
    'role_id': roleId,
    if (farmId != null) 'farm_id': farmId,
  };
}

/// Modelo de rol
class RoleModel {
  final String id;
  final String name;
  final String priority;

  const RoleModel({
    required this.id,
    required this.name,
    required this.priority,
  });

  factory RoleModel.fromJson(Map<String, dynamic> json) {
    return RoleModel(
      id: json['id'] as String,
      name: json['name'] as String,
      priority: json['priority'] as String,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'priority': priority,
  };
}

/// Modelo de usuario (para uso en la app)
class UserModel {
  final String id;
  final String username;
  final String role; // Nombre del rol
  final String rolePriority; // Prioridad del rol
  final String roleId;
  final String? farmId;

  const UserModel({
    required this.id,
    required this.username,
    required this.role,
    required this.rolePriority,
    required this.roleId,
    this.farmId,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      username: json['username'] as String,
      role: json['role'] as String,
      rolePriority: json['role_priority'] as String,
      roleId: json['role_id'] as String,
      farmId: json['farm_id'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
    'id': id,
    'username': username,
    'role': role,
    'role_priority': rolePriority,
    'role_id': roleId,
    if (farmId != null) 'farm_id': farmId,
  };
}
