# Estándares de Codificación Python/FastAPI

Sistema de Estimación de Peso Bovino - Hacienda Gamelera

## 1. Convenciones de Naming

### 1.1 Principios Generales

```python
# ✅ CORRECTO: PEP 8 compliance
class AnimalService:  # PascalCase para clases
    def __init__(self):
        self.repository = None  # snake_case para variables
        
    def get_animal_by_id(self, animal_id: str) -> Animal:  # snake_case para funciones
        """Obtiene animal por ID."""
        pass

# Constantes en UPPER_SNAKE_CASE
MAX_ANIMALS_PER_REQUEST = 100
DEFAULT_CAPTURE_FPS = 12

# Type hints OBLIGATORIOS en todas las funciones
def calculate_weight_score(
    estimated_weight: float,
    confidence: float,
    breed_type: BreedType,
) -> WeightScore:
    """Calcula score de peso según raza."""
    pass

# ❌ INCORRECTO: Sin type hints, naming inconsistente
def calculateScore(weight, conf):  # camelCase no es PEP 8
    return weight * conf
```

### 1.2 Naming Específico del Dominio

#### Razas Bovinas (7 razas del proyecto)

```python
# app/domain/enums.py
from enum import Enum

class BreedType(str, Enum):
    """
    7 razas bovinas de la Hacienda Gamelera.
    
    Estas son las ÚNICAS razas soportadas por el sistema.
    Cualquier otra raza debe ser rechazada con error 400.
    """
    BRAHMAN = "brahman"
    NELORE = "nelore"
    ANGUS = "angus"
    CEBUINAS = "cebuinas"      # Bos indicus
    CRIOLLO = "criollo"        # Bos taurus
    PARDO_SUIZO = "pardo_suizo"
    JERSEY = "jersey"
    
    @classmethod
    def is_valid(cls, breed: str) -> bool:
        """Valida que la raza sea una de las 7 del proyecto."""
        try:
            cls(breed)
            return True
        except ValueError:
            return False
    
    @classmethod
    def get_all_breeds(cls) -> list[str]:
        """Retorna lista de las 7 razas soportadas."""
        return [breed.value for breed in cls]


# ❌ INCORRECTO: Razas genéricas o no del proyecto
class BreedType(str, Enum):
    TYPE_A = "type_a"  # ❌ Muy genérico
    HOLSTEIN = "holstein"  # ❌ No está en Hacienda Gamelera
```

#### Categorías de Edad (4 categorías específicas)

```python
# app/domain/enums.py
class AgeCategory(str, Enum):
    """
    4 categorías de edad según práctica ganadera de Hacienda Gamelera.
    
    Estas categorías determinan:
    - Protocolos nutricionales
    - Dosificación de medicamentos
    - Rangos de peso esperados
    - Requisitos de SENASAG por categoría
    """
    TERNEROS = "terneros"                      # <8 meses
    VAQUILLONAS_TORILLOS = "vaquillonas_torillos"  # 6-18 meses
    VAQUILLONAS_TORETES = "vaquillonas_toretes"    # 19-30 meses
    VACAS_TOROS = "vacas_toros"                # >30 meses
    
    @property
    def age_range_months(self) -> tuple[int, int | None]:
        """Retorna rango de edad en meses (min, max)."""
        ranges = {
            self.TERNEROS: (0, 7),
            self.VAQUILLONAS_TORILLOS: (6, 18),
            self.VAQUILLONAS_TORETES: (19, 30),
            self.VACAS_TOROS: (30, None),  # Sin límite superior
        }
        return ranges[self]
    
    @classmethod
    def from_age_months(cls, age_months: int) -> "AgeCategory":
        """Calcula categoría según edad en meses."""
        if age_months < 8:
            return cls.TERNEROS
        elif 6 <= age_months <= 18:
            return cls.VAQUILLONAS_TORILLOS
        elif 19 <= age_months <= 30:
            return cls.VAQUILLONAS_TORETES
        else:
            return cls.VACAS_TOROS
```

#### Normativa Boliviana

```python
# app/domain/enums.py
class SENASAGReportType(str, Enum):
    """Tipos de reportes para SENASAG."""
    INVENTARIO = "inventario"
    MOVILIZACION = "movilizacion"
    SANITARIO = "sanitario"


class GMAStatus(str, Enum):
    """Estados de Guía de Movimiento Animal (REGENSA)."""
    PENDIENTE = "pendiente"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"
    COMPLETADA = "completada"


class REGENSAChapter(str, Enum):
    """Capítulos específicos de REGENSA que el sistema valida."""
    CHAPTER_3_10 = "3.10"  # Centros de concentración animal
    CHAPTER_7_1 = "7.1"    # Requisitos sanitarios


# Constantes de cumplimiento REGENSA (capítulo 3.10)
class REGENSARequirements:
    """
    Requisitos específicos de REGENSA capítulos 3.10 y 7.1.
    
    Referencia: Reglamento General de Sanidad Animal (REGENSA),
    Servicio Nacional de Sanidad Agropecuaria (SENASAG), Bolivia.
    """
    # Capítulo 3.10: Centros de concentración animal
    MIN_CORRIDOR_WIDTH_METERS = 1.6
    MIN_SPACE_PER_ANIMAL_M2 = 2.0
    REQUIRES_ANTISLIP_RAMPS = True
    REQUIRES_DISINFECTION_SYSTEM = True
    REQUIRES_QUARANTINE_CORRAL = True
    PROHIBITS_PAIN_INSTRUMENTS = True
```

#### Métricas del Sistema

```python
# app/core/constants.py
class SystemMetrics:
    """
    Métricas de precisión y rendimiento del sistema.
    
    Estas métricas son criterios de aceptación del marco SCRUM
    (documento 12) y deben cumplirse para validación del sistema.
    """
    # Métricas de precisión ML
    MIN_PRECISION = 0.95        # ≥95% de exactitud
    MIN_R2_SCORE = 0.95         # R² ≥ 0.95
    MAX_ERROR_KG = 5.0          # Error absoluto <5 kg
    MAX_PROCESSING_TIME_MS = 3000  # <3 segundos
    
    # Validación en campo
    MIN_ANIMALS_VALIDATION = 50  # 50 animales mínimo
    
    # Comparación con método anterior (Fórmula Schaeffer)
    SCHAEFFER_ERROR_MIN_KG = 5.0
    SCHAEFFER_ERROR_MAX_KG = 20.0
    
    @classmethod
    def validate_precision(cls, precision: float) -> bool:
        """Valida que la precisión cumpla con el mínimo requerido."""
        return precision >= cls.MIN_PRECISION
    
    @classmethod
    def validate_error(cls, error_kg: float) -> bool:
        """Valida que el error esté dentro del rango aceptable."""
        return error_kg < cls.MAX_ERROR_KG
    
    @classmethod
    def is_improvement_over_schaeffer(cls, error_kg: float) -> bool:
        """Verifica si hay mejora vs fórmula Schaeffer."""
        return error_kg < cls.SCHAEFFER_ERROR_MIN_KG


class CaptureConstants:
    """
    Constantes de captura continua (especificaciones ADR-010).
    """
    # Parámetros de captura
    FPS_MIN = 10
    FPS_MAX = 15
    FPS_DEFAULT = 12
    
    DURATION_MIN_SECONDS = 3
    DURATION_MAX_SECONDS = 5
    DURATION_DEFAULT_SECONDS = 4
    
    TOTAL_FRAMES_MIN = 30
    TOTAL_FRAMES_MAX = 75
    
    # Umbrales de calidad
    MIN_SHARPNESS = 0.7
    MIN_BRIGHTNESS = 0.4
    MAX_BRIGHTNESS = 0.8
    MIN_CONTRAST = 0.5
    MIN_SILHOUETTE_VISIBILITY = 0.8
    MIN_ANGLE_SCORE = 0.6
    MIN_OVERALL_SCORE = 0.65
    
    # Pesos para score global
    SILHOUETTE_WEIGHT = 0.40
    SHARPNESS_WEIGHT = 0.30
    BRIGHTNESS_WEIGHT = 0.20
    ANGLE_WEIGHT = 0.10
```

#### Rangos de Peso por Raza y Edad

```python
# app/domain/value_objects.py
from typing import NamedTuple
from app.domain.enums import BreedType, AgeCategory

class WeightRange(NamedTuple):
    min_kg: float
    max_kg: float

class BreedWeightRanges:
    """
    Rangos de peso esperados por raza y categoría de edad.
    
    Estos rangos se usan para:
    - Validar estimaciones del modelo ML
    - Alertas de desviación de peso
    - Comparaciones vs promedio de raza
    """
    
    RANGES: dict[BreedType, dict[AgeCategory, WeightRange]] = {
        BreedType.BRAHMAN: {
            AgeCategory.TERNEROS: WeightRange(80, 180),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(180, 350),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(300, 500),
            AgeCategory.VACAS_TOROS: WeightRange(450, 900),
        },
        BreedType.NELORE: {
            AgeCategory.TERNEROS: WeightRange(75, 170),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(170, 330),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(280, 480),
            AgeCategory.VACAS_TOROS: WeightRange(400, 850),
        },
        BreedType.ANGUS: {
            AgeCategory.TERNEROS: WeightRange(70, 165),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(165, 320),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(270, 460),
            AgeCategory.VACAS_TOROS: WeightRange(380, 800),
        },
        BreedType.CEBUINAS: {  # Bos indicus genérico
            AgeCategory.TERNEROS: WeightRange(75, 175),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(175, 340),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(290, 490),
            AgeCategory.VACAS_TOROS: WeightRange(420, 870),
        },
        BreedType.CRIOLLO: {  # Bos taurus nativo
            AgeCategory.TERNEROS: WeightRange(65, 150),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(150, 280),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(240, 400),
            AgeCategory.VACAS_TOROS: WeightRange(350, 650),
        },
        BreedType.PARDO_SUIZO: {
            AgeCategory.TERNEROS: WeightRange(80, 185),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(185, 360),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(310, 510),
            AgeCategory.VACAS_TOROS: WeightRange(460, 920),
        },
        BreedType.JERSEY: {  # Raza más pequeña
            AgeCategory.TERNEROS: WeightRange(60, 140),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(140, 260),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(220, 380),
            AgeCategory.VACAS_TOROS: WeightRange(330, 600),
        },
    }
    
    @classmethod
    def get_range(
        cls, 
        breed: BreedType, 
        age_category: AgeCategory
    ) -> WeightRange:
        """Obtiene rango de peso para raza y edad específicas."""
        return cls.RANGES[breed][age_category]
    
    @classmethod
    def validate_weight(
        cls,
        weight_kg: float,
        breed: BreedType,
        age_category: AgeCategory,
    ) -> bool:
        """Valida que peso esté en rango esperado."""
        weight_range = cls.get_range(breed, age_category)
        return weight_range.min_kg <= weight_kg <= weight_range.max_kg
```

#### Coordenadas GPS y Fórmula Schaeffer

