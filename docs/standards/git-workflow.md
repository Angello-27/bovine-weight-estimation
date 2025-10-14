# Estándares de Git Workflow

## Contexto del Proyecto

**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Cliente**: Hacienda Gamelera (Bruno Brito Macedo)  
**Repositorio**: https://github.com/your-org/bovine-weight-estimation  
**Metodología**: Scrum con sprints de 2 semanas

## Git Flow Strategy

### Branches Principales

```
main (producción)
  │
  ├─ development (desarrollo activo)
  │    │
  │    ├─ feature/US-001-captura-continua
  │    ├─ feature/US-002-estimacion-ia
  │    ├─ feature/US-007-reportes-senasag
  │    └─ feature/US-008-gran-paititi
  │
  └─ release/v1.0.0 (preparación release)
```

### Tipos de Branches

| Branch | Propósito | Naming | Lifetime |
|--------|-----------|--------|----------|
| **main** | Código en producción | `main` | Permanente |
| **development** | Integración continua | `development` | Permanente |
| **feature/** | Nueva funcionalidad (US) | `feature/US-XXX-descripcion` | Temporal (1 sprint) |
| **bugfix/** | Corrección de bugs | `bugfix/descripcion-corta` | Temporal (1-3 días) |
| **hotfix/** | Corrección urgente producción | `hotfix/descripcion-urgente` | Temporal (horas) |
| **release/** | Preparación de release | `release/v1.0.0` | Temporal (1-2 días) |

### Workflow por User Story

```bash
# 1. Crear branch desde development para US-007 (Reportes SENASAG)
git checkout development
git pull origin development
git checkout -b feature/US-007-reportes-senasag

# 2. Desarrollo con commits frecuentes
# ... hacer cambios ...
git add app/api/routes/senasag.py
git commit -m "feat(senasag): agregar endpoint generación reportes PDF

- Implementar POST /senasag/reports
- Generar PDF con logo SENASAG y datos Hacienda Gamelera
- Validar estructura según normativa boliviana
- Tests unitarios con cobertura >80%

US-007"

# 3. Push regularmente
git push origin feature/US-007-reportes-senasag

# 4. Pull Request cuando US está Done según DoD
# Título: feat(US-007): Reportes SENASAG automáticos
# Descripción: Implementa generación de reportes de trazabilidad...
# Checklist DoD adjunto

# 5. Code review → Merge a development
# 6. Eliminar branch después de merge
git branch -d feature/US-007-reportes-senasag
```

---

## Conventional Commits

### Formato Obligatorio

```
<type>(<scope>): <subject>

[body opcional]

[footer opcional con US-XXX]
```

### Types (Tipos de Cambio)

| Type | Uso | Ejemplo |
|------|-----|---------|
| **feat** | Nueva funcionalidad (US) | `feat(senasag): agregar reportes PDF` |
| **fix** | Corrección de bug | `fix(camera): corregir FPS en captura continua` |
| **docs** | Documentación | `docs(readme): actualizar guía de instalación` |
| **style** | Formato código (no afecta lógica) | `style(flutter): aplicar dartfmt` |
| **refactor** | Refactorización | `refactor(repository): extraer lógica común` |
| **perf** | Mejora de performance | `perf(search): optimizar búsqueda 500 animales` |
| **test** | Agregar tests | `test(senasag): agregar tests unitarios` |
| **build** | Cambios en build/dependencies | `build(deps): actualizar TensorFlow a 2.13` |
| **ci** | Cambios en CI/CD | `ci(github): agregar workflow de tests` |
| **chore** | Tareas mantenimiento | `chore(gitignore): agregar .env a gitignore` |

### Scopes (Ámbito del Cambio)

**Por componente**:
- `mobile`, `backend`, `ml-training`, `docs`

**Por feature**:
- `camera`, `estimation`, `animals`, `weighings`
- `senasag`, `regensa`, `gran-paititi`, `asocebu`

**Por área funcional**:
- `data-management`, `analytics`, `monitoring`, `user-features`, `operations`

### Ejemplos de Buenos Commits

```bash
# ✅ Feature completa (US-001)
git commit -m "feat(camera): implementar captura continua 10-15 FPS

- Captura automática durante 3-5 segundos
- Evaluación en tiempo real de calidad (nitidez, iluminación, silueta)
- Selección automática del mejor fotograma con score ponderado
- Almacenamiento local en SQLite (offline-first)
- Validado con Bruno Brito Macedo en Hacienda Gamelera

Métricas:
- FPS promedio: 12
- Fotogramas capturados: 48 (4 segundos)
- Tiempo selección: <500ms

US-001"

# ✅ Fix de bug
git commit -m "fix(estimation): corregir validación de raza Pardo Suizo

Problema: Modelo TFLite no cargaba para raza 'pardo_suizo'
Causa: Nombre de archivo con guion bajo vs camelCase
Solución: Normalizar nombres de archivo a kebab-case

Afecta: BreedType.pardoSuizo → pardo-suizo-v1.0.0.tflite"

# ✅ Performance improvement
git commit -m "perf(search): optimizar búsqueda en 500 animales

- Agregar índice compuesto (tag_number, breed_type) en SQLite
- Implementar paginación con límite 50
- Reducir tiempo búsqueda de 8s a 1.2s

Validado con dataset completo de Hacienda Gamelera (500 animales)

US-006"

# ✅ Documentation
git commit -m "docs(standards): agregar estándares Python/FastAPI

- Constantes de las 7 razas bovinas
- Pydantic schemas con validaciones
- Ejemplos de código con type hints
- Referencias a Hacienda Gamelera

Sprint 3"
```

### Ejemplos de Malos Commits

```bash
# ❌ Mensaje vago
git commit -m "update files"

# ❌ Sin contexto
git commit -m "fix bug"

# ❌ Multiple cambios no relacionados
git commit -m "feat: agregar captura, estimación, búsqueda y reportes"

# ❌ Sin referencia a US
git commit -m "feat: agregar nueva funcionalidad importante"

# ❌ Typos o spanglish
git commit -m "feat: agreagar reporte"
git commit -m "feat: add reporte SENASAG"  # Mezcla inglés/español
```

---

## Pull Request Template

```markdown
## Descripción

**User Story**: US-007 - Reportes SENASAG  
**Sprint**: Sprint 3 (28 oct - 10 nov 2024)  
**Tipo**: Feature

Implementa generación automática de reportes de trazabilidad ganadera para SENASAG cumpliendo normativa boliviana obligatoria.

### Cambios realizados

- ✅ Endpoint POST /senasag/reports (generación)
- ✅ Endpoint GET /senasag/reports (listado historial)
- ✅ Endpoint GET /senasag/reports/{id}/download (descarga)
- ✅ Generación PDF con logo SENASAG y datos Hacienda Gamelera
- ✅ Exportación CSV con estructura estándar
- ✅ Exportación XML compatible con sistemas SENASAG
- ✅ Envío automático por email (background task)
- ✅ Validación de datos antes de generación

### Validación con Bruno Brito Macedo

- ✅ Bruno puede generar reporte de 500 cabezas en <5 minutos
- ✅ Reportes son claros y profesionales
- ✅ Estructura CSV es compatible con Excel
- ✅ Envío por email funciona correctamente

### Métricas

- **Tiempo generación PDF**: 3.2 segundos (500 animales)
- **Tiempo generación CSV**: 1.1 segundos (500 animales)
- **Tamaño PDF**: 850 KB (10 páginas)
- **Tests pasando**: 15/15 (100%)
- **Cobertura**: 87%

## Definition of Done - Checklist

### Done - Código Individual
- [x] Código implementado según estándares Python
- [x] Type hints completos en todas las funciones
- [x] Docstrings con Google Style
- [x] Tests unitarios pasando (>80% cobertura)
- [x] Linting sin errores (ruff, black, mypy)
- [x] Code review aprobado

### Done - Feature Completa
- [x] Criterios de aceptación 100% cumplidos (10/10)
- [x] Tests de integración pasando (API + MongoDB)
- [x] Performance dentro de métricas (<5 min para 500 animales)
- [x] Manejo de errores implementado
- [x] Documentación API (OpenAPI/Swagger) actualizada

### Done - Sprint
- [x] Validación con Bruno Brito Macedo exitosa
- [x] Testing con datos reales de Hacienda Gamelera (500 cabezas)
- [x] Demo funcional en Sprint Review
- [x] Aceptación formal del Product Owner
- [x] Documentación técnica actualizada

## Screenshots / Videos

[Adjuntar capturas de pantalla de reporte PDF generado]
[Adjuntar video de generación completa]

## Checklist Técnico

- [x] Endpoints FastAPI funcionando
- [x] Schemas Pydantic validando correctamente
- [x] Service generando PDF/CSV/XML sin errores
- [x] Repository guardando historial en MongoDB
- [x] Background tasks enviando emails
- [x] Tests cubriendo casos happy path y edge cases
- [x] Logs estructurados con loguru

## Revisores

@rodrigo-escobar-moron (Scrum Master)  
@team-backend

## Relacionado

- User Story: US-007 (Reportes SENASAG)
- Sprint Goal: `docs/sprints/sprint-03/sprint-goal.md`
- Definition of Done: `docs/product/definition-of-done.md`
```

---

## Commits por Sprint

### Sprint 1 (Validación Core)

```bash
feat(mobile): inicializar proyecto Flutter con estructura Clean Architecture
feat(core): agregar constantes de 7 razas bovinas de Hacienda Gamelera
feat(camera): implementar captura continua 10-15 FPS (US-001)
feat(estimation): agregar modelos TFLite por raza (US-002)
feat(animals): implementar registro de animales (US-003)
test(camera): agregar tests unitarios de captura continua
test(estimation): validar precisión >95% con 3 razas principales
docs(sprint-1): actualizar Sprint 1 Goal con resultados
```

### Sprint 2 (Funcionalidad Completa)

```bash
feat(analytics): implementar historial de pesajes con gráficos (US-004)
feat(sync): implementar sincronización offline-first (US-005)
feat(search): implementar búsqueda optimizada 500 animales (US-006)
perf(search): agregar índices SQLite para búsqueda <3s
test(sync): validar sincronización con conectividad intermitente
docs(sprint-2): preparar presentación 23 octubre
```

### Sprint 3 (Integración Normativa) - ACTUAL

```bash
feat(senasag): implementar generación reportes PDF/CSV/XML (US-007)
feat(regensa): implementar creación GMA digital (US-008)
feat(gran-paititi): integrar con API gubernamental (US-008)
feat(asocebu): implementar exportación datos competencias (US-009)
test(senasag): validar estructura reportes contra normativa
docs(sprint-3): preparar presentación final 6 noviembre
```

---

## .gitignore

```gitignore
# .gitignore - Root del proyecto

# ==========================================
# MOBILE (Flutter)
# ==========================================

mobile/.dart_tool/
mobile/build/
mobile/.flutter-plugins
mobile/.flutter-plugins-dependencies
mobile/.packages
mobile/pubspec.lock

# Generados
mobile/ios/Pods/
mobile/ios/Runner.xcworkspace/
mobile/android/.gradle/
mobile/android/local.properties

# ==========================================
# BACKEND (Python/FastAPI)
# ==========================================

backend/__pycache__/
backend/*.py[cod]
backend/*$py.class
backend/.pytest_cache/
backend/.coverage
backend/htmlcov/
backend/.env
backend/venv/
backend/env/

# ==========================================
# ML TRAINING
# ==========================================

ml-training/data/raw/              # Imágenes grandes (usar DVC)
ml-training/data/processed/
ml-training/.ipynb_checkpoints/
ml-training/experiments/mlruns/
ml-training/__pycache__/
ml-training/models/*.h5
ml-training/models/*/saved_model/

