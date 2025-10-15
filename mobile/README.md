# Mobile App - Sistema de Estimación de Peso Bovino

Aplicación móvil Flutter para Hacienda Gamelera.

## 🏗️ Arquitectura

**Clean Architecture** con 3 capas:

```
lib/
├── core/           # Constantes, utilidades, casos de uso base
├── data/           # DataSources, Models, Repositories (implementación)
├── domain/         # Entities, Repositories (interfaces), UseCases
└── presentation/   # Pages, Providers, Widgets (Atomic Design)
```

## 🎯 Características Sprint 1

- ✅ US-001: Captura continua de fotogramas (10-15 FPS)
- ✅ US-002: Selección automática del mejor fotograma
- ✅ US-003: Estimación de peso con IA offline (TFLite)

## 📱 Requisitos

- Flutter 3.35.6+
- Dart 3.9.2+
- iOS 12.0+ / Android 8.0+

## 🚀 Instalación

```bash
flutter pub get
flutter run
```

## 🧪 Testing

```bash
flutter test
flutter test --coverage
```

## 📦 Build

```bash
# Android
flutter build apk --release

# iOS
flutter build ios --release
```

## 🔧 Configuración

Ver `pubspec.yaml` para dependencias y configuración.

## 📊 Datos Críticos

**7 Razas**: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey  
**4 Categorías de Edad**: Terneros, Vaquillonas/Torillos, Vaquillonas/Toretes, Vacas/Toros  
**Métricas**: Precisión ≥95%, Error <5kg, Tiempo <3s
