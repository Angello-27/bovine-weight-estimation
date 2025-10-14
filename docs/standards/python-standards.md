# Estándares de Desarrollo Python/FastAPI

## Contexto del Proyecto

**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Tecnología**: Python 3.11+ / FastAPI / MongoDB  
**Propósito**: Backend API, reportes normativos, integración Gran Paitití

## Principios Fundamentales Python

1. **Type Hints Obligatorios**: Toda función debe tener anotaciones de tipo
2. **Pydantic v2**: Validación estricta de datos
3. **Clean Architecture**: api → services → repositories
4. **Async/Await**: Operaciones asíncronas siempre que sea posible
5. **PEP 8 Compliance**: Estilo de código consistente

---

## Stack Tecnológico Backend

### Herramientas Core

| Propósito | Herramienta | Justificación | Versión |
|-----------|-------------|---------------|---------|
| **API principal** | FastAPI | Framework asíncrono, tipado, OpenAPI automático | ^0.104.0 |
| **Validación** | Pydantic v2 | Validación tipada estricta | ^2.4.0 |
| **Base de datos** | Motor + Beanie | ODM MongoDB asíncrono moderno | ^1.4.0, ^1.23.0 |
| **Autenticación** | PyJWT | Tokens JWT para RBAC | ^2.8.0 |
| **HTTP client** | httpx | Cliente HTTP asíncrono (Gran Paitití) | ^0.25.0 |
| **PDF generation** | reportlab | Reportes SENASAG en PDF | ^4.0.0 |
| **CSV/XML** | csv (stdlib), xmltodict | Exportación SENASAG | ^0.13.0 |
| **QR codes** | qrcode + Pillow | Códigos QR en GMA | ^7.4.0 |
| **Background tasks** | FastAPI BackgroundTasks | Sincronización asíncrona | Incluido |
| **Logs** | loguru | Logs estructurados JSON | ^0.7.2 |
| **Testing** | pytest + httpx | Unit e integration tests | ^7.4.0 |
| **Environment** | python-dotenv | Variables de entorno | ^1.0.0 |
| **CORS** | FastAPI middleware | CORS para Flutter app | Incluido |

---

## Estructura de Carpetas (Clean Architecture)

```
backend/
├── app/
│   ├── core/                              # Código compartido
│   │   ├── config.py                      # Configuración desde .env
│   │   ├── security.py                    # JWT, hashing, RBAC
│   │   ├── exceptions.py                  # Excepciones custom
│   │   ├── logging.py                     # Setup de loguru
│   │   │
│   │   └── constants/                     # Constantes del dominio
│   │       ├── __init__.py
│   │       ├── breeds.py                  # 7 razas EXACTAS
│   │       ├── age_categories.py          # 4 categorías EXACTAS
│   │       ├── capture_constants.py       # 10-15 FPS, 3-5s
│   │       ├── metrics.py                 # ≥95%, <5kg, <3s
│   │       ├── hacienda_constants.py      # GPS Hacienda Gamelera
│   │       └── regulatory.py              # SENASAG/REGENSA/ASOCEBU
│   │
│   ├── domain/                            # Domain Layer (puro)
│   │   ├── entities/                      # Entidades de negocio
│   │   │   ├── animal.py
│   │   │   ├── weighing.py
│   │   │   ├── senasag_report.py
│   │   │   ├── gma.py                     # Guía Movimiento Animal
│   │   │   └── asocebu_data.py
│   │   │
│   │   ├── enums.py                       # BreedType, AgeCategory, etc.
│   │   │
│   │   └── value_objects/                 # Value objects
│   │       ├── breed_weight_ranges.py     # Rangos válidos por raza/edad
│   │       ├── hacienda_location.py       # GPS validado
│   │       └── gma_number.py              # Formato número GMA
│   │
│   ├── api/                               # Presentation Layer (FastAPI)
│   │   ├── routes/                        # Endpoints REST
│   │   │   ├── __init__.py
│   │   │   ├── health.py                  # Health check
│   │   │   ├── auth.py                    # Login, registro
│   │   │   ├── animals.py                 # CRUD animales
│   │   │   ├── weighings.py               # CRUD pesajes
│   │   │   ├── senasag.py                 # US-007: Reportes SENASAG
│   │   │   ├── regensa.py                 # US-008: GMA REGENSA
│   │   │   ├── gran_paititi.py            # US-008: Integración API
│   │   │   └── asocebu.py                 # US-009: Exportación ASOCEBU
│   │   │
│   │   ├── schemas/                       # Pydantic schemas (request/response)
│   │   │   ├── animal_schemas.py
│   │   │   ├── weighing_schemas.py
│   │   │   ├── senasag_schemas.py
│   │   │   ├── gma_schemas.py
│   │   │   └── asocebu_schemas.py
│   │   │
│   │   ├── dependencies.py                # FastAPI dependencies
│   │   └── middleware.py                  # CORS, logging, etc.
│   │
│   ├── services/                          # Business Logic Layer
│   │   ├── animal_service.py              # CRUD + lógica animales
│   │   ├── weighing_service.py            # Estimación + validación
│   │   ├── senasag_service.py             # US-007: Generación reportes
│   │   ├── gma_service.py                 # US-008: Generación GMA + QR
│   │   ├── gran_paititi_service.py        # US-008: Cliente API
│   │   └── asocebu_service.py             # US-009: Certificaciones
│   │
│   ├── repositories/                      # Data Layer (MongoDB)
│   │   ├── animal_repository.py
│   │   ├── weighing_repository.py
│   │   ├── senasag_repository.py          # Historial reportes
│   │   ├── gma_repository.py              # Historial GMAs
│   │   └── asocebu_repository.py
│   │
│   ├── clients/                           # HTTP clients externos
│   │   └── gran_paititi_client.py         # Cliente API Gran Paitití
│   │
│   ├── database/                          # Database setup
│   │   ├── mongodb.py                     # Conexión Motor
│   │   ├── models.py                      # Beanie models
│   │   └── seed_data.py                   # Seed: 7 razas, Bruno, etc.
│   │
│   ├── ml/                                # Machine Learning (si aplica backend)
│   │   ├── model_loader.py                # Carga modelos TFLite
│   │   ├── inference.py                   # Inferencia
│   │   └── preprocessing.py               # Preprocesamiento
│   │
│   └── main.py                            # FastAPI app entry point
│
├── tests/                                 # Tests
│   ├── unit/
│   │   ├── services/
│   │   └── repositories/
│   ├── integration/
│   │   ├── api/
│   │   └── database/
│   └── conftest.py                        # Fixtures compartidos
│
├── alembic/                               # Migraciones (si se usa SQL)
│
├── requirements.txt                       # Dependencies producción
├── requirements-dev.txt                   # Dependencies desarrollo
├── .env.example                           # Template variables entorno
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── pyproject.toml
└── README.md
```

---

## Constantes del Dominio (CRÍTICAS)

### 1. Razas Bovinas (7 EXACTAS - NO MODIFICAR)

