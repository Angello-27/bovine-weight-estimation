"""
Application Lifespan Management
Gestión del ciclo de vida de la aplicación FastAPI
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import (
    close_mongodb_connection,
    connect_to_mongodb,
    init_database,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager para FastAPI.

    Inicializa MongoDB/Beanie al startup y cierra conexiones al shutdown.

    Args:
        app: Instancia de FastAPI

    Yields:
        None: Control vuelve a FastAPI durante la ejecución
    """
    # Startup
    print(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"🏢 Hacienda: {settings.HACIENDA_NAME} - {settings.HACIENDA_OWNER}")
    print(f"🌍 Ambiente: {settings.ENVIRONMENT}")

    # Conectar a MongoDB
    client = await connect_to_mongodb()

    # Inicializar Beanie con modelos
    await init_database(client)
    print(f"✅ MongoDB conectado: {settings.MONGODB_DB_NAME}")

    yield

    # Shutdown
    print("🔴 Cerrando conexiones...")
    await close_mongodb_connection(client)
    print("👋 Servidor detenido")
