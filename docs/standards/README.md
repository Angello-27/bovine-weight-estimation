# 📚 Estándares de Desarrollo

## Contexto del Proyecto

**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Ubicación**: San Ignacio de Velasco, Bolivia  
**Objetivo**: Sistema con precisión >95%, error <5 kg, funcionamiento offline

Este directorio contiene todos los estándares de desarrollo, arquitectura, testing y despliegue del proyecto. **Todos los desarrolladores DEBEN leer y seguir estos estándares antes de escribir código**.

---

## 📋 Índice de Estándares

### 1. [Arquitectura del Sistema](architecture-standards.md) 📐
**Qué cubre**:
- Arquitectura C4 (Contexto, Contenedores, Componentes)
- Clean Architecture (3 capas: Presentation → Domain → Data)
- Patrones de diseño (Repository, Use Case, Provider, Factory, Strategy)
- Estructura de carpetas (Mobile, Backend, ML Training)
- Requisitos no funcionales (Performance, Disponibilidad, Escalabilidad)
- Cumplimiento normativo (SENASAG, REGENSA, ASOCEBU)

**Cuándo leer**: PRIMERO, antes de cualquier desarrollo

**Conceptos clave**:
- ✅ Offline-first obligatorio
- ✅ Clean Architecture en todas las capas
- ✅ 7 razas bovinas EXACTAS (Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey)
- ✅ 4 categorías de edad EXACTAS
- ✅ Métricas OBLIGATORIAS (≥95%, <5kg, <3s)

---

### 2. [Estándares Flutter](flutter-standards.md) 📱
**Qué cubre**:
- Stack tecnológico (Provider, SQLite/Drift, Dio, TFLite, FL Chart)
- Estructura Clean Architecture en Flutter
- Constantes del dominio (breeds.dart, age_categories.dart, metrics.dart)
- Naming conventions (archivos, clases, variables, enums)
- Gestión de estado con Provider
- Manejo de errores con Either<L, R>
- Testing unitario, widget e integración
- Dependencias recomendadas (pubspec.yaml)

**Cuándo leer**: Antes de desarrollar funcionalidades móviles (US-001, US-002, US-003, US-004, US-006)

**Conceptos clave**:
- ✅ BreedType enum con 7 razas EXACTAS
- ✅ AgeCategory enum con 4 categorías EXACTAS
- ✅ Offline-first con SQLite como fuente primaria
- ✅ Validaciones automáticas siempre
- ✅ Comentarios en español, código en inglés

---

### 3. [Estándares Python/FastAPI](python-standards.md) 🐍
**Qué cubre**:
- Stack tecnológico (FastAPI, Pydantic v2, Motor+Beanie, httpx, reportlab)
- Estructura Clean Architecture en backend
- Constantes del dominio (breeds.py, age_categories.py, regulatory.py)
- Type hints obligatorios
- Pydantic schemas con validaciones
- Beanie ODM para MongoDB
- Testing con pytest y httpx
- Logging estructurado con loguru
- Dependency injection en FastAPI

**Cuándo leer**: Antes de desarrollar backend API (US-007, US-008, US-009)

**Conceptos clave**:
- ✅ Type hints en TODAS las funciones
- ✅ BreedType enum con 7 razas EXACTAS
- ✅ Pydantic validaciones automáticas
- ✅ Docstrings con Google Style
- ✅ Tests con cobertura >80%

---

### 4. [Estándares ML Training](ml-training-standards.md) 🤖
**Qué cubre**:
- Stack tecnológico (TensorFlow 2.13, MLflow, DVC, albumentations, OpenCV)
- Estructura de carpetas ML (data, notebooks, src, experiments, models)
- 7 modelos TFLite (uno por raza)
- Métricas obligatorias (R² ≥0.95, MAE <5kg, MAPE <5%)
- Arquitectura CNN (MobileNetV2 transfer learning)
- Preprocesamiento con OpenCV
- Data augmentation con albumentations
- MLflow tracking de experimentos
- Exportación a TFLite optimizado
- Validación en campo (≥50 animales)

**Cuándo leer**: Antes de entrenar/actualizar modelos ML (US-002)

**Conceptos clave**:
- ✅ UN modelo por raza (7 modelos TFLite)
- ✅ R² ≥0.95 obligatorio para producción
- ✅ MAE <5 kg obligatorio
- ✅ MLflow tracking SIEMPRE
- ✅ Validación con Bruno en Hacienda Gamelera

---

### 5. [Git Workflow](git-workflow.md) 🔄
**Qué cubre**:
- Git Flow strategy (main, development, feature, bugfix, hotfix, release)
- Conventional Commits (feat, fix, docs, perf, test, etc.)
- Branch naming (feature/US-XXX-descripcion)
- Pull Request template
- Commits por Sprint (ejemplos reales)
- .gitignore completo
- Tags y releases (SemVer)
- Changelog
- Branch protection rules