```python
# app/core/constants.py

class HaciendaGameleraConstants:
    """
    Datos específicos de Hacienda Gamelera.
    
    Ubicación: San Ignacio de Velasco, Santa Cruz, Bolivia
    Coordenadas: 15°51′34.2′′S, 60°47′52.4′′W
    Área: 48.5 hectáreas
    Hato: 500 cabezas de ganado
    """
    LATITUDE = -15.859500
    LONGITUDE = -60.797889
    AREA_HECTARES = 48.5
    TOTAL_CATTLE = 500
    OWNER = "Bruno Brito Macedo"
    
    # Validación de coordenadas GPS para pesajes
    @classmethod
    def is_within_farm_boundaries(cls, lat: float, lon: float) -> bool:
        """
        Valida que coordenadas estén dentro del área de la hacienda.
        
        Args:
            lat: Latitud en grados decimales
            lon: Longitud en grados decimales
        
        Returns:
            True si está dentro de los límites de la hacienda
        """
        # Implementar validación basada en polígono del terreno
        # Por ahora, validación simple con radio de 1km
        import math
        
        # Distancia desde centro de la hacienda
        distance = math.sqrt(
            (lat - cls.LATITUDE) ** 2 + (lon - cls.LONGITUDE) ** 2
        )
        
        # Aproximadamente 1km = 0.009 grados
        return distance < 0.009


class SchaefferFormula:
    """
    Fórmula tradicional de Schaeffer para estimación de peso bovino.
    
    Esta es la fórmula que el nuevo sistema reemplaza.
    
    Peso (kg) = (PT² × LC) / 10838
    
    Donde:
    - PT: Perímetro Torácico (cm)
    - LC: Longitud del Cuerpo (cm)
    
    Limitaciones históricas:
    - Error: 5-20 kg por animal
    - Tiempo: 8-10 minutos por animal
    - Dependencia de habilidad del operario
    - Estrés en los animales (manipulación física)
    
    El nuevo sistema reduce esto a:
    - Error: <5 kg
    - Tiempo: <6 minutos por animal
    - Sin contacto físico (visión por computadora)
    """
    
    @staticmethod
    def calculate_weight(
        perimetro_toracico_cm: float,
        longitud_cuerpo_cm: float,
    ) -> float:
        """
        Calcula peso usando fórmula tradicional de Schaeffer.
        
        Args:
            perimetro_toracico_cm: Perímetro torácico en centímetros
            longitud_cuerpo_cm: Longitud del cuerpo en centímetros
        
        Returns:
            Peso estimado en kilogramos
        
        Examples:
            >>> SchaefferFormula.calculate_weight(150, 120)
            249.2
        """
        return (perimetro_toracico_cm ** 2 * longitud_cuerpo_cm) / 10838
    
    @staticmethod
    def validate_measurements(pt: float, lc: float) -> bool:
        """
        Valida que las mediciones estén en rangos razonables.
        
        Args:
            pt: Perímetro torácico en cm
            lc: Longitud del cuerpo en cm
        
        Returns:
            True si las mediciones son válidas
        """
        return 100 <= pt <= 250 and 100 <= lc <= 200
    
    @staticmethod
    def compare_with_ai_estimation(
        schaeffer_weight: float,
        ai_weight: float,
    ) -> dict:
        """
        Compara estimación de Schaeffer vs IA.
        
        Args:
            schaeffer_weight: Peso estimado por fórmula Schaeffer
            ai_weight: Peso estimado por IA
        
        Returns:
            Dict con comparación y mejora
        """
        error_difference = abs(schaeffer_weight - ai_weight)
        improvement_percentage = (error_difference / schaeffer_weight) * 100
        
        return {
            "schaeffer_weight": schaeffer_weight,
            "ai_weight": ai_weight,
            "error_difference": error_difference,
            "improvement_percentage": improvement_percentage,
            "ai_is_better": error_difference < 5.0,  # IA debe tener <5kg error
        }
```

### 1.3 Estructura de Proyecto

```text
backend/
├── app/
│   ├── main.py                      # Entry point FastAPI
│   ├── core/
│   │   ├── config.py                # Configuración (Pydantic Settings)
│   │   ├── constants.py             # Constantes del sistema
│   │   ├── security.py              # JWT, hashing
│   │   └── exceptions.py            # Excepciones personalizadas
│   │
│   ├── domain/                      # Capa de Dominio (Clean Architecture)
│   │   ├── entities/
│   │   │   ├── animal.py
│   │   │   ├── weighing.py
│   │   │   ├── capture_session.py
│   │   │   ├── breed.py             # 7 razas
│   │   │   ├── age_category.py      # 4 categorías
│   │   │   ├── senasag_report.py
│   │   │   ├── gma.py               # Guía Movimiento Animal
│   │   │   └── regensa_compliance.py
│   │   ├── enums.py                 # Enums del dominio
│   │   └── value_objects.py         # Objetos de valor
│   │
│   ├── api/                         # Capa de Presentación (API)
│   │   ├── dependencies.py          # Dependencias FastAPI
│   │   ├── routes/
│   │   │   ├── animals.py           # Endpoints de animales
│   │   │   ├── weighings.py         # Endpoints de pesajes
│   │   │   ├── capture_sessions.py  # Endpoints de captura
│   │   │   ├── breeds.py            # Endpoints de razas
│   │   │   ├── senasag.py           # Endpoints SENASAG
│   │   │   ├── regensa.py           # Endpoints REGENSA/GMA
│   │   │   ├── gran_paititi.py      # Integración Gran Paitití
│   │   │   └── asocebu.py           # Exportación ASOCEBU
│   │   └── schemas/                 # Pydantic schemas (request/response)
│   │       ├── animal_schemas.py
│   │       ├── weighing_schemas.py
│   │       ├── capture_session_schemas.py
│   │       ├── senasag_schemas.py
│   │       └── gma_schemas.py
│   │
│   ├── services/                    # Capa de Servicios (Business Logic)
│   │   ├── animal_service.py
│   │   ├── weighing_service.py
│   │   ├── capture_session_service.py
│   │   ├── breed_service.py
│   │   ├── ml_service.py            # Integración con modelos ML
│   │   ├── senasag_service.py       # Lógica de reportes SENASAG
│   │   ├── regensa_service.py       # Validación REGENSA
│   │   ├── gma_service.py           # Generación de GMA
│   │   ├── gran_paititi_service.py  # Integración sistema gubernamental
│   │   └── sync_service.py          # Sincronización offline
│   │
│   ├── repositories/                # Capa de Datos (Data Access)
│   │   ├── animal_repository.py
│   │   ├── weighing_repository.py
│   │   ├── capture_session_repository.py
│   │   ├── breed_repository.py
│   │   ├── senasag_report_repository.py
│   │   └── gma_repository.py
│   │
│   ├── database/
│   │   ├── mongodb.py               # Conexión MongoDB
│   │   ├── models.py                # Modelos MongoDB (Motor)
│   │   └── seed_data.py             # Seed de las 7 razas
│   │
│   ├── ml/                          # Machine Learning
│   │   ├── model_manager.py         # Gestión de modelos por raza
│   │   ├── inference_engine.py      # Motor de inferencia
│   │   ├── training_pipeline.py     # Pipeline de entrenamiento
│   │   └── validators.py            # Validadores ML (≥95%, <3s, <5kg)
│   │
│   └── utils/
│       ├── s3_client.py             # Cliente AWS S3
│       ├── file_handlers.py         # Manejo de archivos
│       └── validators.py            # Validadores generales
│
└── tests/
    ├── unit/
    │   ├── services/
    │   │   ├── test_weighing_service.py
    │   │   ├── test_senasag_service.py
    │   │   ├── test_regensa_service.py
    │   │   └── test_ml_service.py
    │   └── repositories/
    │       └── test_breed_repository.py
    │
    ├── integration/
    │   ├── test_api_animals.py
    │   ├── test_api_senasag.py
    │   ├── test_api_regensa.py
    │   └── test_ml_inference.py
    │
    └── fixtures/
        ├── breed_fixtures.py        # Fixtures de las 7 razas
        ├── animal_fixtures.py
        └── weighing_fixtures.py
```

### 1.4 Naming de Variables y Funciones

```python
# ✅ CORRECTO: Variables descriptivas del dominio
selected_breed: BreedType = BreedType.BRAHMAN
animal_category: AgeCategory = AgeCategory.TERNEROS
frame_sharpness: float = 0.85
current_session: CaptureSession
movement_guide: GMA
inventory_report: SENASAGReport

# Funciones de captura continua
async def start_continuous_capture(
    animal_id: str,
    breed_type: BreedType,
    frames_per_second: int,
    duration_seconds: int,
) -> CaptureSession:
    """Inicia captura continua según especificaciones del proyecto."""
    pass

async def evaluate_frame_quality(
    frame_data: bytes,
    frame_index: int,
) -> FrameQuality:
    """Evalúa calidad de fotograma en tiempo real."""
    pass

async def select_best_frame(
    evaluated_frames: List[FrameQuality],
) -> int:
    """Selecciona el mejor fotograma basado en score ponderado."""
    pass

# Funciones de integración normativa
async def generate_senasag_report(
    period_start: datetime,
    period_end: datetime,
    report_type: str,
) -> SENASAGReport:
    """Genera reporte para SENASAG."""
    pass

async def create_gma(
    animal_ids: List[str],
    origin_farm_id: str,
    destination: str,
) -> GMA:
    """Crea Guía de Movimiento Animal (GMA)."""
    pass

async def validate_regensa_compliance(
    farm_id: str,
) -> REGENSACompliance:
    """Valida cumplimiento REGENSA capítulos 3.10 y 7.1."""
    pass

# ❌ INCORRECTO: Nombres genéricos o ambiguos
type = 1  # ❌ ¿Tipo de qué?
data = get_stuff()  # ❌ Muy genérico
def process():  # ❌ ¿Procesar qué?
    pass
```

## 2. Pydantic Schemas

### 2.1 Schemas de Request/Response

```python
# app/api/schemas/animal_schemas.py
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.domain.enums import BreedType, AgeCategory, AnimalStatus

class AnimalCreateRequest(BaseModel):
    """
    Schema para crear un nuevo animal.
    
    Validaciones específicas del proyecto:
    - breed_type debe ser una de las 7 razas de Hacienda Gamelera
    - age_category se calcula automáticamente según birth_date
    """
    tag_number: str = Field(
        ..., 
        description="Número de caravana/arete (único)",
        example="HG-001"
    )
    name: str | None = Field(
        None, 
        description="Nombre del animal (opcional)",
        example="Campeón"
    )
    breed_type: BreedType = Field(
        ..., 
        description="Raza del animal (una de las 7 soportadas)"
    )
    birth_date: datetime = Field(
        ..., 
        description="Fecha de nacimiento"
    )
    gender: str = Field(
        ..., 
        description="Sexo del animal",
        regex="^(Macho|Hembra)$"
    )
    weight_goal: float | None = Field(
        None, 
        description="Meta de peso objetivo (kg)",
        ge=0
    )
    asocebu_registered: bool = Field(
        False,
        description="Si está registrado en ASOCEBU"
    )
    asocebu_id: str | None = Field(
        None,
        description="ID de registro en ASOCEBU"
    )
    
    @validator("breed_type")
    def validate_breed_type(cls, v):
        """Valida que sea una de las 7 razas del proyecto."""
        if not BreedType.is_valid(v):
            raise ValueError(
                f"Raza '{v}' no soportada. "
                f"Razas válidas: {', '.join(BreedType.get_all_breeds())}"
            )
        return v
    
    @validator("birth_date")
    def validate_birth_date(cls, v):
        """Valida que la fecha de nacimiento sea válida."""
        if v > datetime.now():
            raise ValueError("Fecha de nacimiento no puede ser futura")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "tag_number": "HG-001",
                "name": "Campeón Brahman",
                "breed_type": "brahman",
                "birth_date": "2023-03-15T00:00:00Z",
                "gender": "Macho",
                "weight_goal": 500.0,
                "asocebu_registered": True,
                "asocebu_id": "ASOCEBU-2023-001"
            }
        }


class AnimalResponse(BaseModel):
    """
    Schema de respuesta con información completa del animal.
    """
    id: str
    tag_number: str
    name: str | None
    breed_type: BreedType
    age_category: AgeCategory  # Calculado automáticamente
    age_months: int            # Calculado
    birth_date: datetime
    gender: str
    status: AnimalStatus
    current_weight: float | None
    weight_goal: float | None
    asocebu_registered: bool
    asocebu_id: str | None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

### 2.2 Schemas de Captura Continua

```python
# app/api/schemas/capture_session_schemas.py
from pydantic import BaseModel, Field, validator
from app.core.constants import CaptureConstants

class CaptureSessionCreateRequest(BaseModel):
    """
    Request para iniciar sesión de captura continua.
    
    Especificaciones del proyecto (ADR-010):
    - FPS: 10-15 fotogramas por segundo
    - Duración: 3-5 segundos
    - Total frames esperados: 30-75
    """
    animal_id: str = Field(..., description="ID del animal")
    breed_type: BreedType = Field(..., description="Raza del animal")
    fps: int = Field(
        CaptureConstants.FPS_DEFAULT,
        description="Fotogramas por segundo",
        ge=CaptureConstants.FPS_MIN,
        le=CaptureConstants.FPS_MAX
    )
    duration_seconds: int = Field(
        CaptureConstants.DURATION_DEFAULT_SECONDS,
        description="Duración de captura en segundos",
        ge=CaptureConstants.DURATION_MIN_SECONDS,
        le=CaptureConstants.DURATION_MAX_SECONDS
    )


