# Mobile App - Sistema de Estimación de Peso Bovino

Aplicación móvil Flutter para **Agrocom** (Taller de Grado - UAGRM).

## 🏗️ Arquitectura

**Clean Architecture** con 4 capas:

```
lib/
├── core/           # Configuración, Theme, Constantes, DI
│   ├── config/     # AppConfig, DependencyInjection
│   ├── theme/      # AppColors, AppSpacing, AppTheme
│   ├── constants/  # Breeds, AgeCategories
│   └── routes/     # AppRouter
│
├── data/           # DataSources, Models, Repositories (implementación)
│   ├── datasources/    # Local (SQLite, TFLite), Remote (API)
│   ├── models/         # Modelos de datos (JSON serialization)
│   └── repositories/   # Implementación de interfaces del Domain
│
├── domain/         # Entities, Repositories (interfaces), UseCases
│   ├── entities/       # Cattle, Frame, WeightEstimation
│   ├── repositories/   # Interfaces puras
│   └── usecases/       # Lógica de negocio
│
└── presentation/   # Pages, Providers, Widgets (Atomic Design)
    ├── pages/          # Pantallas completas (composición pura)
    ├── providers/      # State management (Provider pattern)
    └── widgets/        # Atomic Design (Atoms → Organisms)
```

## 🎨 Design System (Sprint 2)

### **Paleta de Colores**

**Tema**: Agro-Tech Premium (Verde Esmeralda + Azul Tecnológico)  
**Inspiración**: AgriWebb, HerdWatch, CattleMax

- 🟢 **Primario**: Verde Esmeralda `#10B981` (Naturaleza + Innovación)
- 🔵 **Secundario**: Azul Tech `#3B82F6` (Precisión + Tecnología)
- 🟡 **Acento**: Ámbar `#F59E0B` (Alertas + CTAs)
- ✅ **Success**: `#10B981` | ❌ **Error**: `#EF4444`
- 🔶 **Warning**: `#F59E0B` | ℹ️ **Info**: `#3B82F6`

### **Atomic Design**

**25+ componentes reutilizables**:
- **Atoms**: `GradientCard`, `GlassCard`, `AnimatedScaleButton`, `FadeInWidget`
- **Molecules**: `StatCard`, `ActionTile`, `StatusCard`, `BreedDropdown`
- **Organisms**: `BreedSelectorGrid`, `CattleRegistrationForm`, `CaptureConfigSection`
- **Pages**: Composición pura 100% sin métodos `_build...()`

Ver documentación completa en: `docs/design/ui-design-system.md`

## 🎯 Características Implementadas

### **Sprint 1** ✅
- US-001: Captura continua de fotogramas (10-15 FPS, 3-5s)
- US-002: Estimación de peso con IA offline (TFLite, 7 razas)
- US-003: Registro automático de animales

### **Sprint 2** ✅
- Modernización UI/UX (paleta vibrante, gradientes, animaciones)
- Dashboard moderno con estadísticas
- Refactorización Atomic Design 100%
- Extension methods pattern para estado → UI
- Glassmorphism y efectos visuales modernos

### **Sprint 3** ✅
- US-005: Sincronización Offline-First con estrategia Last-Write-Wins
- Endpoints de sincronización (health, cattle, weight-estimations)

## 📱 Requisitos

- **Flutter**: 3.35.6+
- **Dart**: 3.9.2+
- **Android**: 8.0+ (API 26+, minSdk: 26)
- **iOS**: 12.0+
- **JDK**: 17+ (para compilación Android)

## 🚀 Instalación

```bash
# Obtener dependencias
flutter pub get

# Generar mocks para testing
flutter pub run build_runner build --delete-conflicting-outputs

# Ejecutar en desarrollo
flutter run

# Ejecutar en dispositivo específico
flutter run -d <device_id>
```

## 🧪 Testing

```bash
# Todos los tests
flutter test

# Tests con coverage
flutter test --coverage

# Tests específicos
flutter test test/domain/
```

## 📦 Build

```bash
# Android APK
flutter build apk --release

# Android App Bundle (Google Play)
flutter build appbundle --release

# iOS
flutter build ios --release
```

## 🔧 Configuración

**Package name**: `com.agrocom.bovine_weight`

**Permisos**:
- 📸 **Cámara**: Just-in-time (solo al capturar)
- 📍 **Ubicación**: Opcional (para metadatos GPS)

**Base de datos**: SQLite offline-first

**IA**: TensorFlow Lite (7 modelos por raza, <50MB total)

## 📊 Datos del Sistema

