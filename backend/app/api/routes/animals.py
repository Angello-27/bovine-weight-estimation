"""
Animals Routes - API Endpoints
Endpoints REST para gestión de animales
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from ...core.dependencies import (
    get_create_animal_usecase,
    get_delete_animal_usecase,
    get_get_animal_by_id_usecase,
    get_get_animals_by_farm_usecase,
    get_update_animal_usecase,
)
from ...domain.usecases.animals import (
    CreateAnimalUseCase,
    DeleteAnimalUseCase,
    GetAnimalByIdUseCase,
    GetAnimalsByFarmUseCase,
    UpdateAnimalUseCase,
)
from ...schemas.animal_schemas import (
    AnimalCreateRequest,
    AnimalResponse,
    AnimalsListResponse,
    AnimalUpdateRequest,
)
from ..mappers import AnimalMapper
from ..utils import handle_domain_exceptions

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
@handle_domain_exceptions
async def create_animal(
    request: AnimalCreateRequest,
    create_usecase: Annotated[CreateAnimalUseCase, Depends(get_create_animal_usecase)],
) -> AnimalResponse:
    """Crea un nuevo animal."""
    params = AnimalMapper.create_request_to_params(request)
    animal = await create_usecase.execute(**params)
    return AnimalMapper.to_response(animal)


@router.get(
    "/{animal_id}",
    response_model=AnimalResponse,
    summary="Obtener animal por ID",
    description="Obtiene los datos completos de un animal específico.",
)
@handle_domain_exceptions
async def get_animal(
    animal_id: UUID,
    get_by_id_usecase: Annotated[
        GetAnimalByIdUseCase, Depends(get_get_animal_by_id_usecase)
    ],
) -> AnimalResponse:
    """Obtiene un animal por ID."""
    animal = await get_by_id_usecase.execute(animal_id)
    return AnimalMapper.to_response(animal)


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
@handle_domain_exceptions
async def list_animals(
    farm_id: UUID = Query(..., description="ID de la hacienda"),
    status: str | None = Query(None, description="Filtro por estado"),
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(50, ge=1, le=100, description="Tamaño de página"),
    get_by_farm_usecase: Annotated[
        GetAnimalsByFarmUseCase, Depends(get_get_animals_by_farm_usecase)
    ] = Depends(get_get_animals_by_farm_usecase),
) -> AnimalsListResponse:
    """Lista animales con paginación."""
    skip = (page - 1) * page_size
    animals = await get_by_farm_usecase.execute(
        farm_id=farm_id, skip=skip, limit=page_size, status=status
    )

    # TODO: Calcular total count para paginación correcta
    total = len(animals)

    return AnimalsListResponse(
        total=total,
        animals=[AnimalMapper.to_response(animal) for animal in animals],
        page=page,
        page_size=page_size,
    )


@router.put(
    "/{animal_id}",
    response_model=AnimalResponse,
    summary="Actualizar animal",
    description="Actualiza datos de un animal existente (solo campos proporcionados).",
)
@handle_domain_exceptions
async def update_animal(
    animal_id: UUID,
    request: AnimalUpdateRequest,
    update_usecase: Annotated[UpdateAnimalUseCase, Depends(get_update_animal_usecase)],
) -> AnimalResponse:
    """Actualiza un animal."""
    params = AnimalMapper.update_request_to_params(request)
    animal = await update_usecase.execute(animal_id=animal_id, **params)
    return AnimalMapper.to_response(animal)


@router.delete(
    "/{animal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar animal",
    description="Elimina un animal (soft delete - marca como inactive).",
)
@handle_domain_exceptions
async def delete_animal(
    animal_id: UUID,
    delete_usecase: Annotated[DeleteAnimalUseCase, Depends(get_delete_animal_usecase)],
):
    """Elimina un animal (soft delete)."""
    await delete_usecase.execute(animal_id)
    return