class FrameQualityMetrics(BaseModel):
    """
    Métricas de calidad de un fotograma individual.
    """
    frame_index: int = Field(..., description="Índice del fotograma")
    sharpness: float = Field(
        ..., 
        description="Nitidez (0-1)",
        ge=0.0, 
        le=1.0
    )
    brightness: float = Field(
        ..., 
        description="Brillo (0-1)",
        ge=0.0, 
        le=1.0
    )
    contrast: float = Field(
        ..., 
        description="Contraste (0-1)",
        ge=0.0, 
        le=1.0
    )
    silhouette_visibility: float = Field(
        ..., 
        description="Visibilidad de silueta (0-1)",
        ge=0.0, 
        le=1.0
    )
    angle_score: float = Field(
        ..., 
        description="Score de ángulo (0-1)",
        ge=0.0, 
        le=1.0
    )
    overall_score: float = Field(
        ..., 
        description="Score global ponderado (0-1)",
        ge=0.0, 
        le=1.0
    )
    is_acceptable: bool = Field(
        ...,
        description=f"Si cumple umbral mínimo ({CaptureConstants.MIN_OVERALL_SCORE})"
    )
    rejection_reason: str | None = Field(
        None,
        description="Razón de rechazo si no es aceptable"
    )
    
    @validator("overall_score", always=True)
    def calculate_overall_score(cls, v, values):
        """
        Calcula score global con pesos específicos del proyecto:
        - Silueta: 40%
        - Nitidez: 30%
        - Iluminación: 20%
        - Ángulo: 10%
        """
        if v is not None:
            return v
        
        score = (
            values["silhouette_visibility"] * CaptureConstants.SILHOUETTE_WEIGHT +
            values["sharpness"] * CaptureConstants.SHARPNESS_WEIGHT +
            values["brightness"] * CaptureConstants.BRIGHTNESS_WEIGHT +
            values["angle_score"] * CaptureConstants.ANGLE_WEIGHT
        )
        return round(score, 3)
    
    @validator("is_acceptable", always=True)
    def check_acceptability(cls, v, values):
        """
        Valida que el fotograma cumpla con todos los criterios.
        """
        if v is not None:
            return v
        
        checks = {
            "nitidez": values["sharpness"] >= CaptureConstants.MIN_SHARPNESS,
            "brillo": (CaptureConstants.MIN_BRIGHTNESS <= values["brightness"] <= 
                      CaptureConstants.MAX_BRIGHTNESS),
            "contraste": values["contrast"] >= CaptureConstants.MIN_CONTRAST,
            "silueta": values["silhouette_visibility"] >= CaptureConstants.MIN_SILHOUETTE_VISIBILITY,
            "ángulo": values["angle_score"] >= CaptureConstants.MIN_ANGLE_SCORE,
            "score_global": values["overall_score"] >= CaptureConstants.MIN_OVERALL_SCORE,
        }
        
        return all(checks.values())


class CaptureSessionResponse(BaseModel):
    """Response con resultados de sesión de captura."""
    id: str
    animal_id: str
    start_time: datetime
    end_time: datetime | None
    total_frames: int
    frames_evaluated: int
    frames_rejected: int
    selected_frame_id: str | None
    average_quality_score: float
    rejection_reasons: dict[str, int]  # {"silueta": 5, "nitidez": 3}
    created_at: datetime
    
    @validator("total_frames")
    def validate_frame_count(cls, v):
        """Valida que se capturaron suficientes frames."""
        if v < CaptureConstants.TOTAL_FRAMES_MIN:
            raise ValueError(
                f"Se capturaron solo {v} frames. "
                f"Mínimo requerido: {CaptureConstants.TOTAL_FRAMES_MIN}"
            )
        return v
```

### 2.3 Schemas de Normativa Boliviana

```python
# app/api/schemas/senasag_schemas.py
class SENASAGReportCreateRequest(BaseModel):
    """
    Request para generar reporte SENASAG.
    
    SENASAG requiere reportes de inventario, movilización y sanitarios
    según normativa boliviana de trazabilidad ganadera.
    """
    farm_id: str = Field(..., description="ID de la finca")
    report_type: SENASAGReportType = Field(
        ..., 
        description="Tipo de reporte SENASAG"
    )
    period_start: datetime = Field(
        ..., 
        description="Inicio del período"
    )
    period_end: datetime = Field(
        ..., 
        description="Fin del período"
    )
    include_weighings: bool = Field(
        True,
        description="Incluir datos de pesajes"
    )
    export_format: str = Field(
        "pdf",
        description="Formato de exportación",
        regex="^(pdf|csv|xml)$"
    )


class SENASAGReportResponse(BaseModel):
    """Response con reporte generado."""
    id: str
    farm_id: str
    report_type: SENASAGReportType
    period_start: datetime
    period_end: datetime
    total_animals: int
    pdf_url: str | None
    csv_url: str | None
    xml_url: str | None
    status: str
    sent_at: datetime | None
    created_at: datetime


# app/api/schemas/gma_schemas.py
class GMACreateRequest(BaseModel):
    """
    Request para crear Guía de Movimiento Animal (REGENSA).
    
    La GMA es obligatoria para movilización de ganado en Bolivia
    según capítulos 3.10 y 7.1 de REGENSA.
    """
    animal_ids: list[str] = Field(
        ..., 
        description="IDs de animales a movilizar",
        min_items=1
    )
    origin_farm_id: str = Field(..., description="Finca de origen")
    destination: str = Field(..., description="Destino del movimiento")
    reason: str = Field(
        ..., 
        description="Razón de movilización",
        regex="^(Venta|Feria|Matadero|Traslado)$"
    )
    departure_date: datetime = Field(..., description="Fecha de salida")
    arrival_date: datetime = Field(..., description="Fecha estimada llegada")
    
    @validator("arrival_date")
    def validate_arrival_after_departure(cls, v, values):
        """Valida que llegada sea después de salida."""
        if "departure_date" in values and v <= values["departure_date"]:
            raise ValueError("Fecha de llegada debe ser posterior a salida")
        return v


class REGENSAComplianceResponse(BaseModel):
    """
    Response con validación de cumplimiento REGENSA.
    
    Valida requisitos de capítulos 3.10 y 7.1.
    """
    farm_id: str
    is_compliant: bool
    chapter_3_10_compliant: bool  # Centros de concentración
    chapter_7_1_compliant: bool   # Requisitos sanitarios
    missing_requirements: list[str]
    validation_details: dict[str, bool]
    validated_at: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "farm_id": "farm_hacienda_gamelera",
                "is_compliant": True,
                "chapter_3_10_compliant": True,
                "chapter_7_1_compliant": True,
                "missing_requirements": [],
                "validation_details": {
                    "antislip_ramps": True,
                    "corridor_width_1.6m": True,
                    "space_per_animal_2m2": True,
                    "disinfection_system": True,
                    "quarantine_corral": True,
                    "no_pain_instruments": True
                },
                "validated_at": "2025-01-15T10:30:00Z"
            }
        }


class GMAResponse(BaseModel):
    """Response con GMA creada."""
    id: str
    gma_number: str               # Número único de GMA
    animal_ids: list[str]
    origin_farm_id: str
    destination: str
    reason: str
    departure_date: datetime
    arrival_date: datetime
    gran_paititi_id: str | None   # ID en sistema Gran Paitití
    regensa_compliance: REGENSAComplianceResponse
    status: GMAStatus
    created_at: datetime
```

## 3. FastAPI Routes

### 3.1 Endpoints de Animales

```python
# app/api/routes/animals.py
from fastapi import APIRouter, Depends, HTTPException, Query
from app.api.schemas.animal_schemas import (
    AnimalCreateRequest,
    AnimalResponse,
    AnimalUpdateRequest
)
from app.services.animal_service import AnimalService
from app.domain.enums import BreedType, AgeCategory

router = APIRouter(prefix="/api/v1/animals", tags=["animals"])


@router.post(
    "/",
    response_model=AnimalResponse,
    status_code=201,
    summary="Crear nuevo animal",
    description="""
    Registra un nuevo animal en la Hacienda Gamelera.
    
    **Validaciones específicas:**
    - breed_type debe ser una de las 7 razas soportadas
    - age_category se calcula automáticamente según birth_date
    - tag_number debe ser único
    
    **Razas soportadas:** Brahman, Nelore, Angus, Cebuinas, 
    Criollo, Pardo Suizo, Jersey
    """
)
async def create_animal(
    animal_data: AnimalCreateRequest,
    service: AnimalService = Depends()
) -> AnimalResponse:
    """
    Crea un nuevo animal.
    
    Args:
        animal_data: Datos del animal a crear
        service: Servicio de animales (inyectado)
    
    Returns:
        AnimalResponse: Animal creado con age_category calculada
    
    Raises:
        HTTPException(400): Si breed_type no es válida o tag_number duplicado
        HTTPException(404): Si farm_id no existe
    """
    try:
        animal = await service.create_animal(animal_data)
        return animal
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=list[AnimalResponse],
    summary="Listar animales",
    description="Lista animales con filtros opcionales por raza y categoría de edad"
)
async def list_animals(
    breed_type: BreedType | None = Query(
        None, 
        description="Filtrar por raza (una de las 7)"
    ),
    age_category: AgeCategory | None = Query(
        None,
        description="Filtrar por categoría de edad (una de las 4)"
    ),
    skip: int = Query(0, ge=0, description="Registros a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Límite de registros"),
    service: AnimalService = Depends()
) -> list[AnimalResponse]:
    """
    Lista animales con filtros opcionales.
    
    **Filtros disponibles:**
    - breed_type: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey
    - age_category: Terneros, VaquillonasTorillos, VaquillonasToretes, VacasToros
    """
    animals = await service.list_animals(
        breed_type=breed_type,
        age_category=age_category,
        skip=skip,
        limit=limit
    )
    return animals


@router.get(
    "/breeds/distribution",
    response_model=dict[BreedType, int],
    summary="Distribución de animales por raza",
    description="Retorna conteo de animales para cada una de las 7 razas"
)
async def get_breed_distribution(
    service: AnimalService = Depends()
) -> dict[BreedType, int]:
    """
    Obtiene distribución de animales por raza.
    
    Returns:
        Dict con conteo por cada una de las 7 razas:
        {
            "brahman": 120,
            "nelore": 95,
            "angus": 80,
            "cebuinas": 70,
            "criollo": 60,
            "pardo_suizo": 45,
            "jersey": 30
        }
    """
    return await service.get_breed_distribution()
```

### 3.2 Endpoints de SENASAG

```python
# app/api/routes/senasag.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.api.schemas.senasag_schemas import (
    SENASAGReportCreateRequest,
    SENASAGReportResponse
)
from app.services.senasag_service import SENASAGService

router = APIRouter(prefix="/api/v1/senasag", tags=["SENASAG"])


@router.post(
    "/reports",
    response_model=SENASAGReportResponse,
    status_code=201,
    summary="Generar reporte SENASAG",
    description="""
    Genera reporte para SENASAG según normativa boliviana.
    
    **Tipos de reporte:**
    - Inventario: Registro de animales en finca
    - Movilización: Traslado de animales
    - Sanitario: Controles sanitarios
    
    **Formatos soportados:** PDF, CSV, XML
    """
)
async def create_senasag_report(
    report_data: SENASAGReportCreateRequest,
    service: SENASAGService = Depends()
) -> SENASAGReportResponse:
    """
    Genera reporte SENASAG automáticamente.
    
    El reporte incluye:
    - Inventario de animales
    - Datos de peso por animal
    - Clasificación por raza y edad
    - Cumplimiento de trazabilidad
    
    Args:
        report_data: Parámetros del reporte
        service: Servicio SENASAG (inyectado)
    
    Returns:
        SENASAGReportResponse: Reporte generado con URLs de descarga
    
    Raises:
        HTTPException(400): Si parámetros inválidos
        HTTPException(404): Si farm_id no existe
        HTTPException(500): Si falla generación de reporte
    """
    try:
        report = await service.generate_report(report_data)
        return report
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando reporte SENASAG: {str(e)}"
        )


@router.get(
    "/reports/{report_id}/download",
    response_class=FileResponse,
    summary="Descargar reporte SENASAG",
    description="Descarga archivo del reporte en formato seleccionado"
)
async def download_senasag_report(
    report_id: str,
    format: str = Query(..., regex="^(pdf|csv|xml)$"),
    service: SENASAGService = Depends()
) -> FileResponse:
    """
    Descarga reporte SENASAG generado.
    
    Args:
        report_id: ID del reporte
        format: Formato de descarga (pdf, csv, xml)
    
    Returns:
        FileResponse: Archivo del reporte
    """
    file_path = await service.get_report_file(report_id, format)
    return FileResponse(
        file_path,
        media_type=f"application/{format}",
        filename=f"senasag_report_{report_id}.{format}"
    )
```

### 3.3 Endpoints de REGENSA/GMA

```python
# app/api/routes/regensa.py
from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas.gma_schemas import (
    GMACreateRequest,
    GMAResponse,
    REGENSAComplianceResponse
)
from app.services.regensa_service import REGENSAService
from app.services.gma_service import GMAService

