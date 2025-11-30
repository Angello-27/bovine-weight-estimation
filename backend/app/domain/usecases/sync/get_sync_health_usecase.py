"""
Get Sync Health Use Case - Domain Layer
Caso de uso para verificar salud del servicio de sincronización
"""

from datetime import datetime

from ...repositories.animal_repository import AnimalRepository


class GetSyncHealthUseCase:
    """
    Caso de uso para verificar salud del servicio de sincronización.

    Single Responsibility: Verificar conectividad y estado de la base de datos.
    """

    def __init__(self, animal_repository: AnimalRepository):
        """
        Inicializa el caso de uso.

        Args:
            animal_repository: Repositorio de animales (para verificar conexión)
        """
        self._animal_repository = animal_repository

    async def execute(self) -> dict[str, str]:
        """
        Ejecuta la verificación de salud.

        Returns:
            Dict con status y database
        """
        try:
            # Verificar MongoDB connection contando documentos
            # El método count() está definido en AnimalRepository (interfaz ABC)
            await self._animal_repository.count()
            return {
                "status": "online",
                "database": "connected",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0",
            }
        except Exception as e:
            return {
                "status": "error",
                "database": f"error: {str(e)}",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0",
            }
