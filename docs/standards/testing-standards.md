# Estándares de Testing y QA

## Contexto del Proyecto

**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Objetivo**: Cobertura >80%, todos los tests pasando antes de merge

## Pirámide de Testing

```
                 ┌─────────────────┐
                 │   E2E Tests     │  10%  - Flujos completos de usuario
                 │  (Integration)  │       - Validación con Bruno
                 └─────────────────┘
              ┌─────────────────────────┐
              │   Integration Tests     │  30%  - APIs + BD + ML
              │  (Component Testing)    │       - Sincronización offline
              └─────────────────────────┘
         ┌──────────────────────────────────────┐
         │         Unit Tests                   │  60%  - Funciones puras
         │  (Lógica de negocio, validaciones)  │       - Use cases, services
         └──────────────────────────────────────┘
```

---

## Herramientas de Testing

### Mobile (Flutter)

| Tipo | Herramienta | Uso |
|------|-------------|-----|
| **Unit tests** | flutter_test | Lógica de negocio, use cases |
| **Widget tests** | flutter_test | Widgets individuales |
| **Integration tests** | integration_test | Flujos completos |
| **Mocking** | mockito + build_runner | Mocks de repositories |
| **Coverage** | lcov | Cobertura de código |

### Backend (Python)

| Tipo | Herramienta | Uso |
|------|-------------|-----|
| **Unit tests** | pytest | Services, repositories |
| **API tests** | pytest + httpx.AsyncClient | Endpoints FastAPI |
| **Mocking** | pytest-mock, unittest.mock | Mocks de MongoDB, S3 |
| **Coverage** | pytest-cov | Cobertura >80% |
| **Fixtures** | pytest fixtures | Datos de prueba |

### ML Training

| Tipo | Herramienta | Uso |
|------|-------------|-----|
| **Notebook tests** | nbval | Validación notebooks |
| **Metrics tests** | pytest | Validar R² ≥0.95, MAE <5kg |
| **Model tests** | TensorFlow test utils | Inferencia correcta |

---

## Testing por Capa (Clean Architecture)

### Domain Layer (Lógica Pura)

**Objetivo**: 100% cobertura (capa más crítica)

