"""
Constantes de Razas Bovinas - Hacienda Gamelera
7 razas tropicales priorizadas (ACTUALIZADO según entrenamiento ML)
San Ignacio de Velasco, Santa Cruz, Bolivia

Razas alineadas con el modelo ML entrenado en Colab.
"""

from enum import Enum
from typing import Literal


class BreedType(str, Enum):
    """
    7 razas bovinas tropicales priorizadas para Santa Cruz.

    IMPORTANTE: Estas son las ÚNICAS razas válidas en el sistema.
    Alineadas con el modelo ML entrenado en Colab (BLOQUE 0-16).

    Prioridad: Nelore (42% del hato), Brahman, Guzerat
    """

    NELORE = "nelore"  # Carne tropical dominante en Santa Cruz (≈42% del hato)
    BRAHMAN = "brahman"  # Cebuino versátil para cruzamientos y climas extremos
    GUZERAT = "guzerat"  # Doble propósito (carne/leche) con gran rusticidad materna
    SENEPOL = "senepol"  # Carne premium adaptada al calor, ideal para "steer" de alta calidad
    GIROLANDO = "girolando"  # Lechera tropical (Holstein × Gyr) muy difundida en sistemas semi-intensivos
    GYR_LECHERO = "gyr_lechero"  # Lechera pura clave para genética tropical y sólidos altos
    SINDI = "sindi"  # Lechera tropical compacta, de alta fertilidad y leche rica en sólidos

    @classmethod
    def is_valid(cls, breed: str) -> bool:
        """Valida si la raza es una de las 7 exactas."""
        try:
            cls(breed)
            return True
        except ValueError:
            return False

    @classmethod
    def get_display_name(cls, breed: "BreedType") -> str:
        """Retorna nombre para mostrar en UI (español)."""
        display_names = {
            cls.NELORE: "Nelore",
            cls.BRAHMAN: "Brahman",
            cls.GUZERAT: "Guzerat",
            cls.SENEPOL: "Senepol",
            cls.GIROLANDO: "Girolando",
            cls.GYR_LECHERO: "Gyr Lechero",
            cls.SINDI: "Sindi",
        }
        return display_names[breed]

    def get_model_filename(self) -> str:
        """Retorna nombre del archivo modelo TFLite."""
        return f"{self.value}-v1.0.0.tflite"


class BovineSpecies(str, Enum):
    """Clasificación taxonómica de bovinos."""

    BOS_INDICUS = "bos_indicus"  # Razas cebuinas
    BOS_TAURUS = "bos_taurus"  # Razas europeas


# Type alias para validación
BreedTypeLiteral = Literal[
    "nelore",
    "brahman",
    "guzerat",
    "senepol",
    "girolando",
    "gyr_lechero",
    "sindi",
]

# Mapeos útiles
BREED_DISPLAY_NAMES = {
    BreedType.NELORE: "Nelore",
    BreedType.BRAHMAN: "Brahman",
    BreedType.GUZERAT: "Guzerat",
    BreedType.SENEPOL: "Senepol",
    BreedType.GIROLANDO: "Girolando",
    BreedType.GYR_LECHERO: "Gyr Lechero",
    BreedType.SINDI: "Sindi",
}

# Mapeo de nombres de archivos de modelos TFLite por raza
# NOTA: Actualmente usamos un modelo genérico (generic-cattle-v1.0.0.tflite)
# que funciona para todas las razas. Este diccionario es para uso futuro
# cuando se implementen modelos específicos por raza (fine-tuning).
BREED_MODEL_FILENAMES = {
    BreedType.NELORE: "nelore-v1.0.0.tflite",
    BreedType.BRAHMAN: "brahman-v1.0.0.tflite",
    BreedType.GUZERAT: "guzerat-v1.0.0.tflite",
    BreedType.SENEPOL: "senepol-v1.0.0.tflite",
    BreedType.GIROLANDO: "girolando-v1.0.0.tflite",
    BreedType.GYR_LECHERO: "gyr_lechero-v1.0.0.tflite",
    BreedType.SINDI: "sindi-v1.0.0.tflite",
}

# Razas prioritarias (más datos disponibles - según distribución en Santa Cruz)
PRIORITY_BREEDS = [
    BreedType.NELORE,  # 42% del hato
    BreedType.BRAHMAN,  # Versátil para cruzamientos
    BreedType.GUZERAT,  # Doble propósito
]

# Clasificación por propósito
MEAT_BREEDS = [
    BreedType.NELORE,
    BreedType.BRAHMAN,
    BreedType.SENEPOL,
]

DAIRY_BREEDS = [
    BreedType.GIROLANDO,
    BreedType.GYR_LECHERO,
    BreedType.SINDI,
]

DUAL_PURPOSE_BREEDS = [
    BreedType.GUZERAT,  # Doble propósito (carne/leche)
]
