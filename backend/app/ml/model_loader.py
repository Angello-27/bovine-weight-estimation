"""
ML Model Loader
Carga y gestión de modelos TensorFlow/TFLite

Single Responsibility: Cargar modelos ML en memoria
"""

from pathlib import Path
from typing import Optional

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
        self.models_path = Path("ml_models")  # Ruta a modelos
        self.model_loaded = False

    def load_model(self, breed: BreedType) -> any:
        """
        Carga modelo TFLite para una raza específica.

        Args:
            breed: Raza del animal (una de las 7)

        Returns:
            Modelo cargado (TFLite Interpreter o Keras Model)

        Raises:
            MLModelException: Si el modelo no se puede cargar
        """
        # Verificar si ya está en cache
        if breed in self._models_cache:
            return self._models_cache[breed]

        # Construir path del modelo
        model_filename = f"{breed.value}-v1.0.0.tflite"
        model_path = self.models_path / model_filename

        # Verificar que existe
        if not model_path.exists():
            raise MLModelException(
                f"Modelo TFLite no encontrado: {model_path}. "
                f"Raza: {breed.value}. "
                f"Los 7 modelos deben estar en: {self.models_path}/"
            )

        try:
            # Por ahora, retornamos un modelo mock
            # TODO: Implementar carga real de TFLite cuando tengamos modelos
            print(f"⚠️ MODO MVP: Usando modelo mock para {breed.value}")
            print(f"   Path esperado: {model_path}")

            # Mock model (diccionario simple)
            mock_model = {
                "breed": breed,
                "version": "1.0.0-mock",
                "loaded": True,
                "path": str(model_path),
            }

            # Cachear
            self._models_cache[breed] = mock_model
            self.model_loaded = True

            return mock_model

        except Exception as e:
            raise MLModelException(
                f"Error al cargar modelo {breed.value}: {str(e)}"
            )

    def load_all_models(self) -> dict[BreedType, any]:
        """
        Carga todos los 7 modelos TFLite.

        Returns:
            Diccionario de modelos cargados por raza

        Raises:
            MLModelException: Si algún modelo falla
        """
        models = {}

        for breed in BreedType:
            try:
                models[breed] = self.load_model(breed)
                print(f"✅ Modelo {breed.value} cargado")
            except MLModelException as e:
                print(f"❌ Error cargando {breed.value}: {e.message}")
                # Continuar con los demás
                continue

        if not models:
            raise MLModelException(
                "No se pudo cargar ningún modelo TFLite. "
                "Verifica que existan en: ml_models/"
            )

        return models

    def is_model_loaded(self, breed: BreedType) -> bool:
        """
        Verifica si un modelo está cargado.

        Args:
            breed: Raza a verificar

        Returns:
            True si está en cache
        """
        return breed in self._models_cache

    def get_loaded_breeds(self) -> list[BreedType]:
        """
        Obtiene lista de razas con modelos cargados.

        Returns:
            Lista de BreedType
        """
        return list(self._models_cache.keys())

    def unload_model(self, breed: BreedType) -> None:
        """
        Descarga un modelo de memoria.

        Args:
            breed: Raza del modelo a descargar
        """
        if breed in self._models_cache:
            del self._models_cache[breed]
            print(f"🗑️ Modelo {breed.value} descargado de memoria")

    def unload_all_models(self) -> None:
        """Descarga todos los modelos de memoria."""
        self._models_cache.clear()
        self.model_loaded = False
        print("🗑️ Todos los modelos descargados")