```python
# app/core/constants/breeds.py

from enum import Enum
from typing import Literal

class BreedType(str, Enum):
    """
    7 razas bovinas de Hacienda Gamelera.
    
    IMPORTANTE: Estas son las ÚNICAS razas válidas en el sistema.
    NO agregar, eliminar o modificar sin autorización de Bruno Brito Macedo.
    
    Clasificación:
    - Bos indicus (cebuinas): Brahman, Nelore, Cebuinas
    - Bos taurus (europeas): Angus, Criollo, Pardo Suizo, Jersey
    """
    BRAHMAN = "brahman"           # Bos indicus
    NELORE = "nelore"             # Bos indicus
    ANGUS = "angus"               # Bos taurus
    CEBUINAS = "cebuinas"         # Bos indicus
    CRIOLLO = "criollo"           # Bos taurus
    PARDO_SUIZO = "pardo_suizo"   # Bos taurus
    JERSEY = "jersey"             # Bos taurus
    
    @classmethod
    def is_valid(cls, breed: str) -> bool:
        """Valida si la raza es una de las 7 exactas."""
        try:
            cls(breed)
            return True
        except ValueError:
            return False
    
    @classmethod
    def get_display_name(cls, breed: 'BreedType') -> str:
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
    
    @classmethod
    def get_species(cls, breed: 'BreedType') -> 'BovineSpecies':
        """Retorna especie bovina (Bos indicus o Bos taurus)."""
        bos_indicus = {cls.BRAHMAN, cls.NELORE, cls.CEBUINAS}
        return BovineSpecies.BOS_INDICUS if breed in bos_indicus else BovineSpecies.BOS_TAURUS
    
    def get_model_filename(self) -> str:
        """Retorna nombre del archivo modelo TFLite."""
        return f"{self.value}-v1.0.0.tflite"

class BovineSpecies(str, Enum):
    """Clasificación taxonómica de bovinos."""
    BOS_INDICUS = "bos_indicus"   # Razas cebuinas (clima tropical)
    BOS_TAURUS = "bos_taurus"     # Razas europeas

# Type alias para validación
BreedTypeLiteral = Literal[
    "brahman", "nelore", "angus", "cebuinas", 
    "criollo", "pardo_suizo", "jersey"
]
```

### 2. Categorías de Edad (4 EXACTAS - NO MODIFICAR)

```python
# app/core/constants/age_categories.py

from enum import Enum
from datetime import datetime
from typing import Tuple, Optional

class AgeCategory(str, Enum):
    """
    4 categorías de edad de bovinos en Hacienda Gamelera.
    
    Basadas en el sistema de manejo de Bruno Brito Macedo.
    """
    TERNEROS = "terneros"                          # <8 meses
    VAQUILLONAS_TORILLOS = "vaquillonas_torillos"  # 6-18 meses
    VAQUILLONAS_TORETES = "vaquillonas_toretes"    # 19-30 meses
    VACAS_TOROS = "vacas_toros"                    # >30 meses
    
    @classmethod
    def get_display_name(cls, category: 'AgeCategory') -> str:
        """Retorna nombre para mostrar en UI (español)."""
        display_names = {
            cls.TERNEROS: "Terneros (<8 meses)",
            cls.VAQUILLONAS_TORILLOS: "Vaquillonas/Torillos (6-18 meses)",
            cls.VAQUILLONAS_TORETES: "Vaquillonas/Toretes (19-30 meses)",
            cls.VACAS_TOROS: "Vacas/Toros (>30 meses)",
        }
        return display_names[category]
    
    @classmethod
    def get_age_range_months(cls, category: 'AgeCategory') -> Tuple[int, Optional[int]]:
        """Retorna rango de edad en meses (min, max)."""
        ranges = {
            cls.TERNEROS: (0, 8),
            cls.VAQUILLONAS_TORILLOS: (6, 18),
            cls.VAQUILLONAS_TORETES: (19, 30),
            cls.VACAS_TOROS: (30, None),  # Sin máximo
        }
        return ranges[category]
    
    @classmethod
    def from_birth_date(cls, birth_date: datetime) -> 'AgeCategory':
        """
        Calcula categoría de edad desde fecha de nacimiento.
        
        Args:
            birth_date: Fecha de nacimiento del animal
            
        Returns:
            AgeCategory correspondiente
            
        Example:
            >>> birth_date = datetime(2023, 1, 15)
            >>> category = AgeCategory.from_birth_date(birth_date)
            >>> print(category.value)
            'vaquillonas_torillos'
        """
        age_months = cls._calculate_age_in_months(birth_date)
        
        if age_months < 8:
            return cls.TERNEROS
        elif 6 <= age_months <= 18:
            return cls.VAQUILLONAS_TORILLOS
        elif 19 <= age_months <= 30:
            return cls.VAQUILLONAS_TORETES
        else:
            return cls.VACAS_TOROS
    
    @staticmethod
    def _calculate_age_in_months(birth_date: datetime) -> int:
        """Calcula edad en meses desde fecha de nacimiento."""
        now = datetime.now()
        return (now.year - birth_date.year) * 12 + (now.month - birth_date.month)
```

### 3. Métricas del Sistema (OBLIGATORIAS)

```python
# app/core/constants/metrics.py

from datetime import timedelta

class SystemMetrics:
    """
    Métricas obligatorias del sistema de estimación de peso.
    
    Definidas en Sprint 0 como requisitos no funcionales críticos.
    Validadas con Bruno Brito Macedo en Hacienda Gamelera.
    """
    
    # Precisión ML
    MIN_PRECISION: float = 0.95              # ≥95% (R² ≥ 0.95)
    MIN_CONFIDENCE: float = 0.95             # Confidence score ≥95%
    
    # Error absoluto
    MAX_ERROR_KG: float = 5.0                # <5 kg
    
    # Tiempo de procesamiento
    MAX_PROCESSING_TIME_MS: int = 3000       # <3 segundos
    MAX_PROCESSING_TIME_SECONDS: float = 3.0
    
    # Tiempo objetivo para 20 animales
    TARGET_TIME_20_ANIMALS_HOURS: float = 2.0  # <2 horas
    
    # Comparación con método tradicional
    TRADITIONAL_METHOD_MIN_ERROR_KG: float = 5.0   # Error mínimo Schaeffer
    TRADITIONAL_METHOD_MAX_ERROR_KG: float = 20.0  # Error máximo Schaeffer
    TRADITIONAL_METHOD_MIN_DAYS: int = 2           # 2-3 días para 20 animales
    TRADITIONAL_METHOD_MAX_DAYS: int = 3
    
    # Objetivo de reducción
    TIME_REDUCTION_TARGET: float = 0.80      # 80% reducción de tiempo

class CaptureConstants:
    """Constantes para captura continua de fotogramas (US-001)."""
    
    FRAMES_PER_SECOND: int = 12              # 10-15 FPS
    CAPTURE_DURATION_SECONDS: int = 4        # 3-5 segundos
    EXPECTED_FRAME_COUNT: int = 48           # 12 FPS × 4s
    
    # Umbrales de calidad de fotograma
    MIN_SHARPNESS: float = 0.7
    MIN_BRIGHTNESS: float = 0.4
    MAX_BRIGHTNESS: float = 0.8
    MIN_CONTRAST: float = 0.5
    MIN_SILHOUETTE_VISIBILITY: float = 0.8
    MIN_ANGLE_SCORE: float = 0.6
    
    # Ponderación score global
    SILHOUETTE_WEIGHT: float = 0.4           # 40%
    SHARPNESS_WEIGHT: float = 0.3            # 30%
    BRIGHTNESS_WEIGHT: float = 0.2           # 20%
    ANGLE_WEIGHT: float = 0.1                # 10%
    
    # Distancia óptima
    MIN_DISTANCE_METERS: float = 2.0
    MAX_DISTANCE_METERS: float = 5.0
```

