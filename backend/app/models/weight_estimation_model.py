"""
Weight Estimation Model - Beanie ODM
Modelo de persistencia para estimaciones de peso en MongoDB
"""

from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import Field, field_validator

from ..core.constants import BreedType, SystemMetrics


class WeightEstimationModel(Document):
    """
    Modelo de estimación de peso para MongoDB.

    Single Responsibility: Persistencia de estimaciones de peso con IA.
    """

    # ID único de la estimación
    id: UUID = Field(default_factory=uuid4, alias="_id")

    # Animal relacionado
    animal_id: Indexed(str) | None = Field(
        None, description="ID del animal (si está vinculado)"
    )

    # Datos de estimación
    breed: Indexed(str) = Field(..., description="Raza del animal")
    estimated_weight_kg: float = Field(
        ..., description="Peso estimado en kg", ge=0, le=1500
    )
    confidence: float = Field(..., description="Confidence score (0.0-1.0)", ge=0, le=1)

    # Metadata de procesamiento
    method: str = Field(default="tflite", description="Método: tflite/schaeffer/manual")
    model_version: str = Field(default="1.0.0", description="Versión del modelo usado")
    processing_time_ms: int = Field(..., description="Tiempo de procesamiento en ms")
    frame_image_path: str = Field(..., description="Path del fotograma usado")

    # Datos de ubicación (opcional)
    latitude: float | None = Field(None, description="Latitud GPS", ge=-90, le=90)
    longitude: float | None = Field(None, description="Longitud GPS", ge=-180, le=180)

    # Timestamps
    timestamp: Indexed(datetime) = Field(
        default_factory=datetime.utcnow, description="Timestamp de la estimación"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creación en sistema"
    )

    # Sincronización (US-005)
    device_id: str | None = Field(
        None, description="ID del dispositivo que creó el registro"
    )
    synced_at: datetime | None = Field(
        None, description="Timestamp de última sincronización"
    )

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """
        Valida que el confidence esté dentro de rangos aceptables.

        Advertencia si es <80%, crítico si es <60%.
        """
        if v < 0.60:
            raise ValueError(
                f"Confidence {v:.2%} es demasiado bajo (mínimo 60% para guardar)"
            )
        return v

    @field_validator("processing_time_ms")
    @classmethod
    def validate_processing_time(cls, v: int) -> int:
        """Valida que el procesamiento sea <3s."""
        if v > SystemMetrics.MAX_PROCESSING_TIME_MS:
            # No falla, solo advierte (métrica de performance)
            pass
        return v

    @field_validator("estimated_weight_kg")
    @classmethod
    def validate_weight(cls, v: float) -> float:
        """Valida que el peso sea razonable."""
        if v <= 0:
            raise ValueError("Peso debe ser mayor a 0 kg")
        if v > 1500:
            raise ValueError("Peso excede máximo razonable (1500 kg)")
        return v

    @property
    def confidence_level(self) -> str:
        """
        Nivel de confianza basado en threshold.

        Returns:
            'high' (≥90%), 'medium' (80-90%), 'low' (<80%)
        """
        if self.confidence >= 0.90:
            return "high"
        if self.confidence >= 0.80:
            return "medium"
        return "low"

    @property
    def meets_quality_criteria(self) -> bool:
        """
        Verifica si cumple criterios de calidad.

        Criterios: Confidence ≥80% y procesamiento <3s
        """
        return (
            self.confidence >= SystemMetrics.MIN_CONFIDENCE
            and self.processing_time_ms < SystemMetrics.MAX_PROCESSING_TIME_MS
        )

    class Settings:
        """Configuración de Beanie."""

        name = "weight_estimations"
        use_state_management = True
        validate_on_save = True

        # Índices
        indexes = [
            "animal_id",  # Filtro por animal
            "breed",  # Filtro por raza
            "timestamp",  # Ordenamiento cronológico
            "confidence",  # Filtro por calidad
            [("animal_id", 1), ("timestamp", -1)],  # Historial por animal
        ]

    class Config:
        """Configuración de Pydantic."""

        json_schema_extra = {
            "example": {
                "_id": "550e8400-e29b-41d4-a716-446655440001",
                "animal_id": "550e8400-e29b-41d4-a716-446655440000",
                "breed": "brahman",
                "estimated_weight_kg": 487.5,
                "confidence": 0.95,
                "method": "tflite",
                "model_version": "1.0.0",
                "processing_time_ms": 2100,
                "frame_image_path": "/frames/frame_001.jpg",
                "latitude": -15.859500,
                "longitude": -60.797889,
                "timestamp": "2024-10-20T14:30:00Z",
            }
        }
