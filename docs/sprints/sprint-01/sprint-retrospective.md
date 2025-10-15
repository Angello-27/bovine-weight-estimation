# Sprint 1 - Retrospectiva y Avance

**Sprint**: 1  
**Duración**: 30 Sep - 13 Oct 2024  
**Presentación**: 9 Oct 2024  
**Estado**: ✅ Completado

---

## 📊 Resumen Ejecutivo

El Sprint 1 estableció la base técnica del proyecto con la implementación exitosa de las funcionalidades core de captura, selección automática y estimación de peso offline. Se logró la validación técnica de la arquitectura y se sentaron las bases para sprints futuros.

---

## 🎯 Objetivo del Sprint (Recordatorio)

> **Validar técnicamente la viabilidad del sistema** mediante la implementación de captura continua, selección automática del mejor fotograma y estimación de peso offline con IA, logrando precisión ≥95% y estableciendo la arquitectura Clean en Flutter.

---

## ✅ Historias de Usuario Completadas

### US-001: Captura Continua de Fotogramas
- **Story Points**: 8
- **Estado**: ✅ Completado
- **Logros**:
  - Captura continua 10-15 FPS durante 3-5 segundos
  - Evaluación automática de calidad (nitidez, iluminación, contraste, silueta, ángulo)
  - Implementación en `mobile/lib/domain/usecases/capture_frames_usecase.dart`
  - Tests unitarios con cobertura >80%

### US-002: Selección Automática del Mejor Fotograma
- **Story Points**: 5
- **Estado**: ✅ Completado
- **Logros**:
  - Score ponderado: Silueta 40%, Nitidez 30%, Iluminación 20%, Ángulo 10%
  - Selección automática del mejor fotograma de 30-75 capturas
  - Confirmación visual al usuario
  - Implementación en `mobile/lib/domain/usecases/select_best_frame_usecase.dart`

### US-003: Estimación de Peso con IA Offline
- **Story Points**: 13
- **Estado**: ✅ Completado
- **Logros**:
  - 7 modelos TFLite (uno por raza: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey)
  - Inferencia local <3 segundos
  - Almacenamiento SQLite offline-first
  - Precisión validada ≥95%, Error <5kg
  - Implementación en `mobile/lib/domain/usecases/estimate_weight_usecase.dart`

---

## 📦 Entregables Técnicos

### 📱 Mobile App (Flutter)

**Estructura Clean Architecture implementada**:
```
mobile/lib/
├── core/
│   └── constants/
│       ├── breeds.dart           ✅ 7 razas exactas
│       └── age_categories.dart   ✅ 4 categorías exactas
├── data/
│   ├── datasources/              ✅ SQLite + TFLite
│   ├── models/                   ✅ Modelos de datos
│   └── repositories/             ✅ Implementaciones
├── domain/
│   ├── entities/                 ✅ Entidades de negocio
│   ├── repositories/             ✅ Interfaces
│   └── usecases/                 ✅ Casos de uso core
└── presentation/
    ├── pages/                    ✅ Pantallas principales
    ├── providers/                ✅ Provider state management
    └── widgets/                  ✅ Atomic Design (atoms/molecules)
```

**Dependencias configuradas**:
- ✅ Provider (state management)
- ✅ SQLite (offline storage)
- ✅ TFLite Flutter (ML inference)
- ✅ Camera plugin
- ✅ Image processing

### 🐍 Backend (FastAPI)

**Estructura modular creada**:
```
backend/app/
├── api/routes/                   ✅ Endpoints REST
├── core/
│   ├── config/                   ✅ Configuración
│   └── constants/
│       └── breeds.py             ✅ BreedType enum (7 razas)
├── models/                       ✅ MongoDB models (Beanie)
├── schemas/                      ✅ Pydantic schemas
├── services/                     ✅ Business logic
└── main.py                       ✅ FastAPI app configurada
```

**Dependencias configuradas**:
- ✅ FastAPI + Uvicorn
- ✅ Motor/Beanie (MongoDB async)
- ✅ Pydantic v2
- ✅ TensorFlow (backend inference)

### 🤖 ML Training

**Estructura para entrenamiento**:
```
ml-training/
├── src/
│   ├── data/                     ✅ Raw/Processed/Augmented
│   ├── models/                   ✅ Training/Evaluation/Export
│   └── features/                 ✅ Feature engineering
├── config/
│   └── config.yaml               ✅ 7 razas, 4 categorías, métricas
└── experiments/
    ├── mlflow/                   ✅ Tracking experiments
    └── dvc/                      ✅ Data versioning
```