### 4. Constantes Regulatorias

```python
# app/core/constants/regulatory.py

from typing import Dict, List

class SENASAGConstants:
    """
    Constantes para reportes SENASAG (US-007).
    
    SENASAG: Servicio Nacional de Sanidad Agropecuaria e Inocuidad Alimentaria
    """
    
    ENTITY_NAME: str = "SENASAG"
    ENTITY_FULL_NAME: str = "Servicio Nacional de Sanidad Agropecuaria e Inocuidad Alimentaria"
    
    # Tipos de reportes
    REPORT_TYPE_INVENTORY: str = "inventario_mensual"
    REPORT_TYPE_MOVEMENTS: str = "movimientos_trimestrales"
    REPORT_TYPE_TRACEABILITY: str = "trazabilidad_animal"
    
    # Formatos de exportación
    FORMAT_PDF: str = "pdf"
    FORMAT_CSV: str = "csv"
    FORMAT_XML: str = "xml"
    
    # Estructura CSV estándar (campos obligatorios)
    CSV_HEADERS: List[str] = [
        "animal_id",
        "numero_caravana",
        "raza",
        "edad_meses",
        "peso_actual_kg",
        "ultimo_pesaje",
        "estado",
        "hacienda",
        "propietario",
    ]
    
    # Frecuencia de reportes
    FREQUENCY_MONTHLY: str = "mensual"
    FREQUENCY_QUARTERLY: str = "trimestral"
    FREQUENCY_ANNUAL: str = "anual"

class REGENSAConstants:
    """
    Constantes para REGENSA - Reglamento General de Sanidad Animal (US-008).
    
    Capítulos aplicables:
    - 3.10: Centros de concentración de animales
    - 7.1: Requisitos para centros de pesaje
    """
    
    ENTITY_NAME: str = "REGENSA"
    ENTITY_FULL_NAME: str = "Reglamento General de Sanidad Animal"
    
    # Capítulos aplicables
    CHAPTER_3_10: str = "3.10"  # Centros de concentración
    CHAPTER_7_1: str = "7.1"    # Requisitos centros pesaje
    
    # Requisitos infraestructura (Capítulo 3.10)
    MIN_RAMP_WIDTH_METERS: float = 1.6
    MIN_SPACE_PER_ANIMAL_M2: float = 2.0
    REQUIRES_DISINFECTION_SYSTEM: bool = True
    REQUIRES_QUARANTINE_CORRAL: bool = True
    PROHIBITS_PAIN_INSTRUMENTS: bool = True
    
    # GMA (Guía de Movimiento Animal)
    GMA_PREFIX: str = "GMA"
    GMA_NUMBER_LENGTH: int = 10  # Formato: GMA-XXXXXXXXXX
    
    # Estados de GMA
    GMA_STATUS_PENDING: str = "pendiente"
    GMA_STATUS_APPROVED: str = "aprobada"
    GMA_STATUS_REJECTED: str = "rechazada"
    GMA_STATUS_COMPLETED: str = "completada"
    
    # Motivos de movimiento
    MOVEMENT_REASON_SALE: str = "venta"
    MOVEMENT_REASON_TRANSFER: str = "traslado"
    MOVEMENT_REASON_SLAUGHTER: str = "sacrificio"
    MOVEMENT_REASON_EXHIBITION: str = "exposicion"

class GranPaititiConstants:
    """
    Constantes para integración con sistema Gran Paitití (US-008).
    
    Gran Paitití: Plataforma gubernamental de registro ganadero.
    """
    
    SYSTEM_NAME: str = "Gran Paitití"
    
    # Endpoints API (sandbox/producción)
    API_BASE_URL_SANDBOX: str = "https://sandbox.granpaititi.gob.bo/api/v1"
    API_BASE_URL_PRODUCTION: str = "https://granpaititi.gob.bo/api/v1"
    
    # Timeout
    API_TIMEOUT_SECONDS: int = 30
    
    # Retry policy
    MAX_RETRIES: int = 3
    RETRY_BACKOFF_SECONDS: List[int] = [5, 15, 30]  # Backoff exponencial

class ASOCEBUConstants:
    """
    Constantes para ASOCEBU - Asociación de Criadores de Cebuinos (US-009).
    """
    
    ENTITY_NAME: str = "ASOCEBU"
    ENTITY_FULL_NAME: str = "Asociación de Criadores de Cebuinos"
    
    # Evento histórico de Hacienda Gamelera
    EVENT_3RD_FAENA_TECNICA_2024: str = "3ª Faena Técnica 2024"
    EVENT_3RD_FAENA_AWARD: str = "Medalla de Bronce - Mejor lote de carcasas de hembras en confinamiento"
    
    # Formatos de exportación
    FORMAT_EXCEL: str = "xlsx"
    FORMAT_PDF_CERTIFICATE: str = "pdf"
    
    # Campos obligatorios para inscripción
    REQUIRED_FIELDS: List[str] = [
        "numero_caravana",
        "raza",
        "edad_precisa",
        "peso_actual_kg",
        "historial_6_meses",
        "gdp_promedio",  # Ganancia Diaria Promedio
    ]
```

### 5. Constantes de Hacienda Gamelera

```python
# app/core/constants/hacienda_constants.py

from typing import NamedTuple

class HaciendaLocation(NamedTuple):
    """Ubicación GPS de Hacienda Gamelera."""
    latitude: float   # 15°51′34.2′′S
    longitude: float  # 60°47′52.4′′W
    name: str
    city: str
    department: str
    country: str

class HaciendaConstants:
    """
    Constantes específicas de Hacienda Gamelera.
    
    Cliente: Bruno Brito Macedo
    Ubicación: San Ignacio de Velasco, Santa Cruz, Bolivia
    """
    
    # Información de la hacienda
    HACIENDA_NAME: str = "Hacienda Gamelera"
    OWNER_NAME: str = "Bruno Brito Macedo"
    CITY: str = "San Ignacio de Velasco"
    DEPARTMENT: str = "Santa Cruz"
    COUNTRY: str = "Bolivia"
    
    # Coordenadas GPS: 15°51′34.2′′S, 60°47′52.4′′W
    LATITUDE: float = -15.859500   # Negativo = Sur
    LONGITUDE: float = -60.797889  # Negativo = Oeste
    
    LOCATION: HaciendaLocation = HaciendaLocation(
        latitude=LATITUDE,
        longitude=LONGITUDE,
        name=HACIENDA_NAME,
        city=CITY,
        department=DEPARTMENT,
        country=COUNTRY,
    )
    
    # Capacidad
    EXTENSION_HECTARES: float = 48.5
    ANIMAL_CAPACITY: int = 500
    
    @staticmethod
    def schaeffer_formula(
        perimeter_thoracic_cm: float,
        body_length_cm: float,
    ) -> float:
        """
        Fórmula Schaeffer (método tradicional para comparación).
        
        Peso (kg) = (PT² × LC) / 10838
        
        Args:
            perimeter_thoracic_cm: Perímetro Torácico en cm
            body_length_cm: Longitud del Cuerpo en cm
            
        Returns:
            Peso estimado en kg (error típico: 5-20 kg)
            
        Note:
            Este método tiene precisión ~85% vs >95% del sistema IA.
            Se usa solo para comparación con método tradicional de Bruno.
        """
        return (perimeter_thoracic_cm ** 2 * body_length_cm) / 10838
    
    # Personal para método tradicional
    TRADITIONAL_METHOD_PERSONNEL: int = 3  # Capataz, vaquero, peón
    TRADITIONAL_METHOD_MIN_DAYS: int = 2   # 2-3 días para 20 animales
    TRADITIONAL_METHOD_MAX_DAYS: int = 3
```

