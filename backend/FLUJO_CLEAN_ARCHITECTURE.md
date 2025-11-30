# Flujo de Datos en Clean Architecture

## 🔄 Flujo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER (API)                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  routes/farm.py                                          │   │
│  │  - Recibe HTTP Request (FarmCreateRequest DTO)            │   │
│  │  - Valida autenticación                                  │   │
│  │  - Llama a Application Service                           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              APPLICATION LAYER (Application Services)            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  application/farm_service.py                              │   │
│  │  - Orquesta Use Cases                                     │   │
│  │  - Convierte DTO → Entity (para use case)                 │   │
│  │  - Convierte Entity → DTO (para response)                │   │
│  │  - NO accede directamente a datos                         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DOMAIN LAYER (Use Cases)                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  domain/usecases/farms/create_farm_usecase.py            │   │
│  │  - Contiene lógica de negocio pura                        │   │
│  │  - Valida reglas de negocio                               │   │
│  │  - Llama a Repository Interface (no implementación)       │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              DATA LAYER (Repository Implementation)             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  data/repositories/farm_repository_impl.py               │   │
│  │  - Implementa Repository Interface                        │   │
│  │  - Accede a MongoDB/Beanie                                │   │
│  │  - Convierte Model → Entity                               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LAYER (Models)                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  data/models/farm_model.py                               │   │
│  │  - Beanie ODM Model                                       │   │
│  │  - Persistencia en MongoDB                                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## 📋 Responsabilidades por Capa

### 1. **Routes (API/Controllers)**
```python
# routes/farm.py
@router.post("")
async def create_farm(
    request: FarmCreateRequest,  # ← DTO (Presentation)
    farm_service: FarmService,     # ← Application Service
) -> FarmResponse:                # ← DTO (Presentation)
    return await farm_service.create_farm(request)
```

**Responsabilidad:**
- ✅ Recibir HTTP requests
- ✅ Validar autenticación/autorización
- ✅ Convertir HTTP → DTO
- ✅ Llamar a Application Service
- ✅ Convertir excepciones → HTTP responses
- ❌ NO contiene lógica de negocio
- ❌ NO accede a datos

---

### 2. **Application Services** (services/)
```python
# application/farm_service.py
class FarmService:
    async def create_farm(self, request: FarmCreateRequest) -> FarmResponse:
        # 1. Llama a Use Case (Domain)
        farm = await self._create_usecase.execute(
            name=request.name,
            owner_id=request.owner_id,
            ...
        )
        
        # 2. Convierte Entity → DTO
        return self._to_response(farm)
```

**Responsabilidad:**
- ✅ **Orquestar Use Cases** (coordinar múltiples use cases si es necesario)
- ✅ **Convertir DTO ↔ Entity** (entre Presentation y Domain)
- ✅ **Inyectar dependencias** (crear repositorios, use cases)
- ❌ NO contiene lógica de negocio (eso va en Use Cases)
- ❌ NO accede directamente a datos (eso va en Repositories)

---

### 3. **Use Cases** (domain/usecases/)
```python
# domain/usecases/farms/create_farm_usecase.py
class CreateFarmUseCase:
    async def execute(self, name: str, owner_id: UUID, ...) -> Farm:
        # 1. Validar reglas de negocio
        owner = await self._user_repository.get_by_id(owner_id)
        if owner is None:
            raise NotFoundException(...)
        
        # 2. Crear entidad
        farm = Farm(name=name, owner_id=owner_id, ...)
        
        # 3. Persistir usando Repository Interface
        return await self._farm_repository.save(farm)
```

**Responsabilidad:**
- ✅ **Contener lógica de negocio pura**
- ✅ **Validar reglas de negocio**
- ✅ **Llamar a Repository Interface** (no implementación)
- ❌ NO conoce DTOs (solo trabaja con Entities)
- ❌ NO conoce cómo se persiste (solo usa interfaces)

---

