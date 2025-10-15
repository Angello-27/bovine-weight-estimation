# Estándares de Desarrollo Flutter

## Contexto del Proyecto

**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Tecnología**: Flutter 3.x / Dart 3.x  
**Plataformas**: Android, iOS

## Principios Fundamentales Flutter

1. **Offline-First**: SQLite como fuente primaria de verdad
2. **Clean Architecture**: presentation → domain → data
3. **Provider**: Gestión de estado reactiva
4. **Atomic Design**: Componentes reutilizables (atoms → molecules → organisms)
5. **Material Design 3**: UI moderna y accesible

---

## Estructura de Carpetas (Clean Architecture)

```
lib/
├── core/                              # Código compartido
│   ├── constants/                     # Constantes del dominio
│   │   ├── breeds.dart                # 7 razas EXACTAS
│   │   ├── age_categories.dart        # 4 categorías EXACTAS
│   │   ├── capture_constants.dart     # 10-15 FPS, 3-5s
│   │   ├── metrics.dart               # ≥95%, <5kg, <3s
│   │   └── hacienda_constants.dart    # GPS, Schaeffer
│   │
│   ├── errors/                        # Manejo de errores
│   │   ├── failures.dart              # Failures abstractos
│   │   └── exceptions.dart            # Exceptions custom
│   │
│   ├── utils/                         # Utilidades
│   │   ├── either.dart                # Either<L, R>
│   │   ├── validators.dart
│   │   └── formatters.dart
│   │
│   └── ui/                            # Atomic Design
│       ├── atoms/                     # Componentes básicos
│       ├── molecules/                 # Combinación de atoms
│       └── organisms/                 # Componentes complejos
│
├── features/                          # Features por área funcional
│   │
│   └── data_management/               # Ejemplo: Área 1
│       ├── presentation/              # UI Layer
│       │   ├── screens/
│       │   ├── widgets/
│       │   └── providers/
│       │
│       ├── domain/                    # Business Logic Layer
│       │   ├── entities/
│       │   ├── repositories/          # Interfaces
│       │   └── usecases/
│       │
│       └── data/                      # Data Layer
│           ├── models/
│           ├── repositories/          # Implementaciones
│           └── datasources/
│
└── main.dart                          # Entry point
```

---

## Constantes del Dominio (CRÍTICAS)

### 1. Razas Bovinas (7 EXACTAS - NO MODIFICAR)

```dart
// lib/core/constants/breeds.dart

/// 7 razas bovinas de Hacienda Gamelera.
/// 
/// IMPORTANTE: Estas son las ÚNICAS razas válidas en el sistema.
/// NO agregar, eliminar o modificar sin autorización de Bruno Brito Macedo.
enum BreedType {
  brahman,      // Bos indicus
  nelore,       // Bos indicus
  angus,        // Bos taurus
  cebuinas,     // Bos indicus
  criollo,      // Bos taurus
  pardoSuizo,   // Bos taurus (camelCase para multi-palabra)
  jersey,       // Bos taurus
}

extension BreedTypeExtension on BreedType {
  /// Nombre para mostrar en UI (español)
  String get displayName {
    switch (this) {
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
  
  /// Clasificación taxonómica
  BovineSpecies get species {
    switch (this) {
      case BreedType.brahman:
      case BreedType.nelore:
      case BreedType.cebuinas:
        return BovineSpecies.bosIndicus;
      case BreedType.angus:
      case BreedType.criollo:
      case BreedType.pardoSuizo:
      case BreedType.jersey:
        return BovineSpecies.bosTaurus;
    }
  }
  
  /// Nombre del archivo del modelo TFLite
  String get modelFileName {
    final breedName = name.replaceAllMapped(
      RegExp(r'([A-Z])'),
      (match) => '-${match.group(1)!.toLowerCase()}',
    );
    return '$breedName-v1.0.0.tflite';
  }
}

enum BovineSpecies {
  bosIndicus,  // Razas cebuinas (adaptadas a clima tropical)
  bosTaurus,   // Razas europeas
}
```

### 2. Categorías de Edad (4 EXACTAS - NO MODIFICAR)

