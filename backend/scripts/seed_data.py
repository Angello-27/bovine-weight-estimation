"""
Seed Data Script - Cargar datos iniciales en MongoDB

Ejecutar: python -m scripts.seed_data

Carga datos de ejemplo para desarrollo y testing con TRAZABILIDAD COMPLETA:
- Roles iniciales (Administrador, Usuario, Invitado)
- Usuario principal: Bruno Brito Macedo
- Finca: Hacienda Gamelera
- 200 animales de las 7 razas tropicales
- Evolución temporal de peso (múltiples pesajes por animal)
- Relaciones familiares (madre/padre)
- Estados variados (active/sold/deceased)
- Datos controlados para demostración de trazabilidad
"""

import asyncio
import random
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from typing import cast
from uuid import UUID

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.constants import AgeCategory, BreedType
from app.models import (
    AlertModel,
    AnimalModel,
    FarmModel,
    RoleModel,
    UserModel,
    WeightEstimationModel,
)
from app.models.alert_model import AlertStatus, AlertType, RecurrenceType
from app.services import AuthService

# IDs fijos para datos de seed (para reproducibilidad)
ADMIN_ROLE_ID = UUID("110e8400-e29b-41d4-a716-446655440000")
USER_ROLE_ID = UUID("220e8400-e29b-41d4-a716-446655440000")
GUEST_ROLE_ID = UUID("330e8400-e29b-41d4-a716-446655440000")
BRUNO_USER_ID = UUID("440e8400-e29b-41d4-a716-446655440000")
FARM_ID = UUID("550e8400-e29b-41d4-a716-446655440000")

# Referencias a imágenes en Drive (el usuario las descargará manualmente)
IMAGE_REFERENCES = {
    "nelore": "https://drive.google.com/file/d/NELORE_IMAGE_ID/view",
    "brahman": "https://drive.google.com/file/d/BRAHMAN_IMAGE_ID/view",
    "guzerat": "https://drive.google.com/file/d/GUZERAT_IMAGE_ID/view",
    "senepol": "https://drive.google.com/file/d/SENEPOL_IMAGE_ID/view",
    "girolando": "https://drive.google.com/file/d/GIROLANDO_IMAGE_ID/view",
    "gyr_lechero": "https://drive.google.com/file/d/GYR_LECHERO_IMAGE_ID/view",
    "sindi": "https://drive.google.com/file/d/SINDI_IMAGE_ID/view",
}

# Distribución realista de razas (basada en Hacienda Gamelera)
# Nelore: 42%, Brahman: 25%, Guzerat: 15%, Senepol: 8%, Girolando: 5%, Gyr Lechero: 3%, Sindi: 2%
BREED_DISTRIBUTION = {
    BreedType.NELORE: 84,  # 42% de 200
    BreedType.BRAHMAN: 50,  # 25% de 200
    BreedType.GUZERAT: 30,  # 15% de 200
    BreedType.SENEPOL: 16,  # 8% de 200
    BreedType.GIROLANDO: 10,  # 5% de 200
    BreedType.GYR_LECHERO: 6,  # 3% de 200
    BreedType.SINDI: 4,  # 2% de 200
}