```dart
// test/features/data_management/domain/usecases/estimate_weight_usecase_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:dartz/dartz.dart';

@GenerateMocks([WeighingRepository])
import 'estimate_weight_usecase_test.mocks.dart';

void main() {
  late EstimateWeightUseCase usecase;
  late MockWeighingRepository mockRepository;
  
  setUp(() {
    mockRepository = MockWeighingRepository();
    usecase = EstimateWeightUseCase(weighingRepository: mockRepository);
  });
  
  group('EstimateWeightUseCase -', () {
    const testAnimalId = 'animal-123';
    const testBreedType = BreedType.brahman;
    const testAgeCategory = AgeCategory.vacasToros;
    final testImageFile = File('test_image.jpg');
    
    final validWeighing = Weighing(
      id: 'weighing-123',
      animalId: testAnimalId,
      estimatedWeightKg: 487.3,
      confidence: 0.97,                        // ✅ >95%
      processingTimeMs: 2543,                  // ✅ <3000ms
      method: WeighingMethod.ia,
      timestamp: DateTime.now(),
    );
    
    test('DADO animal válido con raza Brahman '
         'CUANDO se estima peso '
         'ENTONCES retorna Weighing exitoso con confidence ≥95%', () async {
      // Arrange
      when(mockRepository.estimateWeight(
        animalId: testAnimalId,
        breedType: testBreedType,
        ageCategory: testAgeCategory,
        imageFile: testImageFile,
      )).thenAnswer((_) async => Right(validWeighing));
      
      // Act
      final result = await usecase(
        animalId: testAnimalId,
        breedType: testBreedType,
        ageCategory: testAgeCategory,
        imageFile: testImageFile,
      );
      
      // Assert
      expect(result.isRight, true);
      result.fold(
        (failure) => fail('No debería ser failure'),
        (weighing) {
          expect(weighing.estimatedWeightKg, 487.3);
          expect(weighing.confidence, greaterThanOrEqualTo(0.95));
          expect(weighing.processingTimeMs, lessThan(3000));
        },
      );
      
      verify(mockRepository.estimateWeight(
        animalId: testAnimalId,
        breedType: testBreedType,
        ageCategory: testAgeCategory,
        imageFile: testImageFile,
      )).called(1);
    });
    
    test('DADO estimación con confidence <95% '
         'CUANDO se valida resultado '
         'ENTONCES retorna PrecisionBelowThresholdFailure', () async {
      // Arrange
      final lowConfidenceWeighing = validWeighing.copyWith(confidence: 0.89);
      when(mockRepository.estimateWeight(
        animalId: any,
        breedType: any,
        ageCategory: any,
        imageFile: any,
      )).thenAnswer((_) async => Right(lowConfidenceWeighing));
      
      // Act
      final result = await usecase(
        animalId: testAnimalId,
        breedType: testBreedType,
        ageCategory: testAgeCategory,
        imageFile: testImageFile,
      );
      
      // Assert
      expect(result.isLeft, true);
      result.fold(
        (failure) {
          expect(failure, isA<PrecisionBelowThresholdFailure>());
          final precisionFailure = failure as PrecisionBelowThresholdFailure;
          expect(precisionFailure.confidence, 0.89);
        },
        (_) => fail('Debería ser Left con PrecisionBelowThresholdFailure'),
      );
    });
    
    test('DADO procesamiento >3 segundos '
         'CUANDO se valida resultado '
         'ENTONCES retorna ProcessingTimeTooSlowFailure', () async {
      // Arrange  
      final slowWeighing = validWeighing.copyWith(processingTimeMs: 3500);
      when(mockRepository.estimateWeight(
        animalId: any,
        breedType: any,
        ageCategory: any,
        imageFile: any,
      )).thenAnswer((_) async => Right(slowWeighing));
      
      // Act
      final result = await usecase(
        animalId: testAnimalId,
        breedType: testBreedType,
        ageCategory: testAgeCategory,
        imageFile: testImageFile,
      );
      
      // Assert
      expect(result.isLeft, true);
      result.fold(
        (failure) {
          expect(failure, isA<ProcessingTimeTooSlowFailure>());
        },
        (_) => fail('Debería ser Left'),
      );
    });
    
    // Tests para las 7 razas bovinas
    for (final breed in BreedType.values) {
      test('DADO raza válida ${breed.name} de Hacienda Gamelera '
           'CUANDO se estima peso '
           'ENTONCES usa modelo TFLite correcto', () async {
        // Arrange
        final weighing = validWeighing.copyWith(breedType: breed);
        when(mockRepository.estimateWeight(
          animalId: any,
          breedType: breed,
          ageCategory: any,
          imageFile: any,
        )).thenAnswer((_) async => Right(weighing));
        
        // Act
        final result = await usecase(
          animalId: testAnimalId,
          breedType: breed,
          ageCategory: testAgeCategory,
          imageFile: testImageFile,
        );
        
        // Assert
        expect(result.isRight, true);
        verify(mockRepository.estimateWeight(
          animalId: any,
          breedType: breed,  // Verifica que se pasó la raza correcta
          ageCategory: any,
          imageFile: any,
        )).called(1);
      });
    }
  });
}
```

### Python Unit Tests (pytest)

