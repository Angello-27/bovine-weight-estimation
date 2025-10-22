"""
Application Configuration
Configuración centralizada usando Pydantic Settings
"""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración de la aplicación.

    Carga valores desde variables de entorno o archivo .env
    Validación automática con Pydantic
    """

    # ===== Application =====
    APP_NAME: str = "Bovine Weight Estimation API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, description="Modo debug (solo desarrollo)")
    ENVIRONMENT: str = Field(
        default="development", description="Ambiente: development/staging/production"
    )

    # ===== API Configuration =====
    API_V1_PREFIX: str = "/api/v1"
    DOCS_URL: str | None = "/api/docs"
    REDOC_URL: str | None = "/api/redoc"
    OPENAPI_URL: str | None = "/api/openapi.json"

    # ===== CORS =====
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Orígenes permitidos para CORS",
    )
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    # ===== MongoDB =====
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017",
        description="URL de conexión MongoDB",
    )
    MONGODB_DB_NAME: str = Field(
        default="bovine_weight_estimation",
        description="Nombre de la base de datos",
    )
    MONGODB_MIN_POOL_SIZE: int = 10
    MONGODB_MAX_POOL_SIZE: int = 100

    # ===== Security =====
    SECRET_KEY: str = Field(
        default="CHANGE_THIS_IN_PRODUCTION_USE_ENV_FILE",
        description="Secret key para JWT (CAMBIAR en producción)",
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 días

    # ===== ML Models =====
    ML_MODELS_PATH: str = Field(
        default="./ml_models",
        description="Path local para modelos TFLite",
    )
    ML_DEFAULT_MODEL: str = "generic-v1.0.0.tflite"
    ML_INPUT_SIZE: int = 224  # 224x224 para TFLite
    ML_CONFIDENCE_THRESHOLD: float = 0.80  # Mínimo 80%

    # ===== AWS S3 (opcional, para modelos en cloud) =====
    AWS_S3_BUCKET_NAME: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_REGION: str = "us-east-1"

    # ===== Logging =====
    LOG_LEVEL: str = Field(default="INFO", description="Nivel de logs")
    LOG_FORMAT: str = "json"  # json o text

    # ===== Performance =====
    MAX_UPLOAD_SIZE_MB: int = 10  # Máximo tamaño de imagen
    REQUEST_TIMEOUT_S: int = 30  # Timeout de requests

    # ===== Hacienda Gamelera =====
    HACIENDA_NAME: str = "Hacienda Gamelera"
    HACIENDA_OWNER: str = "Bruno Brito Macedo"
    HACIENDA_LOCATION: str = "San Ignacio de Velasco, Santa Cruz, Bolivia"
    HACIENDA_CAPACITY: int = 500  # 500 cabezas de ganado bovino
    PROJECT_TYPE: str = "Proyecto académico final de carrera"
    PROJECT_DEADLINE: str = "Finales noviembre / inicio diciembre 2024"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Valida que el ambiente sea válido."""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment debe ser uno de: {allowed}")
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Valida nivel de log."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v_upper = v.upper()
        if v_upper not in allowed:
            raise ValueError(f"LOG_LEVEL debe ser uno de: {allowed}")
        return v_upper

    @property
    def is_production(self) -> bool:
        """Verifica si está en producción."""
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        """Verifica si está en desarrollo."""
        return self.ENVIRONMENT == "development"

    def get_mongodb_uri(self) -> str:
        """Construye URI completo de MongoDB."""
        return self.MONGODB_URL


@lru_cache
def get_settings() -> Settings:
    """
    Obtiene instancia singleton de Settings.

    Usa lru_cache para evitar re-parsear .env en cada request.

    Returns:
        Settings: Configuración de la aplicación
    """
    return Settings()


# Instancia global (singleton)
settings = get_settings()
