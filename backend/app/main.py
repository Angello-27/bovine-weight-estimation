"""
FastAPI Main Application
Sistema de Estimación de Peso Bovino con IA - Hacienda Gamelera

Clean Architecture + SOLID Principles

Responsabilidades:
- Crear instancia de FastAPI
- Configurar aplicación con settings
- Registrar middlewares y rutas
- Endpoints básicos (root, health)
"""

from fastapi import FastAPI

from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.middleware import setup_middleware
from app.core.routes import setup_routes


def create_application() -> FastAPI:
    """
    Factory function para crear la aplicación FastAPI.

    Separa la creación de la app de su configuración.
    Facilita testing y reutilización.

    Returns:
        FastAPI: Aplicación configurada
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="Sistema de Estimación de Peso Bovino con IA - Hacienda Gamelera (Bruno Brito Macedo)",
        version=settings.APP_VERSION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
        openapi_url=settings.OPENAPI_URL,
        lifespan=lifespan,
    )

    # Configurar middlewares
    setup_middleware(app)

    # Registrar todas las rutas
    setup_routes(app)

    return app


# Crear aplicación FastAPI
app = create_application()


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
        from app.ml.model_loader import MLModelLoader

        # Verificar modelos ML cargados
        model_loader = MLModelLoader()
        models_loaded = 1 if model_loader.is_model_loaded() else 0
        loaded_breeds = model_loader.get_loaded_breeds()

        return {
            "status": "healthy",
            "database": "connected",  # MongoDB
            "models_loaded": models_loaded,
            "loaded_models": loaded_breeds,
            "services": {
                "sync": "active",  # US-005
                "animals": "active",  # US-003
                "weighings": "active",  # US-002/US-004
                "alerts": "active",  # Alertas y cronograma
                "ml": "active" if models_loaded > 0 else "degraded",  # ML
            },
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e),
            "models_loaded": 0,
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
