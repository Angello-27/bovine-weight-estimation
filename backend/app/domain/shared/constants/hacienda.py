"""
Hacienda Gamelera Constants
Constantes reales de Hacienda Gamelera (Bruno Brito Macedo)
"""


class HaciendaConstants:
    """
    Constantes de Hacienda Gamelera - San Ignacio de Velasco, Bolivia.

    Datos proporcionados por Bruno Brito Macedo.
    """

    # Información básica
    HACIENDA_NAME = "Hacienda Gamelera"
    OWNER_NAME = "Bruno Brito Macedo"
    LOCATION = "San Ignacio de Velasco, Santa Cruz, Bolivia"

    # Coordenadas GPS (15°51′34.2′′S, 60°47′52.4′′W)
    LATITUDE = -15.859500
    LONGITUDE = -60.797889
    GPS_FORMATTED = "15°51′34.2″S, 60°47′52.4″W"

    # Capacidad
    ANIMAL_CAPACITY = 500  # 500 cabezas
    AREA_HECTARES = 48.5  # 48.5 hectáreas

    @staticmethod
    def schaeffer_formula(perimeter_cm: float, length_cm: float) -> float:
        """
        Fórmula Schaeffer tradicional (método actual de Bruno).

        Fórmula: Peso (kg) = (PT² × LC) / 10,838

        Args:
            perimeter_cm: Perímetro torácico en centímetros
            length_cm: Longitud corporal en centímetros

        Returns:
            Peso estimado en kilogramos

        Note:
            Error típico: ±5-20 kg
            Nuestro objetivo: <5 kg con IA (mejora 75%)
        """
        if perimeter_cm <= 0 or length_cm <= 0:
            raise ValueError("Perímetro y longitud deben ser positivos")

        return (perimeter_cm**2 * length_cm) / 10838

    @staticmethod
    def is_within_bounds(latitude: float, longitude: float) -> bool:
        """
        Verifica si coordenadas GPS están dentro de Hacienda Gamelera.

        Args:
            latitude: Latitud GPS
            longitude: Longitud GPS

        Returns:
            True si está dentro de un radio razonable (~5 km)
        """
        # Radio simple de 0.05 grados (~5 km)
        lat_diff = abs(latitude - HaciendaConstants.LATITUDE)
        lon_diff = abs(longitude - HaciendaConstants.LONGITUDE)

        return lat_diff < 0.05 and lon_diff < 0.05
