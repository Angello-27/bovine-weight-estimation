"""
ML Model Loader
Carga y gestión de modelos TensorFlow/TFLite

Single Responsibility: Cargar modelos ML en memoria
"""

from pathlib import Path
from typing import Optional

import numpy as np

try:
    import tflite_runtime.interpreter as tflite
    TFLITE_AVAILABLE = True
except ImportError:
    # Fallback para desarrollo (si no está instalado)
    tflite = None
    TFLITE_AVAILABLE = False

from ..core.config import settings
from ..core.constants import BreedType
from ..core.errors import MLModelException


class MLModelLoader:
    """
    Loader de modelos ML (TensorFlow/TFLite).

    Singleton pattern para mantener modelos en memoria.
    Soporta 7 modelos específicos por raza.
    """

    _instance: Optional["MLModelLoader"] = None
    _models_cache: dict[BreedType, any] = {}  # Cache de modelos cargados

    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Inicializa loader."""
        self.models_path = Path(settings.ML_MODELS_PATH)
        self.models_path.mkdir(parents=True, exist_ok=True)
        self.model_loaded = False

    def load_generic_model(self) -> any:
        """
        Carga modelo genérico TFLite (para todas las razas).
        
        El modelo exportado desde Colab es genérico y funciona para todas las razas.

        Returns:
            Diccionario con interpreter TFLite y metadatos

        Raises:
            MLModelException: Si el modelo no se puede cargar
        """
        # Verificar cache
        if "generic" in self._models_cache:
            return self._models_cache["generic"]

        # Construir path del modelo genérico
        model_filename = settings.ML_DEFAULT_MODEL
        model_path = self.models_path / model_filename

        # Verificar que existe
        if not model_path.exists():
            raise MLModelException(
                f"Modelo TFLite no encontrado: {model_path}. "
                f"Descarga el modelo desde Colab/Drive a: {self.models_path}/. "
                f"Ver guía: backend/INTEGRATION_GUIDE.md"
            )

        try:
            # Verificar que TFLite está disponible
            if not TFLITE_AVAILABLE:
                raise MLModelException(
                    "tensorflow-lite-runtime no instalado. "
                    "Ejecuta: pip install tensorflow-lite-runtime"
                )

            # Cargar TFLite Interpreter
            interpreter = tflite.Interpreter(model_path=str(model_path))
            interpreter.allocate_tensors()

            # Obtener input/output details
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()

            print(f"✅ Modelo TFLite cargado: {model_filename}")
            print(f"   Input shape: {input_details[0]['shape']}")
            print(f"   Output shape: {output_details[0]['shape']}")

            # Crear diccionario con modelo y metadatos
            model_data = {
                "interpreter": interpreter,
                "input_details": input_details,
                "output_details": output_details,
                "version": "1.0.0",
                "path": str(model_path),
                "loaded": True,
            }

            # Cachear
            self._models_cache["generic"] = model_data
            self.model_loaded = True

            return model_data

        except MLModelException:
            raise
        except Exception as e:
            raise MLModelException(f"Error al cargar modelo TFLite: {str(e)}")

    def load_model(self, breed: BreedType) -> any:
        """
        Carga modelo TFLite (usa modelo genérico para todas las razas).
        
        Por ahora, el modelo exportado desde Colab es genérico.
        En el futuro, puede haber modelos específicos por raza.

        Args:
            breed: Raza del animal (usado para validación)

        Returns:
            Modelo genérico cargado

        Raises:
            MLModelException: Si el modelo no se puede cargar
        """
        # Por ahora, usar modelo genérico para todas las razas
        return self.load_generic_model()

    def load_all_models(self) -> dict[str, any]:
        """
        Carga modelo genérico TFLite (por ahora solo hay uno genérico).

        Returns:
            Diccionario con modelo genérico cargado

        Raises:
            MLModelException: Si el modelo falla
        """
        try:
            generic_model = self.load_generic_model()
            return {"generic": generic_model}
        except MLModelException as e:
            raise MLModelException(
                f"No se pudo cargar modelo TFLite: {e.message}. "
                f"Verifica que exista en: {self.models_path}/"
            )

    def is_model_loaded(self, breed: BreedType | None = None) -> bool:
        """
        Verifica si un modelo está cargado.

        Args:
            breed: Raza a verificar (opcional, por ahora usa modelo genérico)

        Returns:
            True si está en cache
        """
        return "generic" in self._models_cache

    def get_loaded_breeds(self) -> list[str]:
        """
        Obtiene lista de modelos cargados.

        Returns:
            Lista de nombres de modelos (por ahora solo "generic")
        """
        return list(self._models_cache.keys())

    def unload_model(self, breed: BreedType | None = None) -> None:
        """
        Descarga modelo de memoria.

        Args:
            breed: Raza del modelo a descargar (opcional, por ahora solo hay genérico)
        """
        if "generic" in self._models_cache:
            del self._models_cache["generic"]
            print("🗑️ Modelo genérico descargado de memoria")

    def unload_all_models(self) -> None:
        """Descarga todos los modelos de memoria."""
        self._models_cache.clear()
        self.model_loaded = False
        print("🗑️ Todos los modelos descargados")
