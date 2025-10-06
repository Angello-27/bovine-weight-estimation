# Estándares de Testing

Sistema de Estimación de Peso Bovino - Hacienda Gamelera

## 1. Cobertura de Testing

### 1.1 Cobertura Mínima Requerida

- **Cobertura general**: 70% mínimo
- **Casos críticos**: 100% obligatorio
- **Funcionalidades normativas**: 100% obligatorio

### 1.2 Casos Críticos (100% Cobertura Obligatoria)

```dart
// Flutter - Casos críticos
✅ Evaluación de calidad de fotogramas (5 criterios)
✅ Selección del mejor fotograma (score ponderado)
✅ Validación de las 7 razas específicas
✅ Cálculo de categorías de edad (4 categorías)
✅ Generación de GMA (Guía de Movimiento Animal)
✅ Validación de cumplimiento REGENSA (capítulos 3.10 y 7.1)
✅ Procesamiento offline-first con SQLite
✅ Sincronización con resolución de conflictos

// Python - Casos críticos
✅ Validación de razas bovinas (7 razas)
✅ Cálculo de métricas de precisión (≥95%, R² ≥ 0.95)
✅ Generación de reportes SENASAG (PDF/CSV/XML)
✅ Integración con Gran Paitití
✅ Validación de cumplimiento normativo
✅ Procesamiento de modelos ML por raza
```

## 2. Estructura de Tests

### 2.1 Organización por Tecnología

```text
# Flutter Tests
test/
├── features/
│   ├── data_management/
│   │   ├── domain/
│   │   │   ├── usecases/
│   │   │   │   ├── start_continuous_capture_usecase_test.dart
│   │   │   │   ├── evaluate_frame_quality_usecase_test.dart
│   │   │   │   ├── select_best_frame_usecase_test.dart
│   │   │   │   ├── process_by_breed_usecase_test.dart
│   │   ├── presentation/
│   │   │   ├── providers/
│   │   │   │   ├── camera_provider_test.dart
│   │   │   │   ├── frame_evaluation_provider_test.dart
│   │   │   ├── widgets/
│   │   │   │   ├── breed_selector_widget_test.dart
│   │   │   │   ├── frame_quality_indicator_test.dart
│   │
│   ├── monitoring/
│   │   ├── domain/
│   │   │   ├── usecases/
│   │   │   │   ├── generate_senasag_report_usecase_test.dart
│   │   │   │   ├── create_gma_usecase_test.dart
│   │   │   │   ├── validate_regensa_compliance_usecase_test.dart
│   │
├── core/
│   ├── utils/
│   │   ├── breed_validator_test.dart
│   │   ├── age_category_calculator_test.dart
│   │   ├── frame_quality_calculator_test.dart
│   │   ├── precision_calculator_test.dart

# Python Tests
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
│   ├── test_precision_metrics.py
```

## 3. Tests Específicos del Dominio

### 3.1 Tests de Validación de Razas (Flutter)

```dart
// test/core/utils/breed_validator_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:bovine_weight_estimation/core/utils/breed_validator.dart';
import 'package:bovine_weight_estimation/core/constants/breeds.dart';

void main() {
  group('BreedValidator - Validación de 7 Razas Específicas', () {
    late BreedValidator validator;
    
    setUp(() {
      validator = BreedValidator();
    });
    
    test('should validate all 7 breeds from Hacienda Gamelera', () {
      // Arrange
      final validBreeds = [
        BreedType.brahman,
        BreedType.nelore,
        BreedType.angus,
        BreedType.cebuinas,
        BreedType.criollo,
        BreedType.pardoSuizo,
        BreedType.jersey,
      ];
      
      // Act & Assert
      for (final breed in validBreeds) {
        expect(validator.isValid(breed), true, 
          reason: '${breed.toString()} debe ser válida para Hacienda Gamelera');
      }
    });
    
    test('should return breed count of exactly 7', () {
      expect(BreedType.values.length, 7,
        reason: 'Deben ser exactamente las 7 razas de Hacienda Gamelera');
    });
    
    test('should reject invalid breeds not in Hacienda Gamelera', () {
      // Arrange
      final invalidBreeds = ['holstein', 'hereford', 'charolais'];
      
      // Act & Assert
      for (final breedName in invalidBreeds) {
        expect(() => validator.validateBreed(breedName), 
          throwsA(isA<InvalidBreedFailure>()),
          reason: '$breedName no está presente en Hacienda Gamelera');
      }
    });
    
    test('should validate scientific names correctly', () {
      // Arrange & Act
      final brahman = validator.getBreedInfo(BreedType.brahman);
      final cebuinas = validator.getBreedInfo(BreedType.cebuinas);
      final criollo = validator.getBreedInfo(BreedType.criollo);
      
      // Assert
      expect(brahman.scientificName, 'Bos indicus');
      expect(cebuinas.scientificName, 'Bos indicus');
      expect(criollo.scientificName, 'Bos taurus');
    });
  });
}
```

