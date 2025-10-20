"""
Age Categories Constants
4 categorías de edad EXACTAS para Hacienda Gamelera
NO MODIFICAR sin autorización de Bruno Brito Macedo
"""

from datetime import datetime
from enum import Enum


class AgeCategory(str, Enum):
    """
    4 categorías de edad bovinas para Hacienda Gamelera.

    Definidas por Bruno Brito Macedo según prácticas ganaderas locales.
    Usadas para: clasificación automática, reportes SENASAG, análisis GDP.
    """

    TERNEROS = "terneros"  # <8 meses
    VAQUILLONAS_TORILLOS = "vaquillonas_torillos"  # 6-18 meses
    VAQUILLONAS_TORETES = "vaquillonas_toretes"  # 19-30 meses
    VACAS_TOROS = "vacas_toros"  # >30 meses

    @classmethod
    def from_birth_date(cls, birth_date: datetime) -> "AgeCategory":
        """
        Calcula categoría de edad desde fecha de nacimiento.

        Args:
            birth_date: Fecha de nacimiento del animal

        Returns:
            AgeCategory correspondiente según edad en meses

        Examples:
            >>> AgeCategory.from_birth_date(datetime(2024, 4, 1))  # 6 meses
            AgeCategory.TERNEROS
        """
        now = datetime.now()
        age_months = (now.year - birth_date.year) * 12 + (now.month - birth_date.month)

        if age_months < 8:
            return cls.TERNEROS
        if 6 <= age_months <= 18:
            return cls.VAQUILLONAS_TORILLOS
        if 19 <= age_months <= 30:
            return cls.VAQUILLONAS_TORETES
        return cls.VACAS_TOROS

    @classmethod
    def from_age_months(cls, age_months: int) -> "AgeCategory":
        """
        Calcula categoría desde edad en meses.

        Args:
            age_months: Edad del animal en meses

        Returns:
            AgeCategory correspondiente
        """
        if age_months < 8:
            return cls.TERNEROS
        if 6 <= age_months <= 18:
            return cls.VAQUILLONAS_TORILLOS
        if 19 <= age_months <= 30:
            return cls.VAQUILLONAS_TORETES
        return cls.VACAS_TOROS

    @property
    def display_name(self) -> str:
        """Nombre para mostrar en UI."""
        return AGE_CATEGORY_DISPLAY_NAMES[self]

    @property
    def range_description(self) -> str:
        """Descripción del rango de edad."""
        return AGE_CATEGORY_RANGES[self][2]


# Mapeos de categorías
AGE_CATEGORY_DISPLAY_NAMES: dict[AgeCategory, str] = {
    AgeCategory.TERNEROS: "Terneros",
    AgeCategory.VAQUILLONAS_TORILLOS: "Vaquillonas/Torillos",
    AgeCategory.VAQUILLONAS_TORETES: "Vaquillonas/Toretes",
    AgeCategory.VACAS_TOROS: "Vacas/Toros",
}

# Rangos: (min_months, max_months, description)
AGE_CATEGORY_RANGES: dict[AgeCategory, tuple[int, int | None, str]] = {
    AgeCategory.TERNEROS: (0, 8, "<8 meses"),
    AgeCategory.VAQUILLONAS_TORILLOS: (6, 18, "6-18 meses"),
    AgeCategory.VAQUILLONAS_TORETES: (19, 30, "19-30 meses"),
    AgeCategory.VACAS_TOROS: (30, None, ">30 meses"),
}
