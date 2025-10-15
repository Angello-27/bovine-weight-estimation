# Metodología de Desarrollo - Base Estándar

**Proyecto**: Sistema de Estimación de Peso Bovino  
**Cliente**: Hacienda Gamelera  
**Establecido**: 28 Oct 2024 (US-001)  
**Estado**: ✅ Validado y aprobado como estándar

---

## 🎯 Propósito

Este documento establece la **metodología de desarrollo estándar** validada durante la implementación de US-001. Todas las User Stories futuras DEBEN seguir este proceso para mantener consistencia, calidad y mantenibilidad del código.

---

## 📋 Principios Fundamentales

### 1. **100% Basado en Documentación** ✅

**TODA implementación DEBE basarse en**:
- `docs/standards/` - Estándares de código y arquitectura
- `docs/design/` - Decisiones arquitectónicas y esquemas
- `docs/product/` - Product Backlog y Definition of Done
- `docs/sprints/` - Objetivos y contexto del sprint

**Antes de codificar**: Leer documentación relevante  
**Durante codificación**: Seguir estándares definidos  
**Después de codificar**: Actualizar documentación de progreso

---

### 2. **Clean Architecture Estricta** ✅

**Orden de implementación obligatorio**:

```
1. Domain Layer (Lógica de negocio pura)
   ├── Entities (objetos de dominio)
   ├── Repository interfaces (contratos)
   └── UseCases (casos de uso)

2. Core Layer (si es necesario)
   ├── Errors (Failures, Exceptions)
   ├── Config (configuración global)
   ├── Utils (utilidades compartidas)
   └── UI (componentes Atomic Design)

3. Data Layer (Implementación de infraestructura)
   ├── Models (serialización)
   ├── DataSources (APIs, DB, cache)
   └── Repository implementations

4. Presentation Layer (UI + state management)
   ├── Providers (state management)
   ├── Pages (coordinadores)
   └── Widgets (Atomic Design)

5. Tests (después de cada capa)
   ├── Unit tests
   ├── Widget tests
   └── Integration tests
```

**Regla**: NUNCA mezclar capas. Domain NO debe depender de Data o Presentation.

---

### 3. **SOLID Principles** ✅

| Principio | Aplicación |
|-----------|------------|
| **S**ingle Responsibility | 1 archivo = 1 responsabilidad clara |
| **O**pen/Closed | Extensible sin modificar código existente |
| **L**iskov Substitution | Widgets/componentes intercambiables |
| **I**nterface Segregation | Interfaces específicas, no genéricas |
| **D**ependency Inversion | DI Container + Provider |

**Validación**: Cada archivo debe tener un comentario claro en la primera línea explicando su Single Responsibility.

```dart
/// Widget: CaptureErrorCard
/// 
/// Card con mensaje de error.
/// Single Responsibility: Mostrar error de captura.
///
/// Page-specific Widget
library;
```

---

### 4. **Atomic Design para UI** ✅

**Jerarquía obligatoria**:

```
core/ui/
├── atoms/ (Componentes básicos indivisibles)
│   ├── buttons/
│   ├── inputs/
│   ├── indicators/
│   ├── icons/
│   └── text/
│
├── molecules/ (Combinación de atoms)
│   ├── cards/
│   ├── sliders/
│   ├── dialogs/
│   └── list_items/
│
├── organisms/ (Componentes complejos)
│   ├── navigation/
│   ├── forms/
│   └── [feature]/
│
└── theme/ (Estilos globales)
    ├── app_theme.dart
    ├── app_colors.dart
    └── app_spacing.dart

presentation/pages/[page]/
├── [page]_page.dart (Coordinador)
└── widgets/ (Page-specific)
```

**Regla de reutilización**:
- Si un componente se usa en >1 página → `core/ui/`
- Si es específico de 1 página → `presentation/pages/[page]/widgets/`

---

### 5. **Separación de Concerns** ✅

**Archivos separados obligatorios**:

```
core/config/
├── app_config.dart           # Constantes globales
└── dependency_injection.dart # DI container

core/routes/
└── app_router.dart           # Rutas centralizadas

core/ui/theme/
├── app_theme.dart            # Tema Material Design 3
├── app_colors.dart           # Paleta de colores
└── app_spacing.dart          # Sistema de espaciado

main.dart                     # SOLO inicialización (≤60 líneas)
```