---

## Schemas con Pydantic v2

### Animal Schemas

```python
# app/api/schemas/animal_schemas.py

from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

from ...core.constants.breeds import BreedType
from ...core.constants.age_categories import AgeCategory
from ...domain.enums import Gender, AnimalStatus

class AnimalBase(BaseModel):
    """Schema base para Animal (campos comunes)."""
    tag_number: str = Field(
        ...,
        description="Número de caravana/arete (único)",
        min_length=1,
        max_length=50,
        examples=["GAM-001", "BRA-456"],
    )
    breed_type: BreedType = Field(
        ...,
        description="Raza del animal (una de las 7 de Hacienda Gamelera)",
    )
    birth_date: datetime = Field(
        ...,
        description="Fecha de nacimiento del animal",
    )
    gender: Gender = Field(
        ...,
        description="Sexo del animal (macho/hembra)",
    )
    status: AnimalStatus = Field(
        default=AnimalStatus.ACTIVE,
        description="Estado actual del animal",
    )
    
    # Campos opcionales
    color: Optional[str] = Field(
        None,
        description="Color del animal (ej: 'Rojo', 'Negro')",
        max_length=100,
    )
    weight_at_birth_kg: Optional[float] = Field(
        None,
        description="Peso al nacer en kilogramos",
        ge=15.0,   # Mínimo realista para ternero
        le=60.0,   # Máximo realista para ternero
    )
    mother_id: Optional[UUID] = Field(
        None,
        description="ID de la madre (si conocido)",
    )
    father_id: Optional[UUID] = Field(
        None,
        description="ID del padre (si conocido)",
    )
    observations: Optional[str] = Field(
        None,
        description="Observaciones generales",
        max_length=500,
    )
    
    @field_validator("breed_type")
    @classmethod
    def validate_breed_type(cls, v: BreedType) -> BreedType:
        """
        Valida que breed_type sea una de las 7 razas exactas de Hacienda Gamelera.
        
        Raises:
            ValueError: Si raza no es una de las 7 exactas
        """
        if not BreedType.is_valid(v.value):
            valid_breeds = ", ".join([b.value for b in BreedType])
            raise ValueError(
                f"Raza inválida '{v.value}'. "
                f"Razas válidas de Hacienda Gamelera: {valid_breeds}"
            )
        return v
    
    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v: datetime) -> datetime:
        """
        Valida que fecha de nacimiento no sea futura.
        
        Raises:
            ValueError: Si fecha es futura
        """
        if v > datetime.now():
            raise ValueError("Fecha de nacimiento no puede ser futura")
        return v

class AnimalCreateRequest(AnimalBase):
    """Request para crear nuevo animal (POST /animals)."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "tag_number": "GAM-001",
                "breed_type": "brahman",
                "birth_date": "2022-03-15T00:00:00",
                "gender": "female",
                "status": "active",
                "color": "Rojo",
                "weight_at_birth_kg": 35.5,
                "observations": "Primera cría de vaca GAM-123",
            }
        }
    )

class AnimalResponse(AnimalBase):
    """Response de Animal (GET /animals/{id})."""
    id: UUID = Field(..., description="UUID del animal")
    age_months: int = Field(..., description="Edad en meses (calculado)")
    age_category: AgeCategory = Field(
        ...,
        description="Categoría de edad (calculado desde birth_date)",
    )
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class AnimalListResponse(BaseModel):
    """Response para lista de animales (GET /animals)."""
    animals: list[AnimalResponse]
    total: int = Field(..., description="Total de animales en Hacienda Gamelera")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=500)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "animals": [],
                "total": 500,
                "page": 1,
                "page_size": 50,
            }
        }
    )
```

---

## FastAPI Routes (Clean Architecture)

### Endpoint SENASAG (US-007)

```python
# app/api/routes/senasag.py

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse
from typing import Optional
from datetime import datetime
import io

from ...core.constants.regulatory import SENASAGConstants
from ..schemas.senasag_schemas import (
    SENASAGReportCreateRequest,
    SENASAGReportResponse,
    SENASAGReportListResponse,
)
from ...services.senasag_service import SENASAGService
from ..dependencies import get_current_user, get_senasag_service

router = APIRouter(
    prefix="/senasag",
    tags=["SENASAG - Trazabilidad Ganadera"],
)

@router.post(
    "/reports",
    response_model=SENASAGReportResponse,
    status_code=201,
    summary="Generar reporte SENASAG",
    description="""
    Genera reporte de trazabilidad ganadera para SENASAG (US-007).
    
    **Formatos disponibles**:
    - PDF: Reporte profesional con logo SENASAG
    - CSV: Estructura estándar para importación
    - XML: Compatible con sistemas SENASAG
    
    **Validaciones**:
    - Hacienda debe tener animales registrados
    - Período debe ser válido (mensual/trimestral/anual)
    - Formato debe ser uno de: pdf, csv, xml
    
    **Cliente**: Hacienda Gamelera (Bruno Brito Macedo)
    **Animales**: 500 cabezas de ganado bovino
    """,
)
async def generate_senasag_report(
    report_request: SENASAGReportCreateRequest,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    senasag_service: SENASAGService = Depends(get_senasag_service),
) -> SENASAGReportResponse:
    """
    Genera reporte SENASAG de trazabilidad ganadera.
    
    Flujo:
    1. Validar período y formato
    2. Consultar animales de Hacienda Gamelera (500 cabezas)
    3. Generar reporte en formato solicitado
    4. Guardar en historial
    5. Enviar por email (background task)
    
    Returns:
        SENASAGReportResponse con reporte_id y URL de descarga
    """
    try:
        report = await senasag_service.generate_report(
            farm_id=current_user.farm_id,
            report_type=report_request.report_type,
            period_start=report_request.period_start,
            period_end=report_request.period_end,
            format=report_request.format,
        )
        
        # Si email configurado, enviar en background
        if report_request.send_email and report_request.email_to:
            background_tasks.add_task(
                senasag_service.send_report_email,
                report_id=report.id,
                email_to=report_request.email_to,
            )
        
        return report
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando reporte SENASAG: {str(e)}",
        )

@router.get(
    "/reports/{report_id}/download",
    summary="Descargar reporte SENASAG",
    description="Descarga archivo de reporte generado (PDF/CSV/XML).",
)
async def download_senasag_report(
    report_id: str,
    current_user = Depends(get_current_user),
    senasag_service: SENASAGService = Depends(get_senasag_service),
):
    """Descarga archivo de reporte SENASAG."""
    try:
        file_data, content_type, filename = await senasag_service.get_report_file(
            report_id=report_id,
            user_id=current_user.id,
        )
        
        return StreamingResponse(
            io.BytesIO(file_data),
            media_type=content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get(
    "/reports",
    response_model=SENASAGReportListResponse,
    summary="Listar reportes SENASAG",
    description="Historial de reportes generados para Hacienda Gamelera.",
)
async def list_senasag_reports(
    page: int = 1,
    page_size: int = 20,
    current_user = Depends(get_current_user),
    senasag_service: SENASAGService = Depends(get_senasag_service),
) -> SENASAGReportListResponse:
    """Lista historial de reportes SENASAG."""
    reports = await senasag_service.list_reports(
        farm_id=current_user.farm_id,
        page=page,
        page_size=page_size,
    )
    return reports
```