### 3.2 Tests de Evaluación de Fotogramas (Flutter)

```dart
// test/features/data_management/domain/usecases/evaluate_frame_quality_usecase_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:bovine_weight_estimation/features/data_management/domain/usecases/evaluate_frame_quality_usecase.dart';
import 'package:bovine_weight_estimation/core/constants/capture_constants.dart';

void main() {
  group('EvaluateFrameQualityUseCase - Criterios de Calidad', () {
    late EvaluateFrameQualityUseCase useCase;
    late MockFrameDataRepository mockRepository;
    
    setUp(() {
      mockRepository = MockFrameDataRepository();
      useCase = EvaluateFrameQualityUseCase(mockRepository);
    });
    
    test('should accept frame with all quality metrics above threshold', () async {
      // Arrange
      final frameData = MockFrameData();
      when(frameData.sharpness).thenReturn(0.85);  // > 0.7 ✅
      when(frameData.brightness).thenReturn(0.6);   // 0.4-0.8 ✅
      when(frameData.contrast).thenReturn(0.7);     // > 0.5 ✅
      when(frameData.silhouetteVisibility).thenReturn(0.9);  // > 0.8 ✅
      when(frameData.angleScore).thenReturn(0.75);  // > 0.6 ✅
      
      // Act
      final result = await useCase(frameData: frameData);
      
      // Assert
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Should not fail with valid frame'),
        (frameQuality) {
          expect(frameQuality.overallScore, greaterThan(CaptureConstants.minOverallScore));
          expect(frameQuality.isAcceptable, true);
          expect(frameQuality.rejectionReason, isNull);
        },
      );
    });
    
    test('should reject frame with low silhouette visibility (<0.8)', () async {
      // Arrange
      final frameData = MockFrameData();
      when(frameData.sharpness).thenReturn(0.85);
      when(frameData.brightness).thenReturn(0.6);
      when(frameData.contrast).thenReturn(0.7);
      when(frameData.silhouetteVisibility).thenReturn(0.5);  // < 0.8 ❌
      when(frameData.angleScore).thenReturn(0.75);
      
      // Act
      final result = await useCase(frameData: frameData);
      
      // Assert
      result.fold(
        (failure) => fail('Should not fail'),
        (frameQuality) {
          expect(frameQuality.isAcceptable, false);
          expect(frameQuality.rejectionReason, contains('silueta'));
          expect(frameQuality.overallScore, lessThan(CaptureConstants.minOverallScore));
        },
      );
    });
    
    test('should calculate weighted overall score correctly', () async {
      // Arrange: Valores específicos para verificar pesos del ADR-010
      final frameData = MockFrameData();
      when(frameData.sharpness).thenReturn(0.8);
      when(frameData.brightness).thenReturn(0.6);
      when(frameData.silhouetteVisibility).thenReturn(0.9);
      when(frameData.angleScore).thenReturn(0.7);
      
      // Act
      final result = await useCase(frameData: frameData);
      
      // Assert
      result.fold(
        (failure) => fail('Should not fail'),
        (frameQuality) {
          // Score esperado: (0.9*0.4) + (0.8*0.3) + (0.6*0.2) + (0.7*0.1) = 0.79
          final expectedScore = (0.9 * CaptureConstants.silhouetteWeight) +
                               (0.8 * CaptureConstants.sharpnessWeight) +
                               (0.6 * CaptureConstants.brightnessWeight) +
                               (0.7 * CaptureConstants.angleWeight);
          expect(frameQuality.overallScore, closeTo(expectedScore, 0.01));
        },
      );
    });
    
    test('should reject frame with insufficient sharpness (<0.7)', () async {
      // Arrange
      final frameData = MockFrameData();
      when(frameData.sharpness).thenReturn(0.5);  // < 0.7 ❌
      when(frameData.brightness).thenReturn(0.6);
      when(frameData.contrast).thenReturn(0.7);
      when(frameData.silhouetteVisibility).thenReturn(0.9);
      when(frameData.angleScore).thenReturn(0.75);
      
      // Act
      final result = await useCase(frameData: frameData);
      
      // Assert
      result.fold(
        (failure) => fail('Should not fail'),
        (frameQuality) {
          expect(frameQuality.isAcceptable, false);
          expect(frameQuality.rejectionReason, contains('nitidez'));
        },
      );
    });
  });
}
```