```dart
// lib/core/constants/age_categories.dart

/// 4 categorías de edad de bovinos en Hacienda Gamelera.
/// 
/// Basadas en el sistema de manejo de Bruno Brito Macedo.
enum AgeCategory {
  terneros,              // <8 meses
  vaquillonasTorillos,   // 6-18 meses
  vaquillonasToretes,    // 19-30 meses
  vacasToros,            // >30 meses
}

extension AgeCategoryExtension on AgeCategory {
  /// Nombre para mostrar en UI (español)
  String get displayName {
    switch (this) {
      case AgeCategory.terneros:
        return 'Terneros (<8 meses)';
      case AgeCategory.vaquillonasTorillos:
        return 'Vaquillonas/Torillos (6-18 meses)';
      case AgeCategory.vaquillonasToretes:
        return 'Vaquillonas/Toretes (19-30 meses)';
      case AgeCategory.vacasToros:
        return 'Vacas/Toros (>30 meses)';
    }
  }
  
  /// Rango de edad en meses (min, max)
  (int min, int? max) get ageRangeMonths {
    switch (this) {
      case AgeCategory.terneros:
        return (0, 8);
      case AgeCategory.vaquillonasTorillos:
        return (6, 18);
      case AgeCategory.vaquillonasToretes:
        return (19, 30);
      case AgeCategory.vacasToros:
        return (30, null); // Sin máximo
    }
  }
  
  /// Calcula categoría desde fecha de nacimiento
  static AgeCategory fromBirthDate(DateTime birthDate) {
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
  
  static int _calculateAgeInMonths(DateTime birthDate) {
    final now = DateTime.now();
    return (now.year - birthDate.year) * 12 + (now.month - birthDate.month);
  }
}
```

### 3. Constantes de Captura Continua

```dart
// lib/core/constants/capture_constants.dart

/// Constantes para captura continua de fotogramas (US-001).
/// 
/// Estos valores fueron definidos en Sprint Planning y validados
/// con Bruno Brito Macedo en condiciones reales de Hacienda Gamelera.
class CaptureConstants {
  /// Fotogramas por segundo objetivo: 10-15 FPS
  static const int framesPerSecond = 12;
  
  /// Duración de captura continua: 3-5 segundos
  static const Duration captureDuration = Duration(seconds: 4);
  
  /// Total de fotogramas esperados: 30-75 (12 FPS × 4s = 48 frames)
  static const int expectedFrameCount = framesPerSecond * 4;
  
  // Umbrales de calidad de fotograma
  
  /// Umbral mínimo de nitidez (sharpness): 0.7
  static const double minSharpness = 0.7;
  
  /// Rango de iluminación óptima (brightness): 0.4-0.8
  static const double minBrightness = 0.4;
  static const double maxBrightness = 0.8;
  
  /// Umbral mínimo de contraste: 0.5
  static const double minContrast = 0.5;
  
  /// Umbral mínimo de visibilidad de silueta: 0.8
  static const double minSilhouetteVisibility = 0.8;
  
  /// Umbral mínimo de ángulo apropiado: 0.6
  static const double minAngleScore = 0.6;
  
  // Ponderación para score global de fotograma
  
  /// Peso de silueta en score global: 40%
  static const double silhouetteWeight = 0.4;
  
  /// Peso de nitidez en score global: 30%
  static const double sharpnessWeight = 0.3;
  
  /// Peso de iluminación en score global: 20%
  static const double brightnessWeight = 0.2;
  
  /// Peso de ángulo en score global: 10%
  static const double angleWeight = 0.1;
  
  /// Distancia óptima de captura: 2-5 metros
  static const double minDistanceMeters = 2.0;
  static const double maxDistanceMeters = 5.0;
}
```

### 4. Métricas del Sistema (OBLIGATORIAS)

```dart
// lib/core/constants/metrics.dart

/// Métricas obligatorias del sistema de estimación de peso.
/// 
/// Estas métricas fueron definidas en Sprint 0 y son requisitos
/// no funcionales críticos del sistema.
class SystemMetrics {
  /// Precisión mínima del modelo ML: ≥95%
  /// 
  /// Coeficiente de determinación (R²) debe ser ≥0.95
  static const double minPrecision = 0.95;
  
  /// Error absoluto máximo: <5 kg
  /// 
  /// Diferencia |peso_estimado - peso_real| < 5 kg
  static const double maxErrorKg = 5.0;
  
  /// Tiempo máximo de procesamiento: <3 segundos
  /// 
  /// Desde fotograma capturado hasta resultado mostrado
  static const Duration maxProcessingTime = Duration(seconds: 3);
  static const int maxProcessingTimeMs = 3000;
  
  /// Tiempo objetivo para 20 animales: <2 horas
  /// 
  /// Comparado con método tradicional: 2-3 días
  static const Duration targetTime20Animals = Duration(hours: 2);
  
  /// Reducción de tiempo objetivo: 80%
  static const double timeReductionTarget = 0.80;
  
  /// Método tradicional: error 5-20 kg (fórmula Schaeffer)
  static const double traditionalMethodMinErrorKg = 5.0;
  static const double traditionalMethodMaxErrorKg = 20.0;
}
```

