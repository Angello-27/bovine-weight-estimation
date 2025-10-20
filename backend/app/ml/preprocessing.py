"""
Image Preprocessing for ML Inference
Preprocesamiento de imágenes para modelos TFLite

Single Responsibility: Transformar imágenes a formato esperado por modelos
"""

import io

import numpy as np
from PIL import Image


class ImagePreprocessor:
    """
    Preprocesador de imágenes para modelos ML.

    Convierte imagen raw (JPEG/PNG) a tensor numpy (224x224x3) normalizado.
    """

    # Configuración de entrada de modelos
    INPUT_SIZE = (224, 224)  # Tamaño esperado por MobileNetV2
    INPUT_CHANNELS = 3  # RGB
    NORMALIZATION_MEAN = [0.485, 0.456, 0.406]  # ImageNet mean
    NORMALIZATION_STD = [0.229, 0.224, 0.225]  # ImageNet std

    @classmethod
    def preprocess_from_bytes(cls, image_bytes: bytes) -> np.ndarray:
        """
        Preprocesa imagen desde bytes.

        Args:
            image_bytes: Bytes de imagen (JPEG/PNG)

        Returns:
            numpy array (1, 224, 224, 3) float32 normalizado

        Raises:
            ValueError: Si la imagen es inválida
        """
        try:
            # Cargar imagen desde bytes
            image = Image.open(io.BytesIO(image_bytes))

            # Convertir a RGB (por si es RGBA o escala de grises)
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Preprocesar
            return cls.preprocess_from_pil(image)

        except Exception as e:
            raise ValueError(f"Error al cargar imagen: {str(e)}")

    @classmethod
    def preprocess_from_pil(cls, image: Image.Image) -> np.ndarray:
        """
        Preprocesa imagen PIL.

        Args:
            image: Imagen PIL en formato RGB

        Returns:
            numpy array (1, 224, 224, 3) float32 normalizado
        """
        # Resize a 224x224
        image = image.resize(cls.INPUT_SIZE, Image.Resampling.BILINEAR)

        # Convertir a numpy array (224, 224, 3) uint8 [0-255]
        img_array = np.array(image, dtype=np.float32)

        # Normalizar a [0-1]
        img_array = img_array / 255.0

        # Normalizar con ImageNet statistics
        img_array = cls._normalize(img_array)

        # Expandir dimensión de batch (1, 224, 224, 3)
        return np.expand_dims(img_array, axis=0)


    @classmethod
    def _normalize(cls, img_array: np.ndarray) -> np.ndarray:
        """
        Normaliza con ImageNet mean/std.

        Args:
            img_array: Array (224, 224, 3) float32 [0-1]

        Returns:
            Array normalizado
        """
        mean = np.array(cls.NORMALIZATION_MEAN, dtype=np.float32)
        std = np.array(cls.NORMALIZATION_STD, dtype=np.float32)

        # Broadcasting: (224, 224, 3) - (3,) / (3,)
        return (img_array - mean) / std


    @classmethod
    def validate_image_size(cls, image: Image.Image) -> bool:
        """
        Valida que la imagen tenga tamaño mínimo aceptable.

        Args:
            image: Imagen PIL

        Returns:
            True si es válida (≥224x224)
        """
        width, height = image.size
        return width >= cls.INPUT_SIZE[0] and height >= cls.INPUT_SIZE[1]