# Rangos de peso por raza y edad (en kg)
# Formato: {raza: {categoría_edad: (min, max)}}
BREED_WEIGHT_RANGES = {
    BreedType.NELORE: {
        AgeCategory.TERNEROS: (80, 180),
        AgeCategory.VAQUILLONAS_TORILLOS: (200, 350),
        AgeCategory.VAQUILLONAS_TORETES: (350, 480),
        AgeCategory.VACAS_TOROS: (400, 550),
    },
    BreedType.BRAHMAN: {
        AgeCategory.TERNEROS: (90, 200),
        AgeCategory.VAQUILLONAS_TORILLOS: (220, 380),
        AgeCategory.VAQUILLONAS_TORETES: (380, 520),
        AgeCategory.VACAS_TOROS: (450, 600),
    },
    BreedType.GUZERAT: {
        AgeCategory.TERNEROS: (85, 190),
        AgeCategory.VAQUILLONAS_TORILLOS: (210, 360),
        AgeCategory.VAQUILLONAS_TORETES: (360, 500),
        AgeCategory.VACAS_TOROS: (420, 580),
    },
    BreedType.SENEPOL: {
        AgeCategory.TERNEROS: (95, 210),
        AgeCategory.VAQUILLONAS_TORILLOS: (230, 400),
        AgeCategory.VAQUILLONAS_TORETES: (400, 550),
        AgeCategory.VACAS_TOROS: (480, 650),
    },
    BreedType.GIROLANDO: {
        AgeCategory.TERNEROS: (90, 200),
        AgeCategory.VAQUILLONAS_TORILLOS: (220, 380),
        AgeCategory.VAQUILLONAS_TORETES: (380, 520),
        AgeCategory.VACAS_TOROS: (450, 600),
    },
    BreedType.GYR_LECHERO: {
        AgeCategory.TERNEROS: (80, 180),
        AgeCategory.VAQUILLONAS_TORILLOS: (200, 350),
        AgeCategory.VAQUILLONAS_TORETES: (350, 480),
        AgeCategory.VACAS_TOROS: (400, 550),
    },
    BreedType.SINDI: {
        AgeCategory.TERNEROS: (70, 160),
        AgeCategory.VAQUILLONAS_TORILLOS: (180, 320),
        AgeCategory.VAQUILLONAS_TORETES: (320, 450),
        AgeCategory.VACAS_TOROS: (350, 500),
    },
}

# Pesos al nacer por raza (en kg)
BIRTH_WEIGHTS = {
    BreedType.NELORE: (25, 35),
    BreedType.BRAHMAN: (28, 38),
    BreedType.GUZERAT: (27, 36),
    BreedType.SENEPOL: (30, 40),
    BreedType.GIROLANDO: (32, 42),
    BreedType.GYR_LECHERO: (28, 37),
    BreedType.SINDI: (24, 32),
}

# Colores típicos por raza
BREED_COLORS = {
    BreedType.NELORE: ["Blanco", "Gris claro", "Blanco con manchas"],
    BreedType.BRAHMAN: ["Gris", "Gris oscuro", "Blanco grisáceo"],
    BreedType.GUZERAT: ["Gris", "Gris claro", "Blanco"],
    BreedType.SENEPOL: ["Rojo", "Rojo oscuro", "Marrón rojizo"],
    BreedType.GIROLANDO: ["Blanco y negro", "Negro", "Blanco"],
    BreedType.GYR_LECHERO: ["Amarillo", "Amarillo claro", "Dorado"],
    BreedType.SINDI: ["Rojo", "Marrón", "Rojo oscuro"],
}


async def create_roles() -> dict[str, RoleModel]:
    """
    Crea roles iniciales del sistema.

    Returns:
        Dict con roles creados: {"admin": RoleModel, "user": RoleModel, "guest": RoleModel}
    """
    roles = {}

    # Rol Administrador
    admin_role = RoleModel(
        id=ADMIN_ROLE_ID,
        name="Administrador",
        description="Rol con acceso completo al sistema",
        priority="Administrador",
        permissions=["read", "write", "delete", "admin"],
    )
    await admin_role.insert()
    roles["admin"] = admin_role
    print(f"   ✅ Rol creado: {admin_role.name}")

    # Rol Usuario
    user_role = RoleModel(
        id=USER_ROLE_ID,
        name="Usuario",
        description="Rol estándar para usuarios del sistema",
        priority="Usuario",
        permissions=["read", "write"],
    )
    await user_role.insert()
    roles["user"] = user_role
    print(f"   ✅ Rol creado: {user_role.name}")

    # Rol Invitado
    guest_role = RoleModel(
        id=GUEST_ROLE_ID,
        name="Invitado",
        description="Rol con acceso limitado de solo lectura",
        priority="Invitado",
        permissions=["read"],
    )
    await guest_role.insert()
    roles["guest"] = guest_role
    print(f"   ✅ Rol creado: {guest_role.name}")

    return roles