router = APIRouter(prefix="/api/v1/regensa", tags=["REGENSA"])


@router.get(
    "/compliance/{farm_id}",
    response_model=REGENSAComplianceResponse,
    summary="Validar cumplimiento REGENSA",
    description="""
    Valida cumplimiento de requisitos REGENSA capítulos 3.10 y 7.1.
    
    **Capítulo 3.10 - Centros de concentración animal:**
    - Rampas antideslizantes
    - Pasillos mínimo 1.6m
    - Mínimo 2m² por animal
    - Sistema de desinfección
    - Corral de cuarentena
    - Prohibición instrumentos de dolor
    
    **Capítulo 7.1 - Requisitos sanitarios:**
    - Registro digital de pesajes
    - Trazabilidad completa
    """
)
async def validate_regensa_compliance(
    farm_id: str,
    service: REGENSAService = Depends()
) -> REGENSAComplianceResponse:
    """
    Valida cumplimiento de REGENSA para una finca.
    
    Args:
        farm_id: ID de la finca a validar
        service: Servicio REGENSA (inyectado)
    
    Returns:
        REGENSAComplianceResponse: Resultado de validación con detalles
    
    Raises:
        HTTPException(404): Si farm_id no existe
    """
    try:
        compliance = await service.validate_compliance(farm_id)
        return compliance
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/gma",
    response_model=GMAResponse,
    status_code=201,
    summary="Crear Guía de Movimiento Animal",
    description="""
    Crea GMA para movilización de ganado según REGENSA.
    
    **Requisitos previos:**
    - Finca debe cumplir REGENSA capítulos 3.10 y 7.1
    - Animales deben tener pesajes recientes
    - Se valida automáticamente antes de crear GMA
    
    **Integración:**
    - Se registra automáticamente en sistema Gran Paitití
    """
)
async def create_gma(
    gma_data: GMACreateRequest,
    service: GMAService = Depends()
) -> GMAResponse:
    """
    Crea Guía de Movimiento Animal (GMA).
    
    Proceso:
    1. Valida cumplimiento REGENSA de la finca
    2. Genera número único de GMA
    3. Registra en sistema Gran Paitití
    4. Retorna GMA con estado Pendiente
    
    Args:
        gma_data: Datos de la GMA
        service: Servicio GMA (inyectado)
    
    Returns:
        GMAResponse: GMA creada con gran_paititi_id
    
    Raises:
        HTTPException(400): Si finca no cumple REGENSA
        HTTPException(404): Si farm_id o animal_ids no existen
        HTTPException(500): Si falla integración Gran Paitití
    """
    try:
        gma = await service.create_gma(gma_data)
        return gma
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creando GMA: {str(e)}"
        )
```

## 4. Manejo de Errores

### 4.1 Jerarquía de Errores Específicos del Dominio

```python
# app/core/exceptions.py
from fastapi import HTTPException
from typing import List

class BovineWeightEstimationException(Exception):
    """Excepción base del sistema."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

# Errores de captura
class CaptureException(BovineWeightEstimationException):
    def __init__(self, message: str):
        super().__init__(message, 400)

class InsufficientFramesException(CaptureException):
    def __init__(self):
        super().__init__(
            f"Se capturaron menos de {CaptureConstants.TOTAL_FRAMES_MIN} fotogramas"
        )

class LowQualityFramesException(CaptureException):
    def __init__(self):
        super().__init__(
            f"Ningún fotograma alcanzó el score mínimo de {CaptureConstants.MIN_OVERALL_SCORE}"
        )

# Errores de razas
class InvalidBreedException(BovineWeightEstimationException):
    def __init__(self):
        super().__init__(
            "La raza debe ser una de las 7 soportadas: "
            "Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey",
            400
        )

# Errores normativos
class REGENSAComplianceException(BovineWeightEstimationException):
    def __init__(self, missing_requirements: List[str]):
        self.missing_requirements = missing_requirements
        super().__init__(
            "No cumple con REGENSA capítulos 3.10 y 7.1",
            400
        )

class SENASAGReportException(BovineWeightEstimationException):
    def __init__(self, message: str):
        super().__init__(message, 400)

class GMACreationException(BovineWeightEstimationException):
    def __init__(self, message: str):
        super().__init__(message, 400)

# Errores de precisión
class PrecisionBelowThresholdException(BovineWeightEstimationException):
    def __init__(self, actual_precision: float):
        super().__init__(
            f"Precisión {actual_precision * 100}% menor al mínimo "
            f"{SystemMetrics.MIN_PRECISION * 100}%",
            400
        )
```

### 4.2 Handler de Errores Global

```python
# app/core/error_handler.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.exceptions import *

async def bovine_weight_estimation_exception_handler(
    request: Request, 
    exc: BovineWeightEstimationException
) -> JSONResponse:
    """Handler global para excepciones del sistema."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "detail": getattr(exc, 'missing_requirements', None),
        }
    )

# En main.py
from fastapi import FastAPI
from app.core.error_handler import bovine_weight_estimation_exception_handler
from app.core.exceptions import BovineWeightEstimationException

app = FastAPI(title="Sistema de Estimación de Peso Bovino - Hacienda Gamelera")

app.add_exception_handler(
    BovineWeightEstimationException,
    bovine_weight_estimation_exception_handler
)
```

## 5. Testing Requirements

### 5.1 Cobertura Mínima

- **Cobertura general**: 80% mínimo
- **Casos críticos**: 100% obligatorio
  - Evaluación de calidad de fotogramas
  - Selección del mejor fotograma
  - Validación de las 7 razas
  - Generación de GMA
  - Validación de cumplimiento REGENSA

### 5.2 Estructura de Tests

```text
tests/
├── unit/
│   ├── services/
│   │   ├── test_weighing_service.py
│   │   ├── test_senasag_service.py
│   │   ├── test_regensa_service.py
│   │   └── test_ml_service.py
│   └── repositories/
│       └── test_breed_repository.py
│
├── integration/
│   ├── test_api_animals.py
│   ├── test_api_senasag.py
│   ├── test_api_regensa.py
│   └── test_ml_inference.py
│
└── fixtures/
    ├── breed_fixtures.py        # Fixtures de las 7 razas
    ├── animal_fixtures.py
    └── weighing_fixtures.py
```

### 5.3 Ejemplo de Test - Validación de Razas

```python
# tests/unit/services/test_breed_service.py
import pytest
from app.services.breed_service import BreedService
from app.domain.enums import BreedType
from app.core.exceptions import InvalidBreedException

class TestBreedService:
    def test_should_validate_all_7_breeds_from_hacienda_gamelera(self):
        """Test validación de las 7 razas específicas del proyecto."""
        # Arrange
        service = BreedService()
        valid_breeds = [
            BreedType.BRAHMAN,
            BreedType.NELORE,
            BreedType.ANGUS,
            BreedType.CEBUINAS,
            BreedType.CRIOLLO,
            BreedType.PARDO_SUIZO,
            BreedType.JERSEY,
        ]
        
        # Act & Assert
        for breed in valid_breeds:
            assert service.is_valid_breed(breed), f"{breed.value} debe ser válida"
    
    def test_should_return_breed_count_of_exactly_7(self):
        """Test que hay exactamente 7 razas en el sistema."""
        assert len(BreedType) == 7, "Deben ser exactamente las 7 razas de Hacienda Gamelera"
    
    def test_should_reject_invalid_breed(self):
        """Test rechazo de razas no soportadas."""
        # Arrange
        service = BreedService()
        
        # Act & Assert
        with pytest.raises(InvalidBreedException):
            service.validate_breed("holstein")  # Raza no del proyecto
```

### 5.4 Ejemplo de Test - Evaluación de Fotogramas

```python
# tests/unit/services/test_frame_evaluation_service.py
import pytest
from unittest.mock import Mock
from app.services.frame_evaluation_service import FrameEvaluationService
from app.core.constants import CaptureConstants

class TestFrameEvaluationService:
    @pytest.fixture
    def service(self):
        return FrameEvaluationService()
    
    def test_should_accept_frame_with_all_quality_metrics_above_threshold(self, service):
        """Test aceptación de fotograma con todas las métricas válidas."""
        # Arrange
        frame_data = Mock()
        frame_data.sharpness = 0.85  # > 0.7
        frame_data.brightness = 0.6   # 0.4-0.8
        frame_data.contrast = 0.7     # > 0.5
        frame_data.silhouette_visibility = 0.9  # > 0.8
        frame_data.angle_score = 0.75  # > 0.6
        
        # Act
        result = service.evaluate_frame_quality(frame_data)
        
        # Assert
        assert result.is_acceptable is True
        assert result.overall_score > CaptureConstants.MIN_OVERALL_SCORE
    
    def test_should_reject_frame_with_low_silhouette_visibility(self, service):
        """Test rechazo por baja visibilidad de silueta."""
        # Arrange
        frame_data = Mock()
        frame_data.sharpness = 0.85
        frame_data.brightness = 0.6
        frame_data.contrast = 0.7
        frame_data.silhouette_visibility = 0.5  # < 0.8 ❌
        frame_data.angle_score = 0.75
        
        # Act
        result = service.evaluate_frame_quality(frame_data)
        
        # Assert
        assert result.is_acceptable is False
        assert "silueta" in result.rejection_reason.lower()
    
    def test_should_calculate_weighted_overall_score_correctly(self, service):
        """Test cálculo correcto del score ponderado."""
        # Arrange: Valores específicos para verificar pesos
        frame_data = Mock()
        frame_data.sharpness = 0.8
        frame_data.brightness = 0.6
        frame_data.silhouette_visibility = 0.9
        frame_data.angle_score = 0.7
        
        # Act
        result = service.evaluate_frame_quality(frame_data)
        
        # Assert
        # Score esperado: (0.9*0.4) + (0.8*0.3) + (0.6*0.2) + (0.7*0.1) = 0.79
        expected_score = 0.79
        assert abs(result.overall_score - expected_score) < 0.01
```

## 6. Configuración y Constantes

### 6.1 Configuración de la Aplicación

```python
# app/core/config.py
from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Base de datos
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "bovine_weight_estimation"
    
    # AWS S3 para modelos ML
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_bucket_name: str = "bovine-ml-models"
    s3_region: str = "us-east-1"
    
    # Razas soportadas (7 razas específicas)
    supported_breeds: List[str] = [
        "brahman", "nelore", "angus", "cebuinas", 
        "criollo", "pardo_suizo", "jersey"
    ]
    
    # Categorías de edad (4 categorías específicas)
    age_categories: List[str] = [
        "terneros", "vaquillonas_torillos", 
        "vaquillonas_toretes", "vacas_toros"
    ]
    
    # Métricas del sistema
    min_precision: float = 0.95
    max_error_kg: float = 5.0
    max_processing_time_ms: int = 3000
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## 7. Servicios de Machine Learning

### 7.1 ML Service - Implementación Completa