```python
# tests/unit/services/test_senasag_service.py

import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

from app.services.senasag_service import SENASAGService
from app.core.constants.breeds import BreedType
from app.core.constants.regulatory import SENASAGConstants
from app.domain.entities.senasag_report import ReportFormat, ReportStatus

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
    """Instancia de SENASAGService con dependencias mockeadas."""
    return SENASAGService(
        animal_repository=mock_animal_repository,
        senasag_repository=mock_senasag_repository,
    )

@pytest.fixture
def sample_animals_hacienda_gamelera():
    """
    Datos de muestra: animales de Hacienda Gamelera.
    
    Incluye las 7 razas exactas con distribución realista.
    """
    animals = []
    
    # Distribuir animales entre las 7 razas
    breed_distribution = {
        BreedType.BRAHMAN: 150,        # 30%
        BreedType.NELORE: 120,         # 24%
        BreedType.ANGUS: 80,           # 16%
        BreedType.CEBUINAS: 70,        # 14%
        BreedType.CRIOLLO: 40,         # 8%
        BreedType.PARDO_SUIZO: 30,     # 6%
        BreedType.JERSEY: 10,          # 2%
    }  # Total: 500 cabezas
    
    for breed, count in breed_distribution.items():
        for i in range(count):
            animals.append(Mock(
                id=uuid4(),
                tag_number=f"{breed.value.upper()[:3]}-{i+1:03d}",
                breed_type=breed,
                age_months=24,
                latest_weight_kg=450.0,
                status="active",
            ))
    
    return animals

@pytest.mark.asyncio
class TestSENASAGService:
    """Tests para SENASAGService (US-007)."""
    
    async def test_generate_pdf_report_success_500_animals(
        self,
        senasag_service,
        mock_animal_repository,
        sample_animals_hacienda_gamelera,
    ):
        """
        DADO: 500 animales registrados en Hacienda Gamelera
        CUANDO: Se genera reporte PDF
        ENTONCES: Reporte exitoso con las 7 razas incluidas
        """
        # Arrange
        farm_id = uuid4()
        period_start = datetime(2024, 10, 1)
        period_end = datetime(2024, 10, 31)
        
        mock_animal_repository.get_animals_by_farm_and_period.return_value = (
            sample_animals_hacienda_gamelera
        )
        
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
        assert report.total_animals == 500  # Total Hacienda Gamelera
        assert report.format == ReportFormat.PDF
        assert report.status == ReportStatus.GENERATED
        assert "hacienda-gamelera" in report.file_path.lower()
        
        # Verificar llamada a repositorio
        mock_animal_repository.get_animals_by_farm_and_period.assert_called_once()
    
    async def test_generate_csv_report_validates_all_7_breeds(
        self,
        senasag_service,
        mock_animal_repository,
        sample_animals_hacienda_gamelera,
    ):
        """
        DADO: Animales de las 7 razas de Hacienda Gamelera
        CUANDO: Se genera reporte CSV
        ENTONCES: CSV incluye las 7 razas sin errores
        """
        # Arrange
        mock_animal_repository.get_animals_by_farm_and_period.return_value = (
            sample_animals_hacienda_gamelera
        )
        
        # Act
        report = await senasag_service.generate_report(
            farm_id=uuid4(),
            report_type=SENASAGConstants.REPORT_TYPE_INVENTORY,
            period_start=datetime.now() - timedelta(days=30),
            period_end=datetime.now(),
            format=ReportFormat.CSV,
        )
        
        # Assert
        assert report.total_animals == 500
        
        # Verificar que CSV se puede parsear
        file_data, _, _ = await senasag_service.get_report_file(
            report_id=str(report.id),
            user_id=uuid4(),
        )
        
        # Parsear CSV
        csv_content = file_data.decode('utf-8')
        lines = csv_content.split('\n')
        
        # Verificar headers
        headers = lines[0].split(',')
        assert all(h in headers for h in SENASAGConstants.CSV_HEADERS)
        
        # Verificar que hay datos de las 7 razas
        breeds_in_csv = set()
        for line in lines[1:]:
            if line.strip():
                breed = line.split(',')[2]  # Columna 'raza'
                breeds_in_csv.add(breed)
        
        assert len(breeds_in_csv) == 7, (
            f"CSV debe incluir las 7 razas de Hacienda Gamelera. "
            f"Encontradas: {len(breeds_in_csv)}"
        )
    
    async def test_generate_report_performance_under_5_minutes(
        self,
        senasag_service,
        mock_animal_repository,
        sample_animals_hacienda_gamelera,
    ):
        """
        DADO: 500 animales en Hacienda Gamelera
        CUANDO: Se genera reporte PDF
        ENTONCES: Generación completa en <5 minutos
        """
        import time
        
        # Arrange
        mock_animal_repository.get_animals_by_farm_and_period.return_value = (
            sample_animals_hacienda_gamelera
        )
        
        # Act
        start_time = time.time()
        report = await senasag_service.generate_report(
            farm_id=uuid4(),
            report_type=SENASAGConstants.REPORT_TYPE_INVENTORY,
            period_start=datetime.now() - timedelta(days=30),
            period_end=datetime.now(),
            format=ReportFormat.PDF,
        )
        end_time = time.time()
        
        # Assert
        generation_time_seconds = end_time - start_time
        assert generation_time_seconds < 300, (  # 5 minutos = 300 segundos
            f"Generación tardó {generation_time_seconds:.1f}s > 300s objetivo "
            f"para 500 animales de Hacienda Gamelera"
        )
```

---

