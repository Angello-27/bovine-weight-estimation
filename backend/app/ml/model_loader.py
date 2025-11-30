"""
ML Model Loader
Carga y gestión de modelos TensorFlow/TFLite

Single Responsibility: Cargar modelos ML en memoria
"""

import logging
import os
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
from typing import Any, Optional

from ..core.config import settings
from ..core.exceptions import MLModelException
from ..domain.shared.constants import BreedType

# Suprimir mensajes informativos de TensorFlow antes de importarlo
os.environ["TF_CPP_MIN_LOG_LEVEL"] = (
    "3"  # 0=all, 1=info, 2=warnings, 3=errors (solo errors críticos)
)

# Suprimir logs de TensorFlow a nivel de Python también
logging.getLogger("tensorflow").setLevel(logging.ERROR)
logging.getLogger("tflite_runtime").setLevel(logging.ERROR)

# Declarar variables globales con tipos explícitos
TFLITE_AVAILABLE: bool = False
TFLITE_SOURCE: str | None = None

try:
    import tflite_runtime.interpreter as tflite  # type: ignore[import-untyped, import-not-found, import]

    TFLITE_AVAILABLE = True
    TFLITE_SOURCE = "tflite_runtime"
except ImportError:
    # Fallback: usar TensorFlow completo (funciona en macOS y otros sistemas)
    try:
        import tensorflow as tf  # type: ignore[import-untyped]

        # TensorFlow completo tiene soporte para TFLite
        class TFLiteWrapper:
            """Wrapper para usar tf.lite.Interpreter como tflite_runtime.interpreter"""

            @staticmethod
            def Interpreter(model_path: str):  # type: ignore[misc]  # noqa: N802
                """Crea un Interpreter de TensorFlow Lite."""
                return tf.lite.Interpreter(model_path=model_path)

        tflite = TFLiteWrapper()  # type: ignore[assignment]
        TFLITE_AVAILABLE = True
        TFLITE_SOURCE = "tensorflow"
        print(
            "✅ Usando TensorFlow completo para cargar modelos TFLite (tflite_runtime no disponible)"
        )
    except ImportError:
        # Sin TensorFlow ni tflite_runtime
        tflite = None  # type: ignore[assignment]
        TFLITE_AVAILABLE = False
        TFLITE_SOURCE = None


class MLModelLoader:
    """
    Loader de modelos ML (TensorFlow/TFLite).

    Singleton pattern para mantener modelos en memoria.
    Soporta 7 modelos específicos por raza.
    """

    _instance: Optional["MLModelLoader"] = None
    _models_cache: dict[str, dict[str, Any]] = (
        {}
    )  # Cache de modelos cargados (key: "generic" o breed.value)

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

    def load_generic_model(self) -> dict[str, Any]:
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
            # Verificar que TFLite está disponible (runtime o TensorFlow completo)
            if not TFLITE_AVAILABLE:
                raise MLModelException(
                    "TensorFlow o tensorflow-lite-runtime no instalado. "
                    "Ejecuta: pip install tensorflow"
                )

            # Cargar TFLite Interpreter
            # Nota: TensorFlow Lite puede imprimir mensajes INFO/WARNING durante la carga,
            # estos son normales y no indican errores (delegados, optimizaciones, etc.)
            if tflite is None:
                raise MLModelException("TFLite runtime no disponible")

            # Redirigir temporalmente stderr para suprimir mensajes de carga del modelo
            stderr_buffer = StringIO()
            with redirect_stderr(stderr_buffer):
                interpreter = tflite.Interpreter(model_path=str(model_path))  # type: ignore[union-attr]
                interpreter.allocate_tensors()  # type: ignore[union-attr]

            # Obtener input/output details
            input_details = interpreter.get_input_details()  # type: ignore[union-attr]
            output_details = interpreter.get_output_details()  # type: ignore[union-attr]

            print(f"✅ Modelo TFLite cargado: {model_filename}")
            print(f"   Input shape: {input_details[0]['shape']}")
            print(f"   Output shape: {output_details[0]['shape']}")
            print(f"   Path: {model_path}")

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

    def load_model(self, breed: BreedType) -> dict[str, Any]:
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

    def load_all_models(self) -> dict[str, dict[str, Any]]:
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
                f"No se pudo cargar modelo TFLite: {str(e)}. "
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
            self.model_loaded = False
            print("🗑️ Modelo genérico descargado de memoria")

    def unload_all_models(self) -> None:
        """Descarga todos los modelos de memoria."""
        self._models_cache.clear()
        self.model_loaded = False
        print("🗑️ Todos los modelos descargados")
