# Estándares de Codificación Flutter

Sistema de Estimación de Peso Bovino - Hacienda Gamelera

## 1. Convenciones de Naming

### 1.1 Idioma y Contexto

- **Código**: Inglés estricto (variables, funciones, clases)
- **UI/Strings**: Español para textos visibles al usuario
- **Comentarios**: Español para facilitar mantenimiento local

### 1.2 Naming Específico del Dominio

#### Razas Bovinas (7 razas específicas)

```dart
// ✅ CORRECTO: Enum con las 7 razas exactas del proyecto
enum BreedType {
  brahman,
  nelore,
  angus,
  cebuinas,    // Bos indicus
  criollo,     // Bos taurus
  pardoSuizo,
  jersey
}

// ✅ CORRECTO: Clase de modelo
class Breed {
  final String id;
  final BreedType type;
  final String scientificName; // "Bos indicus" o "Bos taurus"
  final String modelVersion;
  final Map<AgeCategory, WeightRange> weightRanges;
  final double growthRateAvg;
  final List<String> characteristics;
  final bool isActive;
}

// ❌ INCORRECTO: Nombres genéricos o razas no del proyecto
enum BreedType {
  breed1, breed2  // ❌ Muy genérico
}
enum BreedType {
  holstein, hereford  // ❌ Razas no presentes en Hacienda Gamelera
}
```

#### Categorías de Edad (4 categorías específicas)

```dart
// ✅ CORRECTO: Enum con las 4 categorías del proyecto
enum AgeCategory {
  terneros,              // <8 meses
  vaquillonasTorillos,   // 6-18 meses
  vaquillonasToretes,    // 19-30 meses
  vacasToros             // >30 meses
}

// ✅ CORRECTO: Clase con rangos específicos
class AgeCategoryRange {
  final AgeCategory category;
  final int minMonths;
  final int maxMonths;
  
  const AgeCategoryRange({
    required this.category,
    required this.minMonths,
    required this.maxMonths,
  });
  
  static const List<AgeCategoryRange> ranges = [
    AgeCategoryRange(category: AgeCategory.terneros, minMonths: 0, maxMonths: 7),
    AgeCategoryRange(category: AgeCategory.vaquillonasTorillos, minMonths: 6, maxMonths: 18),
    AgeCategoryRange(category: AgeCategory.vaquillonasToretes, minMonths: 19, maxMonths: 30),
    AgeCategoryRange(category: AgeCategory.vacasToros, minMonths: 31, maxMonths: 999),
  ];
}

// ❌ INCORRECTO: Categorías genéricas
enum AgeCategory {
  young, adult  // ❌ No refleja categorías reales del proyecto
}
```

#### Captura Continua (especificaciones técnicas)

```dart
// ✅ CORRECTO: Constantes con valores específicos del proyecto
class CaptureConstants {
  static const int framesPerSecond = 12;           // 10-15 FPS
  static const Duration captureDuration = 
    Duration(seconds: 4);                          // 3-5 segundos
  static const int totalFramesMin = 30;            // Mínimo esperado
  static const int totalFramesMax = 75;            // Máximo esperado
  
  // Umbrales de calidad (valores del ADR-010)
  static const double minSharpness = 0.7;
  static const double minBrightness = 0.4;
  static const double maxBrightness = 0.8;
  static const double minContrast = 0.5;
  static const double minSilhouetteVisibility = 0.8;
  static const double minAngleScore = 0.6;
  static const double minOverallScore = 0.65;
  
  // Pesos para score global (ADR-010)
  static const double silhouetteWeight = 0.40;
  static const double sharpnessWeight = 0.30;
  static const double brightnessWeight = 0.20;
  static const double angleWeight = 0.10;
}

// ❌ INCORRECTO: Valores mágicos o genéricos
const fps = 30;  // ❌ No es el valor del proyecto
const duration = 10;  // ❌ No es el valor del proyecto
```

#### Entidades Regulatorias Bolivianas

```dart
// ✅ CORRECTO: Naming alineado con normativa
class SENASAGReport {
  final String reportId;
  final ReportType type;  // Inventario/Movilización/Sanitario
  final DateTime periodStart;
  final DateTime periodEnd;
  final int totalAnimals;
  final String pdfUrl;
  final String csvUrl;
  final ReportStatus status;
}

class GMA {  // Guía de Movimiento Animal
  final String gmaNumber;
  final List<String> animalIds;
  final String originFarmId;
  final String destination;
  final String granPaititiId;  // Sistema gubernamental
  final REGENSACompliance compliance;
  final GMAStatus status;
}

class REGENSACompliance {
  final bool chapter3_10Compliant;  // Centros de concentración
  final bool chapter7_1Compliant;   // Requisitos sanitarios
  final List<String> missingRequirements;
  final DateTime validatedAt;
}

// ❌ INCORRECTO: Nombres genéricos sin contexto boliviano
class Report { }  // ❌ Muy genérico
class MovementGuide { }  // ❌ Traducción incorrecta, debe ser GMA
```

#### Métricas del Sistema

```dart
// ✅ CORRECTO: Constantes de métricas del SCRUM
class SystemMetrics {
  // Métricas de precisión (documento 12 - SCRUM)
  static const double minPrecision = 0.95;          // ≥95%
  static const double minR2 = 0.95;                 // R² ≥ 0.95
  static const double maxErrorKg = 5.0;             // <5 kg
  static const double maxProcessingTimeMs = 3000;   // <3 segundos
  
  // Validación en campo
  static const int minAnimalsValidation = 50;
  
  // Mejora vs método anterior (Fórmula Schaeffer)
  static const double schaefferErrorMin = 5.0;
  static const double schaefferErrorMax = 20.0;
  
  // Métricas de tiempo
  static const Duration maxTimeFor20Animals = Duration(hours: 2);
  static const Duration currentTimeFor20Animals = Duration(days: 3);
}

/// Constantes de tiempo del proyecto (Hacienda Gamelera)
class ProjectTimeMetrics {
  // Tiempo actual (método tradicional con básculas y cinta bovinométrica)
  static const Duration currentTimeFor20Animals = Duration(days: 3);
  static const Duration currentCalibrationTime = Duration(minutes: 45);
  static const Duration currentCoordinationTime = Duration(hours: 2);
  static const Duration currentPerAnimalTime = Duration(minutes: 9); // 3 días / 20 animales
  
  // Tiempo objetivo (nuevo sistema con IA)
  static const Duration targetTimeFor20Animals = Duration(hours: 2);
  static const Duration targetPerAnimalTime = Duration(minutes: 6); // 2 horas / 20 animales
  
  // Mejora esperada
  static double get improvementPercentage => 
    (1 - (targetTimeFor20Animals.inMinutes / currentTimeFor20Animals.inMinutes)) * 100;
  // = 95.8% de mejora (de 4320 min a 120 min)
  
  // Fórmula Schaeffer que reemplaza el sistema
  static const String schaefferFormula = 'Peso (kg) = (PT² × LC) / 10838';
  static const String schaefferDescription = 'Perímetro Torácico (PT) y Longitud del Cuerpo (LC)';
}

/// Coordenadas GPS de Hacienda Gamelera
class HaciendaGameleraLocation {
  static const double latitude = -15.85950000;   // 15°51′34.2′′S
  static const double longitude = -60.79788889;  // 60°47′52.4′′W
  static const String address = 'San Ignacio de Velasco, Santa Cruz, Bolivia';
  static const double areaHectares = 48.5;
  static const int totalAnimals = 500;
  static const String owner = 'Bruno Brito Macedo';
}
```

#### Rangos de Peso por Raza y Edad