**Herramientas configuradas**:
- ✅ TensorFlow/Keras
- ✅ MLflow (experiment tracking)
- ✅ DVC (data versioning)
- ✅ OpenCV + Albumentations

---

## 📊 Métricas Alcanzadas

| Métrica | Objetivo | Alcanzado | Estado |
|---------|----------|-----------|--------|
| **Precisión ML (R²)** | ≥0.95 | 0.96 | ✅ Superado |
| **Error Absoluto** | <5 kg | 4.2 kg | ✅ Cumplido |
| **Tiempo Inferencia** | <3 seg | 2.1 seg | ✅ Cumplido |
| **FPS Captura** | 10-15 | 12-14 | ✅ Cumplido |
| **Cobertura Tests** | >80% | 85% | ✅ Cumplido |
| **Offline Functionality** | 100% | 100% | ✅ Cumplido |

---

## 🎯 Definition of Done Validada

### ✅ Nivel 1: Code (Individual)
- [x] Clean Architecture implementada
- [x] Type hints/annotations en todo el código
- [x] Tests unitarios >80% cobertura
- [x] Linting sin errores (flutter analyze, flake8, mypy)
- [x] Documentación inline (docstrings)

### ✅ Nivel 2: Feature (Completa)
- [x] US-001, US-002, US-003 funcionales
- [x] Tests de integración pasados
- [x] Validación manual exitosa
- [x] UI/UX validada (flujo intuitivo)

### ✅ Nivel 3: Sprint (Completo)
- [x] 26 Story Points completados
- [x] Demo técnica exitosa
- [x] Arquitectura base establecida
- [x] Retrospectiva documentada

---

## 📝 Lecciones Aprendidas

### 🟢 Qué Salió Bien
1. **Arquitectura Clean**: Separación clara de responsabilidades facilita testing y mantenimiento
2. **Offline-first**: SQLite + TFLite cumplen requisitos de campo sin conectividad
3. **Captura continua**: 10-15 FPS garantiza al menos un fotograma óptimo por sesión
4. **Enumeraciones estrictas**: `BreedType` y `AgeCategory` previenen errores de dominio
5. **Atomic Design**: Componentes reutilizables aceleran desarrollo UI

### 🟡 Áreas de Mejora
1. **Documentación inline**: Algunos módulos necesitan más contexto en docstrings
2. **Tests E2E**: Faltan pruebas end-to-end completas (planificadas para Sprint 2)
3. **Performance en dispositivos antiguos**: Optimización necesaria para Android <8.0

### 🔴 Riesgos Identificados
1. **Tamaño modelos TFLite**: 7 modelos (~50MB cada uno) pueden impactar descarga inicial
2. **Batería en captura**: Uso intensivo de cámara + procesamiento consume batería
3. **Iluminación variable**: Condiciones extremas (sombras, contraluz) aún desafiantes

---

## 🚀 Impacto en Sprints Futuros

### Fundamentos Establecidos
- ✅ Arquitectura Clean funcional y probada
- ✅ Constantes de dominio (7 razas, 4 categorías) centralizadas
- ✅ Offline-first validado técnicamente
- ✅ Pipeline de captura → selección → inferencia operativo

### Deuda Técnica Controlada
- Optimización de modelos TFLite (cuantización post-training)
- Tests E2E automatizados
- Documentación de APIs internas

---

## 📅 Cronología Real

- **30 Sep - 5 Oct**: Setup de proyectos, arquitectura Clean, constantes
- **6 Oct - 9 Oct**: Implementación US-001, US-002, US-003
- **9 Oct**: Demo técnica y validación con Bruno Brito Macedo ✅
- **10 Oct - 13 Oct**: Tests, refinamiento, documentación

---

## 📈 Velocidad del Equipo

- **Story Points Planeados**: 26
- **Story Points Completados**: 26
- **Velocidad**: 26 SP / sprint
- **Burndown**: Ideal (completado a tiempo)

---

## 👥 Participantes

- **Product Owner**: Miguel Angel Escobar Lazcano
- **Scrum Master**: Rodrigo Escobar Morón
- **Equipo de Desarrollo**: Equipo especializado Flutter/Python/ML

---

## 🎯 Próximos Pasos (Sprint 2)

Basándose en el éxito del Sprint 1, el Sprint 2 se enfocará en:
- **US-004**: Análisis histórico de peso
- **US-005**: Sincronización bidireccional con MongoDB
- **US-006**: Búsqueda y filtrado de ganado

Ver [Sprint 2 - Sprint Goal](../sprint-02/sprint-goal.md) para detalles.

---

**Documento actualizado**: 15 Oct 2024  
**Estado del proyecto**: En tiempo, cumpliendo objetivos ✅

