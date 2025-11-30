# Registro de Migración a Clean Architecture

**Fecha de inicio**: Diciembre 2024  
**Estrategia**: Migración incremental por módulo  
**Estado**: En progreso - 4 módulos completados

---

## 📋 Resumen Ejecutivo

### **Módulos Migrados**:
- ✅ **Animal** (completado)
- ✅ **User** (completado)
- ✅ **Role** (completado)
- ✅ **Auth** (completado)

### **Módulos Pendientes**:
- ⏳ Weighing
- ⏳ Alert
- ⏳ Farm
- ⏳ Sync
- ⏳ Schemas (mover a api/schemas/)

---

## 🗂️ Cambios por Carpeta - Backend

### **1. Domain Layer** (NUEVO - Creado)

#### **Archivos Creados**:

```
backend/app/domain/
├── __init__.py                                    ✅ NUEVO
├── entities/
│   ├── __init__.py                               ✅ NUEVO
│   ├── animal.py                                  ✅ NUEVO (Entidad pura)
│   ├── user.py                                    ✅ NUEVO (Entidad pura)
│   └── role.py                                    ✅ NUEVO (Entidad pura)
├── repositories/
│   ├── __init__.py                               ✅ NUEVO
│   ├── animal_repository.py                      ✅ NUEVO (Interfaz ABC)
│   ├── user_repository.py                         ✅ NUEVO (Interfaz ABC)
│   └── role_repository.py                         ✅ NUEVO (Interfaz ABC)
├── usecases/
│   ├── __init__.py                               ✅ NUEVO
│   ├── animals/
│   │   ├── __init__.py                           ✅ NUEVO
│   │   ├── create_animal_usecase.py              ✅ NUEVO
│   │   ├── get_animal_by_id_usecase.py           ✅ NUEVO
│   │   ├── get_animals_by_farm_usecase.py        ✅ NUEVO
│   │   ├── update_animal_usecase.py              ✅ NUEVO
│   │   └── delete_animal_usecase.py              ✅ NUEVO
│   ├── users/
│   │   ├── __init__.py                           ✅ NUEVO
│   │   ├── create_user_usecase.py                ✅ NUEVO
│   │   ├── get_user_by_id_usecase.py             ✅ NUEVO
│   │   ├── get_all_users_usecase.py              ✅ NUEVO
│   │   ├── update_user_usecase.py                ✅ NUEVO
│   │   └── delete_user_usecase.py                ✅ NUEVO
│   ├── roles/
│   │   ├── __init__.py                           ✅ NUEVO
│   │   ├── create_role_usecase.py               ✅ NUEVO
│   │   ├── get_role_by_id_usecase.py             ✅ NUEVO
│   │   ├── get_all_roles_usecase.py              ✅ NUEVO
│   │   ├── update_role_usecase.py                ✅ NUEVO
│   │   └── delete_role_usecase.py                ✅ NUEVO
│   └── auth/
│       ├── __init__.py                           ✅ NUEVO
│       ├── authenticate_user_usecase.py          ✅ NUEVO
│       └── get_user_by_token_usecase.py          ✅ NUEVO
└── shared/
    └── constants/                                 ✅ NUEVO (movido desde core/)
        ├── breeds.py
        ├── age_categories.py
        ├── metrics.py
        └── hacienda.py
```

**Total**: ~35 archivos nuevos

**Propósito**: Lógica de negocio pura sin dependencias externas

---

### **2. Data Layer** (NUEVO - Creado)

#### **Archivos Creados**:

```
backend/app/data/
├── __init__.py                                    ✅ NUEVO
├── models/
│   ├── __init__.py                               ✅ NUEVO
│   ├── animal_model.py                           ✅ NUEVO (Movido desde models/)
│   ├── user_model.py                             ✅ NUEVO (Movido desde models/)
│   └── role_model.py                              ✅ NUEVO (Movido desde models/)
└── repositories/
    ├── __init__.py                               ✅ NUEVO
    ├── animal_repository_impl.py                  ✅ NUEVO (Implementación)
    ├── user_repository_impl.py                    ✅ NUEVO (Implementación)
    └── role_repository_impl.py                    ✅ NUEVO (Implementación)
```

