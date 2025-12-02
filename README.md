# 🐄 Sistema de Estimación de Peso Bovino con IA

[![Flutter](https://img.shields.io/badge/Flutter-3.x-blue.svg)](https://flutter.dev/)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal.svg)](https://fastapi.tiangolo.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow_Lite-2.13+-orange.svg)](https://tensorflow.org/lite)
[![MongoDB](https://img.shields.io/badge/MongoDB-5+-green.svg)](https://mongodb.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Sistema inteligente de estimación de peso bovino mediante visión artificial, desarrollado específicamente para la Hacienda Gamelera en San Ignacio de Velasco, Bolivia.**

## 📋 Tabla de Contenidos

- [🎯 Visión General](#-visión-general)
- [🏢 Contexto del Cliente](#-contexto-del-cliente)
- [❌ Problema Actual](#-problema-actual)
- [✅ Solución Propuesta](#-solución-propuesta)
- [🏗️ Arquitectura Técnica](#️-arquitectura-técnica)
- [📊 Métricas de Éxito](#-métricas-de-éxito)
- [🚀 Quick Start](#-quick-start)
- [📱 Uso de la Aplicación](#-uso-de-la-aplicación)
- [📋 Cumplimiento Normativo](#-cumplimiento-normativo)
- [🔧 Desarrollo](#-desarrollo)
- [📚 Documentación](#-documentación)
- [👥 Stakeholders](#-stakeholders)
- [📄 Licencia](#-licencia)

## 🎯 Visión General

Este sistema revoluciona la estimación de peso bovino en la ganadería boliviana, reemplazando métodos tradicionales costosos y lentos con tecnología de inteligencia artificial. La solución permite estimar el peso de ganado bovino mediante captura continua de imágenes con dispositivos móviles, eliminando la necesidad de básculas tradicionales y reduciendo significativamente el tiempo de procesamiento.

### 🎪 Impacto del Proyecto

- **Reducción de tiempo**: De 2-3 días a <2 horas para 20 animales
- **Mejora de precisión**: De 5-20 kg de error a <5 kg con >95% precisión
- **Eliminación de costos**: Sin calibración diaria ni equipos especializados
- **Cumplimiento normativo**: Reportes automáticos para entidades bolivianas
- **Preparación competitiva**: Optimización para eventos ASOCEBU

## 🏢 Contexto del Cliente

### 🐄 Hacienda Gamelera

- **👨‍💼 Propietario**: Bruno Brito Macedo
- **📍 Ubicación**: San Ignacio de Velasco, Santa Cruz, Bolivia
- **🗺️ Coordenadas GPS**: 15°51′34.2′′S, 60°47′52.4′′W
- **📏 Extensión**: 48.5 hectáreas
- **🐄 Hato**: 500 cabezas de ganado bovino

### 🐮 Razas Soportadas

El sistema está optimizado para las **7 razas tropicales priorizadas** presentes en la Hacienda Gamelera y alineadas con el modelo ML entrenado:

| Raza | Descripción | Categoría |
|------|-------------|-----------|
| **Nelore** | Carne tropical dominante en Santa Cruz (≈42% del hato) | Cebuino (Carne) |
| **Brahman** | Cebuino versátil para cruzamientos y climas extremos | Cebuino (Carne) |
| **Guzerat** | Doble propósito (carne/leche) con gran rusticidad materna | Cebuino (Doble) |
| **Senepol** | Carne premium adaptada al calor, ideal para "steer" de alta calidad | Europeo (Carne) |
| **Girolando** | Lechera tropical (Holstein × Gyr) muy difundida en sistemas semi-intensivos | Europeo (Leche) |
| **Gyr lechero** | Lechera pura clave para genética tropical y sólidos altos | Cebuino (Leche) |
| **Sindi** | Lechera tropical compacta, de alta fertilidad y leche rica en sólidos | Cebuino (Leche) |

> **Nota**: Estas razas cubren el portafolio real de Santa Cruz (carne tropical + lecheras adaptadas) y están alineadas con el modelo ML genérico entrenado en Colab.

### 📅 Categorías de Edad

- **Terneros**: <8 meses
- **Vaquillonas/Torillos**: 6-18 meses  
- **Vaquillonas/Toretes**: 19-30 meses
- **Vacas/Toros**: >30 meses

## ❌ Problema Actual

### 🔧 Método Tradicional (Fórmula Schaeffer)

**Proceso actual**:

```text
Peso (kg) = (PT² × LC) / 10838
```

Donde:

- **PT**: Perímetro Torácico (cm)
- **LC**: Longitud del Cuerpo (cm)

### ⏱️ Cuellos de Botella Identificados

| Proceso | Tiempo | Personal | Problemas |
|---------|--------|----------|-----------|
| **Calibración diaria** | 30-45 min | 1 técnico | Limpieza, ajustes |
| **Convocatoria personal** | 1-2 horas | 3-4 personas | Traslados, coordinación |
| **Captura y aseguramiento** | 5-10 min/animal | 2-3 operarios | Manejo, contención |
| **Lecturas inestables** | 10-15 min extra | - | 10% reintentos |
| **Registro manual** | 30-45 min | 1 escribiente | Errores digitación |

### 📊 Impacto Real

- **Tiempo total**: 2-3 días para 20 animales
- **Error de estimación**: 5-20 kg por animal
- **Tasa de reintentos**: 10% (2-3 intentos por animal)
- **Limitaciones competitivas**: Solo 10 de 15 hembras procesadas para 3a Faena Técnica ASOCEBU 2024
- **Riesgos operativos**: Errores en dosificación médica, cruces subóptimos

## ✅ Solución Propuesta

### 🤖 Tecnología Innovadora

**Captura continua inteligente** (no fotografías manuales):

- **Frecuencia**: 10-15 fotogramas por segundo durante 3-5 segundos
- **Evaluación en tiempo real** de cada fotograma:
  - Nitidez (sharpness > 0.7)
  - Iluminación (brightness 0.4-0.8)
  - Contraste (contrast > 0.5)
  - Visibilidad de silueta (silhouette_visibility > 0.8)
  - Ángulo apropiado (angle_score > 0.6)
- **Selección automática**: Score ponderado (Silueta 40%, Nitidez 30%, Iluminación 20%, Ángulo 10%)
- **Modelo genérico**: TensorFlow Lite optimizado para todas las razas bovinas (7 razas tropicales)

### 🎯 Resultados Esperados

| Aspecto | Método Anterior | Sistema Actual | Mejora |
|---------|----------------|----------------|--------|
| **Tiempo de pesaje** | 2-3 días (20 animales) | <2 horas | **80% reducción** |
| **Error de estimación** | 5-20 kg (fórmula Schaeffer) | <5 kg | **75% mejora** |
| **Precisión** | ~85% | >95% (R² ≥ 0.95) | **12% mejora** |
| **Calibración diaria** | 30-45 minutos | Eliminada | **100% ahorro** |
| **Tasa de reintentos** | 10% (2-3 intentos) | 0% | **100% eliminación** |
| **Personal requerido** | 3-4 personas | 1 operador | **75% reducción** |

## 🏗️ Arquitectura Técnica

### 🛠️ Stack Tecnológico

| Componente | Tecnología | Responsabilidad |
|------------|------------|-----------------|
| **Mobile App** | Flutter 3.x + SQLite + TFLite | Captura, procesamiento local, UI |
| **Backend API** | FastAPI + Python 3.11+ | Lógica de negocio, integraciones |
| **ML Engine** | TensorFlow Lite | Inferencia de peso (modelo genérico multi-raza) |
| **Database** | MongoDB | Almacenamiento de datos |
| **Cloud Storage** | AWS S3 | Modelos ML y archivos |
| **Local DB** | SQLite | Funcionalidad offline |

### 🏛️ Componentes Principales

1. **Mobile App**: Captura continua, procesamiento local, UI intuitiva, sincronización
2. **Backend API**: Lógica de negocio, integraciones normativas, gestión de datos
3. **ML Engine**: Modelo genérico TensorFlow Lite (`generic-cattle-v1.0.0.tflite`) integrado y funcionando para todas las razas, inferencia optimizada
4. **Database**: MongoDB (cloud) + SQLite (local offline)
5. **Cloud Storage**: AWS S3 para modelos ML y manifest.json

> 📖 **Arquitectura detallada**: Ver [docs/design/](docs/design/) para diagramas completos y decisiones técnicas

### 🎨 Design System Moderno (Sprint 2)

**Tema**: Agro-Tech Premium - Diseño inspirado en líderes del mercado (AgriWebb, HerdWatch, CattleMax)

**Características visuales**:
- 🌈 **Paleta vibrante**: Verde Esmeralda (#10B981) + Azul Tech (#3B82F6) + Ámbar (#F59E0B)
- ✨ **Gradientes predefinidos**: Profundidad visual con transiciones suaves
- 🎴 **Dashboard moderno**: Estadísticas con glassmorphism + Grid de acciones
- 🎬 **Animaciones fluidas**: Scale, fade-in, transitions (200ms)
- 📐 **Atomic Design 100%**: 25+ componentes reutilizables (Atoms → Organisms)
- 🧩 **Composición pura**: Pages sin lógica de construcción de UI
- 🔧 **Extension methods**: Estado → UI mapping cohesivo

**Componentes destacados**:
- `GradientCard` - Cards con gradientes configurables
- `GlassCard` - Glassmorphism con blur effect
- `AnimatedScaleButton` - Bounce effect al tocar
- `ActionTile` - Tiles de acción con iconos grandes
- `StatCard` - Estadísticas con glass effect

> 🎨 **Design System completo**: Ver [docs/design/ui-design-system.md](docs/design/ui-design-system.md)

## 📊 Métricas de Éxito

### 🎯 Objetivos del Proyecto

| Métrica | Objetivo | Estado |
|---------|----------|--------|
| **Precisión** | ≥95% (R² ≥ 0.95) | ✅ Validado |
| **Error absoluto** | <5 kg por animal | ✅ Validado |
| **Tiempo procesamiento** | <3 segundos | ✅ Validado |
| **Tiempo por lote** | <2 horas (20 animales) | ✅ Validado |
| **Funcionalidad offline** | 100% | ✅ Implementado |
| **Cumplimiento normativo** | SENASAG/REGENSA/ASOCEBU | ✅ Implementado |

### 📈 Validación Técnica

- **Coeficiente de determinación (R²)**: ≥0.95
- **Error absoluto promedio**: <5 kg por animal
- **Tiempo de captura y procesamiento**: <3 segundos por estimación
- **Disponibilidad del sistema**: >99% uptime offline
- **Cobertura de razas**: 7 razas bovinas soportadas

## 🚀 Quick Start

### ⚡ Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/your-org/bovine-weight-estimation.git
cd bovine-weight-estimation

# 2. Backend (FastAPI + MongoDB)
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 3. Mobile App (Flutter)
cd ../mobile
flutter pub get
flutter run
```

### 🎯 ¿Qué hace el sistema?

- **Captura continua**: 10-15 FPS durante 3-5 segundos
- **IA automática**: Selecciona el mejor fotograma y estima peso
- **Precisión**: >95% con error <5 kg
- **Offline-first**: Funciona sin conexión a internet
- **Tiempo**: <2 horas para 20 animales (vs 2-3 días tradicional)

## 📱 Uso de la Aplicación

### 🎬 Flujo de Captura de Peso

1. **Selección de Animal**: Buscar por caravana o nombre
2. **Captura Continua**: Apuntar cámara (10-15 FPS, 3-5 segundos)
3. **Procesamiento IA**: Selección automática del mejor fotograma
4. **Resultado**: Peso estimado con confianza >95%

### 📊 Reportes Automáticos

- **SENASAG**: Trazabilidad ganadera
- **REGENSA**: Cumplimiento normativo (capítulos 3.10 y 7.1)
- **ASOCEBU**: Datos para competencias ganaderas

## 📋 Cumplimiento Normativo

### 🏛️ Entidades Regulatorias Bolivianas

#### 📋 SENASAG

- **Trazabilidad ganadera** obligatoria
- **Reportes de inventario** (PDF/CSV/XML)
- **Certificados digitales** de trazabilidad
- **Frecuencia**: Mensual/trimestral según normativa

#### 📜 REGENSA (Capítulos 3.10 y 7.1)

- **Integración sistema Gran Paitití** (plataforma gubernamental)
- **Guía de Movimiento Animal (GMA)** digital
- **Registro obligatorio** con timestamp y ubicación GPS
- **Requisitos infraestructura**: rampas, corrales, desinfección

#### 🏆 ASOCEBU

- **Datos históricos** para competencias ganaderas
- **Certificaciones de peso** para participación en ferias
- **Preparación competitiva** optimizada

> 📖 **Detalles normativos**: Ver [docs/architecture/01-system-context.md](docs/architecture/01-system-context.md) para requisitos específicos

## 🔧 Desarrollo

### 🏗️ Estructura del Proyecto

```text
bovine-weight-estimation/
├── 📱 mobile/          # Aplicación Flutter
│   └── README.md       # Guía del proyecto móvil
├── 🐍 backend/         # API FastAPI  
│   └── README.md       # Guía del backend
├── 🤖 ml-training/     # Entrenamiento de modelos
│   └── README.md       # Guía de ML Training
└── 📚 docs/            # Documentación técnica completa
    ├── design/         # Arquitectura y diseño
    ├── product/        # Product Backlog, DoD
    ├── sprints/        # Documentación de sprints
    ├── standards/      # Estándares de desarrollo
    ├── tools/          # Setup y herramientas
    └── vision/         # Visión y contexto del sistema
```

### 📂 READMEs por Proyecto

Cada proyecto tiene su propia documentación específica:

- **📱 Mobile App**: [mobile/README.md](mobile/README.md) - Setup Flutter, arquitectura Clean, estructura de carpetas
- **🐍 Backend API**: [backend/README.md](backend/README.md) - Setup FastAPI, endpoints, MongoDB
- **🤖 ML Training**: [ml-training/README.md](ml-training/README.md) - Entrenamiento, MLflow, DVC, exportación TFLite

### 🧪 Testing

```bash
# Backend
cd backend && pytest tests/ --cov=app

# Flutter  
cd mobile && flutter test --coverage

# ML Training
cd ml-training && pytest tests/ -v
```

### 📝 Estándares de Desarrollo

- **📱 Flutter**: [docs/standards/flutter-standards.md](docs/standards/flutter-standards.md)
- **🐍 Python Backend**: [docs/standards/python-standards.md](docs/standards/python-standards.md)
- **🤖 ML Training**: [docs/standards/ml-training-standards.md](docs/standards/ml-training-standards.md)
- **🏗️ Arquitectura**: [docs/standards/architecture-standards.md](docs/standards/architecture-standards.md)
- **🔄 Git Workflow**: [docs/standards/git-workflow.md](docs/standards/git-workflow.md)
- **🧪 Testing**: [docs/standards/testing-standards.md](docs/standards/testing-standards.md)
- **🚀 Deployment**: [docs/standards/deployment-standards.md](docs/standards/deployment-standards.md)

### 🎯 Metodología

- **Scrum**: Sprints iterativos con historias de usuario (ver [docs/product/](docs/product/))
- **Clean Architecture**: Separación clara de responsabilidades (ver [docs/design/](docs/design/))
- **SOLID**: Principios de diseño orientado a objetos
- **Atomic Design**: Componentes reutilizables y escalables (Flutter)
- **Provider**: Gestión de estado reactiva en Flutter

## 📚 Documentación

### 🎯 Visión del Producto

- [📋 Contexto del Sistema](docs/vision/01-system-context.md) - Negocio y stakeholders
- [🏗️ Visión de Arquitectura](docs/vision/02-architecture-vision.md) - Visión arquitectónica
- [🧩 Áreas Funcionales](docs/vision/03-areas-funcionales.md) - Alcance por áreas
- [🗄️ Modelo de Dominio](docs/vision/04-domain-model.md) - Modelo conceptual

### 📋 Producto (Scrum)

- [📝 Product Backlog](docs/product/product-backlog.md) - User stories priorizadas (versión ejecutiva)
- [📄 Product Backlog Detallado](docs/product/product-backlog-detailed.md) - Formato académico 3C completo
- [✅ Definition of Done](docs/product/definition-of-done.md) - Criterios de completitud por nivel

### 🚀 Sprints (Evolución del Proyecto)

- [🎯 Sprint 1 - Validación Core](docs/sprints/sprint-01/sprint-goal.md) - Captura, selección, estimación offline (✅ Completado)
- [📊 Sprint 2 - Modernización + Análisis](docs/sprints/sprint-02/sprint-goal.md) - UI/UX moderna, análisis, sincronización (✅ Completado)
  - [📈 Sprint 2 Progress](docs/sprints/sprint-02/sprint-progress.md) - Detalles de modernización UI/UX
- [🔗 Sprint 3 - Integraciones](docs/sprints/sprint-03/sprint-goal.md) - SENASAG, REGENSA, ASOCEBU (🔄 60% completado)
  - [📈 Sprint 3 Progress](docs/sprints/sprint-03/sprint-progress.md) - Reportes backend completos, integraciones normativas en progreso

### 🏗️ Diseño y Arquitectura

- [🎯 Decisiones Arquitectónicas (ADRs)](docs/design/architecture-decisions.md) - Decisiones clave registradas
- [🗄️ Esquema de Base de Datos](docs/design/database-schema.md) - MongoDB y SQLite
- [🎨 UI Design System](docs/design/ui-design-system.md) - Paleta, componentes, Atomic Design

### 📖 Estándares de Desarrollo

- [📋 Índice de Estándares](docs/standards/README.md) - Resumen y quick reference
- [📱 Flutter Standards](docs/standards/flutter-standards.md) - Clean Architecture, Atomic Design, Provider
- [🐍 Python Backend Standards](docs/standards/python-standards.md) - FastAPI, Pydantic, Type Hints
- [🤖 ML Training Standards](docs/standards/ml-training-standards.md) - TensorFlow, MLflow, DVC
- [🏗️ Architecture Standards](docs/standards/architecture-standards.md) - Patrones, NFRs, compliance
- [🔄 Git Workflow](docs/standards/git-workflow.md) - Git Flow, Conventional Commits
- [🧪 Testing Standards](docs/standards/testing-standards.md) - Estrategia de testing, cobertura
- [🚀 Deployment Standards](docs/standards/deployment-standards.md) - CI/CD, Docker, AWS

### 🛠️ Herramientas y Setup

- [🔧 Development Setup](docs/tools/development-setup.md) - Configuración del entorno
- [📅 Herramientas por Sprint](docs/tools/herramientas-por-sprint.md) - Roadmap de herramientas

### 🔗 Enlaces Útiles

- [📖 Documentación Flutter](https://docs.flutter.dev/)
- [🚀 Documentación FastAPI](https://fastapi.tiangolo.com/)
- [🤖 TensorFlow Lite](https://tensorflow.org/lite)
- [🍃 MongoDB](https://docs.mongodb.com/)
- [📊 MLflow](https://mlflow.org/docs/latest/index.html)
- [📦 DVC](https://dvc.org/doc)

## 🤝 Contribución

1. **Fork** el repositorio
2. **Crear** rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -m 'feat: agregar funcionalidad'`)
4. **Push** y **Pull Request**

> 📋 **Guías**: Seguir [estándares](docs/standards/), escribir tests, usar commits semánticos

## 👥 Stakeholders

### 🏢 Cliente Principal

- **🐄 Bruno Brito Macedo** - Propietario, Hacienda Gamelera

### 🏛️ Entidades Regulatorias

- **📋 SENASAG** - Servicio Nacional de Sanidad Agropecuaria e Inocuidad Alimentaria
- **📜 REGENSA** - Registro General de Sanidad Agropecuaria  
- **🏆 ASOCEBU** - Asociación de Criadores de Cebuinos

### 👨‍💻 Equipo de Desarrollo

- **🎯 Product Owner**: Miguel Angel Escobar Lazcano
- **🔄 Scrum Master**: Rodrigo Escobar Morón
- **👨‍💻 Desarrolladores**: Equipo de desarrollo especializado

### 🌍 Impacto Social

- **🏞️ Ganaderos rurales** de Bolivia
- **📈 Sector ganadero** nacional
- **🔬 Investigación** en IA aplicada a ganadería

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

---

## 🐄 Desarrollado con ❤️ para la ganadería boliviana

> **Sistema de Estimación de Peso Bovino con IA - Hacienda Gamelera**

[📧 Contacto](mailto:contact@bovine-weight-estimation.com) • [🌐 Sitio Web](https://bovine-weight-estimation.com)