---

## Services (Business Logic)

```python
# app/services/senasag_service.py

from typing import Tuple
from datetime import datetime
from uuid import UUID, uuid4
from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import csv
import xmltodict

from ..core.constants.regulatory import SENASAGConstants
from ..core.constants.breeds import BreedType
from ..repositories.animal_repository import AnimalRepository
from ..repositories.senasag_repository import SENASAGRepository
from ..domain.entities.senasag_report import SENASAGReport, ReportFormat, ReportStatus

class SENASAGService:
    """
    Servicio para generación de reportes SENASAG (US-007).
    
    Responsabilidades:
    1. Generar reportes de trazabilidad en PDF/CSV/XML
    2. Validar estructura según normativa SENASAG
    3. Guardar historial de reportes
    4. Enviar reportes por email
    """
    
    def __init__(
        self,
        animal_repository: AnimalRepository,
        senasag_repository: SENASAGRepository,
    ):
        self._animal_repo = animal_repository
        self._senasag_repo = senasag_repository
    
    async def generate_report(
        self,
        farm_id: UUID,
        report_type: str,
        period_start: datetime,
        period_end: datetime,
        format: ReportFormat,
    ) -> SENASAGReport:
        """
        Genera reporte SENASAG de trazabilidad ganadera.
        
        Args:
            farm_id: UUID de Hacienda Gamelera
            report_type: Tipo (inventario, movimientos, trazabilidad)
            period_start: Inicio del período
            period_end: Fin del período
            format: Formato (PDF, CSV, XML)
            
        Returns:
            SENASAGReport con reporte generado y guardado
            
        Raises:
            ValueError: Si no hay animales en el período
            
        Note:
            Para Hacienda Gamelera (500 cabezas), generación debe ser <5 minutos.
        """
        # 1. Obtener animales del período
        animals = await self._animal_repo.get_animals_by_farm_and_period(
            farm_id=farm_id,
            period_start=period_start,
            period_end=period_end,
        )
        
        if not animals:
            raise ValueError(
                f"No hay animales registrados en Hacienda Gamelera "
                f"para el período {period_start.date()} - {period_end.date()}"
            )
        
        # 2. Generar archivo según formato
        if format == ReportFormat.PDF:
            file_data = self._generate_pdf_report(animals, period_start, period_end)
            content_type = "application/pdf"
            extension = "pdf"
        elif format == ReportFormat.CSV:
            file_data = self._generate_csv_report(animals)
            content_type = "text/csv"
            extension = "csv"
        elif format == ReportFormat.XML:
            file_data = self._generate_xml_report(animals)
            content_type = "application/xml"
            extension = "xml"
        else:
            raise ValueError(f"Formato inválido: {format}")
        
        # 3. Crear entidad SENASAGReport
        report = SENASAGReport(
            id=uuid4(),
            farm_id=farm_id,
            report_type=report_type,
            period_start=period_start,
            period_end=period_end,
            format=format,
            status=ReportStatus.GENERATED,
            file_path=f"senasag-reports/{farm_id}/{uuid4()}.{extension}",
            total_animals=len(animals),
            generated_at=datetime.now(),
        )
        
        # 4. Guardar reporte en repositorio
        await self._senasag_repo.save_report(report, file_data)
        
        return report
    
    def _generate_pdf_report(
        self,
        animals: list,
        period_start: datetime,
        period_end: datetime,
    ) -> bytes:
        """
        Genera reporte PDF profesional con logo SENASAG.
        
        Estructura:
        - Header: Logo SENASAG, título, período
        - Datos Hacienda: Nombre, propietario, ubicación GPS
        - Inventario: Total animales por raza
        - Detalle: Tabla con todos los animales
        - Footer: Firma digital Bruno Brito Macedo
        """
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Header
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, height - 50, "REPORTE DE TRAZABILIDAD GANADERA")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, height - 70, SENASAGConstants.ENTITY_FULL_NAME)
        
        # Datos de Hacienda Gamelera
        y_position = height - 110
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, "Hacienda:")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(150, y_position, "Hacienda Gamelera")
        
        y_position -= 20
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, "Propietario:")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(150, y_position, "Bruno Brito Macedo")
        
        y_position -= 20
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, "Ubicación:")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(150, y_position, "San Ignacio de Velasco, Santa Cruz, Bolivia")
        
        y_position -= 20
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, "GPS:")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(150, y_position, "15°51′34.2′′S, 60°47′52.4′′W")
        
        # Período
        y_position -= 30
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, "Período:")
        pdf.setFont("Helvetica", 11)
        pdf.drawString(150, y_position, 
                      f"{period_start.strftime('%d/%m/%Y')} - {period_end.strftime('%d/%m/%Y')}")
        
        # Inventario por raza
        y_position -= 40
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y_position, "Inventario por Raza:")
        
        breed_counts = self._count_by_breed(animals)
        y_position -= 20
        for breed in BreedType:
            count = breed_counts.get(breed, 0)
            pdf.setFont("Helvetica", 11)
            pdf.drawString(70, y_position, 
                          f"• {BreedType.get_display_name(breed)}: {count} cabezas")
            y_position -= 20
        
        # Total
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(70, y_position, f"TOTAL: {len(animals)} cabezas")
        
        # Footer
        pdf.setFont("Helvetica-Oblique", 10)
        pdf.drawString(50, 50, 
                      f"Generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        pdf.drawString(50, 35, "Sistema de Estimación de Peso Bovino con IA")
        
        pdf.showPage()
        pdf.save()
        
        buffer.seek(0)
        return buffer.read()
    
    def _generate_csv_report(self, animals: list) -> bytes:
        """
        Genera reporte CSV estructura estándar SENASAG.
        
        Headers: animal_id, numero_caravana, raza, edad_meses, 
                 peso_actual_kg, ultimo_pesaje, estado, hacienda, propietario
        """
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=SENASAGConstants.CSV_HEADERS)
        
        writer.writeheader()
        for animal in animals:
            writer.writerow({
                "animal_id": str(animal.id),
                "numero_caravana": animal.tag_number,
                "raza": BreedType.get_display_name(animal.breed_type),
                "edad_meses": animal.age_months,
                "peso_actual_kg": animal.latest_weight_kg or "N/A",
                "ultimo_pesaje": animal.latest_weighing_date.strftime('%d/%m/%Y') if animal.latest_weighing_date else "N/A",
                "estado": animal.status.value,
                "hacienda": "Hacienda Gamelera",
                "propietario": "Bruno Brito Macedo",
            })
        
        return output.getvalue().encode('utf-8')
    
    def _generate_xml_report(self, animals: list) -> bytes:
        """Genera reporte XML compatible con sistemas SENASAG."""
        report_dict = {
            "reporte_trazabilidad": {
                "@version": "1.0",
                "hacienda": {
                    "nombre": "Hacienda Gamelera",
                    "propietario": "Bruno Brito Macedo",
                    "ubicacion": "San Ignacio de Velasco, Santa Cruz, Bolivia",
                    "gps": {
                        "latitud": "-15.859500",
                        "longitud": "-60.797889",
                    },
                },
                "inventario": {
                    "total_animales": len(animals),
                    "animales": {
                        "animal": [
                            {
                                "@id": str(animal.id),
                                "caravana": animal.tag_number,
                                "raza": animal.breed_type.value,
                                "edad_meses": animal.age_months,
                                "peso_kg": animal.latest_weight_kg,
                                "estado": animal.status.value,
                            }
                            for animal in animals
                        ]
                    },
                },
            }
        }
        
        xml_string = xmltodict.unparse(report_dict, pretty=True)
        return xml_string.encode('utf-8')
    
    def _count_by_breed(self, animals: list) -> dict[BreedType, int]:
        """Cuenta animales por raza."""
        counts = {breed: 0 for breed in BreedType}
        for animal in animals:
            counts[animal.breed_type] += 1
        return counts
    
    async def send_report_email(
        self,
        report_id: UUID,
        email_to: str,
    ) -> None:
        """
        Envía reporte por email (background task).
        
        Args:
            report_id: ID del reporte generado
            email_to: Email destino (ej: bruno@haciendagamelera.com)
        """
        # Implementar con SMTP o servicio de email
        # TODO: Integrar con SendGrid/AWS SES
        pass
```