# DVC
ml-training/.dvc/cache/
ml-training/.dvc/tmp/

# ==========================================
# MODELOS (usar DVC y S3)
# ==========================================

models/*.tflite                    # Modelos grandes (subir a S3)
models/*/saved_model/

# ==========================================
# LOGS Y TEMPORALES
# ==========================================

*.log
logs/
tmp/
.DS_Store
Thumbs.db

# ==========================================
# IDEs
# ==========================================

.vscode/
.idea/
*.swp
*.swo

# ==========================================
# SEGURIDAD (NUNCA COMMITEAR)
# ==========================================

*.env
.env.local
.env.production
secrets/
credentials/
*.pem
*.key
```

---

## Conventional Commits Detallado

### Estructura de Mensaje

```
<type>(<scope>): <subject en español, imperativo, <50 chars>

[body opcional: explicación detallada del cambio en español]
[puede tener múltiples párrafos]

[footer: referencias a US, breaking changes]
```

### Ejemplos Completos por Tipo

#### feat (Nueva Funcionalidad)

```bash
feat(senasag): agregar generación reportes PDF con logo SENASAG

Implementa endpoint POST /senasag/reports que genera reportes
de trazabilidad ganadera en formato PDF profesional.

Características:
- Logo SENASAG en header
- Datos de Hacienda Gamelera (nombre, propietario, GPS)
- Inventario por raza (7 razas exactas)
- Tabla detallada con todos los animales
- Firma digital de Bruno Brito Macedo en footer

