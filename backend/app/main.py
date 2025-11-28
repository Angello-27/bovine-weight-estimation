"""
FastAPI Main Application
Sistema de Estimación de Peso Bovino con IA - Hacienda Gamelera

Clean Architecture + SOLID Principles
"""

from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.routes import (
    animals_router,
    auth_router,
    farm_router,
    ml_router,
    role_router,
    sync_router,
    user_router,
    weighings_router,
)
from app.core.config import settings
from app.models import (
    AnimalModel,
    FarmModel,
    RoleModel,
    UserModel,
    WeightEstimationModel,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager para FastAPI.

    Inicializa MongoDB/Beanie al startup y cierra conexiones al shutdown.
    """
    # Startup
    print(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"🏢 Hacienda: {settings.HACIENDA_NAME} - {settings.HACIENDA_OWNER}")
    print(f"🌍 Ambiente: {settings.ENVIRONMENT}")

    # Conectar a MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)

    # Inicializar Beanie con modelos
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[
            AnimalModel,
            FarmModel,
            RoleModel,
            UserModel,
            WeightEstimationModel,
        ],
    )
    print(f"✅ MongoDB conectado: {settings.MONGODB_DB_NAME}")

    yield

    # Shutdown
    print("🔴 Cerrando conexiones...")
    client.close()
    print("👋 Servidor detenido")


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="Sistema de Estimación de Peso Bovino con IA - Hacienda Gamelera (Bruno Brito Macedo)",
    version=settings.APP_VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Include Routers (separados por dominio)
app.include_router(auth_router)  # Autenticación y autorización
app.include_router(user_router)  # Gestión de usuarios
app.include_router(role_router)  # Gestión de roles
app.include_router(farm_router)  # Gestión de fincas
app.include_router(animals_router)  # US-003: Registro de Animales
app.include_router(weighings_router)  # US-002/US-004: Estimación y Historial
app.include_router(ml_router)  # US-002: Inferencia ML (Core del proyecto)
app.include_router(sync_router)  # US-005: Sincronización Offline


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - Información del sistema.

    Returns:
        Información básica del servicio
    """
    return {
        "status": "online",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "hacienda": settings.HACIENDA_NAME,
        "owner": settings.HACIENDA_OWNER,
        "environment": settings.ENVIRONMENT,
        "docs": f"{settings.DOCS_URL}",
    }


@app.get("/health", tags=["Root"])
async def health():
    """
    Health check detallado.

    Verifica estado de servicios críticos.

    Returns:
        Estado de componentes del sistema
    """
    try:
        # TODO: Verificar MongoDB connection pool
        # TODO: Verificar modelos ML cargados

        return {
            "status": "healthy",
            "database": "connected",  # MongoDB
            "models_loaded": 0,  # TODO: Cargar modelos TFLite
            "services": {
                "sync": "active",  # US-005
                "animals": "active",  # US-003
                "weighings": "active",  # US-002/US-004
            },
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