### 3.3 Tests de Integración Normativa (Python)

```python
# tests/services/test_regensa_compliance_service.py
import pytest
from unittest.mock import Mock
from app.services.monitoring.regensa_compliance_service import REGENSAComplianceService
from app.models.regensa_compliance import REGENSACompliance
from app.core.exceptions import REGENSAComplianceException

class TestREGENSAComplianceService:
    @pytest.fixture
    def service(self):
        return REGENSAComplianceService()
    
    def test_should_validate_chapter_3_10_requirements_centros_concentracion(self, service):
        """Test validación de capítulo 3.10 - Centros de concentración animal"""
        # Arrange
        farm_data = Mock()
        farm_data.has_antislip_ramps = True
        farm_data.corridor_width_meters = 1.8      # ≥ 1.6m ✅
        farm_data.space_per_animal_m2 = 2.5         # ≥ 2m² ✅
        farm_data.has_disinfection_system = True
        farm_data.has_quarantine_corral = True
        farm_data.prohibits_pain_instruments = True
        
        # Act
        result = service.validate_chapter_3_10(farm_data)
        
        # Assert
        assert result.is_compliant is True
        assert result.chapter_3_10_compliant is True
        assert len(result.missing_requirements) == 0
    
    def test_should_fail_if_corridor_width_less_than_1_6m(self, service):
        """Test falla si ancho de corredor < 1.6m"""
        # Arrange
        farm_data = Mock()
        farm_data.has_antislip_ramps = True
        farm_data.corridor_width_meters = 1.4      # < 1.6m ❌
        farm_data.space_per_animal_m2 = 2.5
        farm_data.has_disinfection_system = True
        farm_data.has_quarantine_corral = True
        farm_data.prohibits_pain_instruments = True
        
        # Act
        result = service.validate_chapter_3_10(farm_data)
        
        # Assert
        assert result.is_compliant is False
        assert result.chapter_3_10_compliant is False
        assert 'corredor_ancho' in result.missing_requirements
    
    def test_should_fail_if_space_per_animal_less_than_2m2(self, service):
        """Test falla si espacio por animal < 2m²"""
        # Arrange
        farm_data = Mock()
        farm_data.has_antislip_ramps = True
        farm_data.corridor_width_meters = 1.8
        farm_data.space_per_animal_m2 = 1.5         # < 2m² ❌
        farm_data.has_disinfection_system = True
        farm_data.has_quarantine_corral = True
        farm_data.prohibits_pain_instruments = True
        
        # Act
        result = service.validate_chapter_3_10(farm_data)
        
        # Assert
        assert result.is_compliant is False
        assert result.chapter_3_10_compliant is False
        assert 'espacio_por_animal' in result.missing_requirements
    
    def test_should_validate_chapter_7_1_requirements_sanitarios(self, service):
        """Test validación de capítulo 7.1 - Requisitos sanitarios"""
        # Arrange
        farm_data = Mock()
        farm_data.has_veterinary_certificate = True
        farm_data.has_health_register = True
        farm_data.has_vaccination_record = True
        farm_data.has_quarantine_protocol = True
        
        # Act
        result = service.validate_chapter_7_1(farm_data)
        
        # Assert
        assert result.is_compliant is True
        assert result.chapter_7_1_compliant is True
        assert len(result.missing_requirements) == 0
    
    def test_should_fail_if_missing_veterinary_certificate(self, service):
        """Test falla si falta certificado veterinario"""
        # Arrange
        farm_data = Mock()
        farm_data.has_veterinary_certificate = False  # ❌
        farm_data.has_health_register = True
        farm_data.has_vaccination_record = True
        farm_data.has_quarantine_protocol = True
        
        # Act
        result = service.validate_chapter_7_1(farm_data)
        
        # Assert
        assert result.is_compliant is False
        assert result.chapter_7_1_compliant is False
        assert 'certificado_veterinario' in result.missing_requirements
```