Validaciones:
- Estructura según normativa SENASAG boliviana
- Período válido (mensual/trimestral/anual)
- Datos completos de 500 cabezas

US-007
```

#### fix (Corrección)

```bash
fix(estimation): corregir cálculo de edad para categoría Terneros

Problema:
- Terneros de 7.5 meses se clasificaban como Vaquillonas/Torillos
- Causaba estimaciones de peso incorrectas (fuera de rango)

Causa:
- Lógica de categorización usaba >= 8 en vez de > 8

Solución:
- Cambiar condición: age_months < 8 (no age_months <= 7)
- Agregar test para edge case (7.9 meses)

Impacto:
- Afecta ~15 animales en Hacienda Gamelera
- Mejora precisión de modelos Brahman y Nelore

Reportado por: Bruno Brito Macedo
```

#### perf (Performance)

```bash
perf(search): optimizar búsqueda de animales con índices compuestos

Mejoras:
- Índice compuesto (farm_id, breed_type, status) en MongoDB
- Query con projection (solo campos necesarios)
- Paginación con cursor (no offset)

Resultados:
- Antes: 8.3 segundos para 500 animales
- Después: 1.2 segundos para 500 animales
- Mejora: 85% más rápido

Validado con dataset completo de Hacienda Gamelera.

US-006
```

#### docs (Documentación)

```bash
docs(standards): agregar estándares Python/FastAPI completos

