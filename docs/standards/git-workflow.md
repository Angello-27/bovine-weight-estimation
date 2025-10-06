# Estándares de Git Workflow

Sistema de Estimación de Peso Bovino - Hacienda Gamelera

## 1. Estrategia de Branching

### 1.1 Git Flow Adaptado para el Proyecto

```text
master (producción)
├── development (desarrollo)
├── feature/data-management-capture (Área 1)
├── feature/analytics-reports (Área 2)
├── feature/monitoring-alerts (Área 3)
├── feature/user-features-search (Área 4)
├── feature/operations-sync (Área 5)
├── hotfix/precision-calculation-bug
└── release/v1.0.0-hacienda-gamelera
```

### 1.2 Tipos de Branches

#### Feature Branches (Desarrollo de Funcionalidades)

```bash
# Naming: feature/area-funcionalidad-descripcion
feature/data-management-continuous-capture
feature/analytics-reports-weight-evolution
feature/monitoring-senasag-integration
feature/user-features-breed-filter
feature/operations-offline-sync

# Ejemplos específicos del proyecto:
feature/data-management-breed-processing   # Procesamiento por las 7 razas
feature/monitoring-regensa-compliance      # Validación capítulos 3.10 y 7.1
feature/analytics-asocebu-export           # Exportación para competencias
feature/operations-gran-paititi-sync       # Sincronización con sistema gubernamental
```

#### Hotfix Branches (Correcciones Urgentes)

```bash
# Naming: hotfix/descripcion-del-problema
hotfix/frame-quality-calculation-error
hotfix/breed-validation-crash
hotfix/senasag-report-generation-fail
hotfix/offline-sync-data-loss

# Ejemplos específicos del proyecto:
hotfix/precision-below-95-percent-threshold  # Métrica crítica del SCRUM
hotfix/capture-frames-insufficient-count     # Menos de 30 fotogramas
hotfix/regensa-compliance-validation-bug     # Error en validación normativa
```

#### Release Branches (Preparación de Versiones)

```bash
# Naming: release/version-descripcion
release/v1.0.0-hacienda-gamelera-initial
release/v1.1.0-senasag-integration
release/v1.2.0-asocebu-competition-support
release/v2.0.0-multi-breed-models

# Ejemplos específicos del proyecto:
release/v1.0.0-7-breeds-support              # Soporte completo de las 7 razas
release/v1.1.0-regensa-compliance            # Cumplimiento normativo completo
release/v1.2.0-50-animals-validation         # Validación con 50 animales
```

## 2. Convenciones de Commits

### 2.1 Formato de Commit Messages

```bash
# Formato: <tipo>(<área>): <descripción>

# Tipos de commit:
feat:     Nueva funcionalidad
fix:      Corrección de bug
docs:     Documentación
style:    Formato, estilo (sin cambios de código)
refactor: Refactorización de código
test:     Agregar o modificar tests
chore:    Tareas de mantenimiento
perf:     Mejoras de rendimiento
ci:       Cambios en CI/CD

# Áreas funcionales (5 áreas del proyecto):
data-management:    Área 1 - Gestión de Datos
analytics:          Área 2 - Análisis y Reportes  
monitoring:         Área 3 - Monitoreo y Planificación
user-features:      Área 4 - Funcionalidades Usuario
operations:         Área 5 - Operación y Respaldos
core:               Funcionalidades core del sistema
```

### 2.2 Ejemplos de Commits Específicos del Proyecto

#### Commits de Funcionalidades

```bash
# Captura continua (Área 1)
feat(data-management): implement continuous capture with 10-15 FPS
feat(data-management): add frame quality evaluation with 5 criteria
feat(data-management): implement breed-specific processing for 7 breeds

# Análisis y reportes (Área 2)
feat(analytics): add weight evolution charts by breed
feat(analytics): implement SENASAG report generation (PDF/CSV/XML)
feat(analytics): add breed comparison analytics

# Monitoreo (Área 3)
feat(monitoring): implement REGENSA compliance validation (chapters 3.10, 7.1)
feat(monitoring): add GMA (Guía de Movimiento Animal) creation
feat(monitoring): integrate with Gran Paitití system

# Funcionalidades usuario (Área 4)
feat(user-features): add breed filter for 7 specific breeds
feat(user-features): implement age category filter (4 categories)
feat(user-features): add custom lists management

# Operaciones (Área 5)
feat(operations): implement offline-first architecture with SQLite
feat(operations): add conflict resolution for sync operations
feat(operations): implement automatic backup system
```