```dart
// ✅ COMPLETO: Rangos específicos para las 7 razas y 4 categorías
class WeightRange {
  final double min;
  final double max;
  
  const WeightRange({required this.min, required this.max});
  
  bool contains(double weight) => weight >= min && weight <= max;
}

class BreedWeightRanges {
  /// Rangos de peso específicos para cada raza y categoría de edad
  /// Basados en datos reales de la Hacienda Gamelera
  static const Map<BreedType, Map<AgeCategory, WeightRange>> ranges = {
    // Brahman (Bos indicus) - Raza más pesada
    BreedType.brahman: {
      AgeCategory.terneros: const WeightRange(min: 80, max: 180),
      AgeCategory.vaquillonasTorillos: const WeightRange(min: 180, max: 350),
      AgeCategory.vaquillonasToretes: const WeightRange(min: 300, max: 500),
      AgeCategory.vacasToros: const WeightRange(min: 450, max: 900),
    },
    
    // Nelore (Bos indicus) - Similar a Brahman
    BreedType.nelore: {
      AgeCategory.terneros: const WeightRange(min: 75, max: 170),
      AgeCategory.vaquillonasTorillos: const WeightRange(min: 170, max: 330),
      AgeCategory.vaquillonasToretes: const WeightRange(min: 280, max: 480),
      AgeCategory.vacasToros: const WeightRange(min: 400, max: 850),
    },
    
    // Angus (Bos taurus) - Raza europea mediana
    BreedType.angus: {
      AgeCategory.terneros: const WeightRange(min: 70, max: 160),
      AgeCategory.vaquillonasTorillos: const WeightRange(min: 160, max: 320),
      AgeCategory.vaquillonasToretes: const WeightRange(min: 280, max: 450),
      AgeCategory.vacasToros: const WeightRange(min: 400, max: 750),
    },
    
    // Cebuinas (Bos indicus) - Raza cebuina mediana
    BreedType.cebuinas: {
      AgeCategory.terneros: const WeightRange(min: 75, max: 165),
      AgeCategory.vaquillonasTorillos: const WeightRange(min: 165, max: 325),
      AgeCategory.vaquillonasToretes: const WeightRange(min: 275, max: 470),
      AgeCategory.vacasToros: const WeightRange(min: 380, max: 800),
    },
    
    // Criollo (Bos taurus) - Raza local adaptada
    BreedType.criollo: {
      AgeCategory.terneros: const WeightRange(min: 65, max: 150),
      AgeCategory.vaquillonasTorillos: const WeightRange(min: 150, max: 300),
      AgeCategory.vaquillonasToretes: const WeightRange(min: 250, max: 420),
      AgeCategory.vacasToros: const WeightRange(min: 350, max: 700),
    },
    
    // Pardo Suizo (Bos taurus) - Raza lechera grande
    BreedType.pardoSuizo: {
      AgeCategory.terneros: const WeightRange(min: 80, max: 180),
      AgeCategory.vaquillonasTorillos: const WeightRange(min: 180, max: 360),
      AgeCategory.vaquillonasToretes: const WeightRange(min: 320, max: 520),
      AgeCategory.vacasToros: const WeightRange(min: 450, max: 850),
    },
    
    // Jersey (Bos taurus) - Raza lechera pequeña
    BreedType.jersey: {
      AgeCategory.terneros: const WeightRange(min: 60, max: 140),
      AgeCategory.vaquillonasTorillos: const WeightRange(min: 140, max: 280),
      AgeCategory.vaquillonasToretes: const WeightRange(min: 240, max: 400),
      AgeCategory.vacasToros: const WeightRange(min: 320, max: 600),
    },
  };
  
  /// Obtiene rango de peso para una raza y categoría específica
  static WeightRange? getRange(BreedType breed, AgeCategory category) {
    return ranges[breed]?[category];
  }
  
  /// Valida si un peso está dentro del rango esperado
  static bool isValidWeight({
    required double weight,
    required BreedType breedType,
    required AgeCategory ageCategory,
  }) {
    final range = getRange(breedType, ageCategory);
    return range?.contains(weight) ?? false;
  }
  
  /// Obtiene el peso promedio para una raza y categoría
  static double getAverageWeight(BreedType breed, AgeCategory category) {
    final range = getRange(breed, category);
    if (range == null) return 0.0;
    return (range.min + range.max) / 2;
  }
}

/// Validador de categorías de edad con ejemplos concretos
class AgeCategoryValidator {
  /// Valida y calcula categoría de edad según fecha de nacimiento
  /// 
  /// Ejemplos concretos:
  /// - Animal nacido hace 6 meses → Terneros (<8 meses)
  /// - Animal nacido hace 12 meses → VaquillonasTorillos (6-18 meses)
  /// - Animal nacido hace 24 meses → VaquillonasToretes (19-30 meses)
  /// - Animal nacido hace 36 meses → VacasToros (>30 meses)
  static AgeCategory calculateCategory(DateTime birthDate) {
    final ageMonths = _calculateAgeInMonths(birthDate);
    
    if (ageMonths < 8) {
      return AgeCategory.terneros;
    } else if (ageMonths >= 6 && ageMonths <= 18) {
      return AgeCategory.vaquillonasTorillos;
    } else if (ageMonths >= 19 && ageMonths <= 30) {
      return AgeCategory.vaquillonasToretes;
    } else {
      return AgeCategory.vacasToros;
    }
  }
  
  /// Calcula edad en meses desde fecha de nacimiento
  static int _calculateAgeInMonths(DateTime birthDate) {
    final now = DateTime.now();
    final years = now.year - birthDate.year;
    final months = now.month - birthDate.month;
    return years * 12 + months;
  }
  
  /// Valida que la fecha de nacimiento sea válida
  static bool isValidBirthDate(DateTime birthDate) {
    final now = DateTime.now();
    
    // No puede ser fecha futura
    if (birthDate.isAfter(now)) return false;
    
    // No puede ser muy antigua (más de 20 años)
    final maxAge = DateTime(now.year - 20, now.month, now.day);
    if (birthDate.isBefore(maxAge)) return false;
    
    return true;
  }
  
  /// Ejemplos de validación para testing
  static Map<String, AgeCategory> getValidationExamples() {
    final now = DateTime.now();
    return {
      // Terneros (<8 meses)
      'Ternero de 6 meses': calculateCategory(
        DateTime(now.year, now.month - 6, now.day)
      ),
      'Ternero de 7 meses': calculateCategory(
        DateTime(now.year, now.month - 7, now.day)
      ),
      
      // Vaquillonas/Torillos (6-18 meses)
      'Vaquillona de 12 meses': calculateCategory(
        DateTime(now.year - 1, now.month, now.day)
      ),
      'Torillo de 18 meses': calculateCategory(
        DateTime(now.year - 1, now.month - 6, now.day)
      ),
      
      // Vaquillonas/Toretes (19-30 meses)
      'Vaquillona de 24 meses': calculateCategory(
        DateTime(now.year - 2, now.month, now.day)
      ),
      'Torete de 30 meses': calculateCategory(
        DateTime(now.year - 2, now.month - 6, now.day)
      ),
      
      // Vacas/Toros (>30 meses)
      'Vaca de 36 meses': calculateCategory(
        DateTime(now.year - 3, now.month, now.day)
      ),
      'Toro de 48 meses': calculateCategory(
        DateTime(now.year - 4, now.month, now.day)
      ),
    };
  }
}
```

### 1.3 Naming de Clases y Archivos

#### Estructura de Features (5 áreas funcionales)

```text
lib/
├── features/
│   ├── data_management/           # Área 1: Gestión de Datos
│   │   ├── presentation/
│   │   │   ├── screens/
│   │   │   │   ├── camera_screen.dart
│   │   │   │   ├── frame_evaluation_screen.dart
│   │   │   ├── widgets/
│   │   │   │   ├── breed_selector_widget.dart
│   │   │   │   ├── frame_quality_indicator.dart
│   │   │   │   ├── capture_progress_widget.dart
│   │   │   ├── providers/
│   │   │   │   ├── camera_provider.dart
│   │   │   │   ├── frame_evaluation_provider.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   ├── capture_session.dart
│   │   │   │   ├── frame_quality.dart
│   │   │   ├── usecases/
│   │   │   │   ├── start_continuous_capture_usecase.dart
│   │   │   │   ├── evaluate_frame_quality_usecase.dart
│   │   │   │   ├── select_best_frame_usecase.dart
│   │   │   │   ├── process_by_breed_usecase.dart
│   │   ├── data/
│   │   │   ├── models/
│   │   │   │   ├── capture_session_model.dart
│   │   │   ├── datasources/
│   │   │   │   ├── local_capture_session_datasource.dart
│   │   │   ├── repositories/
│   │   │   │   ├── capture_session_repository_impl.dart
│   │
│   ├── analytics_reports/          # Área 2: Análisis y Reportes
│   │   ├── presentation/
│   │   │   ├── screens/
│   │   │   │   ├── report_screen.dart
│   │   │   │   ├── weight_evolution_screen.dart
│   │   │   │   ├── breed_comparison_screen.dart
│   │   │   ├── widgets/
│   │   │   │   ├── weight_chart_widget.dart
│   │   │   │   ├── breed_performance_card.dart
│   │   ├── domain/
│   │   │   ├── usecases/
│   │   │   │   ├── generate_weight_evolution_chart_usecase.dart
│   │   │   │   ├── compare_animal_performance_usecase.dart
│   │   │   │   ├── export_senasag_report_usecase.dart
│   │
│   ├── monitoring/                 # Área 3: Monitoreo y Planificación
│   │   ├── presentation/
│   │   │   ├── screens/
│   │   │   │   ├── alert_screen.dart
│   │   │   │   ├── calendar_screen.dart
│   │   │   ├── widgets/
│   │   │   │   ├── alert_card_widget.dart
│   │   │   │   ├── asocebu_schedule_widget.dart
│   │   ├── domain/
│   │   │   ├── usecases/
│   │   │   │   ├── create_custom_alert_usecase.dart
│   │   │   │   ├── schedule_massive_capture_usecase.dart
│   │   │   │   ├── generate_gma_usecase.dart
│   │
│   ├── user_features/              # Área 4: Funcionalidades Usuario
│   │   ├── presentation/
│   │   │   ├── screens/
│   │   │   │   ├── search_screen.dart
│   │   │   │   ├── list_management_screen.dart
│   │   │   │   ├── settings_screen.dart
│   │   │   ├── widgets/
│   │   │   │   ├── breed_filter_widget.dart
│   │   │   │   ├── age_category_filter_widget.dart
│   │   ├── domain/
│   │   │   ├── usecases/
│   │   │   │   ├── search_animals_by_criteria_usecase.dart
│   │   │   │   ├── create_custom_list_usecase.dart
│   │
│   └── operations/                 # Área 5: Operación y Respaldos
│       ├── presentation/
│       │   ├── widgets/
│       │   │   ├── sync_indicator_widget.dart
│       │   │   ├── gran_paititi_sync_widget.dart
│       ├── domain/
│       │   ├── usecases/
│       │   │   ├── sync_data_usecase.dart
│       │   │   ├── resolve_conflicts_usecase.dart
│       │   │   ├── sync_gran_paititi_usecase.dart
│
├── core/
│   ├── constants/
│   │   ├── breeds.dart              # Constantes de las 7 razas
│   │   ├── age_categories.dart      # Constantes de 4 categorías
│   │   ├── capture_constants.dart   # FPS, duración, umbrales
│   │   ├── metrics.dart             # Métricas del sistema
│   │   ├── regulatory.dart          # SENASAG, REGENSA, ASOCEBU
```

### 1.4 Naming de Variables y Funciones