**Regla**: `main.dart` NUNCA debe contener:
- Lógica de negocio
- Widgets complejos
- Configuración inline
- DI inline

---

## 🔄 Proceso de Desarrollo por User Story

### Fase 1: Análisis (30 min)

**Checklist**:
- [ ] Leer formato 3C completo de la US (`docs/product/product-backlog-detailed.md`)
- [ ] Identificar dependencias técnicas con otras US
- [ ] Revisar criterios de aceptación
- [ ] Verificar estándares aplicables (`docs/standards/`)
- [ ] Listar archivos a crear/modificar

**Output**: Lista clara de archivos y componentes necesarios

---

### Fase 2: Domain Layer (1-2h)

**Orden**:
1. **Entities** (`domain/entities/`)
   - Objetos de negocio puros
   - Usar `Equatable` para comparación
   - Sin dependencias externas

2. **Repository Interfaces** (`domain/repositories/`)
   - Contratos con `Either<Failure, T>`
   - Métodos async (`Future<Either<...>>`)
   - Documentación clara de params y returns

3. **UseCases** (`domain/usecases/`)
   - `implements UseCase<Type, Params>`
   - Lógica de negocio pura
   - Sin referencias a UI o Data

**Commit**: `feat(US-XXX): implementar Domain Layer`

---

### Fase 3: Core Layer (30 min - 1h, si necesario)

**Solo si la US requiere**:
- Nuevos tipos de Failures/Exceptions
- Configuración específica
- Componentes UI reutilizables (Atomic Design)

**Commit**: `feat(US-XXX): agregar componentes Core`

---

### Fase 4: Data Layer (2-3h)

**Orden**:
1. **Models** (`data/models/`)
   - Extienden Entities
   - Métodos `toJson()`, `fromJson()`, `toSQLite()`, `fromSQLite()`
   - Serialización completa

2. **DataSources** (`data/datasources/`)
   - Interfaces y implementaciones
   - Un DataSource por fuente (API, DB, Cache)
   - Lanzan Exceptions (no Failures)

3. **Repository Implementations** (`data/repositories/`)
   - Implementan interfaces de Domain
   - Convierten Exceptions → Failures
   - Coordinan DataSources

**Commit**: `feat(US-XXX): implementar Data Layer con datasources y repositories`

---

### Fase 5: Presentation Layer (2-3h)

**Orden**:
1. **Provider** (`presentation/providers/`)
   - `extends ChangeNotifier`
   - State management reactivo
   - Llama a UseCases
   - Gestiona loading/error/success

2. **Page** (`presentation/pages/[page]/`)
   - Coordinador de componentes
   - `Consumer<Provider>` para reactive UI
   - Lógica de navegación

3. **Widgets específicos** (`presentation/pages/[page]/widgets/`)
   - Componentes de la página
   - Reutilizan Atoms/Molecules/Organisms
   - Single Responsibility

**Commit**: `feat(US-XXX): implementar Presentation Layer con Provider y UI`

---

### Fase 6: Refactorización (1h, si necesario)

**Si la página >200 líneas**:
- Extraer widgets a Atomic Design
- Separar lógica compleja a Utils
- Crear Organisms reutilizables

**Commit**: `refactor(US-XXX): aplicar Atomic Design y SOLID`

---

### Fase 7: Tests (2h)

**Cobertura mínima >80%**:

1. **Unit Tests** (`test/domain/`, `test/data/`)
   - UseCases
   - Repositories
   - DataSources (mocked)
   - Usar Mockito para mocks

2. **Widget Tests** (`test/presentation/`)
   - Providers (state changes)
   - Pages (rendering)
   - Widgets específicos

3. **Integration Tests** (opcional)
   - Flujos completos de US

**Commit**: `test(US-XXX): agregar tests unitarios y de widgets (>80% coverage)`

---

### Fase 8: Documentación (30 min)