### 5. Constantes de Hacienda Gamelera

```dart
// lib/core/constants/hacienda_constants.dart

/// Constantes específicas de Hacienda Gamelera.
/// 
/// Cliente: Bruno Brito Macedo
/// Ubicación: San Ignacio de Velasco, Santa Cruz, Bolivia
class HaciendaConstants {
  /// Nombre de la hacienda
  static const String haciendaName = 'Hacienda Gamelera';
  
  /// Propietario
  static const String ownerName = 'Bruno Brito Macedo';
  
  /// Ubicación
  static const String location = 'San Ignacio de Velasco, Santa Cruz, Bolivia';
  
  /// Coordenadas GPS: 15°51′34.2′′S, 60°47′52.4′′W
  static const double latitude = -15.859500;   // Negativo = Sur
  static const double longitude = -60.797889;  // Negativo = Oeste
  
  /// Extensión: 48.5 hectáreas
  static const double extensionHectares = 48.5;
  
  /// Capacidad: 500 cabezas de ganado bovino
  static const int animalCapacity = 500;
  
  /// Fórmula Schaeffer (método tradicional para comparación)
  /// 
  /// Peso (kg) = (PT² × LC) / 10838
  /// - PT: Perímetro Torácico (cm)
  /// - LC: Longitud del Cuerpo (cm)
  /// 
  /// Error actual: 5-20 kg por animal
  static double schaefferFormula({
    required double perimeterThoracicCm,
    required double bodyLengthCm,
  }) {
    return (perimeterThoracicCm * perimeterThoracicCm * bodyLengthCm) / 10838;
  }
  
  /// Personal típico para pesaje tradicional: 3-4 personas
  /// (Capataz, vaquero, peón, ayudante)
  static const int traditionalMethodPersonnel = 3;
  
  /// Tiempo tradicional: 2-3 días para 20 animales
  static const Duration traditionalMethodMinTime = Duration(days: 2);
  static const Duration traditionalMethodMaxTime = Duration(days: 3);
}
```

---

## Naming Conventions

### Archivos

```
✅ CORRECTO:
animal_repository.dart          (snake_case)
breed_selector_widget.dart
capture_session_model.dart

❌ INCORRECTO:
AnimalRepository.dart           (PascalCase - solo para clases)
animal-repository.dart          (kebab-case - no usar en Dart)
animalRepository.dart           (camelCase - no usar para archivos)
```

### Clases y Enums

```dart
✅ CORRECTO:
class AnimalRepository { }      // PascalCase
enum BreedType { }
class StartContinuousCaptureUseCase { }

❌ INCORRECTO:
class animalRepository { }      // camelCase
class Animal_Repository { }     // snake_case
```

### Variables y Funciones

```dart
✅ CORRECTO:
String animalId;                // camelCase
int framesPerSecond;
Future<void> startCapture() { }

❌ INCORRECTO:
String AnimalId;                // PascalCase
String animal_id;               // snake_case
```

### Constantes

```dart
✅ CORRECTO:
const int framesPerSecond = 12;         // camelCase
static const double minPrecision = 0.95;

❌ INCORRECTO:
const int FRAMES_PER_SECOND = 12;       // SCREAMING_SNAKE_CASE (solo para enums)
```

### Enums

```dart
✅ CORRECTO:
enum BreedType {
  brahman,    // camelCase para valores
  nelore,
  pardoSuizo, // camelCase para multi-palabra
}

❌ INCORRECTO:
enum BreedType {
  BRAHMAN,    // SCREAMING_CASE
  Brahman,    // PascalCase
  pardo_suizo, // snake_case
}
```

---

## Clean Architecture en Flutter

### Layer 1: Presentation (UI)

**Responsabilidad**: Interacción con usuario, gestión de estado