**7 Razas Soportadas** (Tropicales Priorizadas):
- **Nelore** – Carne tropical dominante en Santa Cruz (≈42% del hato)
- **Brahman** – Cebuino versátil para cruzamientos y climas extremos
- **Guzerat** – Doble propósito (carne/leche) con gran rusticidad materna
- **Senepol** – Carne premium adaptada al calor, ideal para "steer" de alta calidad
- **Girolando** – Lechera tropical (Holstein × Gyr) muy difundida en sistemas semi-intensivos
- **Gyr lechero** – Lechera pura clave para genética tropical y sólidos altos
- **Sindi** – Lechera tropical compacta, de alta fertilidad y leche rica en sólidos

> Estas razas están alineadas con el modelo ML entrenado en Colab y cubren el portafolio real de Santa Cruz (carne tropical + lecheras adaptadas).

**4 Categorías de Edad**:
- Terneros (0-6 meses)
- Vaquillonas/Torillos (7-12 meses)
- Vaquillonas/Toretes (13-24 meses)
- Vacas/Toros (25+ meses)

**Métricas de Precisión**:
- R² ≥ 0.95 (correlación con báscula)
- MAE < 5 kg (error absoluto medio)
- Tiempo procesamiento < 3s

---

## 📚 Documentación

### Guías de Integración

1. **[Guía de Sincronización](./docs/integration/FLUTTER_SYNC_GUIDE.md)**
   - Flujo completo de sincronización offline-first
   - Endpoints de sync (health, cattle, weight-estimations)
   - Estrategia Last-Write-Wins
   - Manejo de errores y reintentos

2. **[Guía de Integración API Completa](./docs/integration/FLUTTER_API_INTEGRATION.md)** ⭐ **NUEVO**
   - Todos los endpoints disponibles para Flutter
   - Autenticación JWT
   - Machine Learning (predict, models/status)
   - CRUD de animales
   - Historial de pesajes
   - Reportes (PDF/Excel)
   - Alertas y cronograma
   - Ejemplos de implementación en Dart

3. **[Análisis del Estado Actual](./docs/integration/FLUTTER_APP_STATUS_ANALYSIS.md)** 📊 **NUEVO**
   - Estado de implementación de endpoints (35% completo)
   - Análisis detallado por categoría
   - Plan de implementación recomendado (6 fases)
   - Checklist de tareas pendientes
   - Mejoras de infraestructura sugeridas

3. **[Guía de Integración API Backend](../docs/integration/API_INTEGRATION_GUIDE.md)**
   - Documentación completa del backend
   - Endpoints para Mobile y Web
   - Especificaciones técnicas

### Endpoints Pendientes de Implementar

Basado en la comparación con la API, estos endpoints aún no están documentados en Flutter:

#### ✅ Ya Documentados
- Sincronización (health, cattle, weight-estimations) - Ver `FLUTTER_SYNC_GUIDE.md`

#### ❌ Pendientes de Documentar/Implementar
- **Autenticación**: POST `/api/v1/auth/login` con manejo de JWT
- **Machine Learning**: 
  - POST `/api/v1/ml/predict` (predicción sin guardar)
  - GET `/api/v1/ml/models/status` (estado de modelos)
- **Gestión de Animales**:
  - POST `/api/v1/animals` (crear)
  - GET `/api/v1/animals` (listar con filtros)
  - GET `/api/v1/animals/{id}` (obtener)
  - PUT `/api/v1/animals/{id}` (actualizar)
  - DELETE `/api/v1/animals/{id}` (eliminar)
  - GET `/api/v1/animals/{id}/timeline` (timeline)
  - GET `/api/v1/animals/{id}/lineage` (linaje)
- **Historial de Pesajes**:
  - GET `/api/v1/weighings/animal/{id}` (historial)
  - GET `/api/v1/weighings/{id}` (detalle)
- **Reportes**:
  - POST `/api/v1/reports/traceability/{id}` (trazabilidad)
  - POST `/api/v1/reports/inventory` (inventario)
  - POST `/api/v1/reports/movements` (movimientos)
  - POST `/api/v1/reports/growth` (crecimiento)
- **Alertas**:
  - POST `/api/v1/alerts` (crear)
  - GET `/api/v1/alerts` (listar)
  - GET `/api/v1/alerts/today` (hoy)
  - GET `/api/v1/alerts/upcoming` (próximas)

> **Nota**: Todos estos endpoints están ahora documentados en [`FLUTTER_API_INTEGRATION.md`](./docs/integration/FLUTTER_API_INTEGRATION.md) con ejemplos de implementación en Dart.

---

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Universidad**: UAGRM (Universidad Autónoma Gabriel René Moreno)  
**Materia**: Taller de Grado  
**Empresa**: Agrocom
