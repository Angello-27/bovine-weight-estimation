"""
Animal Repository Implementation - Data Layer
Implementación del repositorio de animales usando Beanie ODM
"""

from uuid import UUID

from ...domain.entities.animal import Animal
from ...domain.repositories.animal_repository import AnimalRepository
from ..models.animal_model import AnimalModel


class AnimalRepositoryImpl(AnimalRepository):
    """
    Implementación del repositorio de animales usando Beanie ODM.

    Single Responsibility: Persistencia de animales en MongoDB.
    """

    def _to_entity(self, model: AnimalModel) -> Animal:
        """
        Convierte AnimalModel (Data) a Animal (Domain Entity).

        Args:
            model: Modelo de Beanie

        Returns:
            Entidad Animal del dominio
        """
        return Animal(
            id=model.id,
            ear_tag=model.ear_tag,
            breed=model.breed,
            birth_date=model.birth_date,
            gender=model.gender,
            name=model.name,
            color=model.color,
            birth_weight_kg=model.birth_weight_kg,
            mother_id=model.mother_id,
            father_id=model.father_id,
            observations=model.observations,
            photo_url=model.photo_url,
            status=model.status,
            farm_id=model.farm_id,
            registration_date=model.registration_date,
            last_updated=model.last_updated,
            device_id=model.device_id,
            synced_at=model.synced_at,
        )

    def _to_model(self, entity: Animal) -> AnimalModel:
        """
        Convierte Animal (Domain Entity) a AnimalModel (Data).

        Args:
            entity: Entidad Animal del dominio

        Returns:
            Modelo de Beanie
        """
        return AnimalModel(
            id=entity.id,
            ear_tag=entity.ear_tag,
            breed=entity.breed,
            birth_date=entity.birth_date,
            gender=entity.gender,
            name=entity.name,
            color=entity.color,
            birth_weight_kg=entity.birth_weight_kg,
            mother_id=entity.mother_id,
            father_id=entity.father_id,
            observations=entity.observations,
            photo_url=entity.photo_url,
            status=entity.status,
            farm_id=entity.farm_id,
            registration_date=entity.registration_date,
            last_updated=entity.last_updated,
            device_id=entity.device_id,
            synced_at=entity.synced_at,
        )

    async def save(self, animal: Animal) -> Animal:
        """
        Guarda o actualiza un animal.

        Args:
            animal: Entidad Animal a persistir

        Returns:
            Animal guardado con ID asignado
        """
        model = self._to_model(animal)
        await model.save()
        return self._to_entity(model)

    async def get_by_id(self, animal_id: UUID) -> Animal | None:
        """
        Obtiene un animal por ID.

        Args:
            animal_id: ID del animal

        Returns:
            Animal si existe, None si no existe
        """
        model = await AnimalModel.get(animal_id)
        if model is None:
            return None
        return self._to_entity(model)

    async def find_by_ear_tag(self, ear_tag: str, farm_id: UUID) -> Animal | None:
        """
        Busca un animal por caravana y hacienda.

        Args:
            ear_tag: Número de caravana
            farm_id: ID de la hacienda

        Returns:
            Animal si existe, None si no existe
        """
        model = await AnimalModel.find_one(
            AnimalModel.ear_tag == ear_tag, AnimalModel.farm_id == farm_id
        )
        if model is None:
            return None
        return self._to_entity(model)

    async def get_by_farm(
        self,
        farm_id: UUID,
        skip: int = 0,
        limit: int = 50,
        status: str | None = None,
    ) -> list[Animal]:
        """
        Obtiene animales de una hacienda con paginación.

        Args:
            farm_id: ID de la hacienda
            skip: Offset para paginación
            limit: Límite de resultados
            status: Filtro opcional por estado

        Returns:
            Lista de Animal
        """
        query = AnimalModel.find(AnimalModel.farm_id == farm_id)

        if status:
            query = query.find(AnimalModel.status == status)

        models = await query.skip(skip).limit(limit).to_list()

        return [self._to_entity(model) for model in models]

    async def delete(self, animal_id: UUID) -> bool:
        """
        Elimina un animal (soft delete).

        Args:
            animal_id: ID del animal

        Returns:
            True si se eliminó exitosamente
        """
        model = await AnimalModel.get(animal_id)
        if model is None:
            return False

        # Soft delete (marcar como inactive)
        model.status = "inactive"
        model.update_timestamp()
        await model.save()

        return True

    async def find_by_criteria(
        self,
        farm_id: UUID,
        breed: str | None = None,
        age_category: str | None = None,
        gender: str | None = None,
        status: str | None = None,
        limit: int | None = None,
    ) -> list[Animal]:
        """
        Busca animales por múltiples criterios de filtrado.

        Args:
            farm_id: ID de la finca (requerido)
            breed: Raza del animal (opcional)
            age_category: Categoría de edad (opcional)
            gender: Género del animal (opcional)
            status: Estado del animal (opcional)
            limit: Límite de resultados (opcional)

        Returns:
            Lista de Animal que cumplen los criterios
        """
        # Construir query base
        query = AnimalModel.find(AnimalModel.farm_id == farm_id)

        # Aplicar filtros
        if breed:
            query = query.find(AnimalModel.breed == breed)
        if gender:
            query = query.find(AnimalModel.gender == gender)
        if status:
            query = query.find(AnimalModel.status == status)

        # Obtener todos los animales que cumplen los filtros básicos
        models = await query.to_list()

        # Filtrar por categoría de edad si se especifica
        if age_category:
            filtered_models = []
            for model in models:
                animal_entity = self._to_entity(model)
                animal_age_category = animal_entity.calculate_age_category()
                if animal_age_category.value == age_category:
                    filtered_models.append(model)
            models = filtered_models

        # Aplicar límite si se especifica
        if limit:
            models = models[:limit]

        return [self._to_entity(model) for model in models]

    async def find_by_criteria_dict(
        self,
        filters: dict,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Animal]:
        """
        Busca animales por criterios de filtrado genérico (patrón estándar).

        Args:
            filters: Diccionario con criterios de filtrado
            skip: Offset para paginación
            limit: Límite de resultados

        Returns:
            Lista de Animal que coinciden con los criterios
        """
        # Construir filtros para Beanie (campos directos)
        beanie_filters = {}
        age_category_filter = None

        for key, value in filters.items():
            if value is not None:
                if key == "age_category":
                    # age_category necesita procesamiento especial
                    age_category_filter = value
                elif hasattr(AnimalModel, key):
                    beanie_filters[key] = value

        # Si no hay filtros básicos, usar find_all(), de lo contrario usar find()
        if not beanie_filters:
            query = AnimalModel.find_all()
        else:
            query = AnimalModel.find(beanie_filters)

        # Obtener modelos
        models = (
            await query.skip(skip)
            .limit(limit * 2 if age_category_filter else limit)
            .to_list()
        )

        # Si hay filtro de age_category, filtrar en memoria
        if age_category_filter:
            filtered_models = []
            for model in models:
                animal_entity = self._to_entity(model)
                animal_age_category = animal_entity.calculate_age_category()
                if animal_age_category.value == age_category_filter:
                    filtered_models.append(model)
                    if len(filtered_models) >= limit:
                        break
            models = filtered_models[:limit]
        else:
            models = models[:limit]

        return [self._to_entity(model) for model in models]

    async def count_by_criteria(self, filters: dict) -> int:
        """
        Cuenta animales que coinciden con criterios de filtrado.

        Args:
            filters: Diccionario con criterios de filtrado

        Returns:
            Número total de animales que coinciden con los criterios
        """
        # Construir filtros para Beanie (campos directos)
        beanie_filters = {}
        age_category_filter = None

        for key, value in filters.items():
            if value is not None:
                if key == "age_category":
                    age_category_filter = value
                elif hasattr(AnimalModel, key):
                    beanie_filters[key] = value

        # Si hay filtro de age_category, necesitamos contar en memoria
        if age_category_filter:
            # Obtener todos los modelos que cumplen los filtros básicos
            if not beanie_filters:
                query = AnimalModel.find_all()
            else:
                query = AnimalModel.find(beanie_filters)

            models = await query.to_list()

            # Filtrar por age_category y contar
            count = 0
            for model in models:
                animal_entity = self._to_entity(model)
                animal_age_category = animal_entity.calculate_age_category()
                if animal_age_category.value == age_category_filter:
                    count += 1
            return count

        # Contar directamente en BD
        if not beanie_filters:
            count = await AnimalModel.find_all().count()
        else:
            count = await AnimalModel.find(beanie_filters).count()
        return count

    async def count(self) -> int:
        """
        Retorna el conteo total de animales.

        Returns:
            Número total de animales
        """
        return await AnimalModel.count()

    async def find_by_mother_id(self, mother_id: str) -> Animal | None:
        """
        Busca la madre de un animal por ID de madre.

        Args:
            mother_id: ID de la madre

        Returns:
            Animal madre si existe, None si no existe
        """
        try:
            mother_uuid = UUID(mother_id)
            model = await AnimalModel.get(mother_uuid)
            if model is None:
                return None
            return self._to_entity(model)
        except (ValueError, TypeError):
            return None

    async def find_by_father_id(self, father_id: str) -> Animal | None:
        """
        Busca el padre de un animal por ID de padre.

        Args:
            father_id: ID del padre

        Returns:
            Animal padre si existe, None si no existe
        """
        try:
            father_uuid = UUID(father_id)
            model = await AnimalModel.get(father_uuid)
            if model is None:
                return None
            return self._to_entity(model)
        except (ValueError, TypeError):
            return None

    async def find_descendants(
        self, parent_id: UUID, parent_role: str = "mother"
    ) -> list[Animal]:
        """
        Busca los descendientes (hijos) de un animal.

        Args:
            parent_id: ID del animal padre/madre
            parent_role: "mother" o "father" para buscar por mother_id o father_id

        Returns:
            Lista de Animal que son hijos del animal especificado
        """
        parent_id_str = str(parent_id)
        if parent_role == "mother":
            models = await AnimalModel.find(
                AnimalModel.mother_id == parent_id_str
            ).to_list()
        elif parent_role == "father":
            models = await AnimalModel.find(
                AnimalModel.father_id == parent_id_str
            ).to_list()
        else:
            # Buscar por ambos
            mother_models = await AnimalModel.find(
                AnimalModel.mother_id == parent_id_str
            ).to_list()
            father_models = await AnimalModel.find(
                AnimalModel.father_id == parent_id_str
            ).to_list()
            # Combinar y eliminar duplicados
            all_models = {model.id: model for model in mother_models + father_models}
            models = list(all_models.values())

        return [self._to_entity(model) for model in models]
