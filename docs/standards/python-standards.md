# Estándares de Codificación Python

Sistema de Estimación de Peso Bovino - Hacienda Gamelera

## 1. Convenciones de Naming

### 1.1 Idioma y Contexto

- **Código**: Inglés estricto (variables, funciones, clases)
- **Documentación**: Español para facilitar mantenimiento local
- **Comentarios**: Español para explicaciones técnicas

### 1.2 Naming Específico del Dominio

#### Razas Bovinas (7 razas específicas)

```python
# ✅ CORRECTO: Enum con las 7 razas exactas del proyecto
from enum import Enum

class BreedType(str, Enum):
    BRAHMAN = "brahman"
    NELORE = "nelore"
    ANGUS = "angus"
    CEBUINAS = "cebuinas"    # Bos indicus
    CRIOLLO = "criollo"      # Bos taurus
    PARDO_SUIZO = "pardo_suizo"
    JERSEY = "jersey"

# ✅ CORRECTO: Modelo Pydantic
from pydantic import BaseModel
from typing import Dict, List

class Breed(BaseModel):
    id: str
    name: BreedType
    scientific_name: str  # "Bos indicus" o "Bos taurus"
    model_version: str
    weight_ranges: Dict[str, Dict[str, float]]  # Por categoría de edad
    growth_rate_avg: float
    characteristics: List[str]
    is_active: bool

# ❌ INCORRECTO: Nombres genéricos
class BreedType(str, Enum):
    BREED_1 = "breed1"  # ❌ Muy genérico
    BREED_2 = "breed2"
```

#### Categorías de Edad (4 categorías específicas)

```python
# ✅ CORRECTO: Enum con las 4 categorías del proyecto
class AgeCategory(str, Enum):
    TERNEROS = "terneros"                    # <8 meses
    VAQUILLONAS_TORILLOS = "vaquillonas_torillos"   # 6-18 meses
    VAQUILLONAS_TORETES = "vaquillonas_toretes"     # 19-30 meses
    VACAS_TOROS = "vacas_toros"              # >30 meses

class AgeCategoryRange(BaseModel):
    category: AgeCategory
    min_months: int
    max_months: int
    
    @classmethod
    def get_ranges(cls) -> List['AgeCategoryRange']:
        return [
            cls(category=AgeCategory.TERNEROS, min_months=0, max_months=7),
            cls(category=AgeCategory.VAQUILLONAS_TORILLOS, min_months=6, max_months=18),
            cls(category=AgeCategory.VAQUILLONAS_TORETES, min_months=19, max_months=30),
            cls(category=AgeCategory.VACAS_TOROS, min_months=31, max_months=999),
        ]
```

#### Entidades Regulatorias Bolivianas

```python
# ✅ CORRECTO: Naming alineado con normativa
from datetime import datetime
from typing import Optional, List

class SENASAGReport(BaseModel):
    report_id: str
    report_type: str  # Inventario/Movilización/Sanitario
    period_start: datetime
    period_end: datetime
    total_animals: int
    pdf_url: Optional[str] = None
    csv_url: Optional[str] = None
    status: str
    created_at: datetime

class GMA(BaseModel):  # Guía de Movimiento Animal
    gma_number: str
    animal_ids: List[str]
    origin_farm_id: str
    destination: str
    gran_paititi_id: Optional[str] = None  # Sistema gubernamental
    regensa_compliance: 'REGENSACompliance'
    status: str
    created_at: datetime

class REGENSACompliance(BaseModel):
    chapter_3_10_compliant: bool  # Centros de concentración
    chapter_7_1_compliant: bool   # Requisitos sanitarios
    missing_requirements: List[str]
    validated_at: datetime
```

#### Métricas del Sistema

```python
# ✅ CORRECTO: Constantes de métricas del SCRUM
class SystemMetrics:
    # Métricas de precisión (documento 12 - SCRUM)
    MIN_PRECISION = 0.95          # ≥95%
    MIN_R2 = 0.95                 # R² ≥ 0.95
    MAX_ERROR_KG = 5.0            # <5 kg
    MAX_PROCESSING_TIME_MS = 3000 # <3 segundos
    
    # Validación en campo
    MIN_ANIMALS_VALIDATION = 50
    
    # Mejora vs método anterior (Fórmula Schaeffer)
    SCHAEFFER_ERROR_MIN = 5.0
    SCHAEFFER_ERROR_MAX = 20.0
```

### 1.3 Naming de Clases y Archivos

#### Estructura de Features (5 áreas funcionales)