---

## Naming Conventions Python

### Archivos y Módulos

```python
✅ CORRECTO:
animal_repository.py          # snake_case
senasag_service.py
gma_schemas.py

❌ INCORRECTO:
AnimalRepository.py           # PascalCase
animal-repository.py          # kebab-case
animalRepository.py           # camelCase
```

### Clases

```python
✅ CORRECTO:
class AnimalRepository:       # PascalCase
class SENASAGService:
class GranPaititiClient:

❌ INCORRECTO:
class animal_repository:      # snake_case
class SENASAG_Service:        # SCREAMING_SNAKE_CASE
```

### Funciones y Variables

```python
✅ CORRECTO:
def create_animal():          # snake_case
def estimate_weight():
animal_id: UUID
breed_type: BreedType

❌ INCORRECTO:
def CreateAnimal():           # PascalCase
def estimateWeight():         # camelCase
```

### Constantes

```python
✅ CORRECTO:
MAX_ERROR_KG = 5.0            # SCREAMING_SNAKE_CASE
MIN_PRECISION = 0.95
HACIENDA_NAME = "Hacienda Gamelera"

❌ INCORRECTO:
maxErrorKg = 5.0              # camelCase
max_error_kg = 5.0            # snake_case (para constantes)
```

---

## Type Hints Obligatorios

### Funciones

```python
✅ CORRECTO: Type hints completos
def estimate_weight(
    image: np.ndarray,
    breed_type: BreedType,
    age_category: AgeCategory,
) -> WeightEstimationResult:
    """Estima peso con todas las anotaciones."""
    pass

async def get_animals_by_breed(
    breed: BreedType,
) -> list[Animal]:
    """Retorna lista de animales."""
    pass

❌ INCORRECTO: Sin type hints
def estimate_weight(image, breed_type, age_category):
    """Falta anotaciones de tipo."""
    pass

⚠️ ACEPTABLE SOLO EN CASOS EXCEPCIONALES:
def complex_function(*args, **kwargs) -> Any:
    """Firma dinámica justificada."""
    pass
```

### Variables

```python
✅ CORRECTO:
animal_id: UUID = uuid4()
breed_type: BreedType = BreedType.BRAHMAN
confidence: float = 0.97

✅ TAMBIÉN CORRECTO (inferido):
animal_id = uuid4()  # UUID inferido
confidence = 0.97     # float inferido
```

---

## Pydantic v2 Schemas

### Validaciones Automáticas

```python
# app/api/schemas/weighing_schemas.py

from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime
from uuid import UUID

from ...core.constants.breeds import BreedType
from ...core.constants.age_categories import AgeCategory
from ...core.constants.metrics import SystemMetrics
from ...domain.value_objects.breed_weight_ranges import BreedWeightRanges

class WeighingCreateRequest(BaseModel):
    """Request para crear pesaje (POST /weighings)."""
    
    animal_id: UUID = Field(
        ...,
        description="UUID del animal a pesar",
    )
    breed_type: BreedType = Field(
        ...,
        description="Raza del animal (una de las 7 de Hacienda Gamelera)",
    )
    age_category: AgeCategory = Field(
        ...,
        description="Categoría de edad del animal",
    )
    estimated_weight_kg: float = Field(
        ...,
        description="Peso estimado en kilogramos",
        gt=0,
        lt=1500,  # Máximo realista para bovino
    )
    confidence: float = Field(
        ...,
        description="Nivel de confianza del modelo ML (0.0-1.0)",
        ge=0.0,
        le=1.0,
    )
    processing_time_ms: int = Field(
        ...,
        description="Tiempo de procesamiento en milisegundos",
        gt=0,
    )
    image_path: Optional[str] = Field(
        None,
        description="Ruta del fotograma usado para estimación",
    )
    
    @field_validator("breed_type")
    @classmethod
    def validate_breed_type(cls, v: BreedType) -> BreedType:
        """
        Valida que raza sea una de las 7 exactas de Hacienda Gamelera.
        
        Raises:
            ValueError: Si raza inválida
        """
        if not BreedType.is_valid(v.value):
            valid_breeds = ", ".join([b.value for b in BreedType])
            raise ValueError(
                f"Raza inválida. Válidas: {valid_breeds}"
            )
        return v
    
    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """
        Valida que confidence sea ≥95% (métrica obligatoria del sistema).
        
        Raises:
            ValueError: Si confidence <95%
        """
        if v < SystemMetrics.MIN_CONFIDENCE:
            raise ValueError(
                f"Confidence {v:.2%} < {SystemMetrics.MIN_CONFIDENCE:.0%} requerido. "
                f"Sistema debe alcanzar precisión ≥95% (US-002)."
            )
        return v
    
    @field_validator("processing_time_ms")
    @classmethod
    def validate_processing_time(cls, v: int) -> int:
        """
        Valida que tiempo de procesamiento sea <3 segundos.
        
        Raises:
            ValueError: Si procesamiento >3000ms
        """
        if v > SystemMetrics.MAX_PROCESSING_TIME_MS:
            raise ValueError(
                f"Procesamiento {v}ms > {SystemMetrics.MAX_PROCESSING_TIME_MS}ms objetivo. "
                f"Sistema debe procesar en <3 segundos (US-002)."
            )
        return v
    
    @model_validator(mode='after')
    def validate_weight_range(self) -> 'WeighingCreateRequest':
        """
        Valida que peso esté en rango válido según raza y categoría de edad.
        
        Raises:
            ValueError: Si peso fuera de rango esperado
        """
        is_valid = BreedWeightRanges.validate_weight(
            weight_kg=self.estimated_weight_kg,
            breed_type=self.breed_type,
            age_category=self.age_category,
        )
        
        if not is_valid:
            expected_range = BreedWeightRanges.get_range(
                breed_type=self.breed_type,
                age_category=self.age_category,
            )
            raise ValueError(
                f"Peso {self.estimated_weight_kg} kg fuera de rango esperado "
                f"para {BreedType.get_display_name(self.breed_type)} "
                f"({AgeCategory.get_display_name(self.age_category)}): "
                f"{expected_range.min_kg}-{expected_range.max_kg} kg"
            )
        
        return self
```