- Constantes de 7 razas bovinas de Hacienda Gamelera
- Pydantic schemas con validaciones ≥95% precisión
- Ejemplos de código con type hints obligatorios
- Testing con pytest y httpx
- Referencias a User Stories de Sprint 3

Archivos:
- docs/standards/python-standards.md (600+ líneas)

Sprint 3
```

---

## Branch Protection Rules

### main branch

```yaml
# Reglas para branch main (producción)

require_pull_request:
  required_approving_review_count: 2          # 2 aprobaciones mínimo
  dismiss_stale_reviews: true
  require_code_owner_reviews: true

require_status_checks:
  strict: true
  contexts:
    - "Tests Backend (Python)"
    - "Tests Mobile (Flutter)"
    - "Lint Backend"
    - "Lint Mobile"
    - "Build Mobile (Android)"

require_signed_commits: false                 # Opcional
include_administrators: true                  # Admins siguen reglas
allow_force_pushes: false                     # NO force push
allow_deletions: false                        # NO eliminar branch
```

### development branch

```yaml
# Reglas para branch development

require_pull_request:
  required_approving_review_count: 1          # 1 aprobación mínimo
  dismiss_stale_reviews: false

require_status_checks:
  strict: true
  contexts:
    - "Tests Backend (Python)"
    - "Tests Mobile (Flutter)"
    - "Lint Backend"
    - "Lint Mobile"

allow_force_pushes: false
```

---

## Tags y Releases

### Versionado Semántico (SemVer)

```bash
# Format: vMAJOR.MINOR.PATCH
# Example: v1.2.3

# MAJOR: Cambios incompatibles en API
v2.0.0  # Cambio de arquitectura, modelos incompatibles

# MINOR: Nuevas funcionalidades compatibles  
v1.1.0  # Agregar soporte para nueva raza
v1.2.0  # Agregar alertas inteligentes (US-010)

# PATCH: Correcciones de bugs
v1.0.1  # Corregir bug en sincronización offline
v1.0.2  # Corregir cálculo de edad
```

### Crear Release

```bash
# Después de Sprint 3 (presentación 6 noviembre)

# 1. Merge de development a main
git checkout main
git merge development --no-ff -m "release: v1.0.0 - Sistema completo funcional

Sistema de Estimación de Peso Bovino con IA listo para producción
en Hacienda Gamelera (Bruno Brito Macedo).

Incremento acumulativo Sprint 1+2+3:
- Captura continua y estimación IA (>95% precisión)
- Gestión completa del hato (500 cabezas offline)
- Cumplimiento normativo SENASAG/REGENSA/ASOCEBU