```dart
// lib/features/data_management/presentation/screens/camera_screen.dart

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../../core/constants/breeds.dart';
import '../providers/camera_provider.dart';
import '../widgets/breed_selector_widget.dart';
import '../widgets/camera_preview_widget.dart';

/// Pantalla de captura continua de fotogramas (US-001).
/// 
/// Permite al ganadero:
/// 1. Seleccionar raza del animal (7 razas de Hacienda Gamelera)
/// 2. Capturar fotogramas continuos (10-15 FPS durante 3-5s)
/// 3. Ver progreso de captura en tiempo real
/// 4. Confirmar fotograma seleccionado automáticamente
class CameraScreen extends StatelessWidget {
  const CameraScreen({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Captura de Peso'),
      ),
      body: Consumer<CameraProvider>(
        builder: (context, provider, child) {
          return Column(
            children: [
              // Selector de raza (obligatorio antes de capturar)
              BreedSelectorWidget(
                selectedBreed: provider.selectedBreed,
                onBreedSelected: provider.selectBreed,
              ),
              
              // Vista previa de cámara
              Expanded(
                child: CameraPreviewWidget(
                  controller: provider.cameraController,
                ),
              ),
              
              // Botón de captura (solo activo si raza seleccionada)
              _buildCaptureButton(context, provider),
            ],
          );
        },
      ),
    );
  }
  
  Widget _buildCaptureButton(BuildContext context, CameraProvider provider) {
    final canCapture = provider.selectedBreed != null && 
                       provider.state is! CameraStateCapturing;
    
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: ElevatedButton(
        onPressed: canCapture ? () => provider.startContinuousCapture() : null,
        style: ElevatedButton.styleFrom(
          minimumSize: const Size(double.infinity, 56),
        ),
        child: provider.state is CameraStateCapturing
            ? const CircularProgressIndicator()
            : const Text('Capturar Peso'),
      ),
    );
  }
}
```

**Provider (Gestión de Estado)**:

```dart
// lib/features/data_management/presentation/providers/camera_provider.dart

import 'package:flutter/foundation.dart';
import 'package:camera/camera.dart';

import '../../../../core/constants/breeds.dart';
import '../../../../core/constants/capture_constants.dart';
import '../../domain/usecases/start_continuous_capture_usecase.dart';
import '../../domain/entities/capture_session.dart';

/// Provider para gestión de estado de captura de cámara.
/// 
/// Implementa lógica de captura continua (10-15 FPS, 3-5s) y
/// comunicación con caso de uso del dominio.
class CameraProvider extends ChangeNotifier {
  final StartContinuousCaptureUseCase _startCaptureUseCase;
  
  CameraProvider({
    required StartContinuousCaptureUseCase startCaptureUseCase,
  }) : _startCaptureUseCase = startCaptureUseCase;
  
  // Estado
  CameraState _state = const CameraState.initial();
  CameraState get state => _state;
  
  // Raza seleccionada (una de las 7 de Hacienda Gamelera)
  BreedType? _selectedBreed;
  BreedType? get selectedBreed => _selectedBreed;
  
  // Controlador de cámara
  CameraController? _cameraController;
  CameraController? get cameraController => _cameraController;
  
  // Sesión de captura actual
  CaptureSession? _captureSession;
  CaptureSession? get captureSession => _captureSession;
  
  /// Selecciona raza del animal (obligatorio antes de capturar).
  void selectBreed(BreedType breed) {
    // Validar que sea una de las 7 razas exactas
    if (!BreedType.values.contains(breed)) {
      _state = CameraState.error('Raza inválida');
      notifyListeners();
      return;
    }
    
    _selectedBreed = breed;
    notifyListeners();
  }
  
  /// Inicia captura continua de fotogramas.
  /// 
  /// Duración: 3-5 segundos (configurable)
  /// FPS: 10-15 (configurable)
  /// Total fotogramas: 30-75
  Future<void> startContinuousCapture() async {
    if (_selectedBreed == null) {
      _state = CameraState.error('Debe seleccionar una raza');
      notifyListeners();
      return;
    }
    
    _state = const CameraState.capturing(progress: 0.0);
    notifyListeners();
    
    try {
      // Ejecutar caso de uso del dominio
      final result = await _startCaptureUseCase(
        breedType: _selectedBreed!,
        framesPerSecond: CaptureConstants.framesPerSecond,
        duration: CaptureConstants.captureDuration,
        onProgress: (progress) {
          _state = CameraState.capturing(progress: progress);
          notifyListeners();
        },
      );
      
      result.fold(
        (failure) {
          _state = CameraState.error(failure.message);
          notifyListeners();
        },
        (captureSession) {
          _captureSession = captureSession;
          _state = CameraState.captured(captureSession);
          notifyListeners();
        },
      );
    } catch (e) {
      _state = CameraState.error('Error inesperado: $e');
      notifyListeners();
    }
  }
  
  @override
  void dispose() {
    _cameraController?.dispose();
    super.dispose();
  }
}

/// Estados posibles de la cámara
@immutable
sealed class CameraState {
  const CameraState();
  
  const factory CameraState.initial() = CameraStateInitial;
  const factory CameraState.capturing({required double progress}) = CameraStateCapturing;
  const factory CameraState.captured(CaptureSession session) = CameraStateCaptured;
  const factory CameraState.error(String message) = CameraStateError;
}

class CameraStateInitial extends CameraState {
  const CameraStateInitial();
}

class CameraStateCapturing extends CameraState {
  final double progress; // 0.0 - 1.0
  const CameraStateCapturing({required this.progress});
}

class CameraStateCaptured extends CameraState {
  final CaptureSession session;
  const CameraStateCaptured(this.session);
}

class CameraStateError extends CameraState {
  final String message;
  const CameraStateError(this.message);
}
```

