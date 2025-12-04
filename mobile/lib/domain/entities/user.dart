/// Entity: User
///
/// Usuario autenticado del sistema.
/// Single Responsibility: Representar usuario con sus datos y permisos.
///
/// Domain Layer - Clean Architecture
library;

import 'package:equatable/equatable.dart';

/// Usuario del sistema
class User extends Equatable {
  /// ID único del usuario
  final String id;

  /// Nombre de usuario
  final String username;

  /// Email del usuario
  final String email;

  /// Rol del usuario
  final UserRole? role;

  /// ID del rol
  final String? roleId;

  /// ID de la finca asignada
  final String? farmId;

  const User({
    required this.id,
    required this.username,
    required this.email,
    this.role,
    this.roleId,
    this.farmId,
  });

  /// Verifica si el usuario tiene una finca asignada
  bool get hasFarm => farmId != null && farmId!.isNotEmpty;

  /// Verifica si el usuario es administrador
  bool get isAdmin => role?.priority == 'Administrador';

  @override
  List<Object?> get props => [id, username, email, role, roleId, farmId];
}

/// Rol del usuario
class UserRole extends Equatable {
  /// ID del rol
  final String id;

  /// Nombre del rol
  final String name;

  /// Prioridad del rol (Administrador, Usuario, Invitado)
  final String priority;

  const UserRole({
    required this.id,
    required this.name,
    required this.priority,
  });

  @override
  List<Object?> get props => [id, name, priority];
}
