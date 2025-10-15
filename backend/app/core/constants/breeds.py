"""
Constantes de Razas Bovinas - Hacienda Gamelera
7 razas exactas (NO MODIFICAR sin autorización de Bruno Brito Macedo)
"""

from enum import Enum
from typing import Literal


class BreedType(str, Enum):
    """
    7 razas bovinas de Hacienda Gamelera.
    
    IMPORTANTE: Estas son las ÚNICAS razas válidas en el sistema.
    """
    
    BRAHMAN = "brahman"  # Bos indicus
    NELORE = "nelore"  # Bos indicus
    ANGUS = "angus"  # Bos taurus
    CEBUINAS = "cebuinas"  # Bos indicus
    CRIOLLO = "criollo"  # Bos taurus
    PARDO_SUIZO = "pardo_suizo"  # Bos taurus
    JERSEY = "jersey"  # Bos taurus

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
            cls.BRAHMAN: "Brahman",
            cls.NELORE: "Nelore",
            cls.ANGUS: "Angus",
            cls.CEBUINAS: "Cebuinas (Bos indicus)",
            cls.CRIOLLO: "Criollo (Bos taurus)",
            cls.PARDO_SUIZO: "Pardo Suizo",
            cls.JERSEY: "Jersey",
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
    "jersey",
]