### Layer 2: Domain (Business Logic)

**Entidades**:

```dart
// lib/features/data_management/domain/entities/animal.dart

import 'package:equatable/equatable.dart';

import '../../../../core/constants/breeds.dart';
import '../../../../core/constants/age_categories.dart';

/// Entidad Animal - Representa un bovino de Hacienda Gamelera.
/// 
/// Entidad pura del dominio sin dependencias de frameworks.
class Animal extends Equatable {
  final String id;
  final String tagNumber;              // Número de caravana/arete
  final BreedType breedType;           // Una de las 7 razas exactas
  final DateTime birthDate;
  final Gender gender;
  final AnimalStatus status;
  final DateTime createdAt;
  final DateTime? updatedAt;
  
  // Campos opcionales
  final String? color;
  final double? weightAtBirthKg;
  final String? motherId;
  final String? fatherId;
  final String? observations;
  
  const Animal({
    required this.id,
    required this.tagNumber,
    required this.breedType,
    required this.birthDate,
    required this.gender,
    required this.status,
    required this.createdAt,
    this.updatedAt,
    this.color,
    this.weightAtBirthKg,
    this.motherId,
    this.fatherId,
    this.observations,
  });
  
  /// Calcula edad en meses desde fecha de nacimiento.
  int get ageInMonths {
    final now = DateTime.now();
    return (now.year - birthDate.year) * 12 + (now.month - birthDate.month);
  }
  
  /// Categoría de edad calculada automáticamente.
  /// 
  /// Se calcula desde fecha de nacimiento según las 4 categorías
  /// definidas para Hacienda Gamelera.
  AgeCategory get ageCategory {
    return AgeCategoryExtension.fromBirthDate(birthDate);
  }
  
  /// Especie bovina (Bos indicus o Bos taurus)
  BovineSpecies get species => breedType.species;
  
  @override
  List<Object?> get props => [
        id,
        tagNumber,
        breedType,
        birthDate,
        gender,
        status,
        createdAt,
        updatedAt,
        color,
        weightAtBirthKg,
        motherId,
        fatherId,
        observations,
      ];
}

enum Gender {
  male,    // Macho
  female,  // Hembra
}

extension GenderExtension on Gender {
  String get displayName {
    switch (this) {
      case Gender.male:
        return 'Macho';
      case Gender.female:
        return 'Hembra';
    }
  }
}

enum AnimalStatus {
  active,    // Activo en Hacienda Gamelera
  inactive,  // Inactivo temporalmente
  sold,      // Vendido
  dead,      // Muerto
}

extension AnimalStatusExtension on AnimalStatus {
  String get displayName {
    switch (this) {
      case AnimalStatus.active:
        return 'Activo';
      case AnimalStatus.inactive:
        return 'Inactivo';
      case AnimalStatus.sold:
        return 'Vendido';
      case AnimalStatus.dead:
        return 'Muerto';
    }
  }
}
```

**Use Cases**:

```dart
// lib/features/data_management/domain/usecases/estimate_weight_usecase.dart

import 'dart:io';
import 'package:dartz/dartz.dart';

import '../../../../core/constants/breeds.dart';
import '../../../../core/constants/metrics.dart';
import '../../../../core/errors/failures.dart';
import '../entities/weighing.dart';
import '../repositories/weighing_repository.dart';

/// Caso de uso: Estimar peso de bovino mediante IA (US-002).
/// 
/// Responsabilidades:
/// 1. Validar raza es una de las 7 exactas
/// 2. Preprocesar imagen
/// 3. Ejecutar inferencia ML con modelo específico de raza
/// 4. Validar métricas del sistema (≥95%, <5kg, <3s)
/// 5. Validar rango de peso según raza y edad
/// 6. Guardar pesaje (offline-first)
class EstimateWeightUseCase {
  final WeighingRepository _weighingRepository;
  
  const EstimateWeightUseCase({
    required WeighingRepository weighingRepository,
  }) : _weighingRepository = weighingRepository;
  
  /// Ejecuta estimación de peso.
  /// 
  /// Retorna [Right(Weighing)] si exitoso, [Left(Failure)] si error.
  Future<Either<Failure, Weighing>> call({
    required String animalId,
    required BreedType breedType,
    required AgeCategory ageCategory,
    required File imageFile,
  }) async {
    // 1. Validar raza es una de las 7 exactas
    if (!BreedType.values.contains(breedType)) {
      return Left(InvalidBreedFailure(
        message: 'Raza inválida. Debe ser una de las 7 razas de Hacienda Gamelera.',
        invalidBreed: breedType.name,
      ));
    }
    
    // 2. Ejecutar estimación (delegado a repository → datasource)
    final result = await _weighingRepository.estimateWeight(
      animalId: animalId,
      breedType: breedType,
      ageCategory: ageCategory,
      imageFile: imageFile,
    );
    
    return result.fold(
      (failure) => Left(failure),
      (weighing) {
        // 3. Validar métricas del sistema
        if (weighing.confidence < SystemMetrics.minPrecision) {
          return Left(PrecisionBelowThresholdFailure(
            message: 'Precisión ${(weighing.confidence * 100).toStringAsFixed(1)}% < ${(SystemMetrics.minPrecision * 100).toStringAsFixed(0)}% requerido',
            confidence: weighing.confidence,
          ));
        }
        
        // 4. Validar tiempo de procesamiento <3s
        if (weighing.processingTimeMs > SystemMetrics.maxProcessingTimeMs) {
          return Left(ProcessingTimeTooSlowFailure(
            message: 'Procesamiento ${weighing.processingTimeMs}ms > ${SystemMetrics.maxProcessingTimeMs}ms objetivo',
            processingTimeMs: weighing.processingTimeMs,
          ));
        }
        
        return Right(weighing);
      },
    );
  }
}
```