#### Commits de Correcciones

```bash
# Correcciones críticas de métricas
fix(data-management): precision calculation below 95% threshold
fix(data-management): frame capture insufficient count (<30 frames)
fix(analytics): SENASAG report generation fails with special characters

# Correcciones de integración normativa
fix(monitoring): REGENSA compliance validation incorrect for chapter 7.1
fix(monitoring): GMA creation fails when animal not in Gran Paitití
fix(operations): offline sync loses data during network interruption

# Correcciones de razas y categorías
fix(core): breed validation allows invalid breeds (not in 7 supported)
fix(core): age category calculation incorrect for vaquillonas_toretes
fix(user-features): breed filter crashes with pardo_suizo selection
```

#### Commits de Documentación

```bash
# Documentación técnica
docs(architecture): update system context with Hacienda Gamelera specifics
docs(architecture): add container architecture for 7 breeds support
docs(standards): create Flutter coding standards for bovine domain

# Documentación de normativa
docs(regulatory): add SENASAG integration requirements
docs(regulatory): document REGENSA chapters 3.10 and 7.1 compliance
docs(regulatory): add ASOCEBU competition export specifications
```

## 3. Workflow de Desarrollo

### 3.1 Flujo para Feature Development

```bash
# 1. Crear feature branch desde development
git checkout development
git pull origin development
git checkout -b feature/data-management-breed-processing

# 2. Desarrollo con commits frecuentes
git add .
git commit -m "feat(data-management): add breed model selector for 7 breeds"
git commit -m "feat(data-management): implement breed-specific parameters"
git commit -m "test(data-management): add tests for all 7 breed validations"

# 3. Push y crear Pull Request
git push origin feature/data-management-breed-processing
# Crear PR en GitHub hacia development

# 4. Code Review (obligatorio)
# - Revisar que soporte las 7 razas específicas
# - Validar métricas de precisión ≥95%
# - Verificar tests de integración normativa

# 5. Merge después de aprobación
git checkout development
git pull origin development
git merge feature/data-management-breed-processing
git push origin development

# 6. Cleanup
git branch -d feature/data-management-breed-processing
```

### 3.2 Flujo para Hotfixes

```bash
# 1. Crear hotfix desde master (producción)
git checkout master
git pull origin master
git checkout -b hotfix/precision-below-95-percent-threshold

# 2. Corrección urgente
git add .
git commit -m "fix(data-management): precision calculation below 95% threshold"
git commit -m "test(data-management): add precision validation tests"

# 3. Merge a master y development
git checkout master
git merge hotfix/precision-below-95-percent-threshold
git push origin master

git checkout development
git merge hotfix/precision-below-95-percent-threshold
git push origin development

# 4. Tag de versión
git tag -a v1.0.1-precision-fix -m "Hotfix: precision calculation below 95%"
git push origin v1.0.1-precision-fix
```

### 3.3 Flujo para Releases

```bash
# 1. Crear release branch desde development
git checkout development
git pull origin development
git checkout -b release/v1.0.0-7-breeds-support

# 2. Preparación de release
# - Actualizar versiones
# - Completar documentación
# - Ejecutar tests completos
# - Validar métricas SCRUM (≥95% precisión, <5kg error, <3s procesamiento)

git commit -m "chore(release): bump version to 1.0.0"
git commit -m "docs(release): update changelog for 7 breeds support"

# 3. Merge a master
git checkout master
git merge release/v1.0.0-7-breeds-support
git push origin master

# 4. Tag de release
git tag -a v1.0.0 -m "Release: Full support for 7 bovine breeds - Hacienda Gamelera"
git push origin v1.0.0

# 5. Merge a development
git checkout development
git merge release/v1.0.0-7-breeds-support
git push origin development
```

## 4. Pull Request Guidelines

### 4.1 Template de Pull Request

