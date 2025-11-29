"""
Database Configuration
Configuración y setup de MongoDB con Beanie ODM
"""

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings
from app.data.models.animal_model import AnimalModel
from app.models import (
    AlertModel,
    FarmModel,
    RoleModel,
    UserModel,
    WeightEstimationModel,
)


async def connect_to_mongodb() -> AsyncIOMotorClient:
    """
    Conecta a MongoDB y retorna el cliente.

    Returns:
        AsyncIOMotorClient: Cliente de MongoDB conectado
    """
    client: AsyncIOMotorClient = AsyncIOMotorClient(settings.MONGODB_URL)  # type: ignore[assignment]
    return client


async def init_database(client: AsyncIOMotorClient) -> AsyncIOMotorDatabase:
    """
    Inicializa Beanie ODM con todos los modelos.

    Args:
        client: Cliente de MongoDB conectado

    Returns:
        AsyncIOMotorDatabase: Base de datos inicializada
    """
    database = client[settings.MONGODB_DB_NAME]

    await init_beanie(  # type: ignore[arg-type]
        database=database,  # type: ignore[arg-type]
        document_models=[
            AlertModel,
            AnimalModel,
            FarmModel,
            RoleModel,
            UserModel,
            WeightEstimationModel,
        ],
    )

    return database


async def close_mongodb_connection(client: AsyncIOMotorClient) -> None:
    """
    Cierra la conexión a MongoDB.

    Args:
        client: Cliente de MongoDB a cerrar
    """
    client.close()