## Integration Tests (API + MongoDB)

```python
# tests/integration/api/test_animals_api.py

import pytest
from httpx import AsyncClient
from fastapi import status

from app.main import app
from app.core.constants.breeds import BreedType

@pytest.mark.asyncio
class TestAnimalsAPI:
    """Tests de integración para endpoints de animales."""
    
    async def test_create_animal_with_valid_brahman_breed(
        self,
        async_client: AsyncClient,
        auth_headers: dict,
    ):
        """
        DADO: Datos válidos de animal raza Brahman
        CUANDO: POST /animals
        ENTONCES: Animal creado exitosamente (201)
        """
        # Arrange
        animal_data = {
            "tag_number": "BRA-001",
            "breed_type": "brahman",  # Una de las 7 razas exactas
            "birth_date": "2022-03-15T00:00:00",
            "gender": "female",
            "status": "active",
            "color": "Rojo",
            "weight_at_birth_kg": 35.5,
        }
        
        # Act
        response = await async_client.post(
            "/api/v1/animals",
            json=animal_data,
            headers=auth_headers,
        )
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        
        data = response.json()
        assert data["tag_number"] == "BRA-001"
        assert data["breed_type"] == "brahman"
        assert data["age_category"] in ["terneros", "vaquillonas_torillos"]  # Depende de fecha actual
        assert "id" in data
        assert "created_at" in data
    
    async def test_create_animal_with_invalid_breed_returns_422(
        self,
        async_client: AsyncClient,
        auth_headers: dict,
    ):
        """
        DADO: Raza inválida (no es de las 7 de Hacienda Gamelera)
        CUANDO: POST /animals
        ENTONCES: Error 422 con mensaje descriptivo
        """
        # Arrange
        animal_data = {
            "tag_number": "HOL-001",
            "breed_type": "holstein",  # ❌ NO es una de las 7 razas
            "birth_date": "2022-03-15T00:00:00",
            "gender": "female",
        }
        
        # Act
        response = await async_client.post(
            "/api/v1/animals",
            json=animal_data,
            headers=auth_headers,
        )
        
        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        error = response.json()
        assert "detail" in error
        assert "holstein" in str(error).lower()
        assert any(breed.value in str(error) for breed in BreedType)  # Mensaje debe listar razas válidas
    
    @pytest.mark.parametrize("breed", [
        BreedType.BRAHMAN,
        BreedType.NELORE,
        BreedType.ANGUS,
        BreedType.CEBUINAS,
        BreedType.CRIOLLO,
        BreedType.PARDO_SUIZO,
        BreedType.JERSEY,
    ])
    async def test_create_animal_accepts_all_7_breeds(
        self,
        async_client: AsyncClient,
        auth_headers: dict,
        breed: BreedType,
    ):
        """
        DADO: Cada una de las 7 razas de Hacienda Gamelera
        CUANDO: POST /animals con raza específica
        ENTONCES: Animal creado exitosamente para todas
        """
        # Arrange
        animal_data = {
            "tag_number": f"{breed.value.upper()[:3]}-TEST",
            "breed_type": breed.value,
            "birth_date": "2022-03-15T00:00:00",
            "gender": "male",
        }
        
        # Act
        response = await async_client.post(
            "/api/v1/animals",
            json=animal_data,
            headers=auth_headers,
        )
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["breed_type"] == breed.value
```

---

## E2E Tests (Flujos Completos)