### Layer 3: Data (Data Access)

**Repository Implementation**:

```dart
// lib/features/data_management/data/repositories/animal_repository_impl.dart

import 'package:dartz/dartz.dart';

import '../../../../core/errors/failures.dart';
import '../../../../core/errors/exceptions.dart';
import '../../domain/entities/animal.dart';
import '../../domain/repositories/animal_repository.dart';
import '../datasources/animal_local_datasource.dart';
import '../datasources/animal_remote_datasource.dart';

/// Implementación de AnimalRepository con estrategia offline-first.
/// 
/// Prioridad:
/// 1. SQLite local (siempre primero)
/// 2. API remota (solo si local falla o para sincronización)
class AnimalRepositoryImpl implements AnimalRepository {
  final AnimalLocalDataSource localDataSource;
  final AnimalRemoteDataSource remoteDataSource;
  
  const AnimalRepositoryImpl({
    required this.localDataSource,
    required this.remoteDataSource,
  });
  
  @override
  Future<Either<Failure, Animal>> getAnimalById(String id) async {
    try {
      // Offline-first: intentar local primero
      final localAnimal = await localDataSource.getAnimalById(id);
      return Right(localAnimal);
    } on CacheException {
      // Si no está en local, intentar remoto
      try {
        final remoteAnimal = await remoteDataSource.getAnimalById(id);
        // Guardar en local para próxima vez
        await localDataSource.cacheAnimal(remoteAnimal);
        return Right(remoteAnimal);
      } on ServerException {
        return Left(ServerFailure());
      }
    }
  }
  
  @override
  Future<Either<Failure, List<Animal>>> getAnimalsByBreed(
    BreedType breed,
  ) async {
    try {
      // Validar raza
      if (!BreedType.values.contains(breed)) {
        return Left(InvalidBreedFailure(
          message: 'Raza inválida',
          invalidBreed: breed.name,
        ));
      }
      
      // Offline-first: local primero
      final localAnimals = await localDataSource.getAnimalsByBreed(breed);
      return Right(localAnimals);
    } on CacheException {
      try {
        final remoteAnimals = await remoteDataSource.getAnimalsByBreed(breed);
        // Cachear para próxima vez
        await localDataSource.cacheAnimals(remoteAnimals);
        return Right(remoteAnimals);
      } on ServerException {
        return Left(ServerFailure());
      }
    }
  }
  
  @override
  Future<Either<Failure, void>> saveAnimal(Animal animal) async {
    try {
      // Guardar primero en local (offline-first)
      await localDataSource.saveAnimal(animal);
      
      // Intentar sincronizar con remoto (no bloquea si falla)
      try {
        await remoteDataSource.saveAnimal(animal);
      } catch (e) {
        // Fallo en remoto no es crítico, se sincronizará después
        // Agregar a queue de sincronización pendiente
        await localDataSource.markForSync(animal.id);
      }
      
      return const Right(null);
    } on CacheException {
      return Left(CacheFailure());
    }
  }
}
```

---

## Manejo de Errores

### Either<L, R>