async def create_users(admin_role: RoleModel) -> UserModel:
    """
    Crea usuarios iniciales del sistema.

    Args:
        admin_role: Rol de administrador

    Returns:
        UserModel de Bruno Brito Macedo
    """
    auth_service = AuthService()

    # Usuario principal: Bruno Brito Macedo
    bruno = UserModel(
        id=BRUNO_USER_ID,
        username="bruno_brito",
        email="bruno@haciendagamelera.com",
        hashed_password=auth_service.get_password_hash(
            "password123"
        ),  # Cambiar en producción
        role_id=admin_role.id,
        farm_id=None,  # Se asignará después de crear la finca
        is_active=True,
        is_superuser=True,
    )
    await bruno.insert()
    print(f"   ✅ Usuario creado: {bruno.username} ({bruno.email})")

    # Usuario de ejemplo (no superusuario)
    example_user = UserModel(
        username="usuario_ejemplo",
        email="usuario@haciendagamelera.com",
        hashed_password=auth_service.get_password_hash("password123"),
        role_id=admin_role.id,  # Usar admin_role por ahora
        farm_id=None,
        is_active=True,
        is_superuser=False,
    )
    await example_user.insert()
    print(f"   ✅ Usuario creado: {example_user.username}")

    return bruno


async def create_farm(owner: UserModel) -> FarmModel:
    """
    Crea la finca Hacienda Gamelera.

    Args:
        owner: Usuario propietario (Bruno)

    Returns:
        FarmModel de Hacienda Gamelera
    """
    farm = FarmModel(
        id=FARM_ID,
        name=settings.HACIENDA_NAME,
        owner_id=owner.id,
        location={
            "type": "Point",
            "coordinates": [
                -60.797889,
                -15.859500,
            ],  # [lon, lat] San Ignacio de Velasco
        },
        capacity=settings.HACIENDA_CAPACITY,
        total_animals=0,  # Se actualizará después de insertar animales
    )
    await farm.insert()
    print(f"   ✅ Finca creada: {farm.name}")
    print(f"      📍 Ubicación: {settings.HACIENDA_LOCATION}")
    print(f"      👤 Propietario: {settings.HACIENDA_OWNER}")
    print(f"      📊 Capacidad: {farm.capacity} animales")

    # Actualizar usuario con farm_id
    owner.farm_id = cast(UUID, farm.id)  # type: ignore[assignment]
    await owner.save()
    print(f"   ✅ Usuario {owner.username} asociado a finca {farm.name}")

    return farm


