"""
Role Use Cases - Domain Layer
Casos de uso para gestión de roles
"""

from .create_role_usecase import CreateRoleUseCase
from .delete_role_usecase import DeleteRoleUseCase
from .get_all_roles_usecase import GetAllRolesUseCase
from .get_role_by_id_usecase import GetRoleByIdUseCase
from .update_role_usecase import UpdateRoleUseCase

__all__ = [
    "CreateRoleUseCase",
    "GetRoleByIdUseCase",
    "GetAllRolesUseCase",
    "UpdateRoleUseCase",
    "DeleteRoleUseCase",
]
