"""
ML Routes - API Endpoints for Machine Learning
Endpoints REST para inferencia ML

US-002: Estimación de Peso por Raza con IA
"""

from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)

from ...core.constants import BreedType
from ...core.errors import MLModelException, ValidationException
from ...services.ml_service import MLService

# Router con prefijo /api/v1/ml
router = APIRouter(
    prefix="/api/v1/ml",
    tags=["Machine Learning"],
    responses={
        400: {"description": "Request inválido"},
        500: {"description": "Error interno del servidor"},
    },
)


# Dependency injection del servicio
def get_ml_service() -> MLService:
    """Dependency para inyectar MLService."""
    return MLService()


@router.post(
    "/predict",
    status_code=status.HTTP_200_OK,
    summary="Predecir peso de bovino con IA",
    description="""
    Endpoint principal de inferencia ML.

    **Proceso**:
    1. Recibe imagen del bovino (JPEG/PNG)
    2. Valida tamaño y formato
    3. Preprocesa imagen (224x224x3, normalización)
    4. Ejecuta inferencia con modelo TFLite específico de la raza
    5. Valida métricas (confidence ≥80%, tiempo <3s)
    6. Guarda estimación en MongoDB
    7. Retorna peso estimado + confidence

    **US-002**: Estimación de Peso por Raza con IA

    **Métricas objetivo**:
    - Precisión: ≥95% (R² ≥0.95)
    - Error: <5 kg
    - Tiempo: <3 segundos
    - Confidence: ≥80%

    **7 Razas soportadas**:
    - brahman, nelore, angus, cebuinas, criollo, pardo_suizo, jersey
    """,
)
async def predict_weight(
    image: UploadFile = File(..., description="Imagen del bovino (JPEG/PNG)"),
    breed: BreedType = Form(..., description="Raza del animal"),
    animal_id: UUID | None = Form(None, description="ID del animal (opcional)"),
    device_id: str | None = Form(None, description="ID del dispositivo"),
    ml_service: Annotated[MLService, Depends(get_ml_service)] = Depends(),
):
    """
    Predice peso de un bovino con IA.

    Args:
        image: Archivo de imagen
        breed: Raza del animal (enum)
        animal_id: ID del animal (opcional)
        device_id: ID del dispositivo (opcional)
        ml_service: Servicio ML (inyectado)

    Returns:
        Estimación de peso con confidence y métricas
    """
    try:
        # Leer bytes de imagen
        image_bytes = await image.read()

        # Ejecutar predicción
        weight_estimation = await ml_service.predict_weight(
            image_bytes=image_bytes,
            breed=breed,
            animal_id=animal_id,
            device_id=device_id,
        )

        # Retornar respuesta
        return {
            "id": str(weight_estimation.id),
            "animal_id": str(weight_estimation.animal_id)
            if weight_estimation.animal_id
            else None,
            "breed": weight_estimation.breed.value,
            "estimated_weight_kg": weight_estimation.estimated_weight_kg,
            "confidence": weight_estimation.confidence,
            "confidence_level": weight_estimation.confidence_level,
            "processing_time_ms": weight_estimation.processing_time_ms,
            "model_version": weight_estimation.model_version,
            "meets_quality_criteria": weight_estimation.meets_quality_criteria,
            "timestamp": weight_estimation.timestamp.isoformat(),
        }

    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except MLModelException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en modelo ML: {e.message}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {str(e)}",
        )


@router.get(
    "/models/status",
    status_code=status.HTTP_200_OK,
    summary="Estado de modelos ML",
    description="""
    Obtiene información de modelos ML cargados.

    **Información incluida**:
    - Total de modelos cargados
    - Razas con modelos disponibles
    - Razas faltantes

    **Útil para**:
    - Verificar que los 7 modelos TFLite estén cargados
    - Diagnosticar problemas de carga
    - Monitoreo de disponibilidad
    """,
)
async def get_models_status(
    ml_service: Annotated[MLService, Depends(get_ml_service)] = Depends(),
):
    """Obtiene estado de modelos ML."""
    try:
        status_info = await ml_service.get_models_status()
        return {
            "status": "ok",
            **status_info,
            "note": "Modelos en modo MVP (mock). Reemplazar con modelos reales entrenados.",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener estado de modelos: {str(e)}",
        )


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check ML",
    description="Verifica que el servicio ML esté operativo.",
)
async def ml_health_check():
    """Health check del servicio ML."""
    return {
        "status": "healthy",
        "service": "ml_inference",
        "models": "mock (MVP)",
        "note": "Modelos TFLite reales pendientes de entrenamiento",
    }