def generate_animals(farm_id: UUID) -> list[AnimalModel]:
    """
    Genera 200 animales con trazabilidad completa.

    Incluye:
    - Distribución realista de razas
    - Fechas de nacimiento variadas (2018-2024)
    - Relaciones familiares (madre/padre)
    - Estados variados
    """
    animals = []
    ear_tag_counter = 1
    now = datetime.utcnow()

    # Generar animales base (padres/madres) primero para relaciones familiares
    base_animals = []
    base_counter = 1

    # Crear 30 animales base (padres/madres) nacidos entre 2018-2020
    for base_idx in range(30):
        breed = random.choice(list(BreedType))
        birth_date = datetime(2018, 1, 1) + timedelta(
            days=random.randint(0, 730)  # 2018-2020
        )
        gender = "female" if base_idx % 2 == 0 else "male"

        animal = AnimalModel(
            ear_tag=f"HG-{breed.value.upper()[:3]}-{base_counter:03d}",
            breed=breed.value,
            birth_date=birth_date,
            gender=gender,
            name=f"{'Vaca' if gender == 'female' else 'Toro'} Base {base_counter}",
            color=random.choice(BREED_COLORS[breed]),
            birth_weight_kg=round(random.uniform(*BIRTH_WEIGHTS[breed]), 1),
            status="active",
            farm_id=farm_id,
            registration_date=birth_date + timedelta(days=random.randint(1, 30)),
            last_updated=now - timedelta(days=random.randint(0, 30)),
            photo_url=IMAGE_REFERENCES.get(breed.value),
            observations=f"Animal base para reproducción. Raza {BreedType.get_display_name(BreedType(breed))}.",
        )
        base_animals.append(animal)
        base_counter += 1

    animals.extend(base_animals)

    # Generar animales según distribución de razas
    for breed, count in BREED_DISTRIBUTION.items():
        for _ in range(count):
            # Fecha de nacimiento variada (2020-2024)
            # Distribución: más animales jóvenes (2023-2024) que adultos
            year = random.choices(
                [2020, 2021, 2022, 2023, 2024],
                weights=[10, 15, 20, 30, 25],  # Más probabilidad en años recientes
            )[0]
            birth_date = datetime(year, 1, 1) + timedelta(days=random.randint(0, 364))

            gender = "female" if random.random() < 0.55 else "male"  # 55% hembras

            # Asignar madre/padre de animales base (si es posible)
            mother_id = None
            father_id = None
            if random.random() < 0.7:  # 70% tienen padre/madre registrados
                mothers = [a for a in base_animals if a.gender == "female"]
                fathers = [a for a in base_animals if a.gender == "male"]
                if mothers and random.random() < 0.8:
                    mother_id = str(random.choice(mothers).id)
                if fathers and random.random() < 0.6:
                    father_id = str(random.choice(fathers).id)

            # Estado: 85% active, 10% sold, 5% deceased
            status_weights = [0.85, 0.10, 0.05]
            status = random.choices(
                ["active", "sold", "deceased"], weights=status_weights
            )[0]

            # Si está muerto, debe haber muerto después de nacer
            if status == "deceased":
                death_date = birth_date + timedelta(
                    days=random.randint(30, (now - birth_date).days)
                )
                last_updated = death_date
            elif status == "sold":
                sold_date = birth_date + timedelta(
                    days=random.randint(180, (now - birth_date).days)
                )
                last_updated = sold_date
            else:
                last_updated = now - timedelta(days=random.randint(0, 30))

            animal = AnimalModel(
                ear_tag=f"HG-{breed.value.upper()[:3]}-{ear_tag_counter:03d}",
                breed=breed.value,
                birth_date=birth_date,
                gender=gender,
                name=f"{BreedType.get_display_name(BreedType(breed))} {ear_tag_counter}",
                color=random.choice(BREED_COLORS[breed]),
                birth_weight_kg=round(random.uniform(*BIRTH_WEIGHTS[breed]), 1),
                mother_id=mother_id,
                father_id=father_id,
                status=status,
                farm_id=farm_id,
                registration_date=birth_date + timedelta(days=random.randint(1, 30)),
                last_updated=last_updated,
                photo_url=IMAGE_REFERENCES.get(breed.value),
                observations=f"Animal de raza {BreedType.get_display_name(BreedType(breed))}. "
                f"Registrado para trazabilidad completa.",
            )
            animals.append(animal)
            ear_tag_counter += 1

    return animals


def calculate_weight_for_age(
    breed: BreedType,
    age_months: int,
    birth_weight: float,
    base_date: datetime,
) -> float:
    """
    Calcula peso esperado para un animal según su edad y raza.

    Simula crecimiento realista con curvas de crecimiento.
    """
    age_category = AgeCategory.from_age_months(age_months)
    min_weight, max_weight = BREED_WEIGHT_RANGES[breed][age_category]

    # Curva de crecimiento: más rápido al inicio, se estabiliza
    if age_months < 12:
        # Crecimiento rápido (0-12 meses)
        growth_factor = min(age_months / 12.0, 1.0)
    elif age_months < 24:
        # Crecimiento moderado (12-24 meses)
        growth_factor = 1.0 + ((age_months - 12) / 12.0) * 0.3
    else:
        # Crecimiento lento (24+ meses)
        growth_factor = 1.3 + min((age_months - 24) / 12.0, 1.0) * 0.2

    # Peso base + crecimiento
    target_weight = birth_weight + (max_weight - birth_weight) * min(growth_factor, 1.5)

    # Variación aleatoria ±10%
    variation = random.uniform(0.90, 1.10)
    weight = target_weight * variation

    # Asegurar que esté en rango
    weight = max(min_weight * 0.9, min(max_weight * 1.1, weight))

    return round(weight, 1)