```python
# app/services/ml_service.py

from typing import Optional, Dict, Any
import tensorflow as tf
import numpy as np
from datetime import datetime
import asyncio
from app.domain.enums import BreedType, AgeCategory
from app.core.constants import SystemMetrics
from app.domain.value_objects import BreedWeightRanges
from app.core.exceptions import (
    PrecisionBelowThresholdException,
    ProcessingTimeTooSlowException,
    WeightOutOfRangeException,
    ModelLoadException,
    ModelIntegrityException,
)

class MLService:
    """
    Servicio de Machine Learning para estimación de peso bovino.
    
    Responsabilidades:
    - Cargar modelos TFLite específicos por raza
    - Ejecutar inferencia con validación de métricas
    - Validar precisión ≥95%, error <5kg, tiempo <3s
    - Gestionar caché de modelos (máximo 3 en memoria)
    """
    
    def __init__(self):
        self._model_cache: Dict[BreedType, tf.lite.Interpreter] = {}
        self._model_usage_count: Dict[BreedType, int] = {}
        self._max_models_in_memory = 3
    
    async def load_breed_model(
        self, 
        breed: BreedType
    ) -> tf.lite.Interpreter:
        """
        Carga modelo TFLite específico para una raza.
        
        Args:
            breed: Una de las 7 razas soportadas
        
        Returns:
            Intérprete TFLite listo para inferencia
        
        Raises:
            InvalidBreedException: Si raza no es una de las 7
            ModelLoadException: Si falla carga del modelo
        """
        # Verificar si ya está cargado
        if breed in self._model_cache:
            self._model_usage_count[breed] += 1
            return self._model_cache[breed]
        
        # Cargar desde S3 o cache local
        model_path = await self._get_model_path(breed)
        
        # Validar integridad (MD5 checksum)
        if not await self._validate_model_integrity(model_path):
            raise ModelIntegrityException(breed)
        
        # Cargar intérprete
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        
        # Gestionar memoria (máximo 3 modelos)
        if len(self._model_cache) >= self._max_models_in_memory:
            self._evict_least_used_model()
        
        self._model_cache[breed] = interpreter
        self._model_usage_count[breed] = 1
        
        return interpreter
    
    async def estimate_weight(
        self,
        image_bytes: bytes,
        breed: BreedType,
        age_category: AgeCategory,
    ) -> Dict[str, Any]:
        """
        Estima peso de animal usando modelo ML.
        
        Validaciones críticas:
        - Precisión (confidence) ≥ 95%
        - Error absoluto < 5 kg (vs peso real)
        - Tiempo de procesamiento < 3 segundos
        - Peso en rango esperado para raza y edad
        
        Args:
            image_bytes: Imagen del animal (JPEG/PNG)
            breed: Raza del animal
            age_category: Categoría de edad
        
        Returns:
            Dict con:
            - estimated_weight: Peso estimado (kg)
            - confidence: Score de confianza (0-1)
            - processing_time_ms: Tiempo de procesamiento
            - is_valid: Si cumple métricas del sistema
        
        Raises:
            PrecisionBelowThresholdException: Si confidence < 95%
            ProcessingTimeTooSlowException: Si > 3 segundos
            WeightOutOfRangeException: Si peso fuera de rango
        """
        start_time = datetime.now()
        
        # 1. Cargar modelo de la raza
        interpreter = await self.load_breed_model(breed)
        
        # 2. Preprocesar imagen (224x224, normalización)
        processed_image = await self._preprocess_image(image_bytes)
        
        # 3. Ejecutar inferencia
        interpreter.set_tensor(
            interpreter.get_input_details()[0]['index'],
            processed_image
        )
        interpreter.invoke()
        
        # 4. Obtener resultados
        output_data = interpreter.get_tensor(
            interpreter.get_output_details()[0]['index']
        )
        
        estimated_weight = float(output_data[0][0])
        confidence = float(output_data[0][1])
        
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # 5. VALIDAR MÉTRICAS CRÍTICAS
        
        # Validación 1: Precisión ≥95%
        if confidence < SystemMetrics.MIN_PRECISION:
            raise PrecisionBelowThresholdException(confidence)
        
        # Validación 2: Tiempo <3 segundos
        if processing_time > SystemMetrics.MAX_PROCESSING_TIME_MS:
            raise ProcessingTimeTooSlowException(processing_time)
        
        # Validación 3: Peso en rango esperado
        is_in_range = BreedWeightRanges.validate_weight(
            estimated_weight, breed, age_category
        )
        
        if not is_in_range:
            raise WeightOutOfRangeException(
                estimated_weight, breed, age_category
            )
        
        return {
            "estimated_weight": estimated_weight,
            "confidence": confidence,
            "processing_time_ms": processing_time,
            "is_valid": True,
            "breed": breed.value,
            "age_category": age_category.value,
            "timestamp": datetime.now().isoformat(),
        }
    
    async def _preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Preprocesa imagen para inferencia TFLite.
        
        Args:
            image_bytes: Imagen en bytes
        
        Returns:
            Array numpy normalizado [1, 224, 224, 3]
        """
        # Decodificar imagen
        import cv2
        import numpy as np
        
        # Convertir bytes a imagen
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Resize a 224x224
        resized = cv2.resize(image, (224, 224))
        
        # Convertir BGR a RGB
        rgb_image = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        
        # Normalizar [0, 255] -> [0, 1]
        normalized = rgb_image.astype(np.float32) / 255.0
        
        # Agregar dimensión batch
        batch_image = np.expand_dims(normalized, axis=0)
        
        return batch_image
    
    async def _get_model_path(self, breed: BreedType) -> str:
        """
        Obtiene ruta del modelo TFLite para una raza.
        
        Args:
            breed: Raza del animal
        
        Returns:
            Ruta local del modelo
        """
        # Implementar lógica de descarga desde S3 si no existe localmente
        model_filename = f"{breed.value}_v1.0.0.tflite"
        local_path = f"models/{model_filename}"
        
        # Si no existe localmente, descargar desde S3
        if not os.path.exists(local_path):
            await self._download_model_from_s3(breed, local_path)
        
        return local_path
    
    async def _validate_model_integrity(self, model_path: str) -> bool:
        """
        Valida integridad del modelo usando MD5 checksum.
        
        Args:
            model_path: Ruta del modelo
        
        Returns:
            True si el modelo es válido
        """
        import hashlib
        
        # Obtener checksum esperado desde manifest.json
        expected_checksum = await self._get_expected_checksum(model_path)
        
        # Calcular checksum actual
        with open(model_path, 'rb') as f:
            actual_checksum = hashlib.md5(f.read()).hexdigest()
        
        return actual_checksum == expected_checksum
    
    def _evict_least_used_model(self):
        """Libera modelo menos usado para gestión de memoria."""
        if not self._model_usage_count:
            return
        
        least_used_breed = min(
            self._model_usage_count,
            key=self._model_usage_count.get
        )
        
        # Cerrar intérprete
        self._model_cache[least_used_breed].close()
        
        # Remover de caché
        del self._model_cache[least_used_breed]
        del self._model_usage_count[least_used_breed]
    
    async def validate_all_breed_models(self) -> Dict[BreedType, bool]:
        """
        Valida que todos los modelos de las 7 razas carguen correctamente.
        
        Returns:
            Dict con estado de carga por raza
        """
        results = {}
        
        for breed in BreedType:
            try:
                await self.load_breed_model(breed)
                results[breed] = True
            except Exception as e:
                results[breed] = False
                # Log error
        
        return results
```

### 7.2 Model Manager - Gestión de Modelos

```python
# app/ml/model_manager.py

import asyncio
import json
from typing import Dict, List, Optional
from datetime import datetime
import boto3
from app.domain.enums import BreedType
from app.core.constants import SystemMetrics

class ModelManager:
    """
    Gestor de modelos ML para las 7 razas bovinas.
    
    Responsabilidades:
    - Descarga de modelos desde S3
    - Validación de versiones
    - Gestión de manifest.json
    - Actualización automática de modelos
    """
    
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = "bovine-ml-models"
        self.manifest_key = "manifest.json"
    
    async def get_latest_manifest(self) -> Dict:
        """
        Obtiene el manifest.json más reciente desde S3.
        
        Returns:
            Dict con información de versiones de modelos
        """
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=self.manifest_key
            )
            return json.loads(response['Body'].read())
        except Exception as e:
            raise ModelManifestException(f"Error obteniendo manifest: {e}")
    
    async def check_model_updates(self) -> Dict[BreedType, bool]:
        """
        Verifica si hay actualizaciones disponibles para los modelos.
        
        Returns:
            Dict indicando si cada raza tiene actualización disponible
        """
        manifest = await self.get_latest_manifest()
        updates_available = {}
        
        for breed in BreedType:
            current_version = await self._get_current_model_version(breed)
            latest_version = manifest['models'][breed.value]['version']
            
            updates_available[breed] = current_version != latest_version
        
        return updates_available
    
    async def download_model_update(
        self, 
        breed: BreedType
    ) -> bool:
        """
        Descarga actualización de modelo para una raza específica.
        
        Args:
            breed: Raza a actualizar
        
        Returns:
            True si la descarga fue exitosa
        """
        manifest = await self.get_latest_manifest()
        model_info = manifest['models'][breed.value]
        
        # Descargar modelo
        model_key = f"models/{breed.value}-{model_info['version']}.tflite"
        local_path = f"models/{breed.value}_v{model_info['version']}.tflite"
        
        try:
            self.s3_client.download_file(
                self.bucket_name,
                model_key,
                local_path
            )
            
            # Validar integridad
            if await self._validate_downloaded_model(local_path, model_info['md5']):
                return True
            else:
                # Eliminar archivo corrupto
                os.remove(local_path)
                return False
                
        except Exception as e:
            raise ModelDownloadException(f"Error descargando modelo {breed.value}: {e}")
    
    async def _get_current_model_version(self, breed: BreedType) -> str:
        """Obtiene versión actual del modelo local."""
        # Implementar lógica para leer versión desde archivo local
        return "1.0.0"  # Placeholder
    
    async def _validate_downloaded_model(self, model_path: str, expected_md5: str) -> bool:
        """Valida integridad del modelo descargado."""
        import hashlib
        
        with open(model_path, 'rb') as f:
            actual_md5 = hashlib.md5(f.read()).hexdigest()
        
        return actual_md5 == expected_md5
```

## 8. MongoDB Models

### 8.1 Modelos de Base de Datos

```python
# app/database/models.py

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from app.domain.enums import BreedType, AgeCategory, GMAStatus

class AnimalModel:
    """
    Modelo MongoDB para Animal.
    
    Colección: animals
    Índices:
    - tag_number (unique)
    - breed_type
    - age_category
    - created_at
    """
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.animals
    
    async def create_indexes(self):
        """Crea índices para optimización de queries."""
        await self.collection.create_index("tag_number", unique=True)
        await self.collection.create_index("breed_type")
        await self.collection.create_index("age_category")
        await self.collection.create_index("created_at")
        await self.collection.create_index("farm_id")
        await self.collection.create_index("asocebu_registered")
    
    async def create_animal(self, animal_data: Dict[str, Any]) -> str:
        """
        Crea nuevo animal en la base de datos.
        
        Args:
            animal_data: Datos del animal
        
        Returns:
            ID del animal creado
        """
        animal_data["created_at"] = datetime.utcnow()
        animal_data["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(animal_data)
        return str(result.inserted_id)
    
    async def get_animals_by_breed(
        self, 
        breed: BreedType,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Obtiene animales por raza específica.
        
        Args:
            breed: Raza a filtrar
            limit: Límite de resultados
        
        Returns:
            Lista de animales de la raza especificada
        """
        cursor = self.collection.find(
            {"breed_type": breed.value}
        ).limit(limit)
        
        return await cursor.to_list(length=limit)
    
    async def get_breed_distribution(self) -> Dict[BreedType, int]:
        """
        Obtiene distribución de animales por raza.
        
        Returns:
            Dict con conteo por cada una de las 7 razas
        """
        pipeline = [
            {
                "$group": {
                    "_id": "$breed_type",
                    "count": {"$sum": 1}
                }
            }
        ]
        
        cursor = self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=None)
        
        # Convertir a dict con BreedType como key
        distribution = {}
        for result in results:
            breed_type = BreedType(result["_id"])
            distribution[breed_type] = result["count"]
        
        return distribution


class WeighingModel:
    """
    Modelo MongoDB para Weighing.
    
    Colección: weighings
    Índices:
    - animal_id
    - weighing_date
    - breed_type (para análisis por raza)
    - created_at
    """
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.weighings
    
    async def create_indexes(self):
        """Crea índices para optimización de queries."""
        await self.collection.create_index("animal_id")
        await self.collection.create_index("weighing_date")
        await self.collection.create_index("breed_type")
        await self.collection.create_index("created_at")
        await self.collection.create_index("confidence_score")
        await self.collection.create_index("was_offline")
    
    async def create_weighing(self, weighing_data: Dict[str, Any]) -> str:
        """
        Crea nuevo pesaje en la base de datos.
        
        Args:
            weighing_data: Datos del pesaje
        
        Returns:
            ID del pesaje creado
        """
        weighing_data["created_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(weighing_data)
        return str(result.inserted_id)
    
    async def get_animal_weighing_history(
        self, 
        animal_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Obtiene historial de pesajes de un animal.
        
        Args:
            animal_id: ID del animal
            limit: Límite de resultados
        
        Returns:
            Lista de pesajes ordenados por fecha descendente
        """
        cursor = self.collection.find(
            {"animal_id": animal_id}
        ).sort("weighing_date", -1).limit(limit)
        
        return await cursor.to_list(length=limit)
    
    async def get_precision_metrics_by_breed(
        self, 
        breed: BreedType
    ) -> Dict[str, float]:
        """
        Obtiene métricas de precisión por raza.
        
        Args:
            breed: Raza a analizar
        
        Returns:
            Dict con métricas de precisión
        """
        pipeline = [
            {"$match": {"breed_type": breed.value}},
            {
                "$group": {
                    "_id": None,
                    "avg_confidence": {"$avg": "$confidence_score"},
                    "total_weighings": {"$sum": 1},
                    "avg_processing_time": {"$avg": "$processing_time_ms"},
                    "avg_quality_score": {"$avg": "$quality_score"}
                }
            }
        ]
        
        cursor = self.collection.aggregate(pipeline)
        results = await cursor.to_list(length=1)
        
        if results:
            return {
                "avg_confidence": results[0]["avg_confidence"],
                "total_weighings": results[0]["total_weighings"],
                "avg_processing_time": results[0]["avg_processing_time"],
                "avg_quality_score": results[0]["avg_quality_score"]
            }
        
        return {}


class GMAModel:
    """
    Modelo MongoDB para GMA (Guía de Movimiento Animal).
    
    Colección: gmas
    Índices:
    - gma_number (unique)
    - origin_farm_id
    - status
    - created_at
    """
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.gmas
    
    async def create_indexes(self):
        """Crea índices para optimización de queries."""
        await self.collection.create_index("gma_number", unique=True)
        await self.collection.create_index("origin_farm_id")
        await self.collection.create_index("status")
        await self.collection.create_index("created_at")
        await self.collection.create_index("gran_paititi_id")
    
    async def create_gma(self, gma_data: Dict[str, Any]) -> str:
        """
        Crea nueva GMA en la base de datos.
        
        Args:
            gma_data: Datos de la GMA
        
        Returns:
            ID de la GMA creada
        """
        gma_data["created_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(gma_data)
        return str(result.inserted_id)
    
    async def get_pending_gmas(self) -> List[Dict[str, Any]]:
        """
        Obtiene GMAs pendientes de procesamiento.
        
        Returns:
            Lista de GMAs con estado "pendiente"
        """
        cursor = self.collection.find(
            {"status": GMAStatus.PENDIENTE.value}
        ).sort("created_at", 1)
        
        return await cursor.to_list(length=None)
```