```markdown
## Descripción
Breve descripción de los cambios realizados.

## Área Funcional
- [ ] Área 1: Gestión de Datos (captura continua, procesamiento, registro)
- [ ] Área 2: Análisis y Reportes (historial, gráficos, comparativas)
- [ ] Área 3: Monitoreo y Planificación (alertas, calendario, sesiones)
- [ ] Área 4: Funcionalidades Usuario (búsqueda, listas, personalización)
- [ ] Área 5: Operación y Respaldos (offline, sincronización, backups)

## Razas Afectadas
- [ ] Brahman
- [ ] Nelore
- [ ] Angus
- [ ] Cebuinas (Bos indicus)
- [ ] Criollo (Bos taurus)
- [ ] Pardo Suizo
- [ ] Jersey

## Categorías de Edad Afectadas
- [ ] Terneros (<8 meses)
- [ ] Vaquillonas/Torillos (6-18 meses)
- [ ] Vaquillonas/Toretes (19-30 meses)
- [ ] Vacas/Toros (>30 meses)

## Integración Normativa
- [ ] SENASAG (reportes, trazabilidad)
- [ ] REGENSA (capítulos 3.10 y 7.1, GMA)
- [ ] Gran Paitití (sistema gubernamental)
- [ ] ASOCEBU (competencias ganaderas)

## Métricas del Sistema
- [ ] Precisión ≥95% (R² ≥ 0.95)
- [ ] Error absoluto <5 kg
- [ ] Tiempo procesamiento <3 segundos
- [ ] Validación con 50 animales

## Testing
- [ ] Unit tests agregados/modificados
- [ ] Integration tests ejecutados
- [ ] Tests de las 7 razas pasando
- [ ] Tests de integración normativa pasando

## Checklist
- [ ] Código sigue estándares de Flutter/Python
- [ ] Documentación actualizada
- [ ] No hay breaking changes
- [ ] Performance no degradada
- [ ] Compatible con arquitectura offline-first
```

### 4.2 Criterios de Aprobación

```markdown
## Criterios Obligatorios para Aprobación

### Funcionalidad
- [ ] Soporta las 7 razas específicas del proyecto
- [ ] Maneja las 4 categorías de edad correctamente
- [ ] Cumple con métricas SCRUM (≥95% precisión, <5kg error, <3s)
- [ ] Integración normativa funcional (SENASAG/REGENSA/ASOCEBU)

### Calidad de Código
- [ ] Sigue estándares de naming del dominio
- [ ] Cobertura de tests ≥70% (críticos 100%)
- [ ] No hay code smells o duplicación
- [ ] Manejo de errores específicos del dominio

### Arquitectura
- [ ] Respeta Clean Architecture (Presentation/Domain/Data)
- [ ] Compatible con offline-first
- [ ] No rompe patrones establecidos
- [ ] Performance aceptable

### Documentación
- [ ] Comentarios en español para mantenimiento local
- [ ] Documentación de APIs actualizada
- [ ] Changelog actualizado
```

## 5. Branch Protection Rules

### 5.1 Reglas para master (Producción)

```yaml
# GitHub Branch Protection para master
branch_protection:
  required_status_checks:
    - "Flutter Tests (7 breeds)"
    - "Python Tests (normative integration)"
    - "Code Coverage ≥70%"
    - "Linting (Flutter/Python)"
    - "Security Scan"
  
  required_reviews: 2
  dismiss_stale_reviews: true
  require_code_owner_reviews: true
  
  restrictions:
    - "Product Owner: Miguel Angel Escobar Lazcano"
    - "Scrum Master: Rodrigo Escobar Morón"
  
  enforce_admins: true
  allow_force_pushes: false
  allow_deletions: false
```

### 5.2 Reglas para development (Desarrollo)

```yaml
# GitHub Branch Protection para development
branch_protection:
  required_status_checks:
    - "Flutter Tests"
    - "Python Tests"
    - "Code Coverage ≥70%"
    - "Linting"
  
  required_reviews: 1
  dismiss_stale_reviews: true
  
  enforce_admins: false
  allow_force_pushes: false
  allow_deletions: false
```

## 6. Git Hooks

### 6.1 Pre-commit Hook

