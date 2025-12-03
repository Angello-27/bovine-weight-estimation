"""
Dashboard Schemas - Pydantic DTOs
Request/Response models para API de dashboard
"""

from pydantic import BaseModel, ConfigDict, Field


class DashboardStatsResponse(BaseModel):
    """Response con estadísticas del dashboard."""

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "totalCattle": 200,
                "averageWeight": 350.5,
                "totalBreeds": 5,
                "totalEstimations": 450,
            }
        },
    )

    total_cattle: int = Field(
        ...,
        alias="totalCattle",
        description="Total de animales en la finca",
        ge=0,
    )
    average_weight: float = Field(
        ...,
        alias="averageWeight",
        description="Peso promedio (kg) de las estimaciones más recientes",
        ge=0,
    )
    total_breeds: int = Field(
        ...,
        alias="totalBreeds",
        description="Número de razas diferentes",
        ge=0,
    )
    total_estimations: int = Field(
        ...,
        alias="totalEstimations",
        description="Total de estimaciones de peso",
        ge=0,
    )