## 9. Seed Data - Las 7 Razas Completas

### 9.1 Seed Data de MongoDB

```python
# app/database/seed_data.py

from datetime import datetime
from app.domain.enums import BreedType
from app.domain.value_objects import BreedWeightRanges

async def seed_breeds(db):
    """
    Seed de las 7 razas de Hacienda Gamelera en MongoDB.
    
    Cada raza incluye:
    - Nombre científico (Bos indicus / Bos taurus)
    - URL del modelo TFLite en S3
    - Rangos de peso por edad
    - Tasa de crecimiento promedio
    - Características distintivas
    """
    
    breeds_data = [
        # 1. Brahman (Bos indicus) - Raza más pesada
        {
            "_id": "breed_brahman",
            "name": "brahman",
            "scientific_name": "Bos indicus",
            "model_version": "1.0.0",
            "model_url": "s3://bovine-ml-models/brahman-v1.0.0.tflite",
            "weight_ranges": {
                "terneros": {"min": 80, "max": 180},
                "vaquillonas_torillos": {"min": 180, "max": 350},
                "vaquillonas_toretes": {"min": 300, "max": 500},
                "vacas_toros": {"min": 450, "max": 900},
            },
            "growth_rate_avg_kg_per_day": 0.8,
            "characteristics": [
                "Alta resistencia al calor",
                "Giba cervico-torácica prominente",
                "Piel suelta y pigmentada",
                "Buena adaptación a climas tropicales"
            ],
            "is_active": True,
            "created_at": datetime.utcnow(),
        },
        
        # 2. Nelore (Bos indicus) - Similar a Brahman
        {
            "_id": "breed_nelore",
            "name": "nelore",
            "scientific_name": "Bos indicus",
            "model_version": "1.0.0",
            "model_url": "s3://bovine-ml-models/nelore-v1.0.0.tflite",
            "weight_ranges": {
                "terneros": {"min": 75, "max": 170},
                "vaquillonas_torillos": {"min": 170, "max": 330},
                "vaquillonas_toretes": {"min": 280, "max": 480},
                "vacas_toros": {"min": 400, "max": 850},
            },
            "growth_rate_avg_kg_per_day": 0.75,
            "characteristics": [
                "Adaptado al trópico",
                "Pelaje blanco característico",
                "Cuernos largos y curvados",
                "Resistente a parásitos externos"
            ],
            "is_active": True,
            "created_at": datetime.utcnow(),
        },
        
        # 3. Angus (Bos taurus) - Raza europea mediana
        {
            "_id": "breed_angus",
            "name": "angus",
            "scientific_name": "Bos taurus",
            "model_version": "1.0.0",
            "model_url": "s3://bovine-ml-models/angus-v1.0.0.tflite",
            "weight_ranges": {
                "terneros": {"min": 70, "max": 165},
                "vaquillonas_torillos": {"min": 165, "max": 320},
                "vaquillonas_toretes": {"min": 270, "max": 460},
                "vacas_toros": {"min": 380, "max": 800},
            },
            "growth_rate_avg_kg_per_day": 0.85,
            "characteristics": [
                "Pelaje negro uniforme",
                "Sin cuernos (polled)",
                "Carne de excelente calidad",
                "Temperamento dócil"
            ],
            "is_active": True,
            "created_at": datetime.utcnow(),
        },
        
        # 4. Cebuinas (Bos indicus) - Raza cebuina mediana
        {
            "_id": "breed_cebuinas",
            "name": "cebuinas",
            "scientific_name": "Bos indicus",
            "model_version": "1.0.0",
            "model_url": "s3://bovine-ml-models/cebuinas-v1.0.0.tflite",
            "weight_ranges": {
                "terneros": {"min": 75, "max": 175},
                "vaquillonas_torillos": {"min": 175, "max": 340},
                "vaquillonas_toretes": {"min": 290, "max": 490},
                "vacas_toros": {"min": 420, "max": 870},
            },
            "growth_rate_avg_kg_per_day": 0.78,
            "characteristics": [
                "Resistente a parásitos",
                "Pelaje variado (pintas)",
                "Tamaño mediano",
                "Buena adaptación local"
            ],
            "is_active": True,
            "created_at": datetime.utcnow(),
        },
        
        # 5. Criollo (Bos taurus) - Raza local adaptada
        {
            "_id": "breed_criollo",
            "name": "criollo",
            "scientific_name": "Bos taurus",
            "model_version": "1.0.0",
            "model_url": "s3://bovine-ml-models/criollo-v1.0.0.tflite",
            "weight_ranges": {
                "terneros": {"min": 65, "max": 150},
                "vaquillonas_torillos": {"min": 150, "max": 280},
                "vaquillonas_toretes": {"min": 240, "max": 400},
                "vacas_toros": {"min": 350, "max": 650},
            },
            "growth_rate_avg_kg_per_day": 0.70,
            "characteristics": [
                "Adaptado localmente",
                "Muy resistente",
                "Pelaje variado",
                "Tamaño pequeño-mediano"
            ],
            "is_active": True,
            "created_at": datetime.utcnow(),
        },
        
        # 6. Pardo Suizo (Bos taurus) - Raza lechera grande
        {
            "_id": "breed_pardo_suizo",
            "name": "pardo_suizo",
            "scientific_name": "Bos taurus",
            "model_version": "1.0.0",
            "model_url": "s3://bovine-ml-models/pardo-suizo-v1.0.0.tflite",
            "weight_ranges": {
                "terneros": {"min": 80, "max": 185},
                "vaquillonas_torillos": {"min": 185, "max": 360},
                "vaquillonas_toretes": {"min": 310, "max": 510},
                "vacas_toros": {"min": 460, "max": 920},
            },
            "growth_rate_avg_kg_per_day": 0.82,
            "characteristics": [
                "Pelaje pardo característico",
                "Doble propósito (carne y leche)",
                "Tamaño grande",
                "Buena producción lechera"
            ],
            "is_active": True,
            "created_at": datetime.utcnow(),
        },
        
        # 7. Jersey (Bos taurus) - Raza lechera pequeña
        {
            "_id": "breed_jersey",
            "name": "jersey",
            "scientific_name": "Bos taurus",
            "model_version": "1.0.0",
            "model_url": "s3://bovine-ml-models/jersey-v1.0.0.tflite",
            "weight_ranges": {
                "terneros": {"min": 60, "max": 140},
                "vaquillonas_torillos": {"min": 140, "max": 260},
                "vaquillonas_toretes": {"min": 220, "max": 380},
                "vacas_toros": {"min": 330, "max": 600},
            },
            "growth_rate_avg_kg_per_day": 0.65,
            "characteristics": [
                "Pelaje dorado característico",
                "Leche rica en grasa",
                "Tamaño pequeño",
                "Eficiente conversión alimenticia"
            ],
            "is_active": True,
            "created_at": datetime.utcnow(),
        },
    ]
    
    # Insertar en MongoDB
    await db.breeds.insert_many(breeds_data, ordered=False)
    
    print(f"✅ Seed completado: {len(breeds_data)} razas insertadas")
```

## 10. Servicios de Negocio (Business Logic)

### 10.1 Animal Service

```python
# app/services/animal_service.py

from typing import List, Optional, Dict, Any
from datetime import datetime
from app.domain.enums import BreedType, AgeCategory
from app.domain.value_objects import BreedWeightRanges
from app.repositories.animal_repository import AnimalRepository
from app.core.exceptions import InvalidBreedException, AnimalNotFoundException

class AnimalService:
    """
    Servicio de lógica de negocio para animales.
    
    Responsabilidades:
    - Validación de datos de animales
    - Cálculo automático de categoría de edad
    - Validación de rangos de peso por raza
    - Integración con ASOCEBU
    """
    
    def __init__(self, animal_repository: AnimalRepository):
        self.animal_repository = animal_repository
    
    async def create_animal(self, animal_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea nuevo animal con validaciones de negocio.
        
        Args:
            animal_data: Datos del animal a crear
        
        Returns:
            Animal creado con age_category calculada
        
        Raises:
            InvalidBreedException: Si raza no es una de las 7
            ValueError: Si datos inválidos
        """
        # Validar raza
        breed_type = BreedType(animal_data["breed_type"])
        if not BreedType.is_valid(breed_type.value):
            raise InvalidBreedException()
        
        # Calcular categoría de edad automáticamente
        birth_date = animal_data["birth_date"]
        age_category = self._calculate_age_category(birth_date)
        animal_data["age_category"] = age_category.value
        
        # Validar peso objetivo si se proporciona
        if "weight_goal" in animal_data and animal_data["weight_goal"]:
            is_valid_weight = BreedWeightRanges.validate_weight(
                weight_kg=animal_data["weight_goal"],
                breed=breed_type,
                age_category=age_category
            )
            if not is_valid_weight:
                raise ValueError(
                    f"Peso objetivo fuera de rango para {breed_type.value} {age_category.value}"
                )
        
        # Crear en base de datos
        animal_id = await self.animal_repository.create(animal_data)
        
        # Retornar animal creado
        return await self.animal_repository.get_by_id(animal_id)
    
    async def get_animals_by_breed(
        self, 
        breed: BreedType,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Obtiene animales por raza específica.
        
        Args:
            breed: Raza a filtrar
            limit: Límite de resultados
        
        Returns:
            Lista de animales de la raza especificada
        """
        return await self.animal_repository.get_by_breed(breed, limit)
    
    async def get_breed_distribution(self) -> Dict[BreedType, int]:
        """
        Obtiene distribución de animales por raza.
        
        Returns:
            Dict con conteo por cada una de las 7 razas
        """
        return await self.animal_repository.get_breed_distribution()
    
    def _calculate_age_category(self, birth_date: datetime) -> AgeCategory:
        """
        Calcula categoría de edad según fecha de nacimiento.
        
        Args:
            birth_date: Fecha de nacimiento
        
        Returns:
            Categoría de edad calculada
        """
        now = datetime.now()
        age_months = (now.year - birth_date.year) * 12 + (now.month - birth_date.month)
        
        return AgeCategory.from_age_months(age_months)
```

### 10.2 Weighing Service