**Total**: 11 archivos nuevos

**Propósito**: Implementación de infraestructura (MongoDB, Beanie)

---

### **3. Services** (MODIFICADO)

#### **Archivos Modificados**:

```
backend/app/services/
├── animal_service.py                              🔄 MODIFICADO
│   - Refactorizado para usar Use Cases
│   - Eliminado acceso directo a Beanie
│   - Ahora orquesta casos de uso del dominio
├── user_service.py                                🔄 MODIFICADO
│   - Refactorizado para usar Use Cases
│   - Eliminado acceso directo a Beanie
│   - Usa casos de uso de usuarios
├── role_service.py                                🔄 MODIFICADO
│   - Refactorizado para usar Use Cases
│   - Eliminado acceso directo a Beanie
│   - Usa casos de uso de roles
└── auth_service.py                                🔄 MODIFICADO
    - Refactorizado para usar Use Cases
    - Usa AuthenticateUserUseCase y GetUserByTokenUseCase
    - Mantiene métodos estáticos para JWT y password hashing
```

**Cambios principales**:
- ✅ Services usan Use Cases en lugar de acceso directo a Beanie
- ✅ Inyectan Repository interfaces (Dependency Inversion)
- ✅ Convierten entre Domain Entities y API Schemas

---

### **4. API Routes** (MODIFICADO)

#### **Archivos Modificados**:

```
backend/app/api/routes/
├── animals.py                                     ✅ SIN CAMBIOS (usa AnimalService)
├── user.py                                        🔄 MODIFICADO
│   - Actualizado para usar entidad User del dominio
│   - Imports actualizados
├── role.py                                        🔄 MODIFICADO
│   - Actualizado para usar entidad User del dominio
│   - Imports actualizados
└── farm.py                                        🔄 MODIFICADO
    - Actualizado para usar entidad User del dominio
    - Imports actualizados
```

**Razón**: Las rutas usan Services que ahora usan Clean Architecture internamente. Solo se actualizaron tipos e imports.

---

### **5. Core** (MODIFICADO)

#### **Archivos Modificados**:

```
backend/app/core/
├── config.py                                      🔄 MODIFICADO
│   - Actualizado para usar Pydantic Settings con Field()
│   - Removidas configuraciones AWS
├── database.py                                    🔄 MODIFICADO
│   - Importa modelos desde data/models/ (Animal, User, Role)
│   - Mantiene compatibilidad con modelos legacy
├── lifespan.py                                    ✅ NUEVO
│   - Gestiona ciclo de vida de FastAPI
├── middleware.py                                  ✅ NUEVO
│   - Configuración de middlewares (CORS)
└── routes.py                                      ✅ NUEVO
    - Registro centralizado de rutas
```

**Cambios principales**:
- ✅ Separación de responsabilidades en `main.py`
- ✅ Configuración mejorada con Pydantic Settings
- ✅ Imports actualizados para modelos migrados

---

### **6. API Dependencies** (MODIFICADO)

#### **Archivos Modificados**:

```
backend/app/api/
├── dependencies.py                                🔄 MODIFICADO
│   - Usa casos de uso directamente (GetUserByTokenUseCase)
│   - Retorna entidades del dominio (User)
│   - Eliminada carpeta dependencies/ (consolidado)
└── dependencies/                                  ❌ ELIMINADO
    └── auth.py                                    ❌ ELIMINADO (consolidado en dependencies.py)
```

**Cambios principales**:
- ✅ `get_current_user` usa `GetUserByTokenUseCase` directamente
- ✅ Retorna entidad `User` del dominio (no `UserModel`)
- ✅ Consolidado en un solo archivo `dependencies.py`

---

### **7. Main** (REFACTORIZADO)

#### **Archivos Modificados**:

```
backend/app/main.py                                🔄 REFACTORIZADO
    - Separado en módulos: database.py, lifespan.py, middleware.py, routes.py
    - Importa modelos desde data/models/ (Animal, User, Role)
    - Mantiene compatibilidad con modelos legacy
```

**Cambios**:
```python
# ANTES: Todo en main.py
# DESPUÉS: Separado en módulos
from app.core.database import connect_to_mongodb, init_database
from app.core.lifespan import lifespan
from app.core.middleware import setup_middleware
from app.core.routes import setup_routes
```

---

### **8. Models** (LEGACY - Coexistencia Temporal)

#### **Estado Actual**:

```
backend/app/models/
├── __init__.py                                    ⚠️  MANTENER (re-exporta desde data/models/)
├── animal_model.py                                ⚠️  MANTENER (temporalmente, para init_beanie)
├── alert_model.py                                 ✅ MANTENER (pendiente migrar)
├── farm_model.py                                  ✅ MANTENER (pendiente migrar)
├── role_model.py                                  ⚠️  MANTENER (temporalmente, para init_beanie)
├── user_model.py                                  ⚠️  MANTENER (temporalmente, para init_beanie)
└── weight_estimation_model.py                    ✅ MANTENER (pendiente migrar)
```

**⚠️ IMPORTANTE**: 
- Los modelos migrados (Animal, User, Role) están en `data/models/` (usados por repositorios)
- Los modelos en `models/` se mantienen temporalmente para `init_beanie` en `database.py`
- `models/__init__.py` re-exporta desde `data/models/` para compatibilidad
- Eliminar modelos de `models/` solo cuando:
  1. Todos los módulos estén migrados
  2. `database.py` importe todos los modelos desde `data/models/`
  3. No haya referencias al modelo antiguo

---

## 📊 Estadísticas de Migración

### **Archivos Creados**: ~50
- Domain Layer: ~35 archivos (entities, repositories, usecases)
- Data Layer: 11 archivos (models, repositories)
- Core: 4 archivos nuevos (lifespan, middleware, routes, database)

### **Archivos Modificados**: 9
- `services/animal_service.py`
- `services/user_service.py`
- `services/role_service.py`
- `services/auth_service.py`
- `api/dependencies.py`
- `api/routes/user.py`
- `api/routes/role.py`
- `api/routes/farm.py`
- `core/database.py`
- `core/config.py`
- `main.py` (refactorizado)

### **Archivos a Eliminar** (futuro): 3
- `models/animal_model.py` (después de migración completa)
- `models/user_model.py` (después de migración completa)
- `models/role_model.py` (después de migración completa)

---

## 🔄 Flujo de Datos (Clean Architecture)

### **ANTES (MVC)**:
```
API Route → Service → Model (Beanie) → MongoDB
```

### **DESPUÉS (Clean Architecture)**:
```
API Route → Service → Use Case → Repository Interface
                                      ↓
                              Repository Implementation → Model (Beanie) → MongoDB
```

---

## 📝 Checklist de Migración por Módulo

### **✅ Módulo Animal** (COMPLETADO)

- [x] Crear `domain/entities/animal.py`
- [x] Crear `domain/repositories/animal_repository.py` (interfaz)
- [x] Crear `domain/usecases/animals/` (5 use cases)
- [x] Mover `models/animal_model.py` → `data/models/animal_model.py`
- [x] Crear `data/repositories/animal_repository_impl.py`
- [x] Refactorizar `services/animal_service.py`
- [x] Actualizar `main.py` (imports)
- [x] Verificar que funciona (sin errores de linter)
- [ ] **Pendiente**: Eliminar `models/animal_model.py` (después de migración completa)

---

### **⏳ Módulo Weighing** (PENDIENTE)

- [ ] Crear `domain/entities/weighing.py`
- [ ] Crear `domain/repositories/weighing_repository.py`
- [ ] Crear `domain/usecases/weighings/` (use cases)
- [ ] Mover `models/weight_estimation_model.py` → `data/models/`
- [ ] Crear `data/repositories/weighing_repository_impl.py`
- [ ] Refactorizar `services/weighing_service.py`
- [ ] Actualizar imports en `main.py`