---

## Beanie (MongoDB ODM)

### Models

```python
# app/database/models.py

from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

from ..core.constants.breeds import BreedType
from ..core.constants.age_categories import AgeCategory
from ..domain.enums import Gender, AnimalStatus

class AnimalModel(Document):
    """
    Modelo MongoDB para Animal usando Beanie ODM.
    
    Collection: animals
    Índices: tag_number (unique), breed_type, status
    """
    
    id: UUID = Field(default_factory=uuid4, alias="_id")
    tag_number: Indexed(str, unique=True) = Field(
        ...,
        description="Número de caravana/arete (único en Hacienda Gamelera)",
    )
    breed_type: Indexed(BreedType) = Field(
        ...,
        description="Una de las 7 razas de Hacienda Gamelera",
    )
    birth_date: datetime
    gender: Gender
    status: Indexed(AnimalStatus) = Field(default=AnimalStatus.ACTIVE)
    
    # Campos opcionales
    color: Optional[str] = None
    weight_at_birth_kg: Optional[float] = None
    mother_id: Optional[UUID] = None
    father_id: Optional[UUID] = None
    observations: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    # Metadatos
    farm_id: UUID  # Hacienda Gamelera ID
    
    class Settings:
        name = "animals"  # Nombre de colección MongoDB
        indexes = [
            "tag_number",    # Búsqueda rápida por caravana
            "breed_type",    # Filtros por raza
            "status",        # Filtros por estado
            "farm_id",       # Filtros por hacienda
        ]
    
    @property
    def age_months(self) -> int:
        """Calcula edad en meses desde fecha de nacimiento."""
        now = datetime.now()
        return (now.year - self.birth_date.year) * 12 + (now.month - self.birth_date.month)
    
    @property
    def age_category(self) -> AgeCategory:
        """Categoría de edad calculada automáticamente."""
        return AgeCategory.from_birth_date(self.birth_date)
```

---

## Testing con Pytest

### Configuración

```python
# pytest.ini

[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
asyncio_mode = auto
```

### Tests Unitarios (Services)

```python
# tests/unit/services/test_senasag_service.py

import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock

from app.services.senasag_service import SENASAGService
from app.core.constants.breeds import BreedType
from app.domain.enums import Gender, AnimalStatus

@pytest.fixture
def mock_animal_repository():
    """Mock de AnimalRepository."""
    return AsyncMock()

@pytest.fixture
def mock_senasag_repository():
    """Mock de SENASAGRepository."""
    return AsyncMock()

@pytest.fixture
def senasag_service(mock_animal_repository, mock_senasag_repository):
    """Instancia de SENASAGService con mocks."""
    return SENASAGService(
        animal_repository=mock_animal_repository,
        senasag_repository=mock_senasag_repository,
    )

@pytest.fixture
def sample_animals():
    """
    Datos de muestra: 10 animales de Hacienda Gamelera.
    
    Incluye las 7 razas exactas distribuidas.
    """
    return [
        Mock(
            id=uuid4(),
            tag_number="GAM-001",
            breed_type=BreedType.BRAHMAN,
            age_months=24,
            latest_weight_kg=450.5,
            status=AnimalStatus.ACTIVE,
        ),
        Mock(
            id=uuid4(),
            tag_number="GAM-002",
            breed_type=BreedType.NELORE,
            age_months=18,
            latest_weight_kg=380.2,
            status=AnimalStatus.ACTIVE,
        ),
        # ... resto de razas
    ]

@pytest.mark.asyncio
async def test_generate_pdf_report_success(
    senasag_service,
    mock_animal_repository,
    sample_animals,
):
    """
    Test: Genera reporte PDF exitosamente para Hacienda Gamelera.
    
    Given: 10 animales registrados en período
    When: Generar reporte PDF
    Then: Reporte generado con datos correctos de Hacienda Gamelera
    """
    # Arrange
    farm_id = uuid4()
    period_start = datetime(2024, 10, 1)
    period_end = datetime(2024, 10, 31)
    
    mock_animal_repository.get_animals_by_farm_and_period.return_value = sample_animals
    
    # Act
    report = await senasag_service.generate_report(
        farm_id=farm_id,
        report_type=SENASAGConstants.REPORT_TYPE_INVENTORY,
        period_start=period_start,
        period_end=period_end,
        format=ReportFormat.PDF,
    )
    
    # Assert
    assert report is not None
    assert report.total_animals == len(sample_animals)
    assert report.format == ReportFormat.PDF
    assert report.status == ReportStatus.GENERATED
    assert "Hacienda Gamelera" in report.file_path
    
    # Verificar que se llamó al repositorio
    mock_animal_repository.get_animals_by_farm_and_period.assert_called_once_with(
        farm_id=farm_id,
        period_start=period_start,
        period_end=period_end,
    )

@pytest.mark.asyncio
async def test_generate_report_validates_breed_types(
    senasag_service,
    mock_animal_repository,
):
    """
    Test: Valida que todos los animales tengan razas de las 7 exactas.
    
    Given: Animales con raza válida (una de las 7)
    When: Generar reporte
    Then: Reporte generado sin errores de validación
    """
    # Arrange
    animals_all_breeds = [
        Mock(breed_type=breed, latest_weight_kg=400.0)
        for breed in BreedType
    ]
    mock_animal_repository.get_animals_by_farm_and_period.return_value = animals_all_breeds
    
    # Act & Assert (no debe lanzar excepción)
    report = await senasag_service.generate_report(
        farm_id=uuid4(),
        report_type=SENASAGConstants.REPORT_TYPE_INVENTORY,
        period_start=datetime.now() - timedelta(days=30),
        period_end=datetime.now(),
        format=ReportFormat.CSV,
    )
    
    assert report.total_animals == 7  # Las 7 razas exactas
```

---

## Logging Estructurado

```python
# app/core/logging.py

from loguru import logger
import sys
import json

def setup_logging(log_level: str = "INFO"):
    """
    Configura logging estructurado con loguru.
    
    Formato JSON para observabilidad (Prometheus, Grafana, ELK).
    """
    # Remover handler por defecto
    logger.remove()
    
    # Agregar handler con formato JSON
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {name}:{function}:{line} | {message}",
        level=log_level,
        serialize=True,  # JSON format
    )
    
    # Agregar handler para archivo
    logger.add(
        "logs/app.log",
        rotation="100 MB",
        retention="30 days",
        compression="zip",
        serialize=True,
    )

# Uso en servicios
from app.core.logging import logger

async def estimate_weight(...):
    logger.info(
        "Estimación de peso iniciada",
        extra={
            "animal_id": str(animal_id),
            "breed_type": breed_type.value,
            "hacienda": "Hacienda Gamelera",
        },
    )
    
    result = await ml_service.estimate(...)
    
    logger.info(
        "Estimación de peso completada",
        extra={
            "animal_id": str(animal_id),
            "breed_type": breed_type.value,
            "weight_kg": result.weight_kg,
            "confidence": result.confidence,
            "processing_time_ms": result.processing_time_ms,
            "meets_metrics": result.confidence >= 0.95 and result.processing_time_ms < 3000,
        },
    )
```

---

## Dependency Injection