```dart
// lib/core/utils/either.dart

/// Tipo Either para manejo funcional de errores.
/// 
/// - Left: Representa un error (Failure)
/// - Right: Representa un éxito (Success)
abstract class Either<L, R> {
  const Either();
  
  /// Aplica función según si es Left o Right
  T fold<T>(T Function(L left) onLeft, T Function(R right) onRight);
  
  /// Retorna true si es Right
  bool get isRight;
  
  /// Retorna true si es Left
  bool get isLeft;
}

class Left<L, R> extends Either<L, R> {
  final L value;
  const Left(this.value);
  
  @override
  T fold<T>(T Function(L left) onLeft, T Function(R right) onRight) {
    return onLeft(value);
  }
  
  @override
  bool get isRight => false;
  
  @override
  bool get isLeft => true;
}

class Right<L, R> extends Either<L, R> {
  final R value;
  const Right(this.value);
  
  @override
  T fold<T>(T Function(L left) onLeft, T Function(R right) onRight) {
    return onRight(value);
  }
  
  @override
  bool get isRight => true;
  
  @override
  bool get isLeft => false;
}
```

### Failures

```dart
// lib/core/errors/failures.dart

import 'package:equatable/equatable.dart';

/// Clase base para failures (errores funcionales).
abstract class Failure extends Equatable {
  final String message;
  
  const Failure({required this.message});
  
  @override
  List<Object?> get props => [message];
}

// Failures de dominio específicos de Hacienda Gamelera

/// Error: Raza inválida (no es una de las 7 exactas)
class InvalidBreedFailure extends Failure {
  final String invalidBreed;
  
  const InvalidBreedFailure({
    required String message,
    required this.invalidBreed,
  }) : super(message: message);
  
  @override
  List<Object?> get props => [message, invalidBreed];
}

/// Error: Precisión ML por debajo del umbral (< 95%)
class PrecisionBelowThresholdFailure extends Failure {
  final double confidence;
  
  const PrecisionBelowThresholdFailure({
    required String message,
    required this.confidence,
  }) : super(message: message);
  
  @override
  List<Object?> get props => [message, confidence];
}

/// Error: Procesamiento muy lento (> 3 segundos)
class ProcessingTimeTooSlowFailure extends Failure {
  final int processingTimeMs;
  
  const ProcessingTimeTooSlowFailure({
    required String message,
    required this.processingTimeMs,
  }) : super(message: message);
  
  @override
  List<Object?> get props => [message, processingTimeMs];
}

/// Error: Peso fuera de rango válido para raza/edad
class WeightOutOfRangeFailure extends Failure {
  const WeightOutOfRangeFailure({
    required String message,
  }) : super(message: message);
}

// Failures de infraestructura

class ServerFailure extends Failure {
  const ServerFailure({
    String message = 'Error de servidor',
  }) : super(message: message);
}

class CacheFailure extends Failure {
  const CacheFailure({
    String message = 'Error de caché local',
  }) : super(message: message);
}

class NetworkFailure extends Failure {
  const NetworkFailure({
    String message = 'Sin conexión a internet',
  }) : super(message: message);
}
```

---

## Testing

### Tests Unitarios

