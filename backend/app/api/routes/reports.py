"""
Reports Routes - API Endpoints
Endpoints REST para generación de reportes
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from ...core.dependencies import (
    get_generate_growth_report_usecase,
    get_generate_inventory_report_usecase,
    get_generate_movements_report_usecase,
    get_generate_traceability_report_usecase,
)
from ...core.utils import ReportGenerator
from ...domain.usecases.reports import (
    GenerateGrowthReportUseCase,
    GenerateInventoryReportUseCase,
    GenerateMovementsReportUseCase,
    GenerateTraceabilityReportUseCase,
)
from ...schemas.report_schemas import (
    GenerateGrowthReportRequest,
    GenerateInventoryReportRequest,
    GenerateMovementsReportRequest,
    GenerateTraceabilityReportRequest,
    ReportFormat,
)
from ..utils.exception_handlers import handle_domain_exceptions

# Router con prefijo /api/v1/reports
router = APIRouter(
    prefix="/api/v1/reports",
    tags=["Reportes"],
    responses={
        400: {"description": "Request inválido"},
        404: {"description": "Recurso no encontrado"},
        500: {"description": "Error interno del servidor"},
    },
)


@router.post(
    "/traceability/{animal_id}",
    status_code=status.HTTP_200_OK,
    summary="Generar reporte de trazabilidad individual",
    description="""
    Genera un reporte de trazabilidad completo de un animal.

    **Incluye**:
    - Información completa del animal
    - Historial de estimaciones de peso
    - Linaje (padre, madre, descendientes)
    - Timeline de eventos

    **Formatos**: PDF, Excel

    **US-004**: Trazabilidad del Ganado
    """,
)
@handle_domain_exceptions
async def generate_traceability_report(
    animal_id: UUID,
    request: GenerateTraceabilityReportRequest,
    usecase: Annotated[
        GenerateTraceabilityReportUseCase,
        Depends(get_generate_traceability_report_usecase),
    ],
) -> StreamingResponse:
    """Genera reporte de trazabilidad de un animal."""
    # 1. Ejecutar use case
    report_data = await usecase.execute(animal_id, request.format.value)

    # 2. Generar archivo según formato
    if request.format == ReportFormat.PDF:
        file_content = ReportGenerator.generate_pdf(report_data, "traceability")
        media_type = "application/pdf"
        filename = f"trazabilidad_{animal_id}.pdf"
    elif request.format == ReportFormat.EXCEL:
        file_content = ReportGenerator.generate_excel(report_data, "traceability")
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"trazabilidad_{animal_id}.xlsx"
    else:
        raise ValueError(f"Formato no soportado: {request.format}")

    # 3. Retornar como streaming response
    return StreamingResponse(
        iter([file_content]),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post(
    "/inventory",
    status_code=status.HTTP_200_OK,
    summary="Generar reporte de inventario",
    description="""
    Genera un reporte de inventario de animales de una finca.

    **Filtros disponibles**:
    - Por estado (active, sold, deceased, inactive)
    - Por raza
    - Por rango de fechas de registro

    **Formatos**: PDF, Excel

    **Cumple normativas SENASAG** (inventario mensual/trimestral)
    """,
)
@handle_domain_exceptions
async def generate_inventory_report(
    request: GenerateInventoryReportRequest,
    usecase: Annotated[
        GenerateInventoryReportUseCase,
        Depends(get_generate_inventory_report_usecase),
    ],
) -> StreamingResponse:
    """Genera reporte de inventario."""
    # 1. Ejecutar use case
    report_data = await usecase.execute(
        farm_id=request.farm_id,
        format=request.format.value,
        status=request.status,
        breed=request.breed,
        date_from=request.date_from,
        date_to=request.date_to,
    )

    # 2. Generar archivo según formato
    if request.format == ReportFormat.PDF:
        file_content = ReportGenerator.generate_pdf(report_data, "inventory")
        media_type = "application/pdf"
        filename = f"inventario_{request.farm_id}.pdf"
    elif request.format == ReportFormat.EXCEL:
        file_content = ReportGenerator.generate_excel(report_data, "inventory")
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"inventario_{request.farm_id}.xlsx"
    else:
        raise ValueError(f"Formato no soportado: {request.format}")

    # 3. Retornar como streaming response
    return StreamingResponse(
        iter([file_content]),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post(
    "/movements",
    status_code=status.HTTP_200_OK,
    summary="Generar reporte de movimientos",
    description="""
    Genera un reporte de movimientos (ventas, fallecimientos).

    **Tipos de movimiento**:
    - sold: Animales vendidos
    - deceased: Animales fallecidos
    - None: Todos los movimientos

    **Formatos**: PDF, Excel

    **Cumple normativas REGENSA** (GMA - Guía de Movimiento Animal)
    """,
)
@handle_domain_exceptions
async def generate_movements_report(
    request: GenerateMovementsReportRequest,
    usecase: Annotated[
        GenerateMovementsReportUseCase,
        Depends(get_generate_movements_report_usecase),
    ],
) -> StreamingResponse:
    """Genera reporte de movimientos."""
    # 1. Ejecutar use case
    report_data = await usecase.execute(
        farm_id=request.farm_id,
        format=request.format.value,
        movement_type=request.movement_type,
        date_from=request.date_from,
        date_to=request.date_to,
    )

    # 2. Generar archivo según formato
    if request.format == ReportFormat.PDF:
        file_content = ReportGenerator.generate_pdf(report_data, "movements")
        media_type = "application/pdf"
        filename = f"movimientos_{request.farm_id}.pdf"
    elif request.format == ReportFormat.EXCEL:
        file_content = ReportGenerator.generate_excel(report_data, "movements")
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"movimientos_{request.farm_id}.xlsx"
    else:
        raise ValueError(f"Formato no soportado: {request.format}")

    # 3. Retornar como streaming response
    return StreamingResponse(
        iter([file_content]),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post(
    "/growth",
    status_code=status.HTTP_200_OK,
    summary="Generar reporte de crecimiento",
    description="""
    Genera un reporte de crecimiento y ganancia diaria promedio (GDP).

    **Tipos de reporte**:
    - Individual: Si se especifica animal_id
    - Grupal: Si se especifica farm_id

    **Métricas incluidas**:
    - GDP (Ganancia Diaria Promedio)
    - Evolución de peso
    - Total de mediciones

    **Formatos**: PDF, Excel

    **Cumple normativas ASOCEBU** (competencias ganaderas)
    """,
)
@handle_domain_exceptions
async def generate_growth_report(
    request: GenerateGrowthReportRequest,
    usecase: Annotated[
        GenerateGrowthReportUseCase, Depends(get_generate_growth_report_usecase)
    ],
) -> StreamingResponse:
    """Genera reporte de crecimiento."""
    # 1. Ejecutar use case
    report_data = await usecase.execute(
        animal_id=request.animal_id,
        farm_id=request.farm_id,
        format=request.format.value,
    )

    # 2. Generar archivo según formato
    report_type = "individual" if request.animal_id else "grupal"
    entity_id = request.animal_id or request.farm_id

    if request.format == ReportFormat.PDF:
        file_content = ReportGenerator.generate_pdf(report_data, "growth")
        media_type = "application/pdf"
        filename = f"crecimiento_{report_type}_{entity_id}.pdf"
    elif request.format == ReportFormat.EXCEL:
        file_content = ReportGenerator.generate_excel(report_data, "growth")
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        report_type = "individual" if request.animal_id else "grupal"
        entity_id = request.animal_id or request.farm_id
        filename = f"crecimiento_{report_type}_{entity_id}.xlsx"
    else:
        raise ValueError(f"Formato no soportado: {request.format}")

    # 3. Retornar como streaming response
    return StreamingResponse(
        iter([file_content]),
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