---

### **⏳ Módulo Alert** (PENDIENTE)

- [ ] Crear `domain/entities/alert.py`
- [ ] Crear `domain/repositories/alert_repository.py`
- [ ] Crear `domain/usecases/alerts/` (use cases)
- [ ] Mover `models/alert_model.py` → `data/models/`
- [ ] Crear `data/repositories/alert_repository_impl.py`
- [ ] Refactorizar `services/alert_service.py`
- [ ] Actualizar imports en `main.py`

---

### **✅ Módulo User** (COMPLETADO)

- [x] Crear `domain/entities/user.py`
- [x] Crear `domain/repositories/user_repository.py` (interfaz)
- [x] Crear `domain/usecases/users/` (5 use cases)
- [x] Mover `models/user_model.py` → `data/models/user_model.py`
- [x] Crear `data/repositories/user_repository_impl.py`
- [x] Refactorizar `services/user_service.py`
- [x] Actualizar `main.py` (imports)
- [x] Actualizar `api/dependencies.py` para usar use cases
- [x] Verificar que funciona (sin errores de linter)

---

### **✅ Módulo Role** (COMPLETADO)

- [x] Crear `domain/entities/role.py`
- [x] Crear `domain/repositories/role_repository.py` (interfaz)
- [x] Crear `domain/usecases/roles/` (5 use cases)
- [x] Mover `models/role_model.py` → `data/models/role_model.py`
- [x] Crear `data/repositories/role_repository_impl.py`
- [x] Refactorizar `services/role_service.py`
- [x] Actualizar `main.py` (imports)
- [x] Verificar que funciona (sin errores de linter)

---

### **✅ Módulo Auth** (COMPLETADO)

- [x] Crear `domain/usecases/auth/` (2 use cases)
- [x] Refactorizar `services/auth_service.py` para usar use cases
- [x] Actualizar `api/dependencies.py` para usar use cases directamente
- [x] Eliminar carpeta `api/dependencies/` (consolidado en `dependencies.py`)
- [x] Verificar que funciona (sin errores de linter)

---

### **⏳ Módulo Farm** (PENDIENTE)

- [ ] Similar a Animal (1 módulo)

---

### **⏳ Módulo Sync** (PENDIENTE)

- [ ] Similar a Animal (usa AnimalRepository y WeighingRepository)

---

### **⏳ Fase Final: Schemas** (PENDIENTE)

- [ ] Mover `schemas/` → `api/schemas/`
- [ ] Actualizar todos los imports en el proyecto
- [ ] Verificar que todo funciona

---

## 🗑️ Archivos a Eliminar (Después de Migración Completa)

### **Backend**:

```
backend/app/models/
├── animal_model.py                                ❌ ELIMINAR
├── weight_estimation_model.py                    ❌ ELIMINAR (después de migrar)
├── alert_model.py                                 ❌ ELIMINAR (después de migrar)
├── user_model.py                                  ❌ ELIMINAR (después de migrar)
├── farm_model.py                                  ❌ ELIMINAR (después de migrar)
└── role_model.py                                  ❌ ELIMINAR (después de migrar)
```

**⚠️ IMPORTANTE**: 
- Eliminar solo cuando **TODOS** los módulos estén migrados
- Verificar que no hay referencias en otros archivos
- Hacer backup antes de eliminar

---

## 📚 Documentación Creada

### **Documentos de Análisis**:

```
backend/
├── ANALISIS_ARQUITECTURA.md                      ✅ NUEVO
│   - Análisis de estructura actual vs Clean Architecture
│   - Comparación de arquitecturas
│   - Estimaciones de tiempo
│
├── PLAN_MIGRACION.md                              ✅ NUEVO
│   - Plan detallado de migración incremental
│   - Orden de migración por módulo
│   - Estrategias de mitigación de riesgos
│
└── MIGRACION_CLEAN_ARCHITECTURE.md                ✅ NUEVO (este archivo)
    - Registro de cambios por carpeta
    - Checklist de migración
    - Archivos a eliminar
```