### 3.4 Tests de Métricas de Precisión (Python)

```python
# tests/core/test_precision_metrics.py
import pytest
from app.core.metrics.precision_calculator import PrecisionCalculator
from app.core.constants.system_metrics import SystemMetrics

class TestPrecisionMetrics:
    @pytest.fixture
    def calculator(self):
        return PrecisionCalculator()
    
    def test_should_calculate_r2_score_above_threshold(self, calculator):
        """Test cálculo de R² ≥ 0.95 (métrica crítica del SCRUM)"""
        # Arrange
        actual_weights = [450, 520, 380, 600, 480, 550, 420]
        predicted_weights = [445, 525, 375, 605, 475, 555, 415]
        
        # Act
        r2_score = calculator.calculate_r2_score(actual_weights, predicted_weights)
        
        # Assert
        assert r2_score >= SystemMetrics.MIN_R2, f"R² {r2_score} debe ser ≥ {SystemMetrics.MIN_R2}"
    
    def test_should_calculate_mae_below_5kg_threshold(self, calculator):
        """Test error absoluto promedio < 5kg (métrica crítica del SCRUM)"""
        # Arrange
        actual_weights = [450, 520, 380, 600, 480, 550, 420]
        predicted_weights = [445, 525, 375, 605, 475, 555, 415]
        
        # Act
        mae = calculator.calculate_mae(actual_weights, predicted_weights)
        
        # Assert
        assert mae < SystemMetrics.MAX_ERROR_KG, f"MAE {mae}kg debe ser < {SystemMetrics.MAX_ERROR_KG}kg"
    
    def test_should_calculate_precision_above_95_percent(self, calculator):
        """Test precisión ≥ 95% (métrica crítica del SCRUM)"""
        # Arrange
        actual_weights = [450, 520, 380, 600, 480, 550, 420]
        predicted_weights = [445, 525, 375, 605, 475, 555, 415]
        
        # Act
        precision = calculator.calculate_precision(actual_weights, predicted_weights)
        
        # Assert
        assert precision >= SystemMetrics.MIN_PRECISION, f"Precisión {precision} debe ser ≥ {SystemMetrics.MIN_PRECISION}"
    
    def test_should_fail_if_precision_below_threshold(self, calculator):
        """Test falla si precisión < 95%"""
        # Arrange
        actual_weights = [450, 520, 380, 600, 480, 550, 420]
        predicted_weights = [400, 480, 320, 550, 420, 500, 370]  # Errores grandes
        
        # Act & Assert
        with pytest.raises(PrecisionBelowThresholdException) as exc_info:
            calculator.validate_precision_threshold(actual_weights, predicted_weights)
        
        assert "Precisión" in str(exc_info.value)
        assert "95%" in str(exc_info.value)
```

## 4. Tests de Integración

### 4.1 Test de Flujo Completo de Captura (Flutter)