def generate_weight_estimations(
    animals: list[AnimalModel],
) -> list[WeightEstimationModel]:
    """
    Genera estimaciones de peso con evolución temporal.

    Crea múltiples pesajes por animal que muestren crecimiento a lo largo del tiempo.
    """
    estimations = []
    now = datetime.utcnow()

    for animal in animals:
        if animal.status == "deceased":
            # Animal muerto: pesajes hasta fecha de muerte
            end_date = animal.last_updated
        elif animal.status == "sold":
            # Animal vendido: pesajes hasta fecha de venta
            end_date = animal.last_updated
        else:
            # Animal activo: pesajes hasta hoy
            end_date = now

        age_at_end = (end_date.year - animal.birth_date.year) * 12 + (
            end_date.month - animal.birth_date.month
        )

        if age_at_end < 1:
            # Animal muy joven: solo 1-2 pesajes
            num_weighings = random.randint(1, 2)
        elif age_at_end < 12:
            # Animal joven: 3-5 pesajes
            num_weighings = random.randint(3, 5)
        elif age_at_end < 24:
            # Animal en crecimiento: 6-10 pesajes
            num_weighings = random.randint(6, 10)
        else:
            # Animal adulto: 10-15 pesajes (historial completo)
            num_weighings = random.randint(10, 15)

        breed = BreedType(animal.breed)
        birth_weight = animal.birth_weight_kg or random.uniform(*BIRTH_WEIGHTS[breed])

        # Generar pesajes distribuidos a lo largo de la vida del animal
        weighing_dates = []
        start_date = animal.birth_date + timedelta(days=random.randint(30, 90))

        if (end_date - start_date).days < 30:
            # Si el período es muy corto, solo un pesaje
            weighing_dates = [
                start_date
                + timedelta(days=random.randint(0, (end_date - start_date).days))
            ]
        else:
            # Distribuir pesajes uniformemente
            days_span = (end_date - start_date).days
            interval = days_span / max(num_weighings, 1)
            for i in range(num_weighings):
                date = start_date + timedelta(
                    days=int(i * interval) + random.randint(-7, 7)
                )
                if date <= end_date:
                    weighing_dates.append(date)

        # Ordenar fechas
        weighing_dates.sort()

        for i, weighing_date in enumerate(weighing_dates):
            # Calcular edad en meses al momento del pesaje
            age_months = (weighing_date.year - animal.birth_date.year) * 12 + (
                weighing_date.month - animal.birth_date.month
            )

            # Calcular peso esperado para esa edad
            weight = calculate_weight_for_age(
                breed, age_months, birth_weight, weighing_date
            )

            # Confidence: más alto para animales adultos, más variable para jóvenes
            if age_months < 6:
                confidence = random.uniform(0.85, 0.92)
            elif age_months < 12:
                confidence = random.uniform(0.88, 0.95)
            else:
                confidence = random.uniform(0.92, 0.98)

            # Processing time: más rápido para animales grandes
            if weight > 400:
                processing_time = random.randint(1200, 2000)
            else:
                processing_time = random.randint(1500, 2500)

            estimation = WeightEstimationModel(
                animal_id=str(animal.id),
                breed=animal.breed,
                estimated_weight_kg=weight,
                confidence=round(confidence, 2),
                method="tflite",
                model_version="1.0.0",
                processing_time_ms=processing_time,
                frame_image_path=f"/frames/{animal.ear_tag}_weighing_{i+1:03d}.jpg",
                latitude=-15.859500,  # San Ignacio de Velasco
                longitude=-60.797889,
                timestamp=weighing_date,
                created_at=weighing_date,
            )
            estimations.append(estimation)

    return estimations