```text
app/
├── api/
│   ├── routes/
│   │   ├── data_management.py      # Área 1: Gestión de Datos
│   │   │   ├── capture_sessions.py
│   │   │   ├── frame_quality.py
│   │   │   ├── breed_processing.py
│   │   ├── analytics_reports.py    # Área 2: Análisis y Reportes
│   │   │   ├── weight_evolution.py
│   │   │   ├── breed_comparison.py
│   │   │   ├── senasag_reports.py
│   │   ├── monitoring.py           # Área 3: Monitoreo y Planificación
│   │   │   ├── alerts.py
│   │   │   ├── calendar.py
│   │   │   ├── gma_management.py
│   │   ├── user_features.py        # Área 4: Funcionalidades Usuario
│   │   │   ├── search.py
│   │   │   ├── lists.py
│   │   │   ├── preferences.py
│   │   └── operations.py           # Área 5: Operación y Respaldos
│   │       ├── sync.py
│   │       ├── backup.py
│   │       └── gran_paititi.py
│
├── services/
│   ├── data_management/
│   │   ├── capture_service.py
│   │   ├── frame_evaluation_service.py
│   │   ├── breed_processing_service.py
│   ├── analytics/
│   │   ├── weight_evolution_service.py
│   │   ├── breed_comparison_service.py
│   │   ├── senasag_report_service.py
│   ├── monitoring/
│   │   ├── alert_service.py
│   │   ├── gma_service.py
│   │   ├── regensa_compliance_service.py
│   ├── operations/
│   │   ├── sync_service.py
│   │   ├── backup_service.py
│   │   └── gran_paititi_service.py
│
├── models/
│   ├── animal.py
│   ├── weighing.py
│   ├── breed.py
│   ├── age_category.py
│   ├── capture_session.py
│   ├── frame_quality.py
│   ├── senasag_report.py
│   ├── gma.py
│   └── regensa_compliance.py
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

## 2. Estructura de Archivos por Feature

### 2.1 Patrón de Organización (Clean Architecture)

Cada feature DEBE seguir la estructura:

```text
feature_name/
├── routes/          # API endpoints
├── services/        # Lógica de negocio
├── models/          # Modelos de datos
└── schemas/         # Esquemas Pydantic
```

### 2.2 Feature Completo - Ejemplo: data_management

```python
# app/models/capture_session.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List

class CaptureSession(BaseModel):
    id: str
    animal_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_frames: int
    frames_evaluated: int
    frames_rejected: int
    selected_frame_id: Optional[str] = None
    average_quality_score: float
    rejection_reasons: Dict[str, int]
    breed_type: BreedType
    created_at: datetime

# app/services/data_management/capture_service.py
from typing import Union
from fastapi import HTTPException

class CaptureService:
    def __init__(self, capture_repository):
        self.capture_repository = capture_repository
    
    async def start_continuous_capture(
        self,
        animal_id: str,
        breed_type: BreedType,
    ) -> Union[CaptureSession, HTTPException]:
        """
        Inicia captura continua según especificaciones del proyecto:
        - 10-15 FPS
        - 3-5 segundos de duración
        - Evaluación en tiempo real de calidad
        """
        # Validar que la raza sea una de las 7 del proyecto
        if not self._is_valid_breed(breed_type):
            raise HTTPException(
                status_code=400,
                detail="La raza debe ser una de las 7 soportadas: "
                       "Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey"
            )
        
        return await self.capture_repository.start_capture(
            animal_id=animal_id,
            breed_type=breed_type,
            fps=12,  # CaptureConstants.FRAMES_PER_SECOND
            duration_seconds=4,  # CaptureConstants.CAPTURE_DURATION
        )
    
    def _is_valid_breed(self, breed: BreedType) -> bool:
        """Valida que la raza sea una de las 7 del proyecto."""
        return breed in BreedType
```

## 3. FastAPI Patterns

### 3.1 Router para Captura Continua

```python
# app/api/routes/data_management/capture_sessions.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter(prefix="/capture-sessions", tags=["capture-sessions"])

@router.post("/start", response_model=CaptureSession)
async def start_capture_session(
    request: StartCaptureRequest,
    capture_service: CaptureService = Depends(get_capture_service),
) -> CaptureSession:
    """
    Inicia captura continua de fotogramas.
    Especificaciones: 10-15 FPS durante 3-5 segundos
    """
    try:
        session = await capture_service.start_continuous_capture(
            animal_id=request.animal_id,
            breed_type=request.breed_type,
        )
        return session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}/frames", response_model=List[FrameQuality])
async def get_evaluated_frames(
    session_id: str,
    frame_service: FrameEvaluationService = Depends(get_frame_service),
) -> List[FrameQuality]:
    """Obtiene fotogramas evaluados de una sesión."""
    return await frame_service.get_evaluated_frames(session_id)