```dart
// test/integration/capture_flow_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:bovine_weight_estimation/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  
  group('Flujo Completo de Captura - Hacienda Gamelera', () {
    testWidgets('should complete full capture flow for Brahman breed', (tester) async {
      // Arrange
      app.main();
      await tester.pumpAndSettle();
      
      // Act - Navegar a pantalla de captura
      await tester.tap(find.text('Captura de Peso'));
      await tester.pumpAndSettle();
      
      // Act - Seleccionar raza Brahman
      await tester.tap(find.byType(BreedDropdown));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Brahman'));
      await tester.pumpAndSettle();
      
      // Act - Iniciar captura continua
      await tester.tap(find.text('Iniciar Captura'));
      await tester.pumpAndSettle();
      
      // Assert - Verificar que inicia captura
      expect(find.text('Capturando fotogramas...'), findsOneWidget);
      
      // Act - Esperar captura (simulada)
      await tester.pump(Duration(seconds: 5));
      
      // Assert - Verificar evaluación de calidad
      expect(find.text('Evaluando calidad...'), findsOneWidget);
      
      // Act - Esperar evaluación
      await tester.pump(Duration(seconds: 2));
      
      // Assert - Verificar selección del mejor fotograma
      expect(find.text('Seleccionando mejor fotograma...'), findsOneWidget);
      
      // Act - Esperar selección
      await tester.pump(Duration(seconds: 1));
      
      // Assert - Verificar resultado
      expect(find.text('Captura exitosa'), findsOneWidget);
      expect(find.textContaining('kg'), findsOneWidget);
      
      // Assert - Verificar que se guardó localmente (offline-first)
      expect(find.text('Guardado localmente'), findsOneWidget);
    });
    
    testWidgets('should validate all 7 breeds in capture flow', (tester) async {
      // Arrange
      app.main();
      await tester.pumpAndSettle();
      
      final breeds = [
        'Brahman', 'Nelore', 'Angus', 'Cebuinas (Bos indicus)',
        'Criollo (Bos taurus)', 'Pardo Suizo', 'Jersey'
      ];
      
      // Act & Assert - Verificar que todas las razas están disponibles
      await tester.tap(find.text('Captura de Peso'));
      await tester.pumpAndSettle();
      
      await tester.tap(find.byType(BreedDropdown));
      await tester.pumpAndSettle();
      
      for (final breed in breeds) {
        expect(find.text(breed), findsOneWidget,
          reason: 'Raza $breed debe estar disponible para Hacienda Gamelera');
      }
    });
  });
}
```

### 4.2 Test de Generación de GMA (Python)

```python
# tests/integration/test_gma_generation_flow.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.gma import GMA
from app.models.regensa_compliance import REGENSACompliance

client = TestClient(app)

class TestGMAGenerationFlow:
    def test_should_generate_gma_with_regensa_compliance(self):
        """Test flujo completo de generación de GMA con validación REGENSA"""
        # Arrange
        farm_id = "hacienda_gamelera_001"
        animal_ids = ["animal_001", "animal_002", "animal_003"]
        destination = "Matadero San Ignacio"
        
        # Act 1 - Validar cumplimiento REGENSA
        compliance_response = client.post(
            "/regensa/validate-compliance",
            json={"farm_id": farm_id}
        )
        
        # Assert 1 - Verificar cumplimiento
        assert compliance_response.status_code == 200
        compliance_data = compliance_response.json()
        assert compliance_data["chapter_3_10_compliant"] is True
        assert compliance_data["chapter_7_1_compliant"] is True
        
        # Act 2 - Crear GMA
        gma_response = client.post(
            "/gma/create",
            json={
                "animal_ids": animal_ids,
                "origin_farm_id": farm_id,
                "destination": destination
            }
        )
        
        # Assert 2 - Verificar GMA creada
        assert gma_response.status_code == 200
        gma_data = gma_response.json()
        assert gma_data["gma_number"] is not None
        assert gma_data["status"] == "Pendiente"
        assert gma_data["regensa_compliance"]["chapter_3_10_compliant"] is True
        assert gma_data["regensa_compliance"]["chapter_7_1_compliant"] is True
    
    def test_should_fail_gma_creation_without_regensa_compliance(self):
        """Test falla creación de GMA sin cumplimiento REGENSA"""
        # Arrange
        farm_id = "farm_non_compliant"
        animal_ids = ["animal_001"]
        destination = "Destino"
        
        # Act - Intentar crear GMA sin cumplimiento
        response = client.post(
            "/gma/create",
            json={
                "animal_ids": animal_ids,
                "origin_farm_id": farm_id,
                "destination": destination
            }
        )
        
        # Assert - Verificar error
        assert response.status_code == 400
        error_data = response.json()
        assert "No cumple con REGENSA" in error_data["message"]
        assert "missing_requirements" in error_data["detail"]
```

## 5. Performance Testing

### 5.1 Tests de Rendimiento (Flutter)

