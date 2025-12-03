"""
Resources Routes - API Endpoints
Endpoints REST para servir recursos estáticos (imágenes)
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from ...core.utils.image_storage import ensure_uploads_directory
from ..utils.exception_handlers import handle_domain_exceptions

# Router con prefijo /api/v1/resources
router = APIRouter(
    prefix="/api/v1/resources",
    tags=["Recursos"],
    responses={
        404: {"description": "Recurso no encontrado"},
        400: {"description": "Request inválido"},
        500: {"description": "Error interno del servidor"},
    },
)


@router.get(
    "/images/{image_path:path}",
    summary="Obtener imagen",
    description="""
    Sirve imágenes desde el directorio de uploads.

    **Path**:
    - image_path: Ruta relativa de la imagen desde uploads/
      - Ejemplo: `nelore/nelore_213.jpg`
      - Ejemplo: `brahman/animal_123.jpg`
      - Ejemplo: `estimations/estimation_456.jpg`

    **Response**:
    - Archivo de imagen con Content-Type apropiado

    **Errores**:
    - 404: Imagen no encontrada
    - 400: Path inválido (intenta acceder fuera de uploads/)
    """,
    response_description="Archivo de imagen",
)
@handle_domain_exceptions
async def get_image(image_path: str) -> FileResponse:
    """
    Endpoint para servir imágenes desde el directorio de uploads.

    Args:
        image_path: Ruta relativa de la imagen desde uploads/
                   (ej: "nelore/nelore_213.jpg")

    Returns:
        FileResponse con el archivo de imagen

    Raises:
        HTTPException 404: Si la imagen no existe
        HTTPException 400: Si el path es inválido (path traversal)
    """
    # Obtener directorio de uploads
    uploads_dir = ensure_uploads_directory()

    # Normalizar el path y prevenir path traversal
    # Remover barras iniciales y normalizar
    normalized_path = image_path.lstrip("/").replace("\\", "/")

    # Construir path completo
    image_file = uploads_dir / normalized_path

    # Verificar que el archivo esté dentro del directorio uploads (prevenir path traversal)
    try:
        image_file.resolve().relative_to(uploads_dir.resolve())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Path inválido: intento de acceso fuera del directorio permitido",
        )

    # Verificar que el archivo existe
    if not image_file.exists() or not image_file.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Imagen no encontrada: {image_path}",
        )

    # Determinar Content-Type basado en extensión
    content_type = "image/jpeg"  # Por defecto JPEG
    suffix = image_file.suffix.lower()
    if suffix in [".png"]:
        content_type = "image/png"
    elif suffix in [".gif"]:
        content_type = "image/gif"
    elif suffix in [".webp"]:
        content_type = "image/webp"

    # Retornar archivo con headers apropiados
    return FileResponse(
        path=str(image_file),
        media_type=content_type,
        headers={
            "Cache-Control": "public, max-age=31536000",  # Cache por 1 año
        },
    )