```dart
// integration_test/capture_and_estimate_flow_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';

import 'package:bovine_weight_estimation/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  
  group('E2E: Captura y Estimación de Peso -', () {
    testWidgets(
      'DADO usuario en pantalla principal '
      'CUANDO completa flujo de captura y estimación para Brahman '
      'ENTONCES peso estimado con precision >95% se muestra correctamente',
      (tester) async {
        // Arrange: Iniciar app
        app.main();
        await tester.pumpAndSettle();
        
        // Step 1: Login
        await tester.enterText(
          find.byKey(Key('email_field')),
          'bruno@haciendagamelera.com',
        );
        await tester.enterText(
          find.byKey(Key('password_field')),
          'test_password',
        );
        await tester.tap(find.byKey(Key('login_button')));
        await tester.pumpAndSettle();
        
        // Step 2: Navegar a captura
        await tester.tap(find.byIcon(Icons.camera_alt));
        await tester.pumpAndSettle();
        
        // Step 3: Seleccionar raza Brahman (una de las 7)
        await tester.tap(find.text('Brahman'));
        await tester.pumpAndSettle();
        
        expect(find.text('Brahman'), findsOneWidget);
        
        // Step 4: Iniciar captura continua
        await tester.tap(find.byKey(Key('capture_button')));
        
        // Esperar captura (3-5 segundos) + procesamiento (<3 segundos)
        await tester.pump(Duration(seconds: 8));
        
        // Step 5: Verificar resultado
        // Debe mostrar peso estimado
        expect(find.byKey(Key('estimated_weight')), findsOneWidget);
        
        // Debe mostrar confidence ≥95%
        final confidenceText = tester.widget<Text>(
          find.byKey(Key('confidence_score')),
        ).data!;
        
        final confidence = double.parse(
          confidenceText.replaceAll('%', ''),
        );
        
        expect(confidence, greaterThanOrEqualTo(95.0));
        
        // Debe tener botón guardar
        expect(find.byKey(Key('save_weighing_button')), findsOneWidget);
        
        // Step 6: Guardar pesaje
        await tester.tap(find.byKey(Key('save_weighing_button')));
        await tester.pumpAndSettle();
        
        // Verificar mensaje de éxito
        expect(find.text('Peso guardado exitosamente'), findsOneWidget);
      },
    );
    
    testWidgets(
      'DADO 10 animales registrados '
      'CUANDO se busca por raza Brahman '
      'ENTONCES solo muestra animales Brahman',
      (tester) async {
        // Test de búsqueda y filtros (US-006)
        // ...
      },
    );
  });
}
```

---

## Testing de Métricas ML

```python
# tests/unit/ml/test_model_metrics.py

import pytest
import numpy as np

from src.evaluation.metrics import MetricsCalculator, ModelMetrics
from app.core.constants.breeds import BreedType

class TestModelMetrics:
    """Tests de validación de métricas ML del sistema."""
    
    def test_metrics_meet_system_requirements(self):
        """
        DADO: Predicciones con alta precisión
        CUANDO: Se calculan métricas
        ENTONCES: R² ≥0.95 y MAE <5 kg (requisitos del sistema)
        """
        # Arrange: Datos simulados con alta precisión
        y_true = np.array([450.0, 480.0, 420.0, 500.0, 390.0])
        y_pred = np.array([452.0, 478.0, 422.0, 497.0, 388.0])  # Diferencias <5 kg
        
        # Act
        metrics = MetricsCalculator.calculate_metrics(
            y_true=y_true,
            y_pred=y_pred,
            breed_type=BreedType.BRAHMAN.value,
        )
        
        # Assert
        assert metrics.r2_score >= 0.95, (
            f"R² {metrics.r2_score:.4f} < 0.95 requerido para Hacienda Gamelera"
        )
        assert metrics.mae_kg < 5.0, (
            f"MAE {metrics.mae_kg:.2f} kg > 5 kg máximo permitido"
        )
        assert metrics.breed_type == BreedType.BRAHMAN.value
    
    def test_metrics_fail_if_precision_below_threshold(self):
        """
        DADO: Predicciones con baja precisión
        CUANDO: Se calculan métricas
        ENTONCES: AssertionError porque no cumple R² ≥0.95
        """
        # Arrange: Datos con baja precisión
        y_true = np.array([450.0, 480.0, 420.0, 500.0, 390.0])
        y_pred = np.array([470.0, 450.0, 440.0, 480.0, 410.0])  # Diferencias grandes
        
        # Act & Assert
        with pytest.raises(AssertionError, match="R².*< 0.95"):
            MetricsCalculator.calculate_metrics(
                y_true=y_true,
                y_pred=y_pred,
                breed_type=BreedType.ANGUS.value,
            )
    
    def test_metrics_fail_if_error_above_threshold(self):
        """
        DADO: Predicciones con error >5 kg
        CUANDO: Se calculan métricas
        ENTONCES: AssertionError porque no cumple MAE <5 kg
        """
        # Arrange
        y_true = np.array([450.0, 480.0, 420.0])
        y_pred = np.array([460.0, 465.0, 430.0])  # Errores: 10, 15, 10 kg
        
        # Act & Assert
        with pytest.raises(AssertionError, match="MAE.*> 5 kg"):
            MetricsCalculator.calculate_metrics(
                y_true=y_true,
                y_pred=y_pred,
                breed_type=BreedType.NELORE.value,
            )
    
    @pytest.mark.parametrize("breed", list(BreedType))
    def test_metrics_calculator_works_for_all_7_breeds(self, breed):
        """
        DADO: Cada una de las 7 razas de Hacienda Gamelera
        CUANDO: Se calculan métricas
        ENTONCES: Cálculo exitoso sin errores
        """
        # Arrange
        y_true = np.random.uniform(300, 600, 50)
        y_pred = y_true + np.random.normal(0, 2, 50)  # Error pequeño
        
        # Act
        metrics = MetricsCalculator.calculate_metrics(
            y_true=y_true,
            y_pred=y_pred,
            breed_type=breed.value,
        )
        
        # Assert
        assert metrics.breed_type == breed.value
        assert metrics.n_samples == 50
```