```dart
// test/performance/capture_performance_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:bovine_weight_estimation/features/data_management/domain/usecases/evaluate_frame_quality_usecase.dart';

void main() {
  group('Performance Tests - Métricas del SCRUM', () {
    test('should process frame evaluation under 3 seconds', () async {
      // Arrange
      final useCase = EvaluateFrameQualityUseCase();
      final frameData = MockFrameData();
      
      // Act
      final stopwatch = Stopwatch()..start();
      final result = await useCase(frameData: frameData);
      stopwatch.stop();
      
      // Assert
      expect(stopwatch.elapsedMilliseconds, lessThan(3000),
        reason: 'Procesamiento debe ser < 3 segundos (métrica SCRUM)');
      expect(result.isRight(), true);
    });
    
    test('should handle 75 frames (maximum) within performance limits', () async {
      // Arrange
      final useCase = EvaluateFrameQualityUseCase();
      final frames = List.generate(75, (index) => MockFrameData());
      
      // Act
      final stopwatch = Stopwatch()..start();
      final results = await Future.wait(
        frames.map((frame) => useCase(frameData: frame))
      );
      stopwatch.stop();
      
      // Assert
      expect(stopwatch.elapsedMilliseconds, lessThan(10000),
        reason: '75 fotogramas deben procesarse en < 10 segundos');
      expect(results.every((result) => result.isRight()), true);
    });
  });
}
```

### 5.2 Tests de Carga (Python)

```python
# tests/performance/test_api_performance.py
import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestAPIPerformance:
    def test_capture_session_creation_under_3_seconds(self):
        """Test creación de sesión de captura < 3 segundos"""
        # Arrange
        request_data = {
            "animal_id": "test_animal_001",
            "breed_type": "brahman"
        }
        
        # Act
        start_time = time.time()
        response = client.post("/capture-sessions/start", json=request_data)
        end_time = time.time()
        
        # Assert
        processing_time = end_time - start_time
        assert processing_time < 3.0, f"Procesamiento {processing_time}s debe ser < 3s"
        assert response.status_code == 200
    
    def test_senasag_report_generation_performance(self):
        """Test generación de reporte SENASAG con rendimiento aceptable"""
        # Arrange
        request_data = {
            "period_start": "2024-01-01T00:00:00Z",
            "period_end": "2024-01-31T23:59:59Z",
            "report_type": "Inventario"
        }
        
        # Act
        start_time = time.time()
        response = client.post("/senasag/generate-report", json=request_data)
        end_time = time.time()
        
        # Assert
        processing_time = end_time - start_time
        assert processing_time < 10.0, f"Generación de reporte {processing_time}s debe ser < 10s"
        assert response.status_code == 200
```

## 6. Configuración de Testing

### 6.1 Configuración Flutter (pubspec.yaml)

```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  integration_test:
    sdk: flutter
  mockito: ^5.4.2
  build_runner: ^2.4.7
  
  # Testing específico del dominio
  test: ^1.24.0
  bloc_test: ^9.1.5
  golden_toolkit: ^0.15.0
  
flutter:
  test:
    # Configuración para tests de las 7 razas
    test_directories:
      - test/
      - test/features/
      - test/core/
      - test/integration/
      - test/performance/
```

### 6.2 Configuración Python (pytest.ini)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=70
    --verbose
    --tb=short

# Configuración específica del proyecto
markers =
    critical: Tests críticos (100% cobertura obligatoria)
    breeds: Tests de las 7 razas específicas
    regulatory: Tests de integración normativa
    performance: Tests de rendimiento
    integration: Tests de integración

# Filtros para tests específicos
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

### 6.3 Scripts de Testing

```bash
#!/bin/bash
# scripts/run_tests.sh

echo "🧪 Ejecutando tests del Sistema de Estimación de Peso Bovino"

# Tests Flutter
echo "📱 Ejecutando tests Flutter..."
flutter test --coverage
flutter test integration_test/ --coverage

# Tests Python
echo "🐍 Ejecutando tests Python..."
pytest tests/ --cov=app --cov-report=html

# Tests críticos (100% cobertura obligatoria)
echo "🎯 Ejecutando tests críticos..."
pytest tests/ -m critical --cov=app --cov-fail-under=100

# Tests de las 7 razas específicas
echo "🐄 Ejecutando tests de razas bovinas..."
pytest tests/ -m breeds --cov=app

# Tests de integración normativa
echo "📋 Ejecutando tests normativos..."
pytest tests/ -m regulatory --cov=app

# Tests de rendimiento
echo "⚡ Ejecutando tests de rendimiento..."
pytest tests/ -m performance

echo "✅ Tests completados"
```