@router.post("/{session_id}/select-best-frame")
async def select_best_frame(
    session_id: str,
    frame_service: FrameEvaluationService = Depends(get_frame_service),
) -> dict:
    """Selecciona el mejor fotograma basado en score ponderado."""
    best_frame = await frame_service.select_best_frame(session_id)
    return {"selected_frame_id": best_frame.id, "score": best_frame.overall_score}
```

### 3.2 Router para Integración SENASAG/REGENSA

```python
# app/api/routes/monitoring/gma_management.py
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/gma", tags=["gma"])

@router.post("/create", response_model=GMA)
async def create_gma(
    request: CreateGMARequest,
    gma_service: GMAService = Depends(get_gma_service),
    compliance_service: REGENSAComplianceService = Depends(get_compliance_service),
) -> GMA:
    """
    Crea Guía de Movimiento Animal (GMA).
    Valida cumplimiento de REGENSA capítulos 3.10 y 7.1
    """
    # Primero validar cumplimiento REGENSA
    compliance = await compliance_service.validate_compliance(request.origin_farm_id)
    
    if not compliance.is_compliant:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "No cumple con REGENSA capítulos 3.10 y 7.1",
                "missing_requirements": compliance.missing_requirements
            }
        )
    
    # Crear GMA
    gma = await gma_service.create_gma(
        animal_ids=request.animal_ids,
        origin_farm_id=request.origin_farm_id,
        destination=request.destination,
    )
    
    return gma

@router.get("/senasag/reports", response_model=List[SENASAGReport])
async def get_senasag_reports(
    period_start: datetime,
    period_end: datetime,
    report_type: str,
    senasag_service: SENASAGReportService = Depends(get_senasag_service),
) -> List[SENASAGReport]:
    """Obtiene reportes generados para SENASAG."""
    return await senasag_service.get_reports(period_start, period_end, report_type)
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
├── api/
│   ├── routes/
│   │   ├── test_capture_sessions.py
│   │   ├── test_gma_management.py
│   │   ├── test_senasag_reports.py
│
├── services/
│   ├── test_capture_service.py
│   ├── test_frame_evaluation_service.py
│   ├── test_gma_service.py
│   ├── test_regensa_compliance_service.py
│
├── models/
│   ├── test_capture_session.py
│   ├── test_breed.py
│   ├── test_gma.py
│
├── core/
│   ├── test_breed_validator.py
│   ├── test_frame_quality_calculator.py
```

### 5.3 Ejemplo de Test - Validación de Razas

```python
# tests/core/test_breed_validator.py
import pytest
from app.core.validators.breed_validator import BreedValidator
from app.models.breed import BreedType

class TestBreedValidator:
    def test_should_validate_all_7_breeds_from_hacienda_gamelera(self):
        # Arrange
        validator = BreedValidator()
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
            assert validator.is_valid(breed), f"{breed.value} debe ser válida"
    
    def test_should_return_breed_count_of_exactly_7(self):
        assert len(BreedType) == 7, "Deben ser exactamente las 7 razas de Hacienda Gamelera"
    
    def test_should_reject_invalid_breed(self):
        # Arrange
        validator = BreedValidator()
        
        # Act & Assert
        with pytest.raises(InvalidBreedException):
            validator.validate_breed("invalid_breed")
```

### 5.4 Ejemplo de Test - Evaluación de Fotogramas

```python
# tests/services/test_frame_evaluation_service.py
import pytest
from unittest.mock import Mock
from app.services.data_management.frame_evaluation_service import FrameEvaluationService
from app.core.constants.capture_constants import CaptureConstants

class TestFrameEvaluationService:
    @pytest.fixture
    def service(self):
        return FrameEvaluationService()
    
    def test_should_accept_frame_with_all_quality_metrics_above_threshold(self, service):
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

### 6.1 Constantes de Captura

```python
# app/core/constants/capture_constants.py
class CaptureConstants:
    # Parámetros de captura
    FRAMES_PER_SECOND = 12           # 10-15 FPS
    CAPTURE_DURATION_SECONDS = 4     # 3-5 segundos
    TOTAL_FRAMES_MIN = 30            # Mínimo esperado
    TOTAL_FRAMES_MAX = 75            # Máximo esperado
    
    # Umbrales de calidad (valores del ADR-010)
    MIN_SHARPNESS = 0.7
    MIN_BRIGHTNESS = 0.4
    MAX_BRIGHTNESS = 0.8
    MIN_CONTRAST = 0.5
    MIN_SILHOUETTE_VISIBILITY = 0.8
    MIN_ANGLE_SCORE = 0.6
    MIN_OVERALL_SCORE = 0.65
    
    # Pesos para score global (ADR-010)
    SILHOUETTE_WEIGHT = 0.40
    SHARPNESS_WEIGHT = 0.30
    BRIGHTNESS_WEIGHT = 0.20
    ANGLE_WEIGHT = 0.10
```

### 6.2 Configuración de la Aplicación

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