```python
# app/api/dependencies.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated

from ..core.security import verify_token
from ..database.mongodb import get_database
from ..repositories.animal_repository import AnimalRepository
from ..services.animal_service import AnimalService

# Security
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """
    Obtiene usuario actual desde JWT token.
    
    Raises:
        HTTPException 401: Si token inválido
    """
    token = credentials.credentials
    user_data = verify_token(token)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        )
    
    return User(**user_data)

# Repositories
async def get_animal_repository(
    db = Depends(get_database),
) -> AnimalRepository:
    """Inyecta AnimalRepository."""
    return AnimalRepository(database=db)

# Services
async def get_animal_service(
    repository: AnimalRepository = Depends(get_animal_repository),
) -> AnimalService:
    """Inyecta AnimalService."""
    return AnimalService(repository=repository)

# Type aliases para cleaner code
CurrentUser = Annotated[User, Depends(get_current_user)]
AnimalServiceDep = Annotated[AnimalService, Depends(get_animal_service)]
```

---

## Requirements.txt

```txt
# requirements.txt - Dependencias de producción

# FastAPI y servidor
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Validación y tipado
pydantic==2.4.2
pydantic-settings==2.0.3
email-validator==2.1.0

# Base de datos MongoDB
motor==3.3.2
beanie==1.23.6

# Autenticación
PyJWT==2.8.0
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0

# HTTP client para Gran Paitití
httpx==0.25.1

# Generación de reportes (US-007, US-009)
reportlab==4.0.7
openpyxl==3.1.2
xmltodict==0.13.0

# Códigos QR (US-008)
qrcode[pil]==7.4.2
Pillow==10.1.0

# Logging
loguru==0.7.2

# Environment
python-dotenv==1.0.0

# AWS S3 (modelos ML, backups)
boto3==1.29.7

# Background tasks (opcional, FastAPI tiene built-in)
# celery[redis]==5.3.4

# CORS
python-cors==1.0.0

# Utilidades
python-dateutil==2.8.2
```

```txt
# requirements-dev.txt - Dependencias desarrollo

-r requirements.txt

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
httpx==0.25.1  # Para tests de API

# Linting
ruff==0.1.6
black==23.11.0
isort==5.12.0
mypy==1.7.1

# Type stubs
types-python-dateutil==2.8.19

# Documentation
mkdocs==1.5.3
mkdocs-material==9.5.0
```

---

## Documentación y Docstrings (Google Style)

```python
def estimate_weight_for_breed(
    image: np.ndarray,
    breed_type: BreedType,
    age_category: AgeCategory,
) -> WeightEstimationResult:
    """
    Estima el peso de un bovino mediante modelo de IA específico por raza.
    
    Este método implementa la inferencia del modelo TensorFlow Lite entrenado
    para la raza específica, garantizando precisión >95% según los requisitos
    de Hacienda Gamelera (Bruno Brito Macedo, San Ignacio de Velasco, Bolivia).
    
    Args:
        image: Imagen preprocesada del bovino (224x224x3, normalizada 0-1).
            Debe ser fotograma seleccionado de captura continua (US-001).
        breed_type: Una de las 7 razas exactas de Hacienda Gamelera.
            Valores válidos: BRAHMAN, NELORE, ANGUS, CEBUINAS, CRIOLLO,
            PARDO_SUIZO, JERSEY.
        age_category: Categoría de edad para validar rango de peso.
            Valores válidos: TERNEROS, VAQUILLONAS_TORILLOS,
            VAQUILLONAS_TORETES, VACAS_TOROS.
    
    Returns:
        WeightEstimationResult con:
            - weight_kg (float): Peso estimado en kilogramos
            - confidence (float): Nivel de confianza (0.0-1.0), debe ser ≥0.95
            - processing_time_ms (int): Tiempo de procesamiento, debe ser <3000ms
            - breed_model_version (str): Versión del modelo usado (ej: "v1.0.0")
    
    Raises:
        InvalidBreedException: Si breed_type no es una de las 7 razas exactas.
        PrecisionBelowThresholdException: Si confidence <0.95.
        WeightOutOfRangeException: Si peso no está en rango válido para raza/edad.
        ProcessingTimeTooSlowException: Si procesamiento >3000ms.
    
    Example:
        >>> image = preprocess_image(raw_image)
        >>> result = estimate_weight_for_breed(
        ...     image=image,
        ...     breed_type=BreedType.BRAHMAN,
        ...     age_category=AgeCategory.VACAS_TOROS,
        ... )
        >>> print(f"Peso: {result.weight_kg} kg (confianza: {result.confidence:.2%})")
        Peso: 487.3 kg (confianza: 97.00%)
    
    Note:
        - Tiempo objetivo: <3 segundos (US-002)
        - Precisión objetivo: ≥95% (R² ≥0.95)
        - Error absoluto objetivo: <5 kg
        - Modelos ubicados en: models/{breed}-v{version}.tflite
        - Validado con Bruno Brito Macedo en Hacienda Gamelera
    
    See Also:
        - US-002: Estimación de Peso por Raza
        - SystemMetrics: Métricas obligatorias del sistema
        - BreedWeightRanges: Rangos de peso válidos por raza/edad
    """
    # Implementación...
    pass
```

---

## Configuración

```python
# app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Configuración de la aplicación desde variables de entorno.
    
    Archivo .env en desarrollo, environment variables en producción.
    """
    
    # General
    APP_NAME: str = "Sistema Estimación Peso Bovino IA"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Hacienda Gamelera
    HACIENDA_NAME: str = "Hacienda Gamelera"
    HACIENDA_OWNER: str = "Bruno Brito Macedo"
    
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "bovine_weight_estimation"
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # AWS S3 (modelos ML)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_S3_BUCKET_NAME: str = "bovine-ml-models"
    AWS_REGION: str = "us-east-1"
    
    # Gran Paitití API
    GRAN_PAITITI_API_URL: str = "https://sandbox.granpaititi.gob.bo/api/v1"
    GRAN_PAITITI_API_KEY: Optional[str] = None
    
    # Email (para envío reportes SENASAG)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: str = "noreply@haciendagamelera.com"
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instancia global
settings = Settings()
```

```env
# .env.example

# General
APP_NAME=Sistema Estimación Peso Bovino IA
APP_VERSION=1.0.0
DEBUG=True

# Hacienda
HACIENDA_NAME=Hacienda Gamelera
HACIENDA_OWNER=Bruno Brito Macedo

# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=bovine_weight_estimation

# JWT (generar con: openssl rand -hex 32)
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# AWS S3 (opcional en desarrollo)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_S3_BUCKET_NAME=bovine-ml-models
AWS_REGION=us-east-1

# Gran Paitití (sandbox en desarrollo)
GRAN_PAITITI_API_URL=https://sandbox.granpaititi.gob.bo/api/v1
GRAN_PAITITI_API_KEY=

# Email SMTP (opcional en desarrollo)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=noreply@haciendagamelera.com
```

---

## Referencias

- **Estándares de arquitectura**: `docs/standards/architecture-standards.md`
- **Product Backlog**: `docs/product/product-backlog.md`
- **Sprint 3 Goal**: `docs/sprints/sprint-03/sprint-goal.md`
- **PEP 8**: https://pep8.org/
- **FastAPI Best Practices**: https://fastapi.tiangolo.com/tutorial/

---

**Documento de Estándares Python/FastAPI v1.0**  
**Fecha**: 28 octubre 2024  
**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Sprint 3**: US-007 (SENASAG), US-008 (Gran Paitití), US-009 (ASOCEBU)