def generate_sample_alerts(
    user_id: UUID, farm_id: UUID, animals: list[AnimalModel]
) -> list[AlertModel]:
    """
    Genera alertas de ejemplo con cronograma para hatos.

    Incluye alertas programadas filtradas por:
    - Raza/especie
    - Categoría de edad
    - Género
    - Cantidad de animales
    """
    alerts = []
    now = datetime.utcnow()

    # Contar animales por criterios
    breed_counts = Counter(animal.breed for animal in animals)

    # Alerta 1: Pesaje masivo de Nelore (raza más común)
    nelore_count = breed_counts.get("nelore", 0)
    if nelore_count > 0:
        alerts.append(
            AlertModel(
                user_id=user_id,
                farm_id=farm_id,
                type=AlertType.SCHEDULED_WEIGHING,
                title="Pesaje Masivo - Nelore",
                message=f"Pesar {min(nelore_count, 50)} animales Nelore del potrero principal",
                status=AlertStatus.PENDING,
                scheduled_at=now + timedelta(days=7),  # Próxima semana
                recurrence=RecurrenceType.MONTHLY,
                reminder_before_days=[7, 1],
                filter_criteria={
                    "breed": "nelore",
                    "count": min(nelore_count, 50),
                },
                location={
                    "type": "Point",
                    "coordinates": [-60.797889, -15.859500],
                },
            )
        )

    # Alerta 2: Tratamiento veterinario para terneros
    terneros = [
        a for a in animals if a.calculate_age_category() == AgeCategory.TERNEROS
    ]
    terneros_count = len(terneros)
    if terneros_count > 0:
        alerts.append(
            AlertModel(
                user_id=user_id,
                farm_id=farm_id,
                type=AlertType.VETERINARY_TREATMENT,
                title="Vacunación - Terneros",
                message=f"Vacunar {terneros_count} terneros (<8 meses) - Programa sanitario",
                status=AlertStatus.PENDING,
                scheduled_at=now + timedelta(days=14),  # En 2 semanas
                recurrence=RecurrenceType.QUARTERLY,
                reminder_before_days=[7, 3, 1],
                filter_criteria={
                    "age_category": "terneros",
                    "count": terneros_count,
                },
            )
        )

    # Alerta 3: Pesaje de vaquillonas hembras
    vaquillonas = [
        a
        for a in animals
        if a.gender == "female"
        and a.calculate_age_category() == AgeCategory.VAQUILLONAS_TORILLOS
    ]
    vaquillonas_count = len(vaquillonas)
    if vaquillonas_count > 0:
        alerts.append(
            AlertModel(
                user_id=user_id,
                farm_id=farm_id,
                type=AlertType.SCHEDULED_WEIGHING,
                title="Control de Peso - Vaquillonas",
                message=f"Pesar {vaquillonas_count} vaquillonas (6-18 meses) para control de desarrollo",
                status=AlertStatus.PENDING,
                scheduled_at=now + timedelta(days=10),
                recurrence=RecurrenceType.MONTHLY,
                reminder_before_days=[7, 1],
                filter_criteria={
                    "age_category": "vaquillonas_torillos",
                    "gender": "female",
                    "count": vaquillonas_count,
                },
            )
        )

    # Alerta 4: Pesaje de Brahman machos
    brahman_males = [a for a in animals if a.breed == "brahman" and a.gender == "male"]
    brahman_males_count = len(brahman_males)
    if brahman_males_count > 0:
        alerts.append(
            AlertModel(
                user_id=user_id,
                farm_id=farm_id,
                type=AlertType.SCHEDULED_WEIGHING,
                title="Pesaje - Toros Brahman",
                message=f"Pesar {brahman_males_count} toros Brahman para evaluación reproductiva",
                status=AlertStatus.PENDING,
                scheduled_at=now + timedelta(days=5),
                recurrence=RecurrenceType.MONTHLY,
                reminder_before_days=[3, 1],
                filter_criteria={
                    "breed": "brahman",
                    "gender": "male",
                    "count": brahman_males_count,
                },
            )
        )

    # Alerta 5: Evento calendario - Competencia ASOCEBU
    alerts.append(
        AlertModel(
            user_id=user_id,
            farm_id=farm_id,
            type=AlertType.CALENDAR_EVENT,
            title="Competencia ASOCEBU - Exposición Ganadera",
            message="Preparar animales Nelore y Brahman para exposición",
            status=AlertStatus.PENDING,
            scheduled_at=now + timedelta(days=30),
            recurrence=RecurrenceType.YEARLY,
            reminder_before_days=[30, 14, 7, 1],
            filter_criteria={
                "breed": ["nelore", "brahman"],
                "count": 10,
            },
        )
    )

    return alerts