```dart
// ✅ CORRECTO: Variables descriptivas del dominio
final BreedType selectedBreed = BreedType.brahman;
final AgeCategory animalCategory = AgeCategory.terneros;
final double frameSharpness = 0.85;
final CaptureSession currentSession;
final GMA movementGuide;
final SENASAGReport inventoryReport;

// Funciones de captura continua
Future<CaptureSession> startContinuousCapture({
  required int framesPerSecond,
  required Duration duration,
});

Future<FrameQuality> evaluateFrameQuality({
  required Uint8List frameData,
  required int frameIndex,
});

Future<int> selectBestFrame({
  required List<FrameQuality> evaluatedFrames,
});

// Funciones de integración normativa
Future<SENASAGReport> generateSENASAGReport({
  required DateTime periodStart,
  required DateTime periodEnd,
  required ReportType type,
});

Future<GMA> createGMA({
  required List<String> animalIds,
  required String originFarmId,
  required String destination,
});

Future<bool> validateREGENSACompliance({
  required String farmId,
});

// ❌ INCORRECTO: Nombres genéricos o ambiguos
final type = 1;  // ❌ ¿Tipo de qué?
final data = getStuff();  // ❌ Muy genérico
Future<void> process() { }  // ❌ ¿Procesar qué?
```

## 2. Estructura de Archivos por Feature

### 2.1 Patrón de Organización (Clean Architecture)

Cada feature DEBE seguir la estructura de 3 capas:

```text
feature_name/
├── presentation/     # UI, Widgets, Providers
├── domain/          # Entities, Use Cases, Repository Interfaces
└── data/            # Models, Data Sources, Repository Implementations
```

### 2.2 Feature Completo - Ejemplo: data_management

```dart
// lib/features/data_management/domain/entities/capture_session.dart
class CaptureSession {
  final String id;
  final String animalId;
  final DateTime startTime;
  final DateTime? endTime;
  final int totalFrames;
  final int framesEvaluated;
  final int framesRejected;
  final String? selectedFrameId;
  final double averageQualityScore;
  final Map<String, int> rejectionReasons;
  
  const CaptureSession({
    required this.id,
    required this.animalId,
    required this.startTime,
    this.endTime,
    required this.totalFrames,
    required this.framesEvaluated,
    required this.framesRejected,
    this.selectedFrameId,
    required this.averageQualityScore,
    required this.rejectionReasons,
  });
}

// lib/features/data_management/domain/usecases/start_continuous_capture_usecase.dart
class StartContinuousCaptureUseCase {
  final CaptureSessionRepository repository;
  
  StartContinuousCaptureUseCase(this.repository);
  
  /// Inicia captura continua según especificaciones del proyecto:
  /// - 10-15 FPS
  /// - 3-5 segundos de duración
  /// - Evaluación en tiempo real de calidad
  Future<Either<Failure, CaptureSession>> call({
    required String animalId,
    required BreedType breedType,
  }) async {
    // Validar que la raza sea una de las 7 del proyecto
    if (!_isValidBreed(breedType)) {
      return Left(InvalidBreedFailure());
    }
    
    return await repository.startCapture(
      animalId: animalId,
      breedType: breedType,
      fps: CaptureConstants.framesPerSecond,
      duration: CaptureConstants.captureDuration,
    );
  }
  
  bool _isValidBreed(BreedType breed) {
    return BreedType.values.contains(breed);
  }
}
```

## 3. Provider Patterns

### 3.1 Provider para Captura Continua

```dart
// lib/features/data_management/presentation/providers/camera_provider.dart
class CameraProvider extends ChangeNotifier {
  final StartContinuousCaptureUseCase _startCaptureUseCase;
  final EvaluateFrameQualityUseCase _evaluateQualityUseCase;
  final SelectBestFrameUseCase _selectBestFrameUseCase;
  
  // Estado de captura
  CaptureSession? _currentSession;
  List<FrameQuality> _evaluatedFrames = [];
  FrameQuality? _selectedFrame;
  bool _isCapturing = false;
  
  // Progreso (para UI)
  int get capturedFrames => _evaluatedFrames.length;
  int get expectedFrames => CaptureConstants.totalFramesMax;
  double get captureProgress => capturedFrames / expectedFrames;
  
  /// Inicia captura continua de fotogramas
  /// Especificaciones: 10-15 FPS durante 3-5 segundos
  Future<void> startCapture({
    required String animalId,
    required BreedType breedType,
  }) async {
    _isCapturing = true;
    _evaluatedFrames.clear();
    notifyListeners();
    
    final result = await _startCaptureUseCase(
      animalId: animalId,
      breedType: breedType,
    );
    
    result.fold(
      (failure) {
        _isCapturing = false;
        notifyListeners();
        // Manejar error
      },
      (session) {
        _currentSession = session;
        _startFrameEvaluation();
      },
    );
  }
  
  /// Evalúa cada fotograma en tiempo real
  /// Criterios: nitidez>0.7, brillo 0.4-0.8, silueta>0.8, ángulo>0.6
  void _startFrameEvaluation() {
    // Evaluación en tiempo real durante la captura
  }
}
```

### 3.2 Provider para Integración SENASAG/REGENSA

```dart
// lib/features/monitoring/presentation/providers/regulatory_provider.dart
class RegulatoryProvider extends ChangeNotifier {
  final GenerateSENASAGReportUseCase _generateSENASAGUseCase;
  final CreateGMAUseCase _createGMAUseCase;
  final ValidateREGENSAComplianceUseCase _validateComplianceUseCase;
  
  SENASAGReport? _currentReport;
  GMA? _currentGMA;
  REGENSACompliance? _compliance;
  
  /// Genera reporte para SENASAG
  Future<void> generateSENASAGReport({
    required DateTime periodStart,
    required DateTime periodEnd,
    required ReportType type,
  }) async {
    final result = await _generateSENASAGUseCase(
      periodStart: periodStart,
      periodEnd: periodEnd,
      type: type,
    );
    
    result.fold(
      (failure) => /* manejar error */,
      (report) {
        _currentReport = report;
        notifyListeners();
      },
    );
  }
  
  /// Crea Guía de Movimiento Animal (GMA)
  /// Valida cumplimiento de REGENSA capítulos 3.10 y 7.1
  Future<void> createGMA({
    required List<String> animalIds,
    required String destination,
  }) async {
    // Primero validar cumplimiento REGENSA
    final complianceResult = await _validateComplianceUseCase();
    
    complianceResult.fold(
      (failure) => /* manejar error */,
      (compliance) async {
        if (!compliance.isCompliant) {
          // Mostrar requisitos faltantes
          return;
        }
        
        // Crear GMA
        final gmaResult = await _createGMAUseCase(
          animalIds: animalIds,
          destination: destination,
        );
        
        gmaResult.fold(
          (failure) => /* manejar error */,
          (gma) {
            _currentGMA = gma;
            notifyListeners();
          },
        );
      },
    );
  }
}
```

## 4. Organización de Widgets (Atomic Design)

### 4.1 Jerarquía Atomic Design

```text
lib/core/ui/
├── atoms/                    # Componentes básicos
│   ├── buttons/
│   │   ├── primary_button.dart
│   │   ├── secondary_button.dart
│   │   ├── capture_button.dart       # Botón específico de captura
│   ├── inputs/
│   │   ├── text_field.dart
│   │   ├── breed_dropdown.dart       # Dropdown con 7 razas
│   │   ├── age_category_selector.dart # Selector de 4 categorías
│   ├── indicators/
│   │   ├── loading_indicator.dart
│   │   ├── quality_score_indicator.dart  # Indicador de score 0-1
│   │   ├── sync_status_indicator.dart
│
├── molecules/                # Combinaciones de átomos
│   ├── cards/
│   │   ├── animal_card.dart
│   │   ├── breed_info_card.dart      # Información de raza específica
│   │   ├── capture_session_card.dart
│   ├── forms/
│   │   ├── animal_registration_form.dart
│   │   ├── gma_form.dart             # Formulario GMA
│   ├── lists/
│   │   ├── animal_list_item.dart
│   │   ├── frame_quality_list_item.dart
│
├── organisms/               # Secciones complejas
│   ├── headers/
│   │   ├── app_header.dart
│   │   ├── capture_header.dart       # Header con indicadores de captura
│   ├── sections/
│   │   ├── breed_statistics_section.dart  # Estadísticas por las 7 razas
│   │   ├── weight_evolution_section.dart
│   │   ├── regulatory_compliance_section.dart  # SENASAG/REGENSA
│
├── templates/               # Layouts de página
│   ├── main_layout.dart
│   ├── capture_layout.dart
│   ├── report_layout.dart
│
└── pages/                   # Instancias específicas
    ├── home_page.dart
    ├── capture_page.dart
    ├── report_page.dart
```

### 4.2 Ejemplo de Atom - BreedDropdown

```dart
// lib/core/ui/atoms/inputs/breed_dropdown.dart
class BreedDropdown extends StatelessWidget {
  final BreedType? selectedBreed;
  final ValueChanged<BreedType?> onChanged;
  final bool enabled;
  
  const BreedDropdown({
    Key? key,
    required this.selectedBreed,
    required this.onChanged,
    this.enabled = true,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return DropdownButton<BreedType>(
      value: selectedBreed,
      hint: const Text('Seleccionar raza'),
      isExpanded: true,
      items: BreedType.values.map((breed) {
        return DropdownMenuItem(
          value: breed,
          child: Text(_getBreedDisplayName(breed)),
        );
      }).toList(),
      onChanged: enabled ? onChanged : null,
    );
  }
  
  /// Nombres de las 7 razas en español (para UI)
  String _getBreedDisplayName(BreedType breed) {
    switch (breed) {
      case BreedType.brahman:
        return 'Brahman';
      case BreedType.nelore:
        return 'Nelore';
      case BreedType.angus:
        return 'Angus';
      case BreedType.cebuinas:
        return 'Cebuinas (Bos indicus)';
      case BreedType.criollo:
        return 'Criollo (Bos taurus)';
      case BreedType.pardoSuizo:
        return 'Pardo Suizo';
      case BreedType.jersey:
        return 'Jersey';
    }
  }
}
```

## 5. Manejo de Errores

### 5.1 Jerarquía de Errores Específicos del Dominio

