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

from ...core.dependencies.weight_estimations import (
    get_estimate_weight_from_image_usecase,
)
from ...core.utils.ml_inference import get_ml_models_status
from ...domain.shared.constants import BreedType
from ...domain.usecases.weight_estimations import EstimateWeightFromImageUseCase
from ..mappers import WeightEstimationMapper
from ..utils.exception_handlers import handle_domain_exceptions

# Router con prefijo /api/v1/ml
router = APIRouter(
    prefix="/api/v1/ml",
    tags=["Machine Learning"],
    responses={
        400: {"description": "Request inválido"},
        500: {"description": "Error interno del servidor"},
    },
)


@router.post(
    "/predict",
    status_code=status.HTTP_200_OK,
    summary="Predecir peso de bovino con IA",
    description="""
    Endpoint principal de inferencia ML (sin guardar).

    **Proceso**:
    1. Recibe imagen del bovino (JPEG/PNG)
    2. Valida tamaño y formato
    3. Preprocesa imagen (224x224x3, normalización)
    4. Ejecuta inferencia con modelo TFLite específico de la raza
    5. Valida métricas (confidence ≥80%, tiempo <3s)
    6. Retorna peso estimado + confidence (NO guarda en BD)

    **US-002**: Estimación de Peso por Raza con IA

    **Métricas objetivo**:
    - Precisión: ≥95% (R² ≥0.95)
    - Error: <5 kg
    - Tiempo: <3 segundos
    - Confidence: ≥80%

    **7 Razas soportadas** (tropicales priorizadas):
    - nelore, brahman, guzerat, senepol, girolando, gyr_lechero, sindi

    **Razas prioritarias** (más datos disponibles en Santa Cruz):
    - nelore (42% del hato), brahman, guzerat
    """,
)
@handle_domain_exceptions
async def predict_weight(
    image: UploadFile = File(..., description="Imagen del bovino (JPEG/PNG)"),
    breed: BreedType = Form(..., description="Raza del animal"),
    animal_id: UUID | None = Form(None, description="ID del animal (opcional)"),
    device_id: str | None = Form(None, description="ID del dispositivo"),
):
    """
    Predice peso de un bovino con IA (sin guardar).

    Args:
        image: Archivo de imagen
        breed: Raza del animal (enum)
        animal_id: ID del animal (opcional)
        device_id: ID del dispositivo (opcional)

    Returns:
        Estimación de peso con confidence y métricas (sin persistir)
    """
    from ...core.utils.ml_inference import estimate_weight_from_image

    # Leer bytes de imagen
    image_bytes = await image.read()

    # Ejecutar inferencia (sin guardar)
    estimation = await estimate_weight_from_image(
        image_bytes=image_bytes,
        breed=breed,
        animal_id=str(animal_id) if animal_id else None,
        device_id=device_id,
    )

    # Retornar respuesta
    return {
        "id": str(estimation.id),
        "animal_id": str(estimation.animal_id) if estimation.animal_id else None,
        "breed": estimation.breed,
        "estimated_weight_kg": estimation.estimated_weight_kg,
        "confidence": estimation.confidence,
        "confidence_level": estimation.get_confidence_level(),
        "processing_time_ms": estimation.processing_time_ms,
        "ml_model_version": estimation.ml_model_version,
        "method": "strategy_based",
        "meets_quality_criteria": estimation.meets_quality_criteria(),
        "timestamp": estimation.timestamp.isoformat(),
    }


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
async def get_models_status():
    """Obtiene estado de modelos ML."""
    status_info = await get_ml_models_status()
    return {
        "status": "ok",
        **status_info,
        "note": "Sistema de estrategias activo: ML entrenado + híbrido YOLO como fallback",
        "method": "strategy_based",
    }


@router.post(
    "/estimate",
    status_code=status.HTTP_200_OK,
    summary="Estimar peso desde web (upload de imagen)",
    description="""
    Endpoint para estimar peso desde el panel web subiendo una imagen.

    **Proceso**:
    1. Recibe imagen del bovino (multipart/form-data)
    2. Valida formato y tamaño
    3. Ejecuta inferencia ML
    4. Guarda estimación en base de datos
    5. Retorna resultado completo

    **Diferencia con /predict**:
    - /predict: Solo hace inferencia, retorna resultado (para móvil)
    - /estimate: Hace inferencia Y guarda automáticamente (para web)

    **US-002**: Estimación de Peso por Raza con IA
    **WEIGHT_ESTIMATION_WEB_PLAN**: Estimación desde panel web
    """,
    response_description="Estimación guardada con peso, confidence y metadatos",
)
@handle_domain_exceptions
async def estimate_weight_from_web(
    estimate_usecase: Annotated[
        EstimateWeightFromImageUseCase,
        Depends(get_estimate_weight_from_image_usecase),
    ],
    image: UploadFile = File(..., description="Imagen del bovino (JPEG/PNG/WEBP)"),
    breed: BreedType = Form(..., description="Raza del animal"),
    animal_id: UUID | None = Form(None, description="ID del animal (opcional)"),
):
    """
    Estima peso desde imagen subida y guarda la estimación.

    Args:
        estimate_usecase: Caso de uso para estimar y guardar (inyectado)
        image: Archivo de imagen
        breed: Raza del animal (enum)
        animal_id: ID del animal (opcional)

    Returns:
        Estimación guardada con todos los datos
    """
    # 1. Validar formato de imagen
    allowed_formats = ["image/jpeg", "image/png", "image/webp"]
    if image.content_type not in allowed_formats:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato de imagen no soportado: {image.content_type}. "
            f"Formatos permitidos: {', '.join(allowed_formats)}",
        )

    # 2. Leer bytes de imagen
    image_bytes = await image.read()

    # 3. Ejecutar caso de uso (inferencia + guardado)
    saved_estimation = await estimate_usecase.execute(
        image_bytes=image_bytes,
        breed=breed,
        animal_id=animal_id,
        device_id="web_panel",  # Identificador para estimaciones desde web
        frame_image_path=f"web_uploads/{animal_id or 'unknown'}_{image.filename}",
    )

    # 4. Convertir a DTO usando mapper
    response = WeightEstimationMapper.to_response(saved_estimation)

    # 5. Retornar respuesta en formato compatible con frontend
    return {
        "id": str(response.id),
        "animal_id": str(response.animal_id) if response.animal_id else None,
        "breed": (
            response.breed.value if hasattr(response.breed, "value") else response.breed
        ),
        "estimated_weight": response.estimated_weight_kg,
        "estimated_weight_kg": response.estimated_weight_kg,
        "confidence_score": response.confidence,
        "confidence": response.confidence,
        "breed_confidence": response.confidence,
        "model_version": response.model_version,
        "processing_time_ms": response.processing_time_ms,
        "image_path": saved_estimation.frame_image_path,
        "method": response.method,
        "meets_quality_criteria": saved_estimation.meets_quality_criteria(),
        "timestamp": response.timestamp.isoformat(),
    }


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
        "method": "strategy_based",
        "description": "Sistema de estrategias: ML entrenado + híbrido YOLO como fallback",
        "note": "Sistema funcional con múltiples estrategias de estimación",
    }
