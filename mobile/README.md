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

**7 Razas Soportadas**:
- Brahman (Bos indicus)
- Nelore (Bos indicus)
- Angus (Bos taurus)
- Cebuinas (Híbrido)
- Criollo (Bos taurus)
- Pardo Suizo (Bos taurus)
- Jersey (Bos taurus)

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

**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Universidad**: UAGRM (Universidad Autónoma Gabriel René Moreno)  
**Materia**: Taller de Grado  
**Empresa**: Agrocom