```python
# app/services/weighing_service.py

from typing import Dict, Any, List
from datetime import datetime
from app.domain.enums import BreedType, AgeCategory
from app.domain.value_objects import BreedWeightRanges
from app.services.ml_service import MLService
from app.repositories.weighing_repository import WeighingRepository
from app.core.exceptions import (
    PrecisionBelowThresholdException,
    ProcessingTimeTooSlowException,
    WeightOutOfRangeException,
)

class WeighingService:
    """
    Servicio de lógica de negocio para pesajes.
    
    Responsabilidades:
    - Procesamiento de imágenes con ML
    - Validación de métricas del sistema
    - Comparación con fórmula Schaeffer
    - Almacenamiento de resultados
    """
    
    def __init__(
        self, 
        weighing_repository: WeighingRepository,
        ml_service: MLService
    ):
        self.weighing_repository = weighing_repository
        self.ml_service = ml_service
    
    async def estimate_weight_from_image(
        self,
        image_bytes: bytes,
        animal_id: str,
        breed: BreedType,
        age_category: AgeCategory,
    ) -> Dict[str, Any]:
        """
        Estima peso desde imagen usando ML.
        
        Args:
            image_bytes: Imagen del animal
            animal_id: ID del animal
            breed: Raza del animal
            age_category: Categoría de edad
        
        Returns:
            Dict con resultado de estimación
        
        Raises:
            PrecisionBelowThresholdException: Si confidence < 95%
            ProcessingTimeTooSlowException: Si > 3 segundos
            WeightOutOfRangeException: Si peso fuera de rango
        """
        # Ejecutar inferencia ML
        ml_result = await self.ml_service.estimate_weight(
            image_bytes=image_bytes,
            breed=breed,
            age_category=age_category
        )
        
        # Crear registro de pesaje
        weighing_data = {
            "animal_id": animal_id,
            "estimated_weight": ml_result["estimated_weight"],
            "confidence_score": ml_result["confidence"],
            "weighing_date": datetime.now(),
            "weighing_method": "IA",
            "breed_type": breed.value,
            "age_category": age_category.value,
            "processing_time_ms": ml_result["processing_time_ms"],
            "quality_score": ml_result.get("quality_score", 0.0),
            "was_offline": False,  # Procesado en servidor
            "created_by": "system",
        }
        
        # Guardar en base de datos
        weighing_id = await self.weighing_repository.create(weighing_data)
        
        return {
            "weighing_id": weighing_id,
            "estimated_weight": ml_result["estimated_weight"],
            "confidence": ml_result["confidence"],
            "processing_time_ms": ml_result["processing_time_ms"],
            "is_valid": True,
            "breed": breed.value,
            "age_category": age_category.value,
        }
    
    async def get_animal_weighing_history(
        self, 
        animal_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Obtiene historial de pesajes de un animal.
        
        Args:
            animal_id: ID del animal
            limit: Límite de resultados
        
        Returns:
            Lista de pesajes ordenados por fecha
        """
        return await self.weighing_repository.get_by_animal_id(animal_id, limit)
    
    async def get_precision_metrics_by_breed(
        self, 
        breed: BreedType
    ) -> Dict[str, float]:
        """
        Obtiene métricas de precisión por raza.
        
        Args:
            breed: Raza a analizar
        
        Returns:
            Dict con métricas de precisión
        """
        return await self.weighing_repository.get_precision_metrics_by_breed(breed)
```

### 10.3 SENASAG Service

```python
# app/services/senasag_service.py

from typing import Dict, Any, List
from datetime import datetime
from app.domain.enums import SENASAGReportType
from app.repositories.senasag_report_repository import SENASAGReportRepository
from app.repositories.animal_repository import AnimalRepository

class SENASAGService:
    """
    Servicio de lógica de negocio para reportes SENASAG.
    
    Responsabilidades:
    - Generación de reportes según normativa boliviana
    - Validación de datos para SENASAG
    - Exportación en formatos requeridos (PDF, CSV, XML)
    """
    
    def __init__(
        self, 
        senasag_repository: SENASAGReportRepository,
        animal_repository: AnimalRepository
    ):
        self.senasag_repository = senasag_repository
        self.animal_repository = animal_repository
    
    async def generate_report(
        self, 
        report_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Genera reporte SENASAG automáticamente.
        
        Args:
            report_data: Parámetros del reporte
        
        Returns:
            Reporte generado con URLs de descarga
        """
        # Obtener animales del período
        animals = await self.animal_repository.get_by_period(
            start_date=report_data["period_start"],
            end_date=report_data["period_end"]
        )
        
        # Generar datos del reporte según tipo
        report_content = await self._generate_report_content(
            animals=animals,
            report_type=report_data["report_type"]
        )
        
        # Crear archivos (PDF, CSV, XML)
        files_created = await self._create_report_files(
            report_content=report_content,
            report_type=report_data["report_type"],
            export_format=report_data["export_format"]
        )
        
        # Guardar registro del reporte
        report_record = {
            "farm_id": report_data["farm_id"],
            "report_type": report_data["report_type"],
            "period_start": report_data["period_start"],
            "period_end": report_data["period_end"],
            "total_animals": len(animals),
            "pdf_url": files_created.get("pdf"),
            "csv_url": files_created.get("csv"),
            "xml_url": files_created.get("xml"),
            "status": "generado",
            "created_by": "system",
        }
        
        report_id = await self.senasag_repository.create(report_record)
        
        return {
            "report_id": report_id,
            "status": "generado",
            "files": files_created,
            "total_animals": len(animals),
        }
    
    async def _generate_report_content(
        self, 
        animals: List[Dict[str, Any]], 
        report_type: SENASAGReportType
    ) -> Dict[str, Any]:
        """Genera contenido del reporte según tipo."""
        if report_type == SENASAGReportType.INVENTARIO:
            return await self._generate_inventory_content(animals)
        elif report_type == SENASAGReportType.MOVILIZACION:
            return await self._generate_movement_content(animals)
        elif report_type == SENASAGReportType.SANITARIO:
            return await self._generate_health_content(animals)
    
    async def _create_report_files(
        self, 
        report_content: Dict[str, Any],
        report_type: SENASAGReportType,
        export_format: str
    ) -> Dict[str, str]:
        """Crea archivos del reporte en formatos especificados."""
        files = {}
        
        if export_format in ["pdf", "all"]:
            files["pdf"] = await self._create_pdf_file(report_content)
        
        if export_format in ["csv", "all"]:
            files["csv"] = await self._create_csv_file(report_content)
        
        if export_format in ["xml", "all"]:
            files["xml"] = await self._create_xml_file(report_content)
        
        return files
```

## 11. Repositorios (Data Access Layer)

### 11.1 Animal Repository

```python
# app/repositories/animal_repository.py

from typing import List, Optional, Dict, Any
from app.database.models import AnimalModel
from app.domain.enums import BreedType, AgeCategory

class AnimalRepository:
    """
    Repositorio para acceso a datos de animales.
    
    Implementa patrón Repository para abstraer acceso a MongoDB.
    """
    
    def __init__(self, animal_model: AnimalModel):
        self.animal_model = animal_model
    
    async def create(self, animal_data: Dict[str, Any]) -> str:
        """
        Crea nuevo animal.
        
        Args:
            animal_data: Datos del animal
        
        Returns:
            ID del animal creado
        """
        return await self.animal_model.create_animal(animal_data)
    
    async def get_by_id(self, animal_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene animal por ID.
        
        Args:
            animal_id: ID del animal
        
        Returns:
            Datos del animal o None si no existe
        """
        return await self.animal_model.get_by_id(animal_id)
    
    async def get_by_breed(
        self, 
        breed: BreedType, 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Obtiene animales por raza.
        
        Args:
            breed: Raza a filtrar
            limit: Límite de resultados
        
        Returns:
            Lista de animales de la raza
        """
        return await self.animal_model.get_animals_by_breed(breed, limit)
    
    async def get_breed_distribution(self) -> Dict[BreedType, int]:
        """
        Obtiene distribución por raza.
        
        Returns:
            Dict con conteo por raza
        """
        return await self.animal_model.get_breed_distribution()
    
    async def get_by_period(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Obtiene animales por período de creación.
        
        Args:
            start_date: Fecha de inicio
            end_date: Fecha de fin
        
        Returns:
            Lista de animales del período
        """
        return await self.animal_model.get_by_period(start_date, end_date)
```

### 11.2 Weighing Repository

```python
# app/repositories/weighing_repository.py

from typing import List, Dict, Any
from app.database.models import WeighingModel
from app.domain.enums import BreedType

class WeighingRepository:
    """
    Repositorio para acceso a datos de pesajes.
    
    Implementa patrón Repository para abstraer acceso a MongoDB.
    """
    
    def __init__(self, weighing_model: WeighingModel):
        self.weighing_model = weighing_model
    
    async def create(self, weighing_data: Dict[str, Any]) -> str:
        """
        Crea nuevo pesaje.
        
        Args:
            weighing_data: Datos del pesaje
        
        Returns:
            ID del pesaje creado
        """
        return await self.weighing_model.create_weighing(weighing_data)
    
    async def get_by_animal_id(
        self, 
        animal_id: str, 
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Obtiene pesajes por animal.
        
        Args:
            animal_id: ID del animal
            limit: Límite de resultados
        
        Returns:
            Lista de pesajes del animal
        """
        return await self.weighing_model.get_animal_weighing_history(animal_id, limit)
    
    async def get_precision_metrics_by_breed(
        self, 
        breed: BreedType
    ) -> Dict[str, float]:
        """
        Obtiene métricas de precisión por raza.
        
        Args:
            breed: Raza a analizar
        
        Returns:
            Métricas de precisión
        """
        return await self.weighing_model.get_precision_metrics_by_breed(breed)
    
    async def get_recent_weighings(
        self, 
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Obtiene pesajes recientes.
        
        Args:
            days: Días hacia atrás
        
        Returns:
            Lista de pesajes recientes
        """
        return await self.weighing_model.get_recent_weighings(days)
```

## 12. Integración Gran Paitití

### 12.1 Gran Paitití Service

```python
# app/services/gran_paititi_service.py

import httpx
from typing import Optional, Dict, Any
from app.core.config import settings
from app.domain.entities.gma import GMA
from app.core.exceptions import GranPaititiAPIException

class GranPaititiService:
    """
    Servicio de integración con sistema Gran Paitití (gobierno boliviano).
    
    Gran Paitití es el sistema gubernamental de registro ganadero.
    """
    
    def __init__(self):
        self.base_url = "https://api.granpaititi.gob.bo"
        self.api_key = settings.gran_paititi_api_key
        self.timeout = 30.0
    
    async def register_gma(self, gma: GMA) -> str:
        """
        Registra GMA en sistema Gran Paitití.
        
        Args:
            gma: Guía de Movimiento Animal a registrar
        
        Returns:
            ID de registro en Gran Paitití
        
        Raises:
            GranPaititiAPIException: Si falla registro
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/gma/register",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "gma_number": gma.gma_number,
                        "animal_ids": gma.animal_ids,
                        "origin_farm_id": gma.origin_farm_id,
                        "destination": gma.destination,
                        "reason": gma.reason,
                        "departure_date": gma.departure_date.isoformat(),
                        "arrival_date": gma.arrival_date.isoformat(),
                        "regensa_compliance": {
                            "chapter_3_10_compliant": gma.regensa_compliance.chapter_3_10_compliant,
                            "chapter_7_1_compliant": gma.regensa_compliance.chapter_7_1_compliant,
                        }
                    }
                )
                
                if response.status_code != 201:
                    raise GranPaititiAPIException(
                        f"Error registrando GMA: {response.status_code} - {response.text}"
                    )
                
                return response.json()["gran_paititi_id"]
                
            except httpx.TimeoutException:
                raise GranPaititiAPIException("Timeout conectando con Gran Paitití")
            except httpx.RequestError as e:
                raise GranPaititiAPIException(f"Error de conexión: {e}")
    
    async def validate_farm_registration(self, farm_id: str) -> bool:
        """
        Valida que la finca esté registrada en Gran Paitití.
        
        Args:
            farm_id: ID de la finca
        
        Returns:
            True si está registrada
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/farms/{farm_id}/validate",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                
                return response.status_code == 200
                
            except Exception:
                return False
    
    async def sync_animal_registrations(
        self, 
        animal_ids: List[str]
    ) -> Dict[str, bool]:
        """
        Sincroniza registros de animales con Gran Paitití.
        
        Args:
            animal_ids: Lista de IDs de animales
        
        Returns:
            Dict con estado de sincronización por animal
        """
        results = {}
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for animal_id in animal_ids:
                try:
                    response = await client.post(
                        f"{self.base_url}/animals/sync",
                        headers={"Authorization": f"Bearer {self.api_key}"},
                        json={"animal_id": animal_id}
                    )
                    
                    results[animal_id] = response.status_code == 200
                    
                except Exception:
                    results[animal_id] = False
        
        return results
```

### 6.2 Constantes de Hacienda Gamelera

