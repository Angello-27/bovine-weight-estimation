"""
Image Storage Utils - Core Layer
Utilidades para guardar y gestionar imágenes en el sistema de archivos

Single Responsibility: Funciones auxiliares para almacenamiento de imágenes
"""

import io
from datetime import datetime
from pathlib import Path
from uuid import UUID, uuid4

from PIL import Image


def ensure_uploads_directory() -> Path:
    """
    Asegura que el directorio de uploads existe.

    Returns:
        Path: Ruta del directorio de uploads
    """
    # Obtener el directorio base del proyecto (subir 3 niveles desde este archivo)
    # backend/app/core/utils/image_storage.py -> backend/uploads
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent.parent
    uploads_dir = project_root / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)
    return uploads_dir


def save_animal_photo(
    image_bytes: bytes,
    animal_id: UUID | str,
    breed: str | None = None,
    filename: str | None = None,
) -> str:
    """
    Guarda la foto de un animal en backend/uploads.

    Estructura de directorios:
    - backend/uploads/{breed}/animal_{animal_id}_{timestamp}.jpg

    Args:
        image_bytes: Bytes de la imagen
        animal_id: ID del animal
        breed: Raza del animal (opcional, para organizar por carpeta)
        filename: Nombre del archivo (opcional, se genera automáticamente si no se proporciona)

    Returns:
        str: Path relativo de la imagen guardada (ej: "brahman/animal_123_20240101.jpg")
    """
    # Asegurar que el directorio existe
    uploads_dir = ensure_uploads_directory()

    # Crear subdirectorio por raza si se proporciona
    if breed:
        breed_dir = uploads_dir / breed.lower()
        breed_dir.mkdir(parents=True, exist_ok=True)
        target_dir = breed_dir
    else:
        target_dir = uploads_dir

    # Generar nombre de archivo si no se proporciona
    if not filename:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        animal_id_str = str(animal_id).replace("-", "")[:8]
        filename = f"animal_{animal_id_str}_{timestamp}.jpg"

    # Asegurar extensión .jpg
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        filename = f"{filename}.jpg"

    # Path completo del archivo
    file_path = target_dir / filename

    # Guardar imagen
    image = Image.open(io.BytesIO(image_bytes))
    # Convertir a RGB si es necesario (para PNG con transparencia)
    if image.mode in ("RGBA", "P"):
        rgb_image = Image.new("RGB", image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
        image = rgb_image

    # Guardar como JPEG
    image.save(file_path, "JPEG", quality=85, optimize=True)

    # Retornar path relativo desde backend/uploads
    if breed:
        return f"{breed.lower()}/{filename}"
    return filename


def save_estimation_frame(
    image_bytes: bytes,
    animal_id: UUID | str | None = None,
    breed: str | None = None,
    estimation_id: UUID | str | None = None,
) -> str:
    """
    Guarda el frame/foto usado para una estimación de peso en backend/uploads.

    Estructura de directorios:
    - backend/uploads/{breed}/estimation_{estimation_id}_{timestamp}.jpg
    - backend/uploads/estimations/estimation_{estimation_id}_{timestamp}.jpg (si no hay raza)

    Args:
        image_bytes: Bytes de la imagen
        animal_id: ID del animal (opcional)
        breed: Raza del animal (opcional, para organizar por carpeta)
        estimation_id: ID de la estimación (opcional, se genera UUID si no se proporciona)

    Returns:
        str: Path relativo de la imagen guardada
    """
    # Asegurar que el directorio existe
    uploads_dir = ensure_uploads_directory()

    # Generar ID de estimación si no se proporciona
    if not estimation_id:
        estimation_id = uuid4()

    # Crear subdirectorio por raza si se proporciona
    if breed:
        breed_dir = uploads_dir / breed.lower()
        breed_dir.mkdir(parents=True, exist_ok=True)
        target_dir = breed_dir
        subdir = breed.lower()
    else:
        # Si no hay raza, usar carpeta "estimations"
        estimations_dir = uploads_dir / "estimations"
        estimations_dir.mkdir(parents=True, exist_ok=True)
        target_dir = estimations_dir
        subdir = "estimations"

    # Generar nombre de archivo
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    estimation_id_str = str(estimation_id).replace("-", "")[:8]
    animal_id_str = f"_{str(animal_id).replace('-', '')[:8]}" if animal_id else ""
    filename = f"estimation_{estimation_id_str}{animal_id_str}_{timestamp}.jpg"

    # Path completo del archivo
    file_path = target_dir / filename

    # Guardar imagen
    image = Image.open(io.BytesIO(image_bytes))
    # Convertir a RGB si es necesario
    if image.mode in ("RGBA", "P"):
        rgb_image = Image.new("RGB", image.size, (255, 255, 255))
        rgb_image.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
        image = rgb_image

    # Guardar como JPEG
    image.save(file_path, "JPEG", quality=85, optimize=True)

    # Retornar path relativo desde backend/uploads
    return f"{subdir}/{filename}"


def get_image_path(relative_path: str) -> Path:
    """
    Obtiene el path absoluto de una imagen desde su path relativo.

    Args:
        relative_path: Path relativo desde backend/uploads (ej: "brahman/animal_123.jpg")

    Returns:
        Path: Path absoluto del archivo
    """
    uploads_dir = ensure_uploads_directory()
    return uploads_dir / relative_path


def image_exists(relative_path: str) -> bool:
    """
    Verifica si una imagen existe en el sistema de archivos.

    Args:
        relative_path: Path relativo desde backend/uploads

    Returns:
        bool: True si la imagen existe, False en caso contrario
    """
    file_path = get_image_path(relative_path)
    return file_path.exists() and file_path.is_file()