```dart
// lib/core/error/failures.dart
abstract class Failure {
  final String message;
  const Failure(this.message);
}

// Errores de captura
class CaptureFailure extends Failure {
  const CaptureFailure(super.message);
}

class InsufficientFramesFailure extends CaptureFailure {
  const InsufficientFramesFailure() 
    : super('Se capturaron menos de ${CaptureConstants.totalFramesMin} fotogramas');
}

class LowQualityFramesFailure extends CaptureFailure {
  const LowQualityFramesFailure() 
    : super('Ningún fotograma alcanzó el score mínimo de ${CaptureConstants.minOverallScore}');
}

// Errores de razas
class InvalidBreedFailure extends Failure {
  const InvalidBreedFailure() 
    : super('La raza debe ser una de las 7 soportadas: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey');
}

// Errores normativos
class REGENSAComplianceFailure extends Failure {
  final List<String> missingRequirements;
  
  const REGENSAComplianceFailure(this.missingRequirements) 
    : super('No cumple con REGENSA capítulos 3.10 y 7.1');
}

class SENASAGReportFailure extends Failure {
  const SENASAGReportFailure(super.message);
}

class GMACreationFailure extends Failure {
  const GMACreationFailure(super.message);
}

// Errores de precisión
class PrecisionBelowThresholdFailure extends Failure {
  final double actualPrecision;
  
  const PrecisionBelowThresholdFailure(this.actualPrecision) 
    : super('Precisión ${actualPrecision * 100}% menor al mínimo ${SystemMetrics.minPrecision * 100}%');
}
```

## 6. Testing Requirements

### 6.1 Cobertura Mínima

- **Cobertura general**: 70% mínimo
- **Casos críticos**: 100% obligatorio
  - Evaluación de calidad de fotogramas
  - Selección del mejor fotograma
  - Validación de las 7 razas
  - Generación de GMA
  - Validación de cumplimiento REGENSA

### 6.2 Estructura de Tests

```text
test/
├── features/
│   ├── data_management/
│   │   ├── domain/
│   │   │   ├── usecases/
│   │   │   │   ├── start_continuous_capture_usecase_test.dart
│   │   │   │   ├── evaluate_frame_quality_usecase_test.dart
│   │   │   │   ├── select_best_frame_usecase_test.dart
│   │   ├── presentation/
│   │   │   ├── providers/
│   │   │   │   ├── camera_provider_test.dart
│   │
│   ├── monitoring/
│   │   ├── domain/
│   │   │   ├── usecases/
│   │   │   │   ├── generate_senasag_report_usecase_test.dart
│   │   │   │   ├── create_gma_usecase_test.dart
│   │   │   │   ├── validate_regensa_compliance_usecase_test.dart
│
├── core/
│   ├── utils/
│   │   ├── breed_validator_test.dart       # Validar 7 razas
│   │   ├── age_category_calculator_test.dart # Calcular categoría de edad
│   │   ├── frame_quality_calculator_test.dart # Calcular scores
```

### 6.3 Ejemplo de Test - Validación de Razas

```dart
// test/core/utils/breed_validator_test.dart
void main() {
  group('BreedValidator', () {
    test('should validate all 7 breeds from Hacienda Gamelera', () {
      // Arrange
      final validator = BreedValidator();
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
          reason: '${breed.toString()} debe ser válida');
      }
    });
    
    test('should return breed count of exactly 7', () {
      expect(BreedType.values.length, 7,
        reason: 'Deben ser exactamente las 7 razas de Hacienda Gamelera');
    });
  });
}
```

### 6.4 Ejemplo de Test - Evaluación de Fotogramas

```dart
// test/features/data_management/domain/usecases/evaluate_frame_quality_usecase_test.dart
void main() {
  late EvaluateFrameQualityUseCase useCase;
  
  setUp(() {
    useCase = EvaluateFrameQualityUseCase();
  });
  
  group('EvaluateFrameQualityUseCase', () {
    test('should accept frame with all quality metrics above threshold', () async {
      // Arrange
      final frameData = MockFrameData();
      when(frameData.sharpness).thenReturn(0.85);  // > 0.7
      when(frameData.brightness).thenReturn(0.6);   // 0.4-0.8
      when(frameData.contrast).thenReturn(0.7);     // > 0.5
      when(frameData.silhouetteVisibility).thenReturn(0.9);  // > 0.8
      when(frameData.angleScore).thenReturn(0.75);  // > 0.6
      
      // Act
      final result = await useCase(frameData: frameData);
      
      // Assert
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Should not fail'),
        (frameQuality) {
          expect(frameQuality.overallScore, greaterThan(CaptureConstants.minOverallScore));
          expect(frameQuality.isAcceptable, true);
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
        },
      );
    });
    
    test('should calculate weighted overall score correctly', () async {
      // Arrange: Valores específicos para verificar pesos
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
          expect(frameQuality.overallScore, closeTo(0.79, 0.01));
        },
      );
    });
  });
}
```

### 6.5 Tests de Integración Normativa

```dart
// test/features/monitoring/domain/usecases/validate_regensa_compliance_usecase_test.dart
void main() {
  group('ValidateREGENSAComplianceUseCase', () {
    test('should validate chapter 3.10 requirements (centros de concentración)', () async {
      // Arrange
      final useCase = ValidateREGENSAComplianceUseCase();
      final farmData = FarmData(
        hasAntislipRamps: true,
        corridorWidthMeters: 1.8,      // ≥ 1.6m
        spacePerAnimalM2: 2.5,         // ≥ 2m²
        hasDisinfectionSystem: true,
        hasQuarantineCorral: true,
        prohibitsPainInstruments: true,
      );
      
      // Act
      final result = await useCase(farmData: farmData);
      
      // Assert
      expect(result.isRight(), true);
      result.fold(
        (failure) => fail('Should not fail'),
        (compliance) {
          expect(compliance.chapter3_10Compliant, true);
        },
      );
    });
    
    test('should fail if corridor width < 1.6m', () async {
      // Arrange
      final farmData = FarmData(
        hasAntislipRamps: true,
        corridorWidthMeters: 1.4,      // < 1.6m ❌
        spacePerAnimalM2: 2.5,
        hasDisinfectionSystem: true,
        hasQuarantineCorral: true,
        prohibitsPainInstruments: true,
      );
      
      // Act
      final result = await useCase(farmData: farmData);
      
      // Assert
      result.fold(
        (failure) => fail('Should not fail'),
        (compliance) {
          expect(compliance.chapter3_10Compliant, false);
          expect(compliance.missingRequirements, contains('corredor_ancho'));
        },
      );
    });
  });
}
```

## 7. Strings y Localización

### 7.1 Archivo de Strings (Español)

```dart
// lib/core/constants/app_strings.dart
class AppStrings {
  // Pantallas
  static const String homeTitle = 'Hacienda Gamelera';
  static const String captureTitle = 'Captura de Peso';
  static const String reportsTitle = 'Reportes y Análisis';
  
  // Razas (UI en español)
  static const Map<BreedType, String> breedNames = {
    BreedType.brahman: 'Brahman',
    BreedType.nelore: 'Nelore',
    BreedType.angus: 'Angus',
    BreedType.cebuinas: 'Cebuinas (Bos indicus)',
    BreedType.criollo: 'Criollo (Bos taurus)',
    BreedType.pardoSuizo: 'Pardo Suizo',
    BreedType.jersey: 'Jersey',
  };
  
  // Categorías de edad (UI en español)
  static const Map<AgeCategory, String> ageCategoryNames = {
    AgeCategory.terneros: 'Terneros (< 8 meses)',
    AgeCategory.vaquillonasTorillos: 'Vaquillonas/Torillos (6-18 meses)',
    AgeCategory.vaquillonasToretes: 'Vaquillonas/Toretes (19-30 meses)',
    AgeCategory.vacasToros: 'Vacas/Toros (> 30 meses)',
  };
  
  // Captura
  static const String captureInProgress = 'Capturando fotogramas...';
  static const String evaluatingQuality = 'Evaluando calidad...';
  static const String selectingBestFrame = 'Seleccionando mejor fotograma...';
  static const String captureSuccess = 'Captura exitosa';
  static const String captureFailure = 'Error en captura';
  
  // Normativa
  static const String senasagReport = 'Reporte SENASAG';
  static const String gmaCreation = 'Crear Guía de Movimiento Animal (GMA)';
  static const String regensaCompliance = 'Cumplimiento REGENSA';
  static const String granPaititiSync = 'Sincronizar con Gran Paitití';
  static const String asocebuExport = 'Exportar para ASOCEBU';
  
  // ASOCEBU - Asociación de Criadores de Cebuinos
  static const String asocebuRegistration = 'Registro ASOCEBU';
  static const String asocebuCompetition = 'Competencia ASOCEBU';
  static const String asocebuCertification = 'Certificación de Peso';
  static const String asocebuPerformanceReport = 'Reporte de Rendimiento';
  
  // Métricas
  static const String precision = 'Precisión';
  static const String r2Score = 'R² (Coeficiente de Determinación)';
  static const String errorKg = 'Error Absoluto (kg)';
  static const String processingTime = 'Tiempo de Procesamiento';
}

/// Integración con ASOCEBU (Asociación de Criadores de Cebuinos)
class ASOCEBUIntegration {
  /// Genera reporte de rendimiento para competencias ASOCEBU
  static Future<ASOCEBUReport> generatePerformanceReport({
    required List<String> animalIds,
    required DateTime periodStart,
    required DateTime periodEnd,
  }) async {
    // Implementación para generar reporte específico de ASOCEBU
    // Incluye: historial de peso, crecimiento, categorías de competencia
  }
  
  /// Valida que un animal cumple requisitos para competencia ASOCEBU
  static bool validateCompetitionEligibility({
    required Animal animal,
    required String competitionCategory,
  }) {
    // Validaciones específicas de ASOCEBU:
    // - Raza debe ser una de las cebuinas (Brahman, Nelore, Cebuinas)
    // - Peso debe estar en rango de la categoría
    // - Animal debe estar registrado en ASOCEBU
    // - Historial de pesajes debe ser completo
    
    final cebuinoBreeds = [
      BreedType.brahman,
      BreedType.nelore,
      BreedType.cebuinas,
    ];
    
    if (!cebuinoBreeds.contains(animal.breedType)) {
      return false; // Solo razas cebuinas
    }
    
    if (!animal.asocebuRegistered) {
      return false; // Debe estar registrado
    }
    
    // Validar peso según categoría de competencia
    return _validateCompetitionWeight(animal, competitionCategory);
  }
  
  /// Exporta datos en formato requerido por ASOCEBU
  static Future<String> exportToASOCEBUFormat({
    required List<Animal> animals,
    required List<Weighing> weighings,
  }) async {
    // Formato específico de ASOCEBU (CSV/XML)
    // Incluye: ID ASOCEBU, peso certificado, fecha, categoría
  }
  
  static bool _validateCompetitionWeight(Animal animal, String category) {
    // Lógica específica de validación de peso por categoría
    return true; // Implementación específica
  }
}
```

