"""
System Metrics Constants
Métricas obligatorias del sistema (NO MODIFICAR)
Definidas en docs/vision/02-architecture-vision.md
"""


class SystemMetrics:
    """
    Métricas obligatorias del sistema de estimación de peso.

    Estas métricas son CRÍTICAS para el valor del proyecto vs método tradicional.
    Validadas con Bruno Brito Macedo.
    """

    # Precisión ML (US-002)
    MIN_PRECISION_R2 = 0.95  # R² ≥ 0.95 (95% precisión)
    MAX_ERROR_KG = 5.0  # Error absoluto <5 kg
    MIN_CONFIDENCE = 0.80  # Confidence mínimo aceptable (80%)
    RECOMMENDED_CONFIDENCE = 0.90  # Confidence recomendado (90%)

    # Performance (US-002)
    MAX_PROCESSING_TIME_MS = 3000  # <3 segundos procesamiento
    MAX_PROCESSING_TIME_S = 3.0

    # Captura (US-001)
    TARGET_FPS_MIN = 10  # 10-15 FPS
    TARGET_FPS_MAX = 15
    CAPTURE_DURATION_MIN_S = 3  # 3-5 segundos
    CAPTURE_DURATION_MAX_S = 5

    # Sincronización (US-005)
    SYNC_BATCH_SIZE = 100  # Máximo items por batch
    SYNC_TIMEOUT_S = 30  # Timeout sincronización
    SYNC_RETRY_BACKOFF = [5, 15, 30, 60, 300]  # Backoff en segundos


class CaptureConstants:
    """
    Constantes para captura continua de fotogramas (US-001).
    """

    # FPS y duración
    MIN_FPS = 10
    MAX_FPS = 15
    MIN_DURATION_S = 3
    MAX_DURATION_S = 5

    # Cantidad de fotogramas esperados
    MIN_FRAMES = MIN_FPS * MIN_DURATION_S  # 30 frames
    MAX_FRAMES = MAX_FPS * MAX_DURATION_S  # 75 frames
    EXPECTED_FRAMES = 45  # Promedio

    # Métricas de calidad de fotograma
    MIN_SHARPNESS = 0.7  # Nitidez >70%
    MIN_BRIGHTNESS = 0.4  # Iluminación 40-80%
    MAX_BRIGHTNESS = 0.8
    MIN_CONTRAST = 0.5  # Contraste >50%
    MIN_SILHOUETTE_SCORE = 0.6  # Silueta visible >60%

    # Ponderación de score
    WEIGHT_SILHOUETTE = 0.40  # 40% - más importante
    WEIGHT_SHARPNESS = 0.30  # 30%
    WEIGHT_LIGHTING = 0.20  # 20%
    WEIGHT_ANGLE = 0.10  # 10%


class WeightConstants:
    """
    Constantes relacionadas con pesos bovinos.
    """

    # Rangos de peso por categoría (kg)
    WEIGHT_RANGES = {
        "terneros": (50, 200),  # Terneros: 50-200 kg
        "vaquillonas_torillos": (150, 350),  # Vaquillonas/Torillos: 150-350 kg
        "vaquillonas_toretes": (300, 500),  # Vaquillonas/Toretes: 300-500 kg
        "vacas_toros": (400, 800),  # Vacas/Toros: 400-800 kg
    }

    # GDP (Ganancia Diaria Promedio) esperada por categoría (kg/día)
    GDP_RANGES = {
        "terneros": (0.3, 0.6),  # 0.3-0.6 kg/día
        "vaquillonas_torillos": (0.5, 0.8),  # 0.5-0.8 kg/día
        "vaquillonas_toretes": (0.6, 1.0),  # 0.6-1.0 kg/día
        "vacas_toros": (0.4, 0.7),  # 0.4-0.7 kg/día (mantenimiento)
    }

    # Límites absolutos
    MIN_WEIGHT_KG = 0.0
    MAX_WEIGHT_KG = 1500.0  # Peso máximo razonable
    MIN_GDP_KG_PER_DAY = 0.3  # GDP mínimo esperado