User Stories completadas: US-001 a US-009 (78 story points)

Métricas validadas:
- Precisión: >95% (R² ≥0.95) ✅
- Error: <5 kg ✅  
- Tiempo: <2 horas para 20 animales ✅
- Offline-first: 100% funcional ✅

Validado en campo con Bruno Brito Macedo.
Presentado académicamente: 23 octubre, 6 noviembre 2024."

# 2. Crear tag
git tag -a v1.0.0 -m "Release v1.0.0 - Sistema completo

- Sprint 1: Validación Core (US-001, US-002, US-003)
- Sprint 2: Funcionalidad Completa (US-004, US-005, US-006)  
- Sprint 3: Integración Normativa (US-007, US-008, US-009)

Sistema listo para producción en Hacienda Gamelera.
Cumple 100% requisitos normativos bolivianos.

Cliente: Bruno Brito Macedo
Hacienda: Gamelera
Ubicación: San Ignacio de Velasco, Bolivia"

# 3. Push tag
git push origin v1.0.0

# 4. Crear GitHub Release con artifacts
# - Archivo: bovine-weight-app-v1.0.0.apk (Android)
# - Archivo: models-manifest-v1.0.0.json
# - Changelog completo
# - Guías de instalación
```

---

## Changelog

```markdown
# Changelog

Todos los cambios notables del proyecto se documentan en este archivo.

Formato basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [1.0.0] - 2024-11-10

**Release Inicial - Sistema Completo**

Sistema de Estimación de Peso Bovino con IA listo para producción en
Hacienda Gamelera (Bruno Brito Macedo, San Ignacio de Velasco, Bolivia).

### Added

**Sprint 1 (30 sept - 13 oct 2024)**:
- Captura continua de fotogramas (10-15 FPS, 3-5s) [US-001]
- Estimación de peso por IA con 7 modelos específicos por raza [US-002]
- Registro de animales con validación única de caravana [US-003]
- Modelos TFLite: brahman, nelore, angus, cebuinas, criollo, pardo-suizo, jersey

**Sprint 2 (14 oct - 27 oct 2024)**:
- Historial de pesajes con gráficos de evolución [US-004]
- Sincronización offline-first con queue y backoff exponencial [US-005]
- Búsqueda optimizada para 500 animales (<3s) [US-006]
- Exportación de reportes en PDF y CSV

**Sprint 3 (28 oct - 10 nov 2024)**:
- Reportes SENASAG automáticos (PDF/CSV/XML) [US-007]
- Integración Gran Paitití con generación de GMA digital [US-008]
- Exportación ASOCEBU para competencias ganaderas [US-009]
- Códigos QR en GMAs para verificación digital

### Métricas Validadas

- ✅ Precisión ML: >95% (R² = 0.97 promedio en 7 razas)
- ✅ Error absoluto: <5 kg (MAE = 3.8 kg promedio)
- ✅ Tiempo procesamiento: <3 segundos (2.5s promedio)
- ✅ Tiempo para 20 animales: <2 horas (1.5 horas validado con Bruno)
- ✅ Funcionamiento offline: 100% sin conexión
- ✅ Cumplimiento normativo: SENASAG/REGENSA/ASOCEBU 100%

### Validación en Campo

- Hacienda Gamelera: 500 cabezas de ganado bovino
- Validado por: Bruno Brito Macedo
- Condiciones: Zona rural, sin conexión, clima tropical
- Feedback: Satisfacción >9/10

## [Unreleased]

### Planned (Sprint 4+)
- Alertas inteligentes configurables [US-010]
- Planificación de sesiones masivas con rutas optimizadas [US-011]
- Soporte para múltiples haciendas
- Dashboard web para análisis ejecutivo
```

---

## Referencias

- **Conventional Commits**: https://www.conventionalcommits.org/es/
- **SemVer**: https://semver.org/lang/es/
- **Sprint Goals**: `docs/sprints/sprint-{1,2,3}-goal.md`
- **Definition of Done**: `docs/product/definition-of-done.md`

---

**Documento de Git Workflow v1.0**  
**Fecha**: 28 octubre 2024  
**Proyecto**: Sistema de Estimación de Peso Bovino con IA  
**Equipo**: Product Owner (Miguel Angel Escobar Lazcano), Scrum Master (Rodrigo Escobar Morón)

