"""
Report Schemas - Pydantic DTOs
Request/Response models para API de reportes
"""

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class ReportFormat(str, Enum):
    """Formatos de reporte disponibles."""

    PDF = "pdf"
    EXCEL = "excel"


class GenerateTraceabilityReportRequest(BaseModel):
    """Request para generar reporte de trazabilidad individual."""

    format: ReportFormat = Field(
        default=ReportFormat.PDF, description="Formato del reporte"
    )


class GenerateInventoryReportRequest(BaseModel):
    """Request para generar reporte de inventario."""

    farm_id: UUID = Field(..., description="ID de la finca")
    format: ReportFormat = Field(
        default=ReportFormat.PDF, description="Formato del reporte"
    )
    status: str | None = Field(
        None, description="Filtro por estado (active, sold, deceased, inactive)"
    )
    breed: str | None = Field(None, description="Filtro por raza")
    date_from: datetime | None = Field(
        None, description="Fecha desde (filtro por registro)"
    )
    date_to: datetime | None = Field(
        None, description="Fecha hasta (filtro por registro)"
    )

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str | None) -> str | None:
        """Valida status."""
        if v is not None and v not in ["active", "inactive", "sold", "deceased"]:
            raise ValueError("Status debe ser: active, inactive, sold o deceased")
        return v


class GenerateMovementsReportRequest(BaseModel):
    """Request para generar reporte de movimientos."""

    farm_id: UUID = Field(..., description="ID de la finca")
    format: ReportFormat = Field(
        default=ReportFormat.PDF, description="Formato del reporte (PDF o CSV)"
    )
    movement_type: str | None = Field(
        None, description="Tipo de movimiento: sold, deceased, o None para todos"
    )
    date_from: datetime | None = Field(None, description="Fecha desde")
    date_to: datetime | None = Field(None, description="Fecha hasta")

    @field_validator("movement_type")
    @classmethod
    def validate_movement_type(cls, v: str | None) -> str | None:
        """Valida movement_type."""
        if v is not None and v not in ["sold", "deceased"]:
            raise ValueError("Movement type debe ser: sold o deceased")
        return v

    @field_validator("format")
    @classmethod
    def validate_format(cls, v: ReportFormat) -> ReportFormat:
        """Valida formato para movimientos (solo PDF o Excel)."""
        if v not in [ReportFormat.PDF, ReportFormat.EXCEL]:
            raise ValueError(
                "Formato debe ser PDF o Excel para reportes de movimientos"
            )
        return v


class GenerateGrowthReportRequest(BaseModel):
    """Request para generar reporte de crecimiento."""

    format: ReportFormat = Field(
        default=ReportFormat.PDF, description="Formato del reporte"
    )
    animal_id: UUID | None = Field(
        None, description="ID del animal (para reporte individual)"
    )
    farm_id: UUID | None = Field(
        None, description="ID de la finca (para reporte grupal)"
    )

    @field_validator("animal_id", "farm_id")
    @classmethod
    def validate_at_least_one(cls, v: UUID | None, info) -> UUID | None:
        """Valida que al menos uno de animal_id o farm_id esté presente."""
        if info.data.get("animal_id") is None and info.data.get("farm_id") is None:
            raise ValueError("Debe especificar animal_id o farm_id")
        return v


class ReportResponse(BaseModel):
    """Response genérico para reportes."""

    filename: str
    content_type: str
    file_size_bytes: int
    format: str
    generated_at: datetime

    class Config:
        from_attributes = True
