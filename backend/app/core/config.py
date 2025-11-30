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
    APP_NAME: str = Field(
        default="Bovine Weight Estimation API",
        description="Nombre de la aplicación",
    )
    APP_VERSION: str = Field(default="1.0.0", description="Versión de la aplicación")
    DEBUG: bool = Field(default=False, description="Modo debug (solo desarrollo)")
    ENVIRONMENT: str = Field(
        default="development", description="Ambiente: development/staging/production"
    )

    # ===== API Configuration =====
    API_V1_PREFIX: str = Field(default="/api/v1", description="Prefijo de la API")
    DOCS_URL: str | None = Field(
        default="/api/docs", description="URL de documentación Swagger"
    )
    REDOC_URL: str | None = Field(
        default="/api/redoc", description="URL de documentación ReDoc"
    )
    OPENAPI_URL: str | None = Field(
        default="/api/openapi.json", description="URL del esquema OpenAPI"
    )

    # ===== CORS =====
    CORS_ORIGINS: str | list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8080"],
        description="Orígenes permitidos para CORS (separados por comas en .env)",
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True, description="Permitir credenciales en CORS"
    )
    CORS_ALLOW_METHODS: str | list[str] = Field(
        default=["*"],
        description="Métodos HTTP permitidos en CORS (separados por comas en .env)",
    )
    CORS_ALLOW_HEADERS: str | list[str] = Field(
        default=["*"],
        description="Headers permitidos en CORS (separados por comas en .env)",
    )

    # ===== MongoDB =====
    MONGODB_URL: str = Field(
        default="mongodb://localhost:27017",
        description="URL de conexión MongoDB",
    )
    MONGODB_DB_NAME: str = Field(
        default="bovine_weight_estimation",
        description="Nombre de la base de datos",
    )
    MONGODB_MIN_POOL_SIZE: int = Field(
        default=10, description="Tamaño mínimo del pool de conexiones MongoDB"
    )
    MONGODB_MAX_POOL_SIZE: int = Field(
        default=100, description="Tamaño máximo del pool de conexiones MongoDB"
    )

    # ===== Security =====
    SECRET_KEY: str = Field(
        default="CHANGE_THIS_IN_PRODUCTION_USE_ENV_FILE",
        description="Secret key para JWT (CAMBIAR en producción)",
    )
    JWT_ALGORITHM: str = Field(default="HS256", description="Algoritmo JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=10080, description="Minutos de expiración del token JWT (7 días)"
    )

    # ===== ML Models =====
    ML_MODELS_PATH: str = Field(
        default="./ml_models",
        description="Path local para modelos TFLite",
    )
    ML_DEFAULT_MODEL: str = Field(
        default="generic-cattle-v1.0.0.tflite",
        description="Nombre del modelo TFLite por defecto",
    )
    ML_INPUT_SIZE: int = Field(
        default=224, description="Tamaño de entrada del modelo ML (224x224 para TFLite)"
    )
    ML_CONFIDENCE_THRESHOLD: float = Field(
        default=0.80, description="Umbral mínimo de confianza ML (80%)"
    )

    # ===== Logging =====
    LOG_LEVEL: str = Field(default="INFO", description="Nivel de logs")
    LOG_FORMAT: str = Field(default="json", description="Formato de logs: json o text")

    # ===== Performance =====
    MAX_UPLOAD_SIZE_MB: int = Field(
        default=10, description="Tamaño máximo de imagen en MB"
    )
    REQUEST_TIMEOUT_S: int = Field(
        default=30, description="Timeout de requests en segundos"
    )

    # ===== Hacienda Gamelera =====
    HACIENDA_NAME: str = Field(
        default="Hacienda Gamelera", description="Nombre de la hacienda"
    )
    HACIENDA_OWNER: str = Field(
        default="Bruno Brito Macedo", description="Propietario de la hacienda"
    )
    HACIENDA_LOCATION: str = Field(
        default="San Ignacio de Velasco, Santa Cruz, Bolivia",
        description="Ubicación de la hacienda",
    )
    HACIENDA_CAPACITY: int = Field(
        default=500, description="Capacidad de ganado bovino en cabezas"
    )
    PROJECT_TYPE: str = Field(
        default="Proyecto académico final de carrera",
        description="Tipo de proyecto",
    )
    PROJECT_DEADLINE: str = Field(
        default="Finales noviembre / inicio diciembre 2024",
        description="Fecha límite del proyecto",
    )

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

    @field_validator(
        "CORS_ORIGINS", "CORS_ALLOW_METHODS", "CORS_ALLOW_HEADERS", mode="before"
    )
    @classmethod
    def validate_cors_list_fields(cls, v: str | list[str] | None) -> list[str]:
        """
        Valida y convierte campos de lista de CORS a lista.

        Acepta:
        - Lista de strings (desde JSON en .env)
        - String separado por comas (desde .env simple)
        - String con "*" (retorna ["*"])
        - None o string vacío (retorna lista vacía)
        """
        if v is None:
            return []
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # Si es string vacío, retornar lista vacía
            if not v.strip():
                return []
            # Si es "*", retornar ["*"]
            if v.strip() == "*":
                return ["*"]
            # Si es string con comas, dividir y limpiar
            return [item.strip() for item in v.split(",") if item.strip()]
        return []

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