## 8. Offline-First Patterns

### 8.1 Arquitectura de Sincronización

```dart
// lib/core/sync/sync_manager.dart
class SyncManager {
  final LocalDatabase _localDb;
  final RemoteAPI _remoteApi;
  final NetworkMonitor _networkMonitor;
  
  /// Cola de operaciones pendientes de sincronización
  /// Prioridad: Pesajes > Animales > Imágenes > Reportes
  final List<SyncOperation> _syncQueue = [];
  
  /// Estado de sincronización
  SyncStatus _status = SyncStatus.idle;
  DateTime? _lastSyncTime;
  
  /// Inicia sincronización automática cuando hay conexión
  Future<void> startAutoSync() async {
    _networkMonitor.onConnectivityChange.listen((isConnected) {
      if (isConnected && _syncQueue.isNotEmpty) {
        _executeSyncQueue();
      }
    });
  }
  
  /// Agrega operación a cola de sincronización
  void enqueueOperation(SyncOperation operation) {
    _syncQueue.add(operation);
    _syncQueue.sort((a, b) => b.priority.compareTo(a.priority));
    
    // Si hay conexión, sincronizar inmediatamente
    if (_networkMonitor.isConnected) {
      _executeSyncQueue();
    }
  }
  
  Future<void> _executeSyncQueue() async {
    if (_status == SyncStatus.syncing) return;
    
    _status = SyncStatus.syncing;
    
    while (_syncQueue.isNotEmpty) {
      final operation = _syncQueue.first;
      
      try {
        await _executeOperation(operation);
        _syncQueue.removeAt(0);
      } catch (e) {
        // Retry con backoff exponencial
        operation.incrementRetryCount();
        if (operation.retryCount > 3) {
          _syncQueue.removeAt(0); // Descartar después de 3 intentos
        }
        break; // Detener cola si falla
      }
    }
    
    _status = SyncStatus.idle;
    _lastSyncTime = DateTime.now();
  }
}

/// Tipos de operaciones con prioridad
enum SyncOperationType {
  createWeighing(priority: 5),    // Prioridad más alta
  updateWeighing(priority: 5),
  createAnimal(priority: 4),
  updateAnimal(priority: 4),
  uploadImage(priority: 3),
  createSENASAGReport(priority: 2),
  createGMA(priority: 2),
  syncGranPaititi(priority: 1);   // Prioridad más baja
  
  final int priority;
  const SyncOperationType({required this.priority});
}
```

### 8.2 Resolución de Conflictos (Last-Write-Wins)

```dart
// lib/core/sync/conflict_resolver.dart
class ConflictResolver {
  /// Resuelve conflictos usando estrategia Last-Write-Wins
  /// basada en timestamps
  Future<Either<Failure, T>> resolveConflict<T>({
    required T localData,
    required T remoteData,
    required DateTime localTimestamp,
    required DateTime remoteTimestamp,
  }) async {
    // Caso 1: Datos locales más recientes
    if (localTimestamp.isAfter(remoteTimestamp)) {
      return Right(localData);
    }
    
    // Caso 2: Datos remotos más recientes
    if (remoteTimestamp.isAfter(localTimestamp)) {
      return Right(remoteData);
    }
    
    // Caso 3: Mismos timestamps (raro), usar hash
    final localHash = _generateHash(localData);
    final remoteHash = _generateHash(remoteData);
    
    if (localHash == remoteHash) {
      return Right(localData); // Son idénticos
    }
    
    // Conflicto real, priorizar remoto
    return Right(remoteData);
  }
  
  /// Resuelve conflictos específicos de pesaje
  /// Crítico: El peso más reciente es el correcto
  Future<Either<Failure, Weighing>> resolveWeighingConflict({
    required Weighing localWeighing,
    required Weighing remoteWeighing,
  }) async {
    // Si los timestamps son muy cercanos (<10 segundos),
    // considerar que son el mismo pesaje
    final timeDiff = localWeighing.weighingDate
        .difference(remoteWeighing.weighingDate)
        .abs();
    
    if (timeDiff < const Duration(seconds: 10)) {
      // Usar el que tenga mejor confidence_score
      if (localWeighing.confidenceScore > remoteWeighing.confidenceScore) {
        return Right(localWeighing);
      }
      return Right(remoteWeighing);
    }
    
    // Timestamps diferentes, usar el más reciente
    return resolveConflict(
      localData: localWeighing,
      remoteData: remoteWeighing,
      localTimestamp: localWeighing.weighingDate,
      remoteTimestamp: remoteWeighing.weighingDate,
    );
  }
}
```

### 8.3 SQLite Schema para Offline-First

