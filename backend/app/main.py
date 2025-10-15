"""
FastAPI Main Application
Sistema de Estimación de Peso Bovino con IA
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Bovine Weight Estimation API",
    description="Sistema de Estimación de Peso Bovino con IA - Hacienda Gamelera",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configurar origins específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Bovine Weight Estimation API",
        "version": "1.0.0",
        "hacienda": "Gamelera",
        "owner": "Bruno Brito Macedo",
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "pending",  # TODO: Check MongoDB connection
        "ml_models": "pending",  # TODO: Check TFLite models loaded
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