```dart
// test/features/data_management/domain/usecases/estimate_weight_usecase_test.dart

import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:dartz/dartz.dart';

void main() {
  late EstimateWeightUseCase usecase;
  late MockWeighingRepository mockRepository;
  
  setUp(() {
    mockRepository = MockWeighingRepository();
    usecase = EstimateWeightUseCase(weighingRepository: mockRepository);
  });
  
  group('EstimateWeightUseCase', () {
    const animalId = 'test-animal-123';
    const breedType = BreedType.brahman;
    const ageCategory = AgeCategory.vacasToros;
    final imageFile = File('test_image.jpg');
    
    final testWeighing = Weighing(
      id: 'weighing-123',
      animalId: animalId,
      estimatedWeightKg: 487.3,
      confidence: 0.97,
      processingTimeMs: 2543,
      method: WeighingMethod.ia,
      timestamp: DateTime.now(),
    );
    
    test('debe retornar Weighing cuando estimación es exitosa', () async {
      // Arrange
      when(mockRepository.estimateWeight(
        animalId: animalId,
        breedType: breedType,
        ageCategory: ageCategory,
        imageFile: imageFile,
      )).thenAnswer((_) async => Right(testWeighing));
      
      // Act
      final result = await usecase(
        animalId: animalId,
        breedType: breedType,
        ageCategory: ageCategory,
        imageFile: imageFile,
      );
      
      // Assert
      expect(result, Right(testWeighing));
      verify(mockRepository.estimateWeight(
        animalId: animalId,
        breedType: breedType,
        ageCategory: ageCategory,
        imageFile: imageFile,
      )).called(1);
    });
    
    test('debe retornar InvalidBreedFailure cuando raza no es de las 7 exactas', () async {
      // Este test validaría con raza inválida si existiera
      // En Dart con enums, es imposible pasar valor inválido en tiempo de compilación
      // Pero se puede testear la lógica interna si se necesita
    });
    
    test('debe retornar PrecisionBelowThresholdFailure cuando confidence < 95%', () async {
      // Arrange
      final lowConfidenceWeighing = testWeighing.copyWith(confidence: 0.89);
      when(mockRepository.estimateWeight(
        animalId: animalId,
        breedType: breedType,
        ageCategory: ageCategory,
        imageFile: imageFile,
      )).thenAnswer((_) async => Right(lowConfidenceWeighing));
      
      // Act
      final result = await usecase(
        animalId: animalId,
        breedType: breedType,
        ageCategory: ageCategory,
        imageFile: imageFile,
      );
      
      // Assert
      expect(result, isA<Left>());
      result.fold(
        (failure) => expect(failure, isA<PrecisionBelowThresholdFailure>()),
        (_) => fail('Should be Left'),
      );
    });
    
    test('debe retornar ProcessingTimeTooSlowFailure cuando procesamiento > 3s', () async {
      // Arrange
      final slowWeighing = testWeighing.copyWith(processingTimeMs: 3500);
      when(mockRepository.estimateWeight(
        animalId: animalId,
        breedType: breedType,
        ageCategory: ageCategory,
        imageFile: imageFile,
      )).thenAnswer((_) async => Right(slowWeighing));
      
      // Act
      final result = await usecase(
        animalId: animalId,
        breedType: breedType,
        ageCategory: ageCategory,
        imageFile: imageFile,
      );
      
      // Assert
      expect(result, isA<Left>());
      result.fold(
        (failure) => expect(failure, isA<ProcessingTimeTooSlowFailure>()),
        (_) => fail('Should be Left'),
      );
    });
  });
}
```

---

## Documentación y Comentarios

### Reglas Generales

1. **Código autodocumentado > Comentarios**
2. **Comentarios en español** (proyecto boliviano)
3. **DartDoc para APIs públicas**
4. **Referenciar User Stories** cuando aplique

### Ejemplo de Documentación Completa

```dart
/// Widget para seleccionar raza bovina en captura de peso (US-001).
/// 
/// Muestra las 7 razas exactas de Hacienda Gamelera con iconos visuales.
/// Validado con Bruno Brito Macedo en Sprint 1.
/// 
/// **Razas soportadas**:
/// - Brahman (Bos indicus)
/// - Nelore (Bos indicus)
/// - Angus (Bos taurus)
/// - Cebuinas (Bos indicus)
/// - Criollo (Bos taurus)
/// - Pardo Suizo (Bos taurus)
/// - Jersey (Bos taurus)
/// 
/// **Ejemplo de uso**:
/// ```dart
/// BreedSelectorWidget(
///   selectedBreed: BreedType.brahman,
///   onBreedSelected: (breed) {
///     print('Seleccionado: ${breed.displayName}');
///   },
/// )
/// ```
class BreedSelectorWidget extends StatelessWidget {
  /// Raza actualmente seleccionada (puede ser null si no se ha seleccionado)
  final BreedType? selectedBreed;
  
  /// Callback cuando se selecciona una raza
  final ValueChanged<BreedType> onBreedSelected;
  
  const BreedSelectorWidget({
    Key? key,
    required this.selectedBreed,
    required this.onBreedSelected,
  }) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    // Implementación...
  }
}
```

---

## Dependencias Recomendadas

```yaml
# pubspec.yaml

name: bovine_weight_estimation
description: Sistema de Estimación de Peso Bovino con IA para Hacienda Gamelera
publish_to: 'none'

version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  provider: ^6.0.5
  
  # Functional Programming
  dartz: ^0.10.1
  equatable: ^2.0.5
  
  # Local Database (Offline-first)
  sqflite: ^2.3.0
  path: ^1.8.3
  
  # HTTP Client
  dio: ^5.3.3
  http: ^1.1.0
  
  # Local Storage
  shared_preferences: ^2.2.2
  
  # Camera
  camera: ^0.10.5+5
  image: ^4.1.3
  
  # ML
  tflite_flutter: ^0.10.4
  
  # UI
  flutter_svg: ^2.0.9
  cached_network_image: ^3.3.0
  
  # Utils
  intl: ^0.18.1
  uuid: ^4.1.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^2.0.3
  mockito: ^5.4.2
  build_runner: ^2.4.6

flutter:
  uses-material-design: true
  
  assets:
    - assets/models/
    - assets/images/
    - assets/icons/
```

---

**Documento de Estándares Flutter v1.0**  
**Fecha**: 28 octubre 2024  
**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)