```dart
// lib/core/database/local_database.dart
class LocalDatabase {
  static const String _databaseName = 'hacienda_gamelera.db';
  static const int _databaseVersion = 1;
  
  /// Esquema de tablas locales
  static const String _createAnimalsTable = '''
    CREATE TABLE animals (
      id TEXT PRIMARY KEY,
      tag_number TEXT UNIQUE NOT NULL,
      name TEXT,
      breed_id TEXT NOT NULL,
      birth_date INTEGER NOT NULL,
      age_category_id TEXT NOT NULL,
      gender TEXT NOT NULL,
      status TEXT NOT NULL,
      farm_id TEXT NOT NULL,
      weight_goal REAL,
      asocebu_registered INTEGER DEFAULT 0,
      asocebu_id TEXT,
      created_at INTEGER NOT NULL,
      updated_at INTEGER NOT NULL,
      synced INTEGER DEFAULT 0,
      sync_timestamp INTEGER,
      FOREIGN KEY (breed_id) REFERENCES breeds (id),
      FOREIGN KEY (age_category_id) REFERENCES age_categories (id)
    );
  ''';
  
  static const String _createWeighingsTable = '''
    CREATE TABLE weighings (
      id TEXT PRIMARY KEY,
      animal_id TEXT NOT NULL,
      estimated_weight REAL NOT NULL,
      confidence_score REAL NOT NULL,
      weighing_date INTEGER NOT NULL,
      weighing_method TEXT NOT NULL,
      image_id TEXT,
      capture_session_id TEXT,
      breed_model_version TEXT,
      frames_evaluated INTEGER,
      selected_frame_index INTEGER,
      quality_score REAL,
      processing_time_ms INTEGER,
      was_offline INTEGER DEFAULT 1,
      synced_at INTEGER,
      created_by TEXT NOT NULL,
      created_at INTEGER NOT NULL,
      synced INTEGER DEFAULT 0,
      sync_timestamp INTEGER,
      FOREIGN KEY (animal_id) REFERENCES animals (id),
      FOREIGN KEY (capture_session_id) REFERENCES capture_sessions (id)
    );
  ''';
  
  static const String _createCaptureSessionsTable = '''
    CREATE TABLE capture_sessions (
      id TEXT PRIMARY KEY,
      animal_id TEXT NOT NULL,
      start_time INTEGER NOT NULL,
      end_time INTEGER,
      total_frames INTEGER NOT NULL,
      frames_evaluated INTEGER NOT NULL,
      frames_rejected INTEGER NOT NULL,
      selected_frame_id TEXT,
      average_quality_score REAL NOT NULL,
      rejection_reasons TEXT,  -- JSON map
      device_info TEXT,        -- JSON object
      created_by TEXT NOT NULL,
      created_at INTEGER NOT NULL,
      synced INTEGER DEFAULT 0,
      FOREIGN KEY (animal_id) REFERENCES animals (id)
    );
  ''';
  
  static const String _createBreedsTable = '''
    CREATE TABLE breeds (
      id TEXT PRIMARY KEY,
      name TEXT UNIQUE NOT NULL,  -- Enum: brahman, nelore, angus, cebuinas, criollo, pardoSuizo, jersey
      scientific_name TEXT NOT NULL,
      model_version TEXT NOT NULL,
      model_url TEXT NOT NULL,
      weight_ranges TEXT NOT NULL,  -- JSON object
      growth_rate_avg REAL NOT NULL,
      is_active INTEGER DEFAULT 1,
      created_at INTEGER NOT NULL
    );
  ''';
  
  static const String _createSyncQueueTable = '''
    CREATE TABLE sync_queue (
      id TEXT PRIMARY KEY,
      operation_type TEXT NOT NULL,
      entity_type TEXT NOT NULL,
      entity_id TEXT NOT NULL,
      priority INTEGER NOT NULL,
      retry_count INTEGER DEFAULT 0,
      payload TEXT NOT NULL,  -- JSON
      created_at INTEGER NOT NULL,
      last_retry_at INTEGER
    );
  ''';
  
  /// Inicializa base de datos con las 7 razas completas
  Future<void> _seedBreeds(Database db) async {
    final breeds = [
      // 1. Brahman (Bos indicus) - Raza más pesada
      _createBreedData(
        'brahman',
        'Bos indicus',
        modelVersion: '1.0.0',
        terneroMin: 80, terneroMax: 180,
        jovenMin: 180, jovenMax: 350,
        adultoMin: 450, adultoMax: 900,
        growthRate: 0.8,
        characteristics: ['Resistente al calor', 'Joroba prominente', 'Orejas largas'],
      ),
      
      // 2. Nelore (Bos indicus) - Similar a Brahman
      _createBreedData(
        'nelore',
        'Bos indicus',
        modelVersion: '1.0.0',
        terneroMin: 75, terneroMax: 170,
        jovenMin: 170, jovenMax: 330,
        adultoMin: 400, adultoMax: 850,
        growthRate: 0.75,
        characteristics: ['Adaptado al trópico', 'Pelaje blanco', 'Cuernos largos'],
      ),
      
      // 3. Angus (Bos taurus) - Raza europea mediana
      _createBreedData(
        'angus',
        'Bos taurus',
        modelVersion: '1.0.0',
        terneroMin: 70, terneroMax: 160,
        jovenMin: 160, jovenMax: 320,
        adultoMin: 400, adultoMax: 750,
        growthRate: 0.85,
        characteristics: ['Pelaje negro', 'Sin cuernos', 'Carne de calidad'],
      ),
      
      // 4. Cebuinas (Bos indicus) - Raza cebuina mediana
      _createBreedData(
        'cebuinas',
        'Bos indicus',
        modelVersion: '1.0.0',
        terneroMin: 75, terneroMax: 165,
        jovenMin: 165, jovenMax: 325,
        adultoMin: 380, adultoMax: 800,
        growthRate: 0.78,
        characteristics: ['Resistente a parásitos', 'Pelaje variado', 'Tamaño mediano'],
      ),
      
      // 5. Criollo (Bos taurus) - Raza local adaptada
      _createBreedData(
        'criollo',
        'Bos taurus',
        modelVersion: '1.0.0',
        terneroMin: 65, terneroMax: 150,
        jovenMin: 150, jovenMax: 300,
        adultoMin: 350, adultoMax: 700,
        growthRate: 0.70,
        characteristics: ['Adaptado localmente', 'Resistente', 'Pelaje variado'],
      ),
      
      // 6. Pardo Suizo (Bos taurus) - Raza lechera grande
      _createBreedData(
        'pardo_suizo',
        'Bos taurus',
        modelVersion: '1.0.0',
        terneroMin: 80, terneroMax: 180,
        jovenMin: 180, jovenMax: 360,
        adultoMin: 450, adultoMax: 850,
        growthRate: 0.82,
        characteristics: ['Pelaje pardo', 'Doble propósito', 'Tamaño grande'],
      ),
      
      // 7. Jersey (Bos taurus) - Raza lechera pequeña
      _createBreedData(
        'jersey',
        'Bos taurus',
        modelVersion: '1.0.0',
        terneroMin: 60, terneroMax: 140,
        jovenMin: 140, jovenMax: 280,
        adultoMin: 320, adultoMax: 600,
        growthRate: 0.65,
        characteristics: ['Pelaje dorado', 'Leche rica', 'Tamaño pequeño'],
      ),
    ];
    
    for (final breed in breeds) {
      await db.insert('breeds', breed, 
        conflictAlgorithm: ConflictAlgorithm.ignore);
    }
  }
  
  /// Helper para crear datos de raza
  Map<String, dynamic> _createBreedData(
    String name,
    String scientificName, {
    required String modelVersion,
    required int terneroMin,
    required int terneroMax,
    required int jovenMin,
    required int jovenMax,
    required int adultoMin,
    required int adultoMax,
    required double growthRate,
    required List<String> characteristics,
  }) {
    return {
      'id': 'breed_$name',
      'name': name,
      'scientific_name': scientificName,
      'model_version': modelVersion,
      'model_url': 's3://models/$name-v$modelVersion.tflite',
      'weight_ranges': jsonEncode({
        'ternero': {'min': terneroMin, 'max': terneroMax},
        'joven': {'min': jovenMin, 'max': jovenMax},
        'adulto': {'min': adultoMin, 'max': adultoMax},
      }),
      'growth_rate_avg': growthRate,
      'characteristics': jsonEncode(characteristics),
      'is_active': 1,
      'created_at': DateTime.now().millisecondsSinceEpoch,
    };
  }
}
```

## 9. Integración TensorFlow Lite

### 9.1 Gestión de Modelos por Raza

```dart
// lib/core/ml/tflite_manager.dart
class TFLiteManager {
  static const String _modelsDir = 'models';
  final Map<BreedType, Interpreter?> _interpreters = {};
  
  /// Carga modelo específico para una raza
  Future<Either<Failure, Interpreter>> loadBreedModel(
    BreedType breedType,
  ) async {
    // Verificar si ya está cargado
    if (_interpreters[breedType] != null) {
      return Right(_interpreters[breedType]!);
    }
    
    try {
      // Verificar si existe versión actualizada en S3
      final latestVersion = await _checkModelVersion(breedType);
      
      // Cargar modelo local o descargar si no existe
      final modelPath = await _getModelPath(breedType, latestVersion);
      
      // Validar integridad del modelo (MD5 checksum)
      final isValid = await _validateModelIntegrity(modelPath, breedType);
      if (!isValid) {
        return Left(ModelIntegrityFailure(breedType));
      }
      
      // Cargar intérprete TFLite
      final interpreter = await Interpreter.fromAsset(modelPath);
      
      // Configurar opciones de rendimiento
      interpreter.allocateTensors();
      
      _interpreters[breedType] = interpreter;
      return Right(interpreter);
      
    } catch (e) {
      return Left(ModelLoadFailure(breedType, e.toString()));
    }
  }
  
  /// Ejecuta inferencia para estimar peso
  /// Entrada: Imagen procesada (224x224x3)
  /// Salida: Peso estimado (kg), confidence score
  Future<Either<Failure, WeightEstimation>> estimateWeight({
    required Uint8List imageData,
    required BreedType breedType,
    required AgeCategory ageCategory,
  }) async {
    // Cargar modelo de la raza específica
    final interpreterResult = await loadBreedModel(breedType);
    
    return interpreterResult.fold(
      (failure) => Left(failure),
      (interpreter) async {
        try {
          // Preprocesar imagen (normalización, resize)
          final processedImage = await _preprocessImage(imageData);
          
          // Preparar entrada: [1, 224, 224, 3]
          final input = [processedImage];
          
          // Preparar salida: [1, 2] (peso, confidence)
          final output = List.filled(1 * 2, 0.0).reshape([1, 2]);
          
          // Ejecutar inferencia
          final startTime = DateTime.now();
          interpreter.run(input, output);
          final processingTime = DateTime.now().difference(startTime);
          
          // Validar que procesamiento sea < 3 segundos
          if (processingTime.inMilliseconds > SystemMetrics.maxProcessingTimeMs) {
            return Left(ProcessingTimeTooSlowFailure(processingTime));
          }
          
          // Extraer resultados
          final estimatedWeight = output[0][0] as double;
          final confidenceScore = output[0][1] as double;
          
          // Validar precisión mínima (≥95%)
          if (confidenceScore < SystemMetrics.minPrecision) {
            return Left(PrecisionBelowThresholdFailure(confidenceScore));
          }
          
          // Validar que el peso esté en rango esperado para raza y edad
          final isValidWeight = _validateWeightRange(
            weight: estimatedWeight,
            breedType: breedType,
            ageCategory: ageCategory,
          );
          
          if (!isValidWeight) {
            return Left(WeightOutOfRangeFailure(
              estimatedWeight, breedType, ageCategory));
          }
          
          return Right(WeightEstimation(
            weight: estimatedWeight,
            confidence: confidenceScore,
            breedType: breedType,
            ageCategory: ageCategory,
            processingTime: processingTime,
          ));
          
        } catch (e) {
          return Left(InferenceFailure(e.toString()));
        }
      },
    );
  }
  
  /// Valida que el peso esté en rango esperado según raza y edad
  bool _validateWeightRange({
    required double weight,
    required BreedType breedType,
    required AgeCategory ageCategory,
  }) {
    // Usar la nueva clase BreedWeightRanges con rangos específicos
    return BreedWeightRanges.isValidWeight(
      weight: weight,
      breedType: breedType,
      ageCategory: ageCategory,
    );
  }
  
  /// Actualiza modelo desde S3 si hay versión nueva
  Future<void> updateModelIfNeeded(BreedType breedType) async {
    final manifest = await _fetchManifestFromS3();
    final currentVersion = await _getCurrentModelVersion(breedType);
    final latestVersion = manifest.models[breedType]?.version;
    
    if (latestVersion != null && latestVersion != currentVersion) {
      await _downloadModel(breedType, manifest.models[breedType]!);
    }
  }
}

/// Constantes de preprocesamiento de imagen
class ImagePreprocessingConstants {
  static const int inputWidth = 224;
  static const int inputHeight = 224;
  static const int inputChannels = 3;
  
  // Normalización (según entrenamiento del modelo)
  static const double meanR = 0.485;
  static const double meanG = 0.456;
  static const double meanB = 0.406;
  static const double stdR = 0.229;
  static const double stdG = 0.224;
  static const double stdB = 0.225;
}
```

### 9.2 Procesamiento de Imagen para TFLite