async def seed_database():
    """Función principal para cargar datos iniciales con trazabilidad completa."""
    print("🌱 Iniciando carga de datos iniciales con TRAZABILIDAD COMPLETA...")
    print(f"📊 Base de datos: {settings.MONGODB_DB_NAME}")
    print(f"🔗 MongoDB URL: {settings.MONGODB_URL}\n")

    # Conectar a MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)

    try:
        # Inicializar Beanie
        await init_beanie(
            database=client[settings.MONGODB_DB_NAME],
            document_models=[
                AlertModel,
                AnimalModel,
                FarmModel,
                RoleModel,
                UserModel,
                WeightEstimationModel,
            ],
        )
        print("✅ Conectado a MongoDB\n")

        # Limpiar datos existentes
        print("🗑️  Limpiando datos existentes...")
        await AlertModel.delete_all()
        await AnimalModel.delete_all()
        await WeightEstimationModel.delete_all()
        await FarmModel.delete_all()
        await UserModel.delete_all()
        await RoleModel.delete_all()
        print("✅ Datos limpiados\n")

        # Crear roles
        print("👥 Creando roles iniciales...")
        roles = await create_roles()
        print(f"✅ {len(roles)} roles creados\n")

        # Crear usuarios
        print("👤 Creando usuarios iniciales...")
        bruno = await create_users(roles["admin"])
        print("✅ Usuarios creados\n")

        # Crear finca
        print("🏢 Creando finca Hacienda Gamelera...")
        farm = await create_farm(bruno)
        farm_id = farm.id
        print("✅ Finca creada\n")

        # Generar animales
        print("🐄 Generando 200 animales con trazabilidad completa...")
        animals = generate_animals(farm_id)
        print(f"   📝 {len(animals)} animales generados")

        # Insertar animales
        await AnimalModel.insert_many(animals)
        print(f"✅ {len(animals)} animales insertados en MongoDB\n")

        # Actualizar contador de animales en la finca
        farm.total_animals = len(animals)
        await farm.save()
        print(f"✅ Contador de animales actualizado en finca: {farm.total_animals}\n")

        # Generar estimaciones de peso con evolución temporal
        print("⚖️  Generando estimaciones de peso con evolución temporal...")
        estimations = generate_weight_estimations(animals)
        print(f"   📝 {len(estimations)} estimaciones generadas")

        # Insertar estimaciones
        await WeightEstimationModel.insert_many(estimations)
        print(f"✅ {len(estimations)} estimaciones insertadas en MongoDB\n")

        # Generar alertas de ejemplo con cronograma
        print("🔔 Generando alertas de ejemplo con cronograma...")
        alerts = generate_sample_alerts(bruno.id, farm_id, animals)
        print(f"   📝 {len(alerts)} alertas generadas")

        # Insertar alertas
        if alerts:
            await AlertModel.insert_many(alerts)
            print(f"✅ {len(alerts)} alertas insertadas en MongoDB\n")

        # Resumen detallado
        print("=" * 70)
        print("📊 RESUMEN DE DATOS CARGADOS - TRAZABILIDAD COMPLETA")
        print("=" * 70)
        print(f"👥 Roles creados: {len(roles)}")
        print("👤 Usuarios creados: 2 (Bruno + Ejemplo)")
        print(f"🏢 Finca: {farm.name}")
        print(f"🐄 Animales totales: {len(animals)}")
        print(f"⚖️  Estimaciones totales: {len(estimations)}")
        print(
            f"📈 Promedio de pesajes por animal: {len(estimations) / len(animals):.1f}"
        )
        alerts_count = len(alerts) if "alerts" in locals() else 0
        if alerts_count > 0:
            print(f"🔔 Alertas programadas: {alerts_count}")
        print(f"🏢 Hacienda ID: {farm_id}\n")

        # Distribución por raza
        print("📋 Distribución por raza:")
        breed_counts = Counter(animal.breed for animal in animals)
        for breed, count in sorted(breed_counts.items()):
            percentage = (count / len(animals)) * 100
            print(
                f"   - {BreedType.get_display_name(BreedType(breed))}: "
                f"{count} animales ({percentage:.1f}%)"
            )

        # Distribución por estado
        print("\n📊 Distribución por estado:")
        status_counts = Counter(animal.status for animal in animals)
        for status, count in sorted(status_counts.items()):
            percentage = (count / len(animals)) * 100
            print(f"   - {status.capitalize()}: {count} animales ({percentage:.1f}%)")

        # Distribución por categoría de edad
        print("\n👶 Distribución por categoría de edad:")
        age_categories = Counter(
            animal.calculate_age_category().value for animal in animals
        )
        for category, count in sorted(age_categories.items()):
            percentage = (count / len(animals)) * 100
            print(f"   - {category}: {count} animales ({percentage:.1f}%)")

        # Animales con relaciones familiares
        animals_with_parents = sum(1 for a in animals if a.mother_id or a.father_id)
        print(
            f"\n👨‍👩‍👧 Animales con padre/madre registrados: "
            f"{animals_with_parents} ({(animals_with_parents/len(animals)*100):.1f}%)"
        )

        # Rango de fechas de nacimiento
        birth_dates = [a.birth_date for a in animals]
        min_birth = min(birth_dates)
        max_birth = max(birth_dates)
        print(
            f"\n📅 Rango de fechas de nacimiento: "
            f"{min_birth.strftime('%Y-%m-%d')} a {max_birth.strftime('%Y-%m-%d')}"
        )

        # Rango de fechas de pesajes
        weighing_dates = [e.timestamp for e in estimations]
        min_weighing = min(weighing_dates)
        max_weighing = max(weighing_dates)
        print(
            f"📅 Rango de fechas de pesajes: "
            f"{min_weighing.strftime('%Y-%m-%d')} a {max_weighing.strftime('%Y-%m-%d')}"
        )

        print("\n" + "=" * 70)
        print("✅ Seed data completado exitosamente!")
        print("\n🔐 CREDENCIALES DE ACCESO:")
        print("   Usuario: bruno_brito")
        print("   Email: bruno@haciendagamelera.com")
        print("   Contraseña: password123")
        print("   ⚠️  CAMBIAR EN PRODUCCIÓN")
        print("\n📸 NOTA: Las referencias a imágenes están en IMAGE_REFERENCES")
        print("   Descarga las imágenes de Drive y actualiza los IDs en el script.")
        print("\n🔍 TRAZABILIDAD:")
        print("   - Roles y usuarios configurados")
        print("   - Finca Hacienda Gamelera creada")
        print("   - Cada animal tiene historial completo de pesajes")
        print("   - Relaciones familiares (madre/padre) registradas")
        print("   - Estados variados (active/sold/deceased)")
        print("   - Evolución temporal de peso documentada")
        print("=" * 70)

    except Exception as e:
        print(f"❌ Error durante seed data: {e}")
        import traceback

        traceback.print_exc()
        raise
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
