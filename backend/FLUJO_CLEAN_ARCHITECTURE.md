# Flujo de Datos en Clean Architecture

## 🔄 Flujo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER (API)                      │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  routes/animals.py                                       │   │
│  │  - Recibe HTTP Request (AnimalCreateRequest DTO)          │   │
│  │  - Valida autenticación                                  │   │
│  │  - Usa Mapper para convertir DTO → parámetros            │   │
│  │  - Llama directamente a Use Case (inyección)             │   │
│  │  - Usa Mapper para convertir Entity → DTO                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DOMAIN LAYER (Use Cases)                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  domain/usecases/animals/create_animal_usecase.py        │   │
│  │  - Contiene lógica de negocio pura                        │   │
│  │  - Valida reglas de negocio                               │   │
│  │  - Llama a Repository Interface (no implementación)       │   │
│  │  - Retorna Entity (no DTO)                                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              DATA LAYER (Repository Implementation)             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  data/repositories/animal_repository_impl.py             │   │
│  │  - Implementa Repository Interface                        │   │
│  │  - Accede a MongoDB/Beanie                                │   │
│  │  - Convierte Entity ↔ Model                               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LAYER (Models)                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  data/models/animal_model.py                             │   │
│  │  - Beanie ODM Model                                       │   │
│  │  - Persistencia en MongoDB                                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## 📋 Responsabilidades por Capa

### 1. **Routes (API/Controllers)**
```python
# routes/animals.py
@router.post("")
@handle_domain_exceptions
async def create_animal(
    request: AnimalCreateRequest,  # ← DTO (Presentation)
    create_usecase: Annotated[
        CreateAnimalUseCase, Depends(get_create_animal_usecase)  # ← Use Case (inyectado)
    ],
) -> AnimalResponse:  # ← DTO (Presentation)
    # 1. Convertir DTO → parámetros usando Mapper
    params = AnimalMapper.create_request_to_params(request)
    
    # 2. Ejecutar Use Case (retorna Entity)
    animal = await create_usecase.execute(**params)
    
    # 3. Convertir Entity → DTO usando Mapper
    return AnimalMapper.to_response(animal)
```

**Responsabilidad:**
- ✅ Recibir HTTP requests
- ✅ Validar autenticación/autorización
- ✅ Convertir HTTP → DTO
- ✅ Usar Mapper para convertir DTO → parámetros del Use Case
- ✅ Llamar directamente a Use Case (inyección de dependencias)
- ✅ Usar Mapper para convertir Entity → DTO
- ✅ Usar decorador `@handle_domain_exceptions` para manejo de errores
- ❌ NO contiene lógica de negocio
- ❌ NO accede a datos

---

### 2. **Mappers** (api/mappers/)
```python
# api/mappers/animal_mapper.py
class AnimalMapper:
    @staticmethod
    def create_request_to_params(request: AnimalCreateRequest) -> dict:
        """Convierte DTO a parámetros para Use Case."""
        return {
            "ear_tag": request.ear_tag,
            "breed": request.breed.value,
            ...
        }
    
    @staticmethod
    def to_response(animal: Animal) -> AnimalResponse:
        """Convierte Entity a DTO."""
        return AnimalResponse(
            id=animal.id,
            ear_tag=animal.ear_tag,
            ...
        )
```

**Responsabilidad:**
- ✅ **Convertir DTO ↔ Entity** (entre Presentation y Domain)
- ✅ **Convertir DTO → parámetros** para Use Cases
- ❌ NO contiene lógica de negocio
- ❌ NO accede a datos

---

### 3. **Utils** (core/utils/ y api/utils/)
```python
# core/utils/ml_inference.py
async def estimate_weight_from_image(...) -> WeightEstimation:
    """Función auxiliar para inferencia ML."""
    ...

# api/utils/pagination.py
def calculate_skip(page: int, page_size: int) -> int:
    """Calcula skip para paginación."""
    ...
```

**Responsabilidad:**
- ✅ Funciones auxiliares reutilizables
- ✅ Sin estado ni lógica de negocio compleja
- ✅ Pueden ser usadas desde Routes o Use Cases