---

## Fixtures de Testing

```python
# tests/conftest.py

import pytest
from httpx import AsyncClient
from typing import AsyncGenerator
from motor.motor_asyncio import AsyncIOMotorClient

from app.main import app
from app.database.mongodb import get_database
from app.core.config import settings

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP asíncrono para tests de API."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def test_db():
    """Base de datos MongoDB de test (se limpia después de cada test)."""
    client = AsyncIOMotorClient(settings.MONGODB_TEST_URL)
    db = client[settings.MONGODB_TEST_DB_NAME]
    
    yield db
    
    # Cleanup: eliminar colecciones de test
    for collection_name in await db.list_collection_names():
        await db[collection_name].drop()
    
    client.close()

@pytest.fixture
def sample_animal_data():
    """Datos de muestra para crear animal de Hacienda Gamelera."""
    return {
        "tag_number": "GAM-TEST-001",
        "breed_type": "brahman",  # Una de las 7 razas exactas
        "birth_date": "2022-03-15T00:00:00",
        "gender": "female",
        "status": "active",
        "color": "Rojo",
        "observations": "Animal de prueba - Hacienda Gamelera",
    }

@pytest.fixture
async def auth_headers(async_client: AsyncClient) -> dict:
    """Headers de autenticación para tests (JWT token)."""
    # Login como Bruno Brito Macedo
    response = await async_client.post(
        "/api/v1/auth/login",
        json={
            "email": "bruno@haciendagamelera.com",
            "password": "test_password",
        },
    )
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

---

## Coverage Requirements

### Mínimos Obligatorios

| Componente | Coverage Mínimo | Objetivo Ideal |
|------------|-----------------|----------------|
| **Domain Layer** | 100% | 100% |
| **Services** | 90% | 95% |
| **Repositories** | 80% | 85% |
| **API Routes** | 80% | 85% |
| **Overall** | 80% | 85% |

### Comandos de Coverage

```bash
# Flutter
cd mobile
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html

# Verificar >80%
flutter test --coverage && lcov --summary coverage/lcov.info

# Python
cd backend
pytest --cov=app --cov-report=html --cov-report=term-missing
open htmlcov/index.html

# Verificar >80% (falla si <80%)
pytest --cov=app --cov-fail-under=80
```

---

## Testing Checklist (Definition of Done)

### Por User Story

```markdown
## US-007: Reportes SENASAG - Testing Checklist

### Unit Tests (Services)
- [x] test_generate_pdf_report_success_500_animals
- [x] test_generate_csv_report_validates_all_7_breeds
- [x] test_generate_xml_report_structure
- [x] test_generate_report_performance_under_5_minutes
- [x] test_send_report_email_background_task
- [x] test_validate_report_period
- [x] test_count_by_breed_returns_7_breeds

### Integration Tests (API + MongoDB)
- [x] test_post_senasag_reports_returns_201
- [x] test_get_senasag_reports_list_with_pagination
- [x] test_download_report_pdf_returns_file
- [x] test_generate_report_saves_to_database

### E2E Tests (Manual con Bruno)
- [x] Bruno genera reporte de 500 cabezas desde app móvil
- [x] Reporte PDF se ve profesional y completo
- [x] CSV se puede abrir en Excel sin errores
- [x] Email con adjunto llega correctamente

### Performance Tests
- [x] Generación PDF <5 minutos para 500 animales
- [x] Generación CSV <2 minutos para 500 animales
- [x] Descarga de archivo <10 segundos