**Actualizar**:
- [ ] `docs/product/product-backlog.md` (marcar US como completada)
- [ ] `docs/sprints/sprint-XX/sprint-progress.md` (agregar progreso)
- [ ] `mobile/pubspec.yaml` (si agregaste dependencias, documentar uso)
- [ ] `README.md` del proyecto (si cambia arquitectura)

**Commit**: `docs(US-XXX): actualizar documentación de progreso`

---

## 📁 Estructura de Commits

### Conventional Commits Obligatorio

```
feat(US-XXX): descripción corta

Descripción detallada (opcional):
- Qué se implementó
- Por qué se hizo así
- Referencias a docs/

Criterios de aceptación cumplidos:
1. ✅ Criterio 1
2. ✅ Criterio 2

Archivos: X archivos, Y líneas

Refs: #US-XXX
```

**Tipos permitidos**:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `refactor`: Refactorización sin cambio funcional
- `test`: Agregar/modificar tests
- `docs`: Solo documentación
- `style`: Formateo, linting
- `perf`: Mejora de performance

---

## ✅ Definition of Done por Fase

### Por Archivo
- [ ] Comentario de Single Responsibility en primera línea
- [ ] Documentación inline (docstrings)
- [ ] Type hints/annotations completos
- [ ] Linting sin errores (`flutter analyze` / `dart analyze`)
- [ ] Naming conventions según `docs/standards/`

### Por Capa
- [ ] Tests unitarios escritos
- [ ] Cobertura >80% de la capa
- [ ] Sin dependencias circulares
- [ ] Separación de concerns respetada

### Por User Story
- [ ] Todos los criterios de aceptación ✅
- [ ] Definition of Done cumplida
- [ ] Documentación actualizada
- [ ] Demo funcional preparada
- [ ] Commit con Conventional Commits

---

## 🎯 Validación de Calidad

**Antes de cada commit, ejecutar**:

```bash
# Linting
flutter analyze

# Tests
flutter test --coverage

# Verificar cobertura >80%
# TODO: Agregar script de validación

# Build (validar que compila)
flutter build apk --debug
```

---

## 📚 Referencias de Documentación

**Leer SIEMPRE antes de implementar**:

| Aspecto | Documento |
|---------|-----------|
| Arquitectura | `docs/standards/architecture-standards.md` |
| Flutter/Dart | `docs/standards/flutter-standards.md` |
| UI/UX | `docs/design/ui-design-system.md` |
| Testing | `docs/standards/testing-standards.md` |
| Git | `docs/standards/git-workflow.md` |
| Base de Datos | `docs/design/database-schema.md` |
| User Stories | `docs/product/product-backlog-detailed.md` |

---

## 🚀 Ejemplo Completo: US-001

**Ver implementación real en**:
- `docs/sprints/sprint-01/sprint-progress.md` (progreso detallado)
- Commits: `5d0841f`, `b20ac44`, `4c2031d`
- 31 archivos creados siguiendo este proceso
- 100% basado en documentación
- 100% cumple SOLID + Clean Architecture + Atomic Design

---

## ⚠️ Prohibiciones Absolutas

**NUNCA hacer**:
- ❌ Código sin leer documentación previa
- ❌ Mezclar capas (Domain no depende de Data/Presentation)
- ❌ Archivos >300 líneas (refactorizar)
- ❌ Lógica de negocio en Presentation
- ❌ UI en Domain o Data
- ❌ DI inline en `main.dart`
- ❌ Commits sin Conventional Commits
- ❌ Merge sin tests >80% coverage
- ❌ Código sin comentario de Single Responsibility

---

## 📊 Métricas de Éxito

| Métrica | Target | Validación |
|---------|--------|------------|
| **Cobertura tests** | >80% | Automatizada |
| **Linting errors** | 0 | `flutter analyze` |
| **Tamaño archivos** | <300 líneas | Code review |
| **Reutilización** | >50% UI | Atomic Design |
| **Mantenibilidad** | Alta | SOLID + Clean |
| **Velocidad desarrollo** | 1 US / 1-2 días | Sprint tracking |

---

**Establecido**: 28 Oct 2024  
**Validado en**: US-001 (Sprint 1)  
**Estado**: ✅ Estándar oficial del proyecto  
**Actualizaciones**: Cada sprint puede refinar (no reemplazar)