```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "🔍 Ejecutando validaciones pre-commit..."

# Validar que no se usen razas no soportadas
if grep -r "holstein\|hereford\|charolais" --include="*.dart" --include="*.py" .; then
    echo "❌ Error: Se encontraron razas no soportadas en Hacienda Gamelera"
    echo "   Razas soportadas: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey"
    exit 1
fi

# Validar métricas críticas
if grep -r "precision.*0\.[0-8]" --include="*.dart" --include="*.py" .; then
    echo "❌ Error: Precisión debe ser ≥95% (0.95)"
    exit 1
fi

# Validar que se usen las 7 razas específicas
if ! grep -r "BreedType\|breed_type" --include="*.dart" --include="*.py" . | grep -q "brahman\|nelore\|angus\|cebuinas\|criollo\|pardo_suizo\|jersey"; then
    echo "⚠️  Advertencia: No se encontraron referencias a las 7 razas específicas"
fi

echo "✅ Validaciones pre-commit exitosas"
```

### 6.2 Commit Message Hook

```bash
#!/bin/sh
# .git/hooks/commit-msg

commit_regex='^(feat|fix|docs|style|refactor|test|chore|perf|ci)\((data-management|analytics|monitoring|user-features|operations|core)\): .{10,}'

if ! grep -qE "$commit_regex" "$1"; then
    echo "❌ Formato de commit inválido"
    echo "   Formato requerido: <tipo>(<área>): <descripción>"
    echo "   Tipos: feat, fix, docs, style, refactor, test, chore, perf, ci"
    echo "   Áreas: data-management, analytics, monitoring, user-features, operations, core"
    echo "   Ejemplo: feat(data-management): implement continuous capture for 7 breeds"
    exit 1
fi

echo "✅ Formato de commit válido"
```

## 7. Release Management

### 7.1 Versionado Semántico

```bash
# Formato: MAJOR.MINOR.PATCH
# Ejemplos específicos del proyecto:

v1.0.0  # Release inicial con soporte completo de 7 razas
v1.1.0  # Integración SENASAG/REGENSA
v1.2.0  # Soporte ASOCEBU para competencias
v2.0.0  # Nuevos modelos ML para mayor precisión
v2.1.0  # Integración completa con Gran Paitití

# Hotfixes
v1.0.1  # Corrección crítica de precisión
v1.1.1  # Fix en generación de GMA
v1.2.1  # Corrección en exportación ASOCEBU
```

### 7.2 Changelog Template

```markdown
# Changelog - Sistema de Estimación de Peso Bovino

## [v1.0.0] - 2024-01-15 - Hacienda Gamelera Initial Release

### ✨ Nuevas Funcionalidades
- **Soporte completo de 7 razas bovinas**: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey
- **Captura continua**: 10-15 FPS durante 3-5 segundos con evaluación en tiempo real
- **Procesamiento por raza**: Modelos ML específicos para cada una de las 7 razas
- **Arquitectura offline-first**: Funcionamiento completo sin conexión a internet
- **Integración normativa**: SENASAG, REGENSA (capítulos 3.10 y 7.1), Gran Paitití

### 🎯 Métricas Alcanzadas
- **Precisión**: ≥95% (R² ≥ 0.95) ✅
- **Error absoluto**: <5 kg por animal ✅
- **Tiempo procesamiento**: <3 segundos ✅
- **Validación**: 50 animales en condiciones reales ✅

### 🏆 Mejoras vs Método Anterior
- **Reducción de tiempo**: De 2-3 días a <2 horas para 20 animales (80% reducción)
- **Eliminación de calibración**: Ahorro de 30-45 minutos diarios
- **Precisión mejorada**: De ±5-20 kg (fórmula Schaeffer) a >95% con error <5 kg
- **Eliminación de reintentos**: De 10% de animales requiriendo 2-3 intentos a 0%

### 🔧 Correcciones
- Validación estricta de las 7 razas específicas del proyecto
- Cálculo correcto de categorías de edad (4 categorías)
- Manejo robusto de errores de captura continua

### 📋 Cumplimiento Normativo
- **SENASAG**: Generación automática de reportes (PDF/CSV/XML)
- **REGENSA**: Validación de capítulos 3.10 y 7.1, generación de GMA
- **Gran Paitití**: Integración con sistema gubernamental
- **ASOCEBU**: Exportación de datos para competencias ganaderas
```