### Security Tests
- [x] Endpoint requiere autenticación (JWT)
- [x] Usuario solo puede ver reportes de su hacienda
- [x] Archivos no son accesibles sin token válido

### Validación Normativa
- [x] Estructura PDF cumple formato SENASAG
- [x] Headers CSV coinciden con SENASAGConstants.CSV_HEADERS
- [x] XML parseable sin errores
- [x] Datos de Hacienda Gamelera correctos (nombre, GPS, propietario)
```

---

## Continuous Testing (CI)

```yaml
# .github/workflows/tests.yml

name: Tests

on:
  push:
    branches: [ development, main ]
  pull_request:
    branches: [ development, main ]

jobs:
  test-backend:
    name: Tests Backend (Python)
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run tests con coverage
        run: |
          cd backend
          pytest --cov=app --cov-fail-under=80 --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
  
  test-mobile:
    name: Tests Mobile (Flutter)
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'
      
      - name: Install dependencies
        run: |
          cd mobile
          flutter pub get
      
      - name: Run tests
        run: |
          cd mobile
          flutter test --coverage
      
      - name: Check coverage >80%
        run: |
          cd mobile
          lcov --summary coverage/lcov.info | grep "lines.*: 8[0-9]\\|9[0-9]\\|100"
```

---

## Validación en Campo (Bruno Brito Macedo)

### Protocolo de Validación

```markdown
# Protocolo de Validación en Campo - Hacienda Gamelera

## Objetivo
Validar que el sistema funciona en condiciones reales con Bruno Brito Macedo.

## Participantes
- **Product Owner**: Miguel Angel Escobar Lazcano
- **Usuario final**: Bruno Brito Macedo
- **Ubicación**: Hacienda Gamelera, San Ignacio de Velasco

## Checklist de Validación

### Pre-validación
- [ ] Sistema instalado en smartphone de Bruno (Android)
- [ ] 50+ animales registrados en sistema
- [ ] Modelos TFLite de las 7 razas cargados
- [ ] Báscula calibrada para comparación de pesos reales

### Validación Funcional

#### US-001: Captura Continua
- [ ] Bruno puede iniciar captura sin ayuda
- [ ] Captura 30-75 fotogramas en 3-5 segundos
- [ ] Fotograma seleccionado es visualmente claro
- [ ] Proceso es más rápido que llevar animal a báscula

#### US-002: Estimación IA
- [ ] Estimación completa en <3 segundos
- [ ] Confidence mostrado es ≥95% en al menos 3 razas
- [ ] Peso estimado está dentro de ±5 kg del peso real (báscula)
- [ ] Bruno confía en usar estimación para decisiones

#### US-007: Reportes SENASAG
- [ ] Bruno genera reporte de 500 cabezas en <5 minutos
- [ ] PDF es profesional y completo
- [ ] CSV se abre correctamente en Excel
- [ ] Bruno aprobaría enviar este reporte a SENASAG

### Validación No Funcional

#### Performance
- [ ] App responde fluidamente (<100ms)
- [ ] Búsqueda en 500 animales es instantánea (<3s)
- [ ] Batería dura toda la jornada (8 horas)

#### Offline-First
- [ ] Sistema funciona 100% sin conexión
- [ ] Sincronización automática al recuperar señal
- [ ] No se pierden datos sin conexión

#### Usabilidad
- [ ] Bruno puede usar todas las funciones sin entrenamiento
- [ ] Interfaz es intuitiva (no necesita manual)
- [ ] Mensajes de error son claros en español
- [ ] Botones son fáciles de tocar (tamaño adecuado)

### Resultados

**Fecha validación**: _______________  
**Satisfacción Bruno**: ___/10  
**Aprobado para producción**: Sí / No  
**Observaciones**: 

_______________________________________________
_______________________________________________
_______________________________________________

**Firma Bruno Brito Macedo**: _______________
```

---

## Referencias

- **Definition of Done**: `docs/product/definition-of-done.md`
- **User Stories**: `docs/product/product-backlog.md`
- **Flutter testing**: https://docs.flutter.dev/testing
- **pytest**: https://docs.pytest.org/

---

**Documento de Testing Standards v1.0**  
**Fecha**: 28 octubre 2024  
**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cobertura objetivo**: >80% (Domain: 100%)