**Cuándo leer**: Antes de crear CUALQUIER branch o commit

**Conceptos clave**:
- ✅ Conventional Commits OBLIGATORIO
- ✅ Branch naming con User Story (feature/US-007-reportes-senasag)
- ✅ Commits en español descriptivos
- ✅ Referencia a US en footer
- ✅ SemVer para releases (v1.0.0)

---

### 6. [Estándares de Testing](testing-standards.md) 🧪
**Qué cubre**:
- Pirámide de testing (60% unit, 30% integration, 10% E2E)
- Herramientas (flutter_test, mockito, pytest, httpx)
- Tests por capa (Domain 100%, Services 90%, API 80%)
- Integration tests (API + MongoDB)
- E2E tests con integration_test
- Testing de métricas ML (R², MAE validación)
- Fixtures reutilizables (conftest.py)
- Coverage requirements (>80% obligatorio)
- CI con GitHub Actions
- Protocolo de validación con Bruno

**Cuándo leer**: Antes de escribir tests (SIEMPRE junto con código)

**Conceptos clave**:
- ✅ Domain Layer: 100% cobertura obligatorio
- ✅ Overall: >80% cobertura mínimo
- ✅ Tests ANTES de merge a development
- ✅ Validación con Bruno en campo obligatoria
- ✅ Métricas ML testeadas automáticamente

---

### 7. [Estándares de Despliegue](deployment-standards.md) 🚀
**Qué cubre**:
- Stack infraestructura (Docker, AWS S3/EC2, MongoDB Atlas, NGINX)
- Docker Compose (local development)
- Dockerfiles (Backend, MLflow)
- Ambientes (Development, Staging, Production)
- CI/CD pipeline completo (GitHub Actions)
- Backups automáticos (rclone + S3)
- NGINX configuration con SSL
- Health checks
- Deployment steps (manual y automatizado)
- Rollback plan
- Disaster recovery plan
- Monitoreo con Prometheus + Grafana
- Security checklist

**Cuándo leer**: Antes de deploy a staging/production

**Conceptos clave**:
- ✅ Docker Compose para todos los ambientes
- ✅ CI/CD automatizado (GitHub Actions)
- ✅ Backups diarios automáticos a S3
- ✅ RTO <2 horas, RPO <24 horas
- ✅ Zero downtime deployments

---

## 🎯 Datos Críticos del Dominio (Memorizar)

### 7 Razas Bovinas de Hacienda Gamelera (EXACTAS - NO MODIFICAR)

1. **Brahman** (Bos indicus) - Modelo: `brahman-v1.0.0.tflite`
2. **Nelore** (Bos indicus) - Modelo: `nelore-v1.0.0.tflite`
3. **Angus** (Bos taurus) - Modelo: `angus-v1.0.0.tflite`
4. **Cebuinas** (Bos indicus) - Modelo: `cebuinas-v1.0.0.tflite`
5. **Criollo** (Bos taurus) - Modelo: `criollo-v1.0.0.tflite`
6. **Pardo Suizo** (Bos taurus) - Modelo: `pardo-suizo-v1.0.0.tflite`
7. **Jersey** (Bos taurus) - Modelo: `jersey-v1.0.0.tflite`

### 4 Categorías de Edad (EXACTAS - NO MODIFICAR)

1. **Terneros** (<8 meses)
2. **Vaquillonas/Torillos** (6-18 meses)
3. **Vaquillonas/Toretes** (19-30 meses)
4. **Vacas/Toros** (>30 meses)

### Métricas del Sistema (OBLIGATORIAS)

- **Precisión ML**: ≥95% (R² ≥ 0.95)
- **Error absoluto**: <5 kg (MAE < 5 kg)
- **Error porcentual**: <5% (MAPE < 5%)
- **Tiempo procesamiento**: <3 segundos
- **Captura continua**: 10-15 FPS durante 3-5 segundos (30-75 fotogramas)
- **Tiempo para 20 animales**: <2 horas (vs 2-3 días tradicional)
- **Reducción de tiempo**: 80%

### Entidades Regulatorias Bolivianas

- **SENASAG**: Trazabilidad ganadera, reportes automáticos PDF/CSV/XML
- **REGENSA**: Capítulos 3.10 (infraestructura) y 7.1 (sanitario), GMA digital
- **Gran Paitití**: Sistema gubernamental, API REST, GMA con código QR
- **ASOCEBU**: Competencias ganaderas, exportación datos, 3ª Faena Técnica 2024

---

## ✅ Checklist Antes de Codificar

### SIEMPRE Validar:

- [ ] ¿Estoy usando las 7 razas EXACTAS? (No genéricos, no otras razas)
- [ ] ¿Estoy usando las 4 categorías de edad EXACTAS?
- [ ] ¿Estoy validando métricas ≥95%, <5kg, <3s?
- [ ] ¿Estoy siguiendo Clean Architecture (3 capas)?
- [ ] ¿Estoy usando offline-first en móvil?
- [ ] ¿Tengo type hints completos (Python)?
- [ ] ¿Tengo tests con cobertura >80%?
- [ ] ¿Mis commits siguen Conventional Commits?
- [ ] ¿He referenciado la User Story (US-XXX)?
- [ ] ¿He mencionado Hacienda Gamelera en comentarios de dominio?

---

## 🚀 Flujo de Desarrollo

```
1. Leer Sprint Goal actual
   ↓
2. Seleccionar User Story
   ↓
3. Leer estándares relevantes:
   - Architecture (SIEMPRE)
   - Flutter (si US es móvil)
   - Python (si US es backend)
   - ML (si US es modelo)
   - Git (SIEMPRE)
   - Testing (SIEMPRE)
   ↓
4. Crear branch: feature/US-XXX-descripcion
   ↓
5. Desarrollar con TDD (Test-Driven Development)
   ↓
6. Validar contra Definition of Done
   ↓
7. Code review
   ↓
8. Merge a development
   ↓
9. Deploy a staging
   ↓
10. Validación con Bruno Brito Macedo
   ↓
11. Deploy a production (si aprobado)
```

---

## 📊 Resumen Ejecutivo

| Documento | Líneas | Tamaño | Conceptos Clave |
|-----------|--------|--------|-----------------|
| **architecture-standards.md** | 1,056 | 41 KB | Clean Architecture, patrones, C4, NFRs |
| **flutter-standards.md** | 1,354 | 36 KB | Flutter, Provider, Atomic Design, Offline-first |
| **python-standards.md** | 1,050+ | 38 KB | FastAPI, Pydantic v2, Beanie ODM, Type hints |
| **ml-training-standards.md** | 650+ | 25 KB | TensorFlow, MLflow, DVC, 7 modelos, R² ≥0.95 |
| **git-workflow.md** | 580+ | 22 KB | Git Flow, Conventional Commits, SemVer |
| **testing-standards.md** | 700+ | 28 KB | Pytest, flutter_test, >80% coverage, E2E |
| **deployment-standards.md** | 920+ | 35 KB | Docker, AWS, CI/CD, Monitoreo, Disaster Recovery |
| **TOTAL** | **6,310+** | **225 KB** | **Base completa para desarrollo** |

---

## 🎯 Estándares por User Story

### Sprint 1: Validación Core

| User Story | Estándares Aplicables |
|------------|----------------------|
| **US-001**: Captura Continua | Architecture, Flutter, Git, Testing |
| **US-002**: Estimación IA | Architecture, Flutter, ML Training, Git, Testing |
| **US-003**: Registro Animales | Architecture, Flutter, Python, Git, Testing |

### Sprint 2: Funcionalidad Completa

| User Story | Estándares Aplicables |
|------------|----------------------|
| **US-004**: Historial Pesajes | Architecture, Flutter, Python, Git, Testing |
| **US-005**: Sincronización Offline | Architecture, Flutter, Python, Git, Testing |
| **US-006**: Búsqueda y Filtros | Architecture, Flutter, Python, Git, Testing |

### Sprint 3: Integración Normativa

| User Story | Estándares Aplicables |
|------------|----------------------|
| **US-007**: Reportes SENASAG | Architecture, Python, Git, Testing, Deployment |
| **US-008**: Gran Paitití/GMA | Architecture, Python, Git, Testing, Deployment |
| **US-009**: Exportación ASOCEBU | Architecture, Python, Git, Testing, Deployment |

---

## 🔍 Búsqueda Rápida

### "¿Cómo valido las 7 razas en Flutter?"
Ver: [flutter-standards.md](flutter-standards.md) → Sección "Constantes del Dominio" → breeds.dart

### "¿Cómo estructuro un endpoint FastAPI?"
Ver: [python-standards.md](python-standards.md) → Sección "FastAPI Routes" → Ejemplo SENASAG

### "¿Qué métricas debe cumplir mi modelo ML?"
Ver: [ml-training-standards.md](ml-training-standards.md) → Sección "Métricas Obligatorias" → R² ≥0.95, MAE <5kg

### "¿Cómo escribo un buen commit?"
Ver: [git-workflow.md](git-workflow.md) → Sección "Conventional Commits" → Ejemplos

### "¿Qué tests debo escribir?"
Ver: [testing-standards.md](testing-standards.md) → Sección "Testing por Capa" → Domain, Services, API