---

### 4. **Use Cases** (domain/usecases/)
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

### 5. **Repository Implementation** (data/repositories/)
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

### 6. **Models** (data/models/)
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

## ❓ ¿Las Routes acceden directamente a datos?

### ❌ NO directamente

Las **Routes**:
- ✅ Se comunican con **Use Cases** (Domain) mediante inyección de dependencias
- ✅ Se comunican con **DTOs** (Presentation) y **Mappers**
- ✅ Usan **Utils** para funciones auxiliares
- ❌ NO se comunican directamente con **Repositories** (eso lo hacen los Use Cases)
- ❌ NO se comunican directamente con **Models/Data** (eso lo hacen los Repositories)

### ✅ Flujo Correcto

```
Routes → Use Case → Repository Interface
  ↓                      ↓
Mappers          Repository Impl → Model → MongoDB
  ↑                      ↓
DTOs ←───────────────────┘
```

**Nota**: Los Application Services fueron eliminados. La conversión DTO ↔ Entity ahora se hace mediante Mappers en la capa de presentación.

---

## 📊 Ejemplo Completo: Crear Animal

```python
# 1. ROUTE (Presentation)
@router.post("")
@handle_domain_exceptions
async def create_animal(
    request: AnimalCreateRequest,  # DTO
    create_usecase: Annotated[
        CreateAnimalUseCase, Depends(get_create_animal_usecase)
    ],
) -> AnimalResponse:  # DTO
    # Convertir DTO → parámetros usando Mapper
    params = AnimalMapper.create_request_to_params(request)
    
    # Ejecutar Use Case (retorna Entity)
    animal = await create_usecase.execute(**params)
    
    # Convertir Entity → DTO usando Mapper
    return AnimalMapper.to_response(animal)

# 2. MAPPER (Presentation)
class AnimalMapper:
    @staticmethod
    def create_request_to_params(request: AnimalCreateRequest) -> dict:
        """Convierte DTO a parámetros para Use Case."""
        return {
            "ear_tag": request.ear_tag,
            "breed": request.breed.value,
            "birth_date": request.birth_date,
            ...
        }
    
    @staticmethod
    def to_response(animal: Animal) -> AnimalResponse:
        """Convierte Entity a DTO."""
        return AnimalResponse(
            id=animal.id,
            ear_tag=animal.ear_tag,
            ...
        )

# 3. USE CASE (Domain)
class CreateAnimalUseCase:
    async def execute(self, ear_tag: str, breed: str, ...) -> Animal:
        # Lógica de negocio
        existing = await self._animal_repository.find_by_ear_tag(ear_tag, farm_id)
        if existing is not None:
            raise AlreadyExistsException(...)
        
        animal = Animal(ear_tag=ear_tag, breed=breed, ...)  # Entity
        return await self._animal_repository.save(animal)  # Repository Interface

# 4. REPOSITORY IMPLEMENTATION (Data)
class AnimalRepositoryImpl:
    async def save(self, animal: Animal) -> Animal:
        model = AnimalModel.from_entity(animal)  # Entity → Model
        await model.insert()  # MongoDB
        return model.to_entity()  # Model → Entity
```

---

## ✅ Conclusión

**Las Routes NO acceden directamente a datos. Usan Use Cases mediante inyección de dependencias.**

Arquitectura actual:
- 🎯 **Routes** → inyectan y llaman directamente a **Use Cases**
- 🔄 **Mappers** → convierten **DTO ↔ Entity** (en capa de presentación)
- 🛠️ **Utils** → funciones auxiliares (ML inference, paginación, etc.)
- 📦 **Use Cases** → contienen lógica de negocio y llaman a **Repository Interfaces**
- 💾 **Repositories** → implementan acceso a **Models/Data**

**Nota histórica**: Los Application Services fueron eliminados durante la migración a Clean Architecture para simplificar el flujo y seguir el patrón estándar: Routes → Use Cases → Repositories.