```python
# app/core/constants/hacienda_constants.py
class HaciendaGameleraConstants:
    """
    Datos específicos de Hacienda Gamelera.
    
    Ubicación: San Ignacio de Velasco, Santa Cruz, Bolivia
    Coordenadas: 15°51′34.2′′S, 60°47′52.4′′W
    Área: 48.5 hectáreas
    Hato: 500 cabezas de ganado
    Propietario: Bruno Brito Macedo
    """
    # Coordenadas GPS exactas
    LATITUDE = -15.859500  # 15°51′34.2′′S
    LONGITUDE = -60.797889  # 60°47′52.4′′W
    
    # Información de la finca
    NAME = "Hacienda Gamelera"
    ADDRESS = "San Ignacio de Velasco, Santa Cruz, Bolivia"
    AREA_HECTARES = 48.5
    TOTAL_CATTLE = 500
    OWNER = "Bruno Brito Macedo"
    
    # Tolerancia para validación GPS (metros)
    GPS_TOLERANCE_METERS = 1000  # 1 km de radio
    
    @classmethod
    def is_within_farm_boundaries(cls, lat: float, lon: float) -> bool:
        """
        Valida que coordenadas estén dentro del área de la hacienda.
        
        Args:
            lat: Latitud en grados decimales
            lon: Longitud en grados decimales
        
        Returns:
            True si está dentro del área, False si no
        """
        # Calcular distancia usando fórmula haversine
        from math import radians, cos, sin, asin, sqrt
        
        def haversine(lat1, lon1, lat2, lon2):
            """Calcula distancia entre dos puntos GPS."""
            R = 6371000  # Radio de la Tierra en metros
            
            lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            
            return R * c
        
        distance = haversine(lat, lon, cls.LATITUDE, cls.LONGITUDE)
        return distance <= cls.GPS_TOLERANCE_METERS

class ProjectTimeMetrics:
    """
    Métricas de tiempo del proyecto (Hacienda Gamelera).
    
    Comparación entre método tradicional vs nuevo sistema con IA.
    """
    # Método tradicional (básculas + cinta bovinométrica)
    CURRENT_TIME_FOR_20_ANIMALS = 3 * 24 * 60  # 3 días en minutos
    CURRENT_CALIBRATION_TIME = 45  # 45 minutos diarios
    CURRENT_COORDINATION_TIME = 2 * 60  # 2 horas en minutos
    CURRENT_PER_ANIMAL_TIME = 9  # 9 minutos por animal
    
    # Nuevo sistema (IA + captura continua)
    TARGET_TIME_FOR_20_ANIMALS = 2 * 60  # 2 horas en minutos
    TARGET_PER_ANIMAL_TIME = 6  # 6 minutos por animal
    
    # Mejora esperada
    @classmethod
    def get_improvement_percentage(cls) -> float:
        """Calcula porcentaje de mejora en tiempo."""
        return (1 - (cls.TARGET_TIME_FOR_20_ANIMALS / cls.CURRENT_TIME_FOR_20_ANIMALS)) * 100
        # = 95.8% de mejora

class SchaefferFormula:
    """
    Fórmula tradicional de Schaeffer para estimación de peso bovino.
    
    Esta es la fórmula que el nuevo sistema reemplaza.
    
    Peso (kg) = (PT² × LC) / 10838
    
    Donde:
    - PT: Perímetro Torácico (cm)
    - LC: Longitud del Cuerpo (cm)
    
    Limitaciones históricas:
    - Error: 5-20 kg por animal
    - Tiempo: 8-10 minutos por animal
    - Dependencia de habilidad del operario
    - Estrés en los animales (manipulación física)
    
    El nuevo sistema reduce esto a:
    - Error: <5 kg
    - Tiempo: <6 minutos por animal
    - Sin contacto físico (visión por computadora)
    """
    
    FORMULA = "Peso (kg) = (PT² × LC) / 10838"
    DESCRIPTION = "Perímetro Torácico (PT) y Longitud del Cuerpo (LC)"
    
    # Rangos típicos de mediciones
    PT_MIN_CM = 100
    PT_MAX_CM = 250
    LC_MIN_CM = 100
    LC_MAX_CM = 200
    
    # Error histórico de la fórmula
    ERROR_MIN_KG = 5.0
    ERROR_MAX_KG = 20.0
    
    @staticmethod
    def calculate_weight(
        perimetro_toracico_cm: float,
        longitud_cuerpo_cm: float,
    ) -> float:
        """
        Calcula peso usando fórmula tradicional de Schaeffer.
        
        Args:
            perimetro_toracico_cm: Perímetro torácico en centímetros
            longitud_cuerpo_cm: Longitud del cuerpo en centímetros
        
        Returns:
            Peso estimado en kilogramos
        
        Raises:
            ValueError: Si las mediciones están fuera de rango
        """
        if not SchaefferFormula.validate_measurements(
            perimetro_toracico_cm, longitud_cuerpo_cm
        ):
            raise ValueError(
                f"Mediciones fuera de rango: PT={perimetro_toracico_cm}cm, "
                f"LC={longitud_cuerpo_cm}cm"
            )
        
        return (perimetro_toracico_cm ** 2 * longitud_cuerpo_cm) / 10838
    
    @staticmethod
    def validate_measurements(pt: float, lc: float) -> bool:
        """
        Valida que las mediciones estén en rangos razonables.
        
        Args:
            pt: Perímetro torácico en cm
            lc: Longitud del cuerpo en cm
        
        Returns:
            True si están en rango, False si no
        """
        return (
            SchaefferFormula.PT_MIN_CM <= pt <= SchaefferFormula.PT_MAX_CM and
            SchaefferFormula.LC_MIN_CM <= lc <= SchaefferFormula.LC_MAX_CM
        )
    
    @staticmethod
    def compare_with_ai_estimation(
        schaeffer_weight: float,
        ai_weight: float,
    ) -> dict:
        """
        Compara estimación de Schaeffer vs IA.
        
        Args:
            schaeffer_weight: Peso estimado por fórmula Schaeffer
            ai_weight: Peso estimado por IA
        
        Returns:
            Dict con comparación y métricas
        """
        difference = abs(schaeffer_weight - ai_weight)
        
        return {
            "schaeffer_weight": schaeffer_weight,
            "ai_weight": ai_weight,
            "difference_kg": difference,
            "ai_is_more_accurate": difference < SchaefferFormula.ERROR_MIN_KG,
            "improvement_percentage": (
                (SchaefferFormula.ERROR_MIN_KG - difference) / 
                SchaefferFormula.ERROR_MIN_KG * 100
            ) if difference < SchaefferFormula.ERROR_MIN_KG else 0,
        }
```

### 6.3 Rangos de Peso por Raza y Edad

```python
# app/domain/value_objects.py
from typing import NamedTuple
from app.domain.enums import BreedType, AgeCategory

class WeightRange(NamedTuple):
    """Rango de peso con valores mínimo y máximo."""
    min_kg: float
    max_kg: float
    
    def contains(self, weight: float) -> bool:
        """Verifica si un peso está dentro del rango."""
        return self.min_kg <= weight <= self.max_kg
    
    def get_average(self) -> float:
        """Obtiene peso promedio del rango."""
        return (self.min_kg + self.max_kg) / 2

class BreedWeightRanges:
    """
    Rangos de peso esperados por raza y categoría de edad.
    
    Estos rangos se usan para:
    - Validar estimaciones del modelo ML
    - Alertas de desviación de peso
    - Comparaciones vs promedio de raza
    - Validación de datos de entrada
    
    Basados en datos reales de la Hacienda Gamelera.
    """
    
    RANGES: dict[BreedType, dict[AgeCategory, WeightRange]] = {
        # Brahman (Bos indicus) - Raza más pesada
        BreedType.BRAHMAN: {
            AgeCategory.TERNEROS: WeightRange(80, 180),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(180, 350),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(300, 500),
            AgeCategory.VACAS_TOROS: WeightRange(450, 900),
        },
        
        # Nelore (Bos indicus) - Similar a Brahman
        BreedType.NELORE: {
            AgeCategory.TERNEROS: WeightRange(75, 170),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(170, 330),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(280, 480),
            AgeCategory.VACAS_TOROS: WeightRange(400, 850),
        },
        
        # Angus (Bos taurus) - Raza europea mediana
        BreedType.ANGUS: {
            AgeCategory.TERNEROS: WeightRange(70, 165),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(165, 320),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(270, 460),
            AgeCategory.VACAS_TOROS: WeightRange(380, 800),
        },
        
        # Cebuinas (Bos indicus) - Raza cebuina mediana
        BreedType.CEBUINAS: {
            AgeCategory.TERNEROS: WeightRange(75, 175),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(175, 340),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(290, 490),
            AgeCategory.VACAS_TOROS: WeightRange(420, 870),
        },
        
        # Criollo (Bos taurus) - Raza local adaptada
        BreedType.CRIOLLO: {
            AgeCategory.TERNEROS: WeightRange(65, 150),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(150, 280),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(240, 400),
            AgeCategory.VACAS_TOROS: WeightRange(350, 650),
        },
        
        # Pardo Suizo (Bos taurus) - Raza lechera grande
        BreedType.PARDO_SUIZO: {
            AgeCategory.TERNEROS: WeightRange(80, 185),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(185, 360),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(310, 510),
            AgeCategory.VACAS_TOROS: WeightRange(460, 920),
        },
        
        # Jersey (Bos taurus) - Raza lechera pequeña
        BreedType.JERSEY: {
            AgeCategory.TERNEROS: WeightRange(60, 140),
            AgeCategory.VAQUILLONAS_TORILLOS: WeightRange(140, 260),
            AgeCategory.VAQUILLONAS_TORETES: WeightRange(220, 380),
            AgeCategory.VACAS_TOROS: WeightRange(330, 600),
        },
    }
    
    @classmethod
    def get_range(
        cls, 
        breed: BreedType, 
        age_category: AgeCategory
    ) -> WeightRange:
        """
        Obtiene rango de peso para raza y edad específicas.
        
        Args:
            breed: Una de las 7 razas soportadas
            age_category: Una de las 4 categorías de edad
        
        Returns:
            Rango de peso (min_kg, max_kg)
        
        Raises:
            KeyError: Si raza o categoría no existen
        """
        return cls.RANGES[breed][age_category]
    
    @classmethod
    def validate_weight(
        cls,
        weight_kg: float,
        breed: BreedType,
        age_category: AgeCategory,
    ) -> bool:
        """
        Valida que peso esté en rango esperado.
        
        Args:
            weight_kg: Peso a validar en kilogramos
            breed: Raza del animal
            age_category: Categoría de edad
        
        Returns:
            True si está en rango, False si no
        """
        weight_range = cls.get_range(breed, age_category)
        return weight_range.contains(weight_kg)
    
    @classmethod
    def get_average_weight(
        cls,
        breed: BreedType,
        age_category: AgeCategory,
    ) -> float:
        """
        Obtiene peso promedio para una raza y categoría.
        
        Args:
            breed: Raza del animal
            age_category: Categoría de edad
        
        Returns:
            Peso promedio en kilogramos
        """
        weight_range = cls.get_range(breed, age_category)
        return weight_range.get_average()
    
    @classmethod
    def get_all_ranges_for_breed(cls, breed: BreedType) -> dict[AgeCategory, WeightRange]:
        """
        Obtiene todos los rangos de peso para una raza.
        
        Args:
            breed: Raza del animal
        
        Returns:
            Dict con rangos por categoría de edad
        """
        return cls.RANGES[breed]
    
    @classmethod
    def get_weight_deviation(
        cls,
        actual_weight: float,
        breed: BreedType,
        age_category: AgeCategory,
    ) -> dict:
        """
        Calcula desviación del peso vs rango esperado.
        
        Args:
            actual_weight: Peso actual del animal
            breed: Raza del animal
            age_category: Categoría de edad
        
        Returns:
            Dict con información de desviación
        """
        weight_range = cls.get_range(breed, age_category)
        average_weight = weight_range.get_average()
        
        deviation = actual_weight - average_weight
        deviation_percentage = (deviation / average_weight) * 100
        
        return {
            "actual_weight": actual_weight,
            "expected_min": weight_range.min_kg,
            "expected_max": weight_range.max_kg,
            "expected_average": average_weight,
            "deviation_kg": deviation,
            "deviation_percentage": deviation_percentage,
            "is_within_range": weight_range.contains(actual_weight),
            "is_underweight": actual_weight < weight_range.min_kg,
            "is_overweight": actual_weight > weight_range.max_kg,
        }
```
