"""
Animals Routes - API Endpoints
Endpoints REST para gestión de animales
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ...core.errors import (
    AlreadyExistsException,
    NotFoundException,
    ValidationException,
)
from ...schemas.animal_schemas import (
    AnimalCreateRequest,
    AnimalResponse,
    AnimalsListResponse,
    AnimalUpdateRequest,
)
from ...services import AnimalService

# Router con prefijo /api/v1/animals
router = APIRouter(
    prefix="/api/v1/animals",
    tags=["Animals"],
    responses={
        404: {"description": "Animal no encontrado"},
        400: {"description": "Request inválido"},
        500: {"description": "Error interno del servidor"},
    },
)


# Dependency injection del servicio
def get_animal_service() -> AnimalService:
    """Dependency para inyectar AnimalService."""
    return AnimalService()


@router.post(
    "",
    response_model=AnimalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear animal",
    description="""
    Crea un nuevo animal en el sistema.

    **Validaciones**:
    - Caravana única por hacienda
    - Raza debe ser una de las 7 exactas
    - Fecha de nacimiento no puede ser futura
    - Género: male o female

    **US-003**: Registro Automático de Animales
    """,
)
async def create_animal(
    request: AnimalCreateRequest,
    service: Annotated[AnimalService, Depends(get_animal_service)],
) -> AnimalResponse:
    """Crea un nuevo animal."""
    try:
        return await service.create_animal(request)
    except AlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear animal: {str(e)}",
        )


@router.get(
    "/{animal_id}",
    response_model=AnimalResponse,
    summary="Obtener animal por ID",
    description="Obtiene los datos completos de un animal específico.",
)
async def get_animal(
    animal_id: UUID,
    service: Annotated[AnimalService, Depends(get_animal_service)],
) -> AnimalResponse:
    """Obtiene un animal por ID."""
    try:
        return await service.get_animal(animal_id)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener animal: {str(e)}",
        )


@router.get(
    "",
    response_model=AnimalsListResponse,
    summary="Listar animales",
    description="""
    Lista animales de una hacienda con paginación y filtros.

    **Filtros disponibles**:
    - status: active/inactive/sold/deceased

    **Paginación**:
    - page: Número de página (default: 1)
    - page_size: Tamaño de página (default: 50, max: 100)
    """,
)
async def list_animals(
    service: Annotated[AnimalService, Depends(get_animal_service)],
    farm_id: UUID = Query(..., description="ID de la hacienda"),
    status: str | None = Query(None, description="Filtro por estado"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamaño de página"),
) -> AnimalsListResponse:
    """Lista animales con paginación."""
    try:
        skip = (page - 1) * page_size
        animals = await service.get_animals_by_farm(
            farm_id=farm_id,
            skip=skip,
            limit=page_size,
            status=status,
        )

        # TODO: Calcular total count para paginación correcta
        total = len(animals)

        return AnimalsListResponse(
            total=total,
            animals=animals,
            page=page,
            page_size=page_size,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar animales: {str(e)}",
        )


@router.put(
    "/{animal_id}",
    response_model=AnimalResponse,
    summary="Actualizar animal",
    description="Actualiza datos de un animal existente (solo campos proporcionados).",
)
async def update_animal(
    animal_id: UUID,
    request: AnimalUpdateRequest,
    service: Annotated[AnimalService, Depends(get_animal_service)],
) -> AnimalResponse:
    """Actualiza un animal."""
    try:
        return await service.update_animal(animal_id, request)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar animal: {str(e)}",
        )


@router.delete(
    "/{animal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar animal",
    description="Elimina un animal (soft delete - marca como inactive).",
)
async def delete_animal(
    animal_id: UUID,
    service: Annotated[AnimalService, Depends(get_animal_service)],
):
    """Elimina un animal (soft delete)."""
    try:
        await service.delete_animal(animal_id)
        return
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar animal: {str(e)}",
        )
