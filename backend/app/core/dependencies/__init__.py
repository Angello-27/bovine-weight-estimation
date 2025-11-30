"""
Dependencies Module - Dependency Injection
Módulo que organiza todas las dependencias por responsabilidad

Single Responsibility: Cada archivo maneja dependencias de un módulo específico
"""

from .alerts import (
    get_create_alert_usecase,
    get_delete_alert_usecase,
    get_get_alert_by_id_usecase,
    get_get_pending_alerts_usecase,
    get_get_scheduled_alerts_usecase,
    get_get_today_alerts_usecase,
    get_get_upcoming_alerts_usecase,
    get_list_alerts_usecase,
    get_mark_alert_as_completed_usecase,
    get_mark_alert_as_read_usecase,
    get_update_alert_usecase,
)
from .animals import (
    get_create_animal_usecase,
    get_delete_animal_usecase,
    get_get_animal_by_id_usecase,
    get_get_animals_by_farm_usecase,
    get_get_animals_by_filter_criteria_usecase,
    get_update_animal_usecase,
)
from .auth import (
    get_authenticate_user_usecase,
    get_current_active_user,
    get_current_superuser,
    get_current_user,
    get_get_user_by_token_usecase,
    security,
)
from .farms import (
    get_create_farm_usecase,
    get_delete_farm_usecase,
    get_get_all_farms_usecase,
    get_get_farm_by_id_usecase,
    get_update_farm_usecase,
)
from .repositories import (
    get_alert_repository,
    get_animal_repository,
    get_farm_repository,
    get_role_repository,
    get_user_repository,
    get_weight_estimation_repository,
)
from .roles import (
    get_create_role_usecase,
    get_delete_role_usecase,
    get_get_all_roles_usecase,
    get_get_role_by_id_usecase,
    get_update_role_usecase,
)
from .sync import (
    get_sync_cattle_batch_usecase,
    get_sync_health_usecase,
    get_sync_weight_estimations_batch_usecase,
)
from .users import (
    get_create_user_usecase,
    get_delete_user_usecase,
    get_get_all_users_usecase,
    get_get_user_by_id_usecase,
    get_update_user_usecase,
)

__all__ = [
    # Repositories
    "get_user_repository",
    "get_role_repository",
    "get_farm_repository",
    "get_animal_repository",
    "get_alert_repository",
    "get_weight_estimation_repository",
    # Auth
    "get_authenticate_user_usecase",
    "get_get_user_by_token_usecase",
    "get_current_user",
    "get_current_active_user",
    "get_current_superuser",
    "security",
    # User Use Cases
    "get_create_user_usecase",
    "get_get_user_by_id_usecase",
    "get_get_all_users_usecase",
    "get_update_user_usecase",
    "get_delete_user_usecase",
    # Role Use Cases
    "get_create_role_usecase",
    "get_get_role_by_id_usecase",
    "get_get_all_roles_usecase",
    "get_update_role_usecase",
    "get_delete_role_usecase",
    # Farm Use Cases
    "get_create_farm_usecase",
    "get_get_farm_by_id_usecase",
    "get_get_all_farms_usecase",
    "get_update_farm_usecase",
    "get_delete_farm_usecase",
    # Animal Use Cases
    "get_create_animal_usecase",
    "get_get_animal_by_id_usecase",
    "get_get_animals_by_farm_usecase",
    "get_get_animals_by_filter_criteria_usecase",
    "get_update_animal_usecase",
    "get_delete_animal_usecase",
    # Alert Use Cases
    "get_create_alert_usecase",
    "get_get_alert_by_id_usecase",
    "get_list_alerts_usecase",
    "get_update_alert_usecase",
    "get_delete_alert_usecase",
    "get_mark_alert_as_read_usecase",
    "get_mark_alert_as_completed_usecase",
    "get_get_pending_alerts_usecase",
    "get_get_scheduled_alerts_usecase",
    "get_get_today_alerts_usecase",
    "get_get_upcoming_alerts_usecase",
    # Sync Use Cases
    "get_sync_cattle_batch_usecase",
    "get_sync_weight_estimations_batch_usecase",
    "get_sync_health_usecase",
    # Repositories
    "get_weight_estimation_repository",
]
