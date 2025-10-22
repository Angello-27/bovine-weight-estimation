"""
Constantes de Razas Bovinas - Hacienda Gamelera
8 razas exactas (ACTUALIZADO según información de Bruno Brito Macedo)
San Ignacio de Velasco, Santa Cruz, Bolivia
"""

from enum import Enum
from typing import Literal


class BreedType(str, Enum):
    """
    8 razas bovinas de Hacienda Gamelera.

    IMPORTANTE: Estas son las ÚNICAS razas válidas en el sistema.
    Prioridad: Brahman, Nelore, Angus (más datos disponibles)
    """

    BRAHMAN = "brahman"  # Bos indicus, muy común en Chiquitanía
    NELORE = "nelore"  # Bos indicus, 80% del Pantanal
    ANGUS = "angus"  # Bos taurus, carne de calidad
    CEBUINAS = "cebuinas"  # Bos indicus general (agrupa varias razas zebu)
    CRIOLLO = "criollo"  # Criollo Chaqueño, adaptado local
    PARDO_SUIZO = "pardo_suizo"  # Bos taurus grande
    GUZERAT = "guzerat"  # Bos indicus, lechero y carne (reemplaza Jersey)
    HOLSTEIN = "holstein"  # Lechera, común en región

    @classmethod
    def is_valid(cls, breed: str) -> bool:
        """Valida si la raza es una de las 8 exactas."""
        try:
            cls(breed)
            return True
        except ValueError:
            return False

    @classmethod
    def get_display_name(cls, breed: "BreedType") -> str:
        """Retorna nombre para mostrar en UI (español)."""
        display_names = {
            cls.BRAHMAN: "Brahman",
            cls.NELORE: "Nelore",
            cls.ANGUS: "Angus",
            cls.CEBUINAS: "Cebuinas (Bos indicus)",
            cls.CRIOLLO: "Criollo Chaqueño",
            cls.PARDO_SUIZO: "Pardo Suizo",
            cls.GUZERAT: "Guzerat",
            cls.HOLSTEIN: "Holstein",
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
    "brahman",
    "nelore",
    "angus",
    "cebuinas",
    "criollo",
    "pardo_suizo",
    "guzerat",
    "holstein",
]

# Mapeos útiles
BREED_DISPLAY_NAMES = {
    BreedType.BRAHMAN: "Brahman",
    BreedType.NELORE: "Nelore",
    BreedType.ANGUS: "Angus",
    BreedType.CEBUINAS: "Cebuinas (Bos indicus)",
    BreedType.CRIOLLO: "Criollo Chaqueño",
    BreedType.PARDO_SUIZO: "Pardo Suizo",
    BreedType.GUZERAT: "Guzerat",
    BreedType.HOLSTEIN: "Holstein",
}

BREED_MODEL_FILENAMES = {
    BreedType.BRAHMAN: "brahman-v1.0.0.tflite",
    BreedType.NELORE: "nelore-v1.0.0.tflite",
    BreedType.ANGUS: "angus-v1.0.0.tflite",
    BreedType.CEBUINAS: "cebuinas-v1.0.0.tflite",
    BreedType.CRIOLLO: "criollo-v1.0.0.tflite",
    BreedType.PARDO_SUIZO: "pardo_suizo-v1.0.0.tflite",
    BreedType.GUZERAT: "guzerat-v1.0.0.tflite",
    BreedType.HOLSTEIN: "holstein-v1.0.0.tflite",
}

# Razas prioritarias (más datos disponibles)
PRIORITY_BREEDS = [
    BreedType.BRAHMAN,
    BreedType.NELORE,
    BreedType.ANGUS,
]

# Clasificación por especie
BOS_INDICUS_BREEDS = [
    BreedType.BRAHMAN,
    BreedType.NELORE,
    BreedType.CEBUINAS,
    BreedType.GUZERAT,
]

BOS_TAURUS_BREEDS = [
    BreedType.ANGUS,
    BreedType.CRIOLLO,
    BreedType.PARDO_SUIZO,
    BreedType.HOLSTEIN,
]