### "¿Cómo hago deploy a producción?"
Ver: [deployment-standards.md](deployment-standards.md) → Sección "Deployment Steps" → Manual/Automatizado

---

## 🎓 Formación del Equipo

### Onboarding de Nuevos Desarrolladores

**Día 1**: Contexto del proyecto
- Leer: `README.md` (root)
- Leer: `docs/vision/01-system-context.md`
- Leer: `docs/product/product-backlog.md`
- **Entender**: Cliente (Bruno), Hacienda Gamelera, 500 cabezas, 7 razas

**Día 2**: Arquitectura y estándares
- Leer: `docs/standards/architecture-standards.md` (COMPLETO)
- Leer: `docs/standards/git-workflow.md`
- **Memorizar**: 7 razas exactas, 4 categorías edad, métricas obligatorias

**Día 3**: Estándares de tecnología específica
- Si Mobile: Leer `flutter-standards.md` (COMPLETO)
- Si Backend: Leer `python-standards.md` (COMPLETO)
- Si ML: Leer `ml-training-standards.md` (COMPLETO)

**Día 4**: Testing y deployment
- Leer: `testing-standards.md`
- Leer: `deployment-standards.md`
- **Practicar**: Escribir primer test, hacer primer commit

**Día 5**: Pair programming
- Trabajar en US sencilla con desarrollador senior
- Aplicar estándares en código real
- Code review y feedback

---

## ⚠️ Reglas Inquebrantables

### 🚫 NUNCA:

1. ❌ **NUNCA** usar nombres genéricos (type1, breed_a, category_x)
2. ❌ **NUNCA** usar razas que no sean las 7 exactas de Hacienda Gamelera
3. ❌ **NUNCA** aceptar confidence <95% en producción
4. ❌ **NUNCA** hacer commit sin mensaje descriptivo
5. ❌ **NUNCA** merge a main sin tests pasando
6. ❌ **NUNCA** deploy sin validación con Bruno
7. ❌ **NUNCA** hard-codear valores (usar constantes)
8. ❌ **NUNCA** skip Definition of Done

### ✅ SIEMPRE:

1. ✅ **SIEMPRE** validar que raza sea una de las 7 exactas
2. ✅ **SIEMPRE** validar métricas del sistema (≥95%, <5kg, <3s)
3. ✅ **SIEMPRE** usar offline-first en móvil (SQLite primario)
4. ✅ **SIEMPRE** seguir Clean Architecture (3 capas)
5. ✅ **SIEMPRE** escribir tests (cobertura >80%)
6. ✅ **SIEMPRE** usar type hints en Python
7. ✅ **SIEMPRE** hacer code review antes de merge
8. ✅ **SIEMPRE** referenciar Hacienda Gamelera en código de dominio

---

## 📞 Contactos

### Equipo Scrum
- **Product Owner**: Miguel Angel Escobar Lazcano
- **Scrum Master**: Rodrigo Escobar Morón

### Cliente
- **Propietario**: Bruno Brito Macedo
- **Hacienda**: Gamelera
- **Ubicación**: San Ignacio de Velasco, Bolivia
- **GPS**: 15°51′34.2′′S, 60°47′52.4′′W

### Soporte Técnico
- **Email**: dev@haciendagamelera.com
- **GitHub**: https://github.com/your-org/bovine-weight-estimation
- **Docs**: https://bovine-docs.haciendagamelera.com

---

## 📖 Referencias Externas

### Tecnologías
- **Flutter**: https://docs.flutter.dev/
- **FastAPI**: https://fastapi.tiangolo.com/
- **TensorFlow**: https://tensorflow.org/lite
- **MongoDB**: https://docs.mongodb.com/
- **Docker**: https://docs.docker.com/

### Estándares
- **Clean Architecture**: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- **Conventional Commits**: https://www.conventionalcommits.org/es/
- **SemVer**: https://semver.org/lang/es/
- **Google Style Guide (Python)**: https://google.github.io/styleguide/pyguide.html

### Scrum
- **Product Backlog**: `docs/product/product-backlog.md`
- **Sprint 1 Goal**: `docs/sprints/sprint-01/sprint-goal.md`
- **Sprint 2 Goal**: `docs/sprints/sprint-02/sprint-goal.md`
- **Sprint 3 Goal**: `docs/sprints/sprint-03/sprint-goal.md`
- **Definition of Done**: `docs/product/definition-of-done.md`

---

## 🐄 Desarrollado para la ganadería boliviana

**Sistema de Estimación de Peso Bovino con IA - Hacienda Gamelera**

*"Tecnología al servicio de la ganadería boliviana"*

---

**Última actualización**: 28 octubre 2024  
**Versión**: 1.0.0  
**Sprint actual**: Sprint 3 (28 oct - 10 nov 2024)  
**Presentación final**: 6 noviembre 2024 🎯