---

## 🔍 Verificación de Cambios

### **Comandos para Verificar**:

```bash
# Ver archivos nuevos en domain/
find backend/app/domain -type f -name "*.py" | sort

# Ver archivos nuevos en data/
find backend/app/data -type f -name "*.py" | sort

# Verificar imports de AnimalModel
grep -r "from.*models.*import.*AnimalModel" backend/app/

# Verificar que no hay referencias al modelo antiguo
grep -r "from.*app\.models.*AnimalModel" backend/app/
```

---

## 📈 Progreso General

| Módulo | Estado | Archivos Creados | Archivos Modificados | Tiempo Estimado |
|--------|--------|------------------|----------------------|-----------------|
| Animal | ✅ Completado | 16 | 2 | 4-6 horas |
| User | ✅ Completado | 16 | 3 | 4-6 horas |
| Role | ✅ Completado | 16 | 2 | 4-6 horas |
| Auth | ✅ Completado | 2 | 2 | 2-3 horas |
| Weighing | ⏳ Pendiente | - | - | 4-6 horas |
| Alert | ⏳ Pendiente | - | - | 3-4 horas |
| Farm | ⏳ Pendiente | - | - | 3-4 horas |
| Sync | ⏳ Pendiente | - | - | 4-6 horas |
| Schemas | ⏳ Pendiente | - | - | 2-3 horas |
| **TOTAL** | **4/9** | **50** | **9** | **~26-41 horas** |

---

## 🎯 Próximos Pasos

1. **Continuar con módulo Weighing**
   - Similar a Animal
   - Usa AnimalRepository (ya creado)

2. **Migrar módulo Alert**
   - Independiente
   - Más simple que Animal

3. **Migrar User/Farm/Role**
   - 3 módulos simples
   - Pueden hacerse en paralelo

4. **Migrar Sync**
   - Más complejo
   - Usa AnimalRepository y WeighingRepository

5. **Mover Schemas**
   - Último paso
   - Actualizar imports en batch

6. **Limpieza Final**
   - Eliminar modelos antiguos en `models/`
   - Verificar que todo funciona
   - Actualizar documentación

---

## 📝 Notas Importantes

1. **No eliminar modelos antiguos todavía**: Otros módulos aún los referencian
2. **Mantener compatibilidad temporal**: Durante migración, ambos sistemas coexisten
3. **Verificar después de cada módulo**: Ejecutar tests y verificar endpoints
4. **Actualizar este documento**: Después de migrar cada módulo

---

**Última actualización**: Diciembre 2024  
**Próxima actualización**: Después de migrar módulo Weighing

---

## 📚 Documentos de Migración

### **Documentos a Mantener**:

- ✅ **`MIGRACION_CLEAN_ARCHITECTURE.md`** (este archivo) - Registro detallado de cambios
- ✅ **`INTEGRATION_GUIDE.md`** - Guía de integración TFLite (útil para ML)

### **Documentos a Consolidar/Eliminar**:

- ⚠️ **`PLAN_MIGRACION.md`** - Plan inicial (ya en ejecución, puede consolidarse)
- ⚠️ **`CAMBIOS_MIGRACION.md`** - Resumen de cambios (consolidado en este documento)
- ⚠️ **`ANALISIS_ARQUITECTURA.md`** - Análisis inicial (ya no necesario, fue pre-migración)

**Recomendación**: 
- Mantener `MIGRACION_CLEAN_ARCHITECTURE.md` como registro principal
- Mantener `INTEGRATION_GUIDE.md` (útil para TFLite)
- Consolidar información de `PLAN_MIGRACION.md` y `CAMBIOS_MIGRACION.md` en este documento
- Eliminar `ANALISIS_ARQUITECTURA.md` (análisis pre-migración, ya no relevante)

