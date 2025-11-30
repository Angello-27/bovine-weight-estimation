"""
Weight Estimation Entity - Domain Layer
Entidad pura del dominio sin dependencias externas
"""

from datetime import datetime
from uuid import UUID, uuid4


class WeightEstimation:
    """
    Entidad WeightEstimation del dominio.

    Single Responsibility: Representar una estimación de peso en el dominio.
    Sin dependencias de frameworks (Beanie, FastAPI, etc.)
    """

    def __init__(
        self,
        id: UUID | None = None,
        animal_id: str | None = None,
        breed: str = "",
        estimated_weight_kg: float = 0.0,
        confidence: float = 0.0,
        method: str = "tflite",
        ml_model_version: str = "1.0.0",
        processing_time_ms: int = 0,
        frame_image_path: str = "",
        latitude: float | None = None,
        longitude: float | None = None,
        timestamp: datetime | None = None,
        device_id: str | None = None,
        synced_at: datetime | None = None,
    ):
        """Inicializa entidad WeightEstimation."""
        self.id = id or uuid4()
        self.animal_id = animal_id
        self.breed = breed
        self.estimated_weight_kg = estimated_weight_kg
        self.confidence = confidence
        self.method = method
        self.ml_model_version = ml_model_version
        self.processing_time_ms = processing_time_ms
        self.frame_image_path = frame_image_path
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp or datetime.utcnow()
        self.device_id = device_id
        self.synced_at = synced_at

    def meets_quality_criteria(self) -> bool:
        """
        Verifica si cumple criterios de calidad.

        Criterios: Confidence ≥80% y procesamiento <3s
        """
        from ..shared.constants import SystemMetrics

        return (
            self.confidence >= SystemMetrics.MIN_CONFIDENCE
            and self.processing_time_ms < SystemMetrics.MAX_PROCESSING_TIME_MS
        )

    def get_confidence_level(self) -> str:
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

    def __eq__(self, other: object) -> bool:
        """Compara dos estimaciones por ID."""
        if not isinstance(other, WeightEstimation):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash basado en ID."""
        return hash(self.id)