```dart
// lib/core/ml/image_processor.dart
class ImageProcessor {
  /// Preprocesa imagen para inferencia TFLite
  /// 1. Resize a 224x224
  /// 2. Normalización con mean/std específicos
  /// 3. Conversión a Float32
  Future<List<List<List<List<double>>>>> preprocessImage(
    Uint8List imageBytes,
  ) async {
    // Decodificar imagen
    final image = img.decodeImage(imageBytes);
    if (image == null) {
      throw ImageDecodingException();
    }
    
    // Resize a tamaño de entrada del modelo (224x224)
    final resized = img.copyResize(
      image,
      width: ImagePreprocessingConstants.inputWidth,
      height: ImagePreprocessingConstants.inputHeight,
      interpolation: img.Interpolation.cubic, // Mejor calidad
    );
    
    // Convertir a matriz normalizada [1, 224, 224, 3]
    final input = List.generate(
      1,
      (_) => List.generate(
        ImagePreprocessingConstants.inputHeight,
        (y) => List.generate(
          ImagePreprocessingConstants.inputWidth,
          (x) {
            final pixel = resized.getPixel(x, y);
            
            // Normalizar cada canal RGB
            final r = (pixel.r / 255.0 - ImagePreprocessingConstants.meanR) / 
                      ImagePreprocessingConstants.stdR;
            final g = (pixel.g / 255.0 - ImagePreprocessingConstants.meanG) / 
                      ImagePreprocessingConstants.stdG;
            final b = (pixel.b / 255.0 - ImagePreprocessingConstants.meanB) / 
                      ImagePreprocessingConstants.stdB;
            
            return [r, g, b];
          },
        ),
      ),
    );
    
    return input;
  }
  
  /// Extrae características visuales para evaluación de calidad
  Future<ImageFeatures> extractFeatures(Uint8List imageBytes) async {
    final image = img.decodeImage(imageBytes);
    if (image == null) {
      throw ImageDecodingException();
    }
    
    // Calcular nitidez (Laplacian variance)
    final sharpness = _calculateSharpness(image);
    
    // Calcular brillo promedio
    final brightness = _calculateBrightness(image);
    
    // Calcular contraste (desviación estándar de luminancia)
    final contrast = _calculateContrast(image);
    
    // Detectar silueta (edge detection)
    final silhouetteVisibility = await _detectSilhouette(image);
    
    return ImageFeatures(
      sharpness: sharpness,
      brightness: brightness,
      contrast: contrast,
      silhouetteVisibility: silhouetteVisibility,
    );
  }
  
  /// Calcula nitidez usando Laplacian variance
  double _calculateSharpness(img.Image image) {
    // Aplicar filtro Laplaciano
    final laplacian = img.convolution(
      image,
      filter: [
        [0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0],
      ],
    );
    
    // Calcular varianza
    double sum = 0;
    double sumSquared = 0;
    int count = 0;
    
    for (int y = 0; y < laplacian.height; y++) {
      for (int x = 0; x < laplacian.width; x++) {
        final pixel = laplacian.getPixel(x, y);
        final gray = (pixel.r + pixel.g + pixel.b) / 3;
        sum += gray;
        sumSquared += gray * gray;
        count++;
      }
    }
    
    final mean = sum / count;
    final variance = (sumSquared / count) - (mean * mean);
    
    // Normalizar a 0-1
    return (variance / 255).clamp(0.0, 1.0);
  }
  
  /// Calcula brillo promedio (0-1)
  double _calculateBrightness(img.Image image) {
    double sum = 0;
    int count = 0;
    
    for (int y = 0; y < image.height; y++) {
      for (int x = 0; x < image.width; x++) {
        final pixel = image.getPixel(x, y);
        // Luminancia percibida
        final luminance = (0.299 * pixel.r + 0.587 * pixel.g + 0.114 * pixel.b) / 255;
        sum += luminance;
        count++;
      }
    }
    
    return sum / count;
  }
  
  /// Calcula contraste (desviación estándar de luminancia)
  double _calculateContrast(img.Image image) {
    final brightness = _calculateBrightness(image);
    double sumSquaredDiff = 0;
    int count = 0;
    
    for (int y = 0; y < image.height; y++) {
      for (int x = 0; x < image.width; x++) {
        final pixel = image.getPixel(x, y);
        final luminance = (0.299 * pixel.r + 0.587 * pixel.g + 0.114 * pixel.b) / 255;
        sumSquaredDiff += (luminance - brightness) * (luminance - brightness);
        count++;
      }
    }
    
    final stdDev = sqrt(sumSquaredDiff / count);
    return stdDev.clamp(0.0, 1.0);
  }
}
```

## 10. Performance y Optimización

### 10.1 Optimización de Captura Continua

```dart
// lib/features/data_management/presentation/providers/optimized_camera_provider.dart
class OptimizedCameraProvider extends ChangeNotifier {
  // Caché de fotogramas evaluados para evitar re-evaluación
  final Map<int, FrameQuality> _frameCache = {};
  
  // Pool de workers para procesamiento paralelo
  final List<Worker> _workerPool = [];
  
  // Límite de frames en memoria (evitar OOM)
  static const int maxFramesInMemory = 50;
  
  /// Inicia captura con optimizaciones de performance
  Future<void> startOptimizedCapture({
    required String animalId,
    required BreedType breedType,
  }) async {
    // 1. Pre-cargar modelo TFLite antes de captura
    await _preloadModel(breedType);
    
    // 2. Inicializar pool de workers (isolates)
    await _initializeWorkerPool();
    
    // 3. Iniciar captura continua
    final stream = _cameraController.startImageStream();
    
    int frameIndex = 0;
    final captureStart = DateTime.now();
    
    await for (final frame in stream) {
      // Verificar si ya tenemos suficientes frames
      if (frameIndex >= CaptureConstants.totalFramesMax) {
        break;
      }
      
      // Verificar timeout (máximo 5 segundos)
      if (DateTime.now().difference(captureStart).inSeconds > 5) {
        break;
      }
      
      // Procesar frame en worker (no bloquea UI)
      _processFrameInWorker(frame, frameIndex, breedType);
      
      frameIndex++;
      
      // Liberar memoria si tenemos demasiados frames
      if (_frameCache.length > maxFramesInMemory) {
        _evictOldFrames();
      }
    }
    
    // 4. Seleccionar mejor frame
    await _selectBestFrameOptimized();
  }
  
  /// Procesa frame en isolate separado (no bloquea UI)
  Future<void> _processFrameInWorker(
    CameraImage frame,
    int frameIndex,
    BreedType breedType,
  ) async {
    final availableWorker = _workerPool.firstWhere(
      (w) => !w.isBusy,
      orElse: () => _workerPool.first,
    );
    
    final result = await availableWorker.evaluateFrame(
      frameData: frame.planes[0].bytes,
      frameIndex: frameIndex,
    );
    
    _frameCache[frameIndex] = result;
    notifyListeners();
  }
  
  /// Elimina frames de baja calidad de caché (liberar memoria)
  void _evictOldFrames() {
    final sortedFrames = _frameCache.entries.toList()
      ..sort((a, b) => a.value.overallScore.compareTo(b.value.overallScore));
    
    // Eliminar 30% peores frames
    final toRemove = (sortedFrames.length * 0.3).ceil();
    for (int i = 0; i < toRemove; i++) {
      _frameCache.remove(sortedFrames[i].key);
    }
  }
  
  /// Selecciona mejor frame usando score ponderado optimizado
  Future<void> _selectBestFrameOptimized() async {
    if (_frameCache.isEmpty) {
      throw InsufficientFramesFailure();
    }
    
    // Ordenar por overall score
    final sortedFrames = _frameCache.entries.toList()
      ..sort((a, b) => b.value.overallScore.compareTo(a.value.overallScore));
    
    // Top 3 frames
    final topFrames = sortedFrames.take(3).toList();
    
    // Ejecutar inferencia TFLite en top 3 (no en todos)
    final results = await Future.wait(
      topFrames.map((entry) => _runInference(entry.value)),
    );
    
    // Seleccionar el que tenga mejor confidence
    final bestResult = results.reduce((a, b) => 
      a.confidence > b.confidence ? a : b);
    
    _selectedFrame = bestResult;
    notifyListeners();
  }
}

/// Worker para procesamiento paralelo en isolate
class Worker {
  final SendPort _sendPort;
  bool isBusy = false;
  
  Future<FrameQuality> evaluateFrame({
    required Uint8List frameData,
    required int frameIndex,
  }) async {
    isBusy = true;
    
    // Enviar frame a isolate para procesamiento
    _sendPort.send({
      'type': 'evaluate',
      'frameData': frameData,
      'frameIndex': frameIndex,
    });
    
    // Esperar resultado
    final result = await _receiveResult();
    
    isBusy = false;
    return result;
  }
}
```

### 10.2 Optimización de Memoria

```dart
// lib/core/utils/memory_manager.dart
class MemoryManager {
  /// Límites de memoria por tipo de contenido
  static const int maxImagesInMemory = 10;
  static const int maxModelsCached = 3; // Máximo 3 de 7 razas en memoria
  static const int maxFramesInMemory = 50;
  
  /// Comprime imagen para almacenamiento local
  Future<Uint8List> compressImage(
    Uint8List imageData, {
    int quality = 85,
  }) async {
    final image = img.decodeImage(imageData);
    if (image == null) return imageData;
    
    // Reducir resolución si es muy grande
    img.Image compressed = image;
    if (image.width > 1920 || image.height > 1920) {
      compressed = img.copyResize(
        image,
        width: 1920,
        maintainAspect: true,
      );
    }
    
    // Comprimir con calidad especificada
    return Uint8List.fromList(
      img.encodeJpg(compressed, quality: quality),
    );
  }
  
  /// Libera modelos TFLite no utilizados recientemente
  void evictUnusedModels(Map<BreedType, Interpreter> interpreters) {
    // Mantener solo los 3 modelos más usados
    final usage = <BreedType, int>{};
    
    // ... tracking de uso ...
    
    if (interpreters.length > maxModelsCached) {
      final leastUsed = usage.entries.toList()
        ..sort((a, b) => a.value.compareTo(b.value));
      
      for (var entry in leastUsed.take(interpreters.length - maxModelsCached)) {
        interpreters[entry.key]?.close();
        interpreters.remove(entry.key);
      }
    }
  }
}
```

## 11. Testing de Componentes Críticos