### 4. **Repository Implementation** (data/repositories/)
```python
# data/repositories/farm_repository_impl.py
class FarmRepositoryImpl(FarmRepository):
    async def save(self, farm: Farm) -> Farm:
        # 1. Convertir Entity → Model
        model = FarmModel.from_entity(farm)
        
        # 2. Persistir en MongoDB
        await model.insert()
        
        # 3. Convertir Model → Entity
        return model.to_entity()
```

**Responsabilidad:**
- ✅ **Implementar Repository Interface**
- ✅ **Acceder a datos** (MongoDB, Beanie)
- ✅ **Convertir Entity ↔ Model**
- ❌ NO contiene lógica de negocio

---

### 5. **Models** (data/models/)
```python
# data/models/farm_model.py
class FarmModel(Document):
    # Beanie ODM para MongoDB
    id: UUID
    name: str
    ...
```

**Responsabilidad:**
- ✅ **Persistencia** (MongoDB, Beanie ODM)
- ✅ **Validación de datos** (Pydantic)
- ❌ NO contiene lógica de negocio

---

## ❓ ¿Los Services se comunican con los datos?

### ❌ NO directamente

Los **Application Services**:
- ✅ Se comunican con **Use Cases** (Domain)
- ✅ Se comunican con **DTOs** (Presentation)
- ❌ NO se comunican directamente con **Repositories** (eso lo hacen los Use Cases)
- ❌ NO se comunican directamente con **Models/Data** (eso lo hacen los Repositories)

### ✅ Flujo Correcto

```
Routes → Application Service → Use Case → Repository → Model → MongoDB
  ↑                                                              ↓
  └────────────────── DTOs (Response) ←────────────────────────┘
```

---

## 🎯 Función de los Application Services

**En resumen, los Application Services:**

1. **Orquestan Use Cases** - Coordinan qué use cases ejecutar
2. **Convierten entre capas** - DTO ↔ Entity
3. **Inyectan dependencias** - Crean repositorios y use cases
4. **NO contienen lógica de negocio** - Eso va en Use Cases
5. **NO acceden a datos** - Eso va en Repositories

---

## 📊 Ejemplo Completo: Crear Finca

```python
# 1. ROUTE (Presentation)
@router.post("")
async def create_farm(
    request: FarmCreateRequest,  # DTO
    farm_service: FarmService,
) -> FarmResponse:  # DTO
    return await farm_service.create_farm(request)

# 2. APPLICATION SERVICE
class FarmService:
    async def create_farm(self, request: FarmCreateRequest) -> FarmResponse:
        # Orquesta Use Case
        farm = await self._create_usecase.execute(
            name=request.name,  # DTO → Use Case params
            owner_id=request.owner_id,
            ...
        )
        # Convierte Entity → DTO
        return FarmResponse(
            id=farm.id,
            name=farm.name,
            ...
        )

# 3. USE CASE (Domain)
class CreateFarmUseCase:
    async def execute(self, name: str, owner_id: UUID, ...) -> Farm:
        # Lógica de negocio
        owner = await self._user_repository.get_by_id(owner_id)
        if owner is None:
            raise NotFoundException(...)
        
        farm = Farm(name=name, ...)  # Entity
        return await self._farm_repository.save(farm)  # Repository Interface

# 4. REPOSITORY IMPLEMENTATION (Data)
class FarmRepositoryImpl:
    async def save(self, farm: Farm) -> Farm:
        model = FarmModel.from_entity(farm)  # Entity → Model
        await model.insert()  # MongoDB
        return model.to_entity()  # Model → Entity
```

---

## ✅ Conclusión

**Los Application Services NO se comunican directamente con los datos.**

Su función es:
- 🎯 **Orquestar** Use Cases
- 🔄 **Convertir** DTO ↔ Entity
- 📦 **Coordinar** entre Presentation y Domain

Los datos los manejan:
- **Use Cases** → llaman a **Repository Interfaces**
- **Repositories** → implementan acceso a **Models/Data**