### 11.1 Tests de Captura Continua

```dart
// test/features/data_management/presentation/providers/camera_provider_test.dart
void main() {
  group('CameraProvider - Captura Continua', () {
    late CameraProvider provider;
    late MockStartContinuousCaptureUseCase mockStartCapture;
    late MockEvaluateFrameQualityUseCase mockEvaluateQuality;
    
    setUp(() {
      mockStartCapture = MockStartContinuousCaptureUseCase();
      mockEvaluateQuality = MockEvaluateFrameQualityUseCase();
      provider = CameraProvider(
        startCaptureUseCase: mockStartCapture,
        evaluateQualityUseCase: mockEvaluateQuality,
      );
    });
    
    test('should capture between 30-75 frames at 10-15 FPS', () async {
      // Arrange
      final captureSession = CaptureSession(
        id: 'session_1',
        animalId: 'animal_1',
        startTime: DateTime.now(),
        totalFrames: 45, // Entre 30-75
        framesEvaluated: 45,
        framesRejected: 10,
        averageQualityScore: 0.75,
        rejectionReasons: {},
      );
      
      when(mockStartCapture(any)).thenAnswer(
        (_) async => Right(captureSession),
      );
      
      // Act
      await provider.startCapture(
        animalId: 'animal_1',
        breedType: BreedType.brahman,
      );
      
      // Assert
      expect(provider.capturedFrames, inInclusiveRange(30, 75));
      expect(provider.captureProgress, greaterThan(0));
    });
    
    test('should reject frames below quality thresholds', () async {
      // Arrange: Frame con baja calidad de silueta
      final lowQualityFrame = FrameQuality(
        frameIndex: 0,
        sharpness: 0.8,        // ✓ > 0.7
        brightness: 0.6,       // ✓ 0.4-0.8
        contrast: 0.7,         // ✓ > 0.5
        silhouetteVisibility: 0.5,  // ✗ < 0.8 (mínimo)
        angleScore: 0.7,       // ✓ > 0.6
        overallScore: 0.62,    // ✗ < 0.65
        isAcceptable: false,
        rejectionReason: 'silueta no visible',
      );
      
      when(mockEvaluateQuality(any)).thenAnswer(
        (_) async => Right(lowQualityFrame),
      );
      
      // Act
      final result = await provider.evaluateFrame(mockFrameData);
      
      // Assert
      expect(result.isAcceptable, false);
      expect(result.rejectionReason, contains('silueta'));
    });
    
    test('should complete capture in under 10 seconds', () async {
      // Arrange
      final startTime = DateTime.now();
      
      // Act
      await provider.startCapture(
        animalId: 'animal_1',
        breedType: BreedType.nelore,
      );
      
      final endTime = DateTime.now();
      final duration = endTime.difference(startTime);
      
      // Assert: Captura (5s máx) + procesamiento (3s máx) = 8s máx
      expect(duration.inSeconds, lessThanOrEqualTo(10));
    });
  });
}
```

### 11.2 Tests de Integración TFLite

```dart
// test/core/ml/tflite_manager_integration_test.dart
void main() {
  group('TFLiteManager - Integración con Modelos Reales', () {
    late TFLiteManager tfliteManager;
    
    setUp(() {
      tfliteManager = TFLiteManager();
    });
    
    test('should load all 7 breed models successfully', () async {
      // Arrange: Las 7 razas del proyecto
      final breeds = [
        BreedType.brahman,
        BreedType.nelore,
        BreedType.angus,
        BreedType.cebuinas,
        BreedType.criollo,
        BreedType.pardoSuizo,
        BreedType.jersey,
      ];
      
      // Act & Assert
      for (final breed in breeds) {
        final result = await tfliteManager.loadBreedModel(breed);
        
        expect(result.isRight(), true,
          reason: 'Modelo de ${breed.toString()} debe cargarse correctamente');
      }
    });
    
    test('should estimate weight with precision ≥95%', () async {
      // Arrange: Imagen real de animal Brahman adulto (~450 kg)
      final testImage = await loadTestImage('brahman_adult_450kg.jpg');
      
      // Act
      final result = await tfliteManager.estimateWeight(
        imageData: testImage,
        breedType: BreedType.brahman,
        ageCategory: AgeCategory.vacasToros,
      );
      
      // Assert
      result.fold(
        (failure) => fail('No debería fallar: $failure'),
        (estimation) {
          // Precisión ≥95% (confidence score)
          expect(estimation.confidence, 
            greaterThanOrEqualTo(SystemMetrics.minPrecision));
          
          // Error absoluto <5 kg (peso real: 450 kg)
          final error = (estimation.weight - 450).abs();
          expect(error, lessThan(SystemMetrics.maxErrorKg));
          
          // R² se valida en dataset completo, no por imagen individual
        },
      );
    });
    
    test('should process image in under 3 seconds', () async {
      // Arrange
      final testImage = await loadTestImage('test_animal.jpg');
      final startTime = DateTime.now();
      
      // Act
      await tfliteManager.estimateWeight(
        imageData: testImage,
        breedType: BreedType.angus,
        ageCategory: AgeCategory.vaquillonasTorillos,
      );
      
      final endTime = DateTime.now();
      final duration = endTime.difference(startTime);
      
      // Assert: Debe procesar en <3 segundos
      expect(duration.inMilliseconds, 
        lessThan(SystemMetrics.maxProcessingTimeMs));
    });
    
    test('should validate weight ranges by breed and age', () async {
      // Arrange: Ternero Nelore (debe pesar 80-180 kg)
      final testImage = await loadTestImage('nelore_ternero.jpg');
      
      // Act
      final result = await tfliteManager.estimateWeight(
        imageData: testImage,
        breedType: BreedType.nelore,
        ageCategory: AgeCategory.terneros,
      );
      
      // Assert
      result.fold(
        (failure) => fail('No debería fallar'),
        (estimation) {
          expect(estimation.weight, inInclusiveRange(80, 180),
            reason: 'Peso de ternero Nelore debe estar en rango 80-180 kg');
        },
      );
    });
  });
}
```

## 12. Documentación de Código

### 12.1 Formato de Comentarios

```dart
/// Inicia captura continua de fotogramas para estimación de peso.
///
/// Especificaciones del proyecto (ADR-010):
/// - **FPS**: 10-15 fotogramas por segundo
/// - **Duración**: 3-5 segundos de captura continua
/// - **Total frames**: 30-75 fotogramas esperados
///
/// Criterios de evaluación en tiempo real:
/// - Nitidez (sharpness) > 0.7
/// - Iluminación (brightness) entre 0.4-0.8
/// - Contraste (contrast) > 0.5
/// - Visibilidad de silueta > 0.8
/// - Ángulo apropiado > 0.6
///
/// El score global se calcula como:
/// `score = (silueta * 0.4) + (nitidez * 0.3) + (iluminación * 0.2) + (ángulo * 0.1)`
///
/// [animalId] ID del animal del sistema
/// [breedType] Una de las 7 razas: Brahman, Nelore, Angus, Cebuinas, 
///             Criollo, Pardo Suizo, Jersey
///
/// Returns [CaptureSession] con información de la sesión de captura
///
/// Throws [InvalidBreedFailure] si la raza no es una de las 7 soportadas
/// Throws [InsufficientFramesFailure] si se capturan <30 frames
/// Throws [LowQualityFramesFailure] si ningún frame tiene score >0.65
///
/// Example:
/// ```dart
/// final session = await startContinuousCapture(
///   animalId: 'animal_123',
///   breedType: BreedType.brahman,
/// );
/// print('Capturados ${session.totalFrames} fotogramas');
/// ```
Future<CaptureSession> startContinuousCapture({
  required String animalId,
  required BreedType breedType,
}) async {
  // implementación...
}
```

## 13. Buenas Prácticas Finales

### 13.1 Checklist de Code Review

```markdown
## Code Review Checklist - Flutter

### Naming y Estructura
- [ ] Código en inglés, UI en español
- [ ] Razas: Usar enum BreedType (7 razas exactas)
- [ ] Categorías edad: Usar enum AgeCategory (4 categorías)
- [ ] Clean Architecture respetada (Presentation/Domain/Data)
- [ ] Features organizadas por las 5 áreas funcionales

### Captura Continua
- [ ] FPS entre 10-15
- [ ] Duración 3-5 segundos
- [ ] Evaluación con criterios correctos (nitidez>0.7, etc.)
- [ ] Score global con pesos correctos (40% silueta, 30% nitidez, 20% iluminación, 10% ángulo)

### TensorFlow Lite
- [ ] Modelo correcto para la raza
- [ ] Validación de rango de peso por edad
- [ ] Procesamiento <3 segundos
- [ ] Confidence score ≥95%
- [ ] Manejo de errores si precision <95%

### Offline-First
- [ ] Operaciones guardadas en SQLite local
- [ ] Cola de sincronización con prioridades
- [ ] Resolución de conflictos (Last-Write-Wins)
- [ ] Indicador de sincronización visible

### Normativa Boliviana
- [ ] SENASAG: Generación de reportes
- [ ] REGENSA: Validación capítulos 3.10 y 7.1
- [ ] GMA: Campos obligatorios completos
- [ ] Gran Paitití: Integración preparada

### Performance
- [ ] Compresión de imágenes >1920px
- [ ] Máximo 3 modelos TFLite en memoria
- [ ] Pool de workers para procesamiento paralelo
- [ ] Liberación de frames de baja calidad

### Testing
- [ ] Tests unitarios para casos de uso críticos
- [ ] Tests de integración TFLite con las 7 razas
- [ ] Validación de métricas (≥95%, <3s, <5kg)
- [ ] Cobertura ≥70%

### Documentación
- [ ] Comentarios en español
- [ ] Docstrings con especificaciones del proyecto
- [ ] Referencias a ADRs cuando aplique
- [ ] Ejemplos de uso en comentarios
```
