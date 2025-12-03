"""
Seed Data Script - Cargar datos iniciales en MongoDB con datos REALISTAS

Ejecutar: python -m scripts.seed_data

Mejoras implementadas:
- Datos de peso basados en CSV real (metadata_estimada.csv)
- Usuarios del equipo Hacienda Gamelera
- Nombres realistas para el ganado por raza
- Relaciones padre/madre validadas por edad, género y raza
- Confianza entre 80-96%
- Evolución temporal de 1 año con pesajes realistas
"""

import asyncio
import csv
import logging
import random
import warnings
from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import cast
from uuid import UUID

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.utils.password import get_password_hash
from app.data.models import (
    AlertModel,
    AnimalModel,
    FarmModel,
    RoleModel,
    UserModel,
    WeightEstimationModel,
)
from app.data.models.alert_model import (
    AlertStatus,
    AlertType,
    RecurrenceType,
)
from app.domain.shared.constants import AgeCategory, BreedType

# Cache de imágenes disponibles por raza
IMAGE_CACHE: dict[str, dict[str, list[str]]] = {}


def load_available_images(uploads_dir: Path) -> dict[str, dict[str, list[str]]]:
    """
    Carga las imágenes disponibles organizadas por raza y tipo (normal/cria).

    Returns:
        Dict con estructura: {breed: {"normal": [...], "cria": [...]}}
    """
    images_by_breed: dict[str, dict[str, list[str]]] = {}

    for breed in BreedType:
        breed_name = breed.value.lower()
        breed_dir = uploads_dir / breed_name

        if not breed_dir.exists():
            print(
                f"   ⚠️  Advertencia: No se encontró directorio para raza {breed_name}"
            )
            images_by_breed[breed_name] = {"normal": [], "cria": []}
            continue

        # Buscar imágenes normales y de crías
        normal_images = []
        cria_images = []

        for img_file in breed_dir.iterdir():
            if not img_file.is_file():
                continue

            filename = img_file.name.lower()
            # Verificar que sea una imagen
            if not filename.endswith((".jpg", ".jpeg", ".png")):
                continue

            # Path relativo desde backend/uploads
            relative_path = f"{breed_name}/{img_file.name}"

            if f"{breed_name}_cria_" in filename:
                cria_images.append(relative_path)
            else:
                # Imágenes normales (formato: {breed}_{numero}.jpg)
                if filename.startswith(f"{breed_name}_") and not filename.startswith(
                    f"{breed_name}_cria_"
                ):
                    normal_images.append(relative_path)

        images_by_breed[breed_name] = {
            "normal": sorted(normal_images),
            "cria": sorted(cria_images),
        }

        print(
            f"   📸 {breed_name}: {len(normal_images)} normales, {len(cria_images)} crías"
        )

    return images_by_breed


def get_animal_photo_url(
    breed: BreedType, age_months: int, images_by_breed: dict[str, dict[str, list[str]]]
) -> str | None:
    """
    Obtiene una URL de foto apropiada para un animal según su edad.

    Args:
        breed: Raza del animal
        age_months: Edad en meses
        images_by_breed: Diccionario de imágenes disponibles

    Returns:
        Path relativo de la imagen o None si no hay disponibles
    """
    breed_name = breed.value.lower()
    breed_images = images_by_breed.get(breed_name, {"normal": [], "cria": []})

    # Si es menor a 8 meses, usar imagen de cría
    if age_months < 8:
        cria_images = breed_images.get("cria", [])
        if cria_images:
            return random.choice(cria_images)
        # Si no hay crías, usar normal
        normal_images = breed_images.get("normal", [])
        if normal_images:
            return random.choice(normal_images)
    else:
        # Animal adulto, usar imagen normal
        normal_images = breed_images.get("normal", [])
        if normal_images:
            return random.choice(normal_images)
        # Si no hay normales, usar cría como fallback
        cria_images = breed_images.get("cria", [])
        if cria_images:
            return random.choice(cria_images)

    return None


def get_estimation_frame_path(
    breed: BreedType, images_by_breed: dict[str, dict[str, list[str]]]
) -> str:
    """
    Obtiene un path de imagen para una estimación de peso.

    Args:
        breed: Raza del animal
        images_by_breed: Diccionario de imágenes disponibles

    Returns:
        Path relativo de la imagen
    """
    breed_name = breed.value.lower()
    breed_images = images_by_breed.get(breed_name, {"normal": [], "cria": []})

    # Preferir imágenes normales para estimaciones
    normal_images = breed_images.get("normal", [])
    if normal_images:
        return random.choice(normal_images)

    # Fallback a crías si no hay normales
    cria_images = breed_images.get("cria", [])
    if cria_images:
        return random.choice(cria_images)

    # Fallback final si no hay imágenes
    return f"{breed_name}/placeholder.jpg"


# Suprimir warnings de bcrypt/passlib (son informativos, no afectan funcionalidad)
warnings.filterwarnings("ignore", message=".*bcrypt.*")
warnings.filterwarnings("ignore", message=".*trapped.*")
logging.getLogger("passlib").setLevel(logging.ERROR)

# IDs fijos
ADMIN_ROLE_ID = UUID("110e8400-e29b-41d4-a716-446655440000")
USER_ROLE_ID = UUID("220e8400-e29b-41d4-a716-446655440000")
GUEST_ROLE_ID = UUID("330e8400-e29b-41d4-a716-446655440000")
BRUNO_USER_ID = UUID("440e8400-e29b-41d4-a716-446655440000")
MIGUEL_USER_ID = UUID("550e8400-e29b-41d4-a716-446655440001")
RODRIGO_USER_ID = UUID("660e8400-e29b-41d4-a716-446655440002")
FARM_ID = UUID("770e8400-e29b-41d4-a716-446655440000")

# Nombres realistas por raza
CATTLE_NAMES = {
    BreedType.NELORE: {
        "male": [
            "Brahma",
            "Zeus",
            "Thor",
            "Apolo",
            "Titan",
            "Hércules",
            "Atlas",
            "Cronos",
            "Ares",
            "Poseidón",
            "Emperador",
            "Capitán",
            "Guerrero",
            "Duque",
            "Rey",
            "León",
            "Trueno",
            "Rayo",
            "Volcán",
            "Coloso",
        ],
        "female": [
            "Reina",
            "Princesa",
            "Diva",
            "Luna",
            "Estrella",
            "Aurora",
            "Perla",
            "Diamante",
            "Jade",
            "Ámbar",
            "Bella",
            "Linda",
            "Graciosa",
            "Emperatriz",
            "Majestad",
            "Venus",
            "Afrodita",
            "Hera",
            "Atenea",
            "Diana",
        ],
    },
    BreedType.BRAHMAN: {
        "male": [
            "Rajá",
            "Sultán",
            "Pachá",
            "Maharajá",
            "Visir",
            "Brahmán",
            "Krishna",
            "Shiva",
            "Indra",
            "Ganesh",
            "Tigre",
            "Pantera",
            "Jaguar",
            "Puma",
            "Cóndor",
            "Halcón",
            "Águila",
            "Fénix",
            "Dragón",
            "Centauro",
        ],
        "female": [
            "Maharaní",
            "Sultana",
            "Lakshmi",
            "Kali",
            "Durga",
            "Saraswati",
            "Parvati",
            "Sita",
            "Radha",
            "Gita",
            "Loto",
            "Jazmín",
            "Magnolia",
            "Orquídea",
            "Rosa",
            "Azucena",
            "Gardenia",
            "Violeta",
            "Dalia",
            "Camelia",
        ],
    },
    BreedType.GUZERAT: {
        "male": [
            "Samurai",
            "Shogun",
            "Ronin",
            "Ninja",
            "Daimyo",
            "Gurú",
            "Sabio",
            "Maestro",
            "Sensei",
            "Oráculo",
            "Templo",
            "Monasterio",
            "Pagoda",
            "Mandala",
            "Nirvana",
            "Karma",
            "Dharma",
            "Zen",
            "Om",
            "Lama",
        ],
        "female": [
            "Geisha",
            "Sakura",
            "Kimono",
            "Lotus",
            "Bambú",
            "Jade",
            "Ópalo",
            "Topacio",
            "Esmeralda",
            "Rubí",
            "Mariposa",
            "Libélula",
            "Colibrí",
            "Golondrina",
            "Tórtola",
            "Paloma",
            "Grulla",
            "Cigüeña",
            "Garza",
            "Flamingo",
        ],
    },
    BreedType.SENEPOL: {
        "male": [
            "Caribe",
            "Trópico",
            "Coral",
            "Arrecife",
            "Huracán",
            "Ciclón",
            "Tifón",
            "Monsón",
            "Vendaval",
            "Tornado",
            "Pirata",
            "Corsario",
            "Bucanero",
            "Navegante",
            "Capitán",
            "Almirante",
            "Marinero",
            "Timonel",
            "Piloto",
            "Grumete",
        ],
        "female": [
            "Isla",
            "Bahía",
            "Laguna",
            "Playa",
            "Costa",
            "Orilla",
            "Ribera",
            "Marina",
            "Náutica",
            "Marítima",
            "Perla",
            "Concha",
            "Caracol",
            "Sirena",
            "Ninfa",
            "Náyade",
            "Oceánida",
            "Nereida",
            "Tritona",
            "Ondina",
        ],
    },
    BreedType.GIROLANDO: {
        "male": [
            "Lechero",
            "Cremoso",
            "Manteca",
            "Yogur",
            "Queso",
            "Nata",
            "Cuajo",
            "Suero",
            "Requesón",
            "Ricota",
            "Holstein",
            "Frisón",
            "Jersey",
            "Guernsey",
            "Ayrshire",
            "Normando",
            "Montbeliard",
            "Simmental",
            "Pardo",
            "Fleckvieh",
        ],
        "female": [
            "Lechera",
            "Cremosa",
            "Mantequilla",
            "Nata",
            "Dulce",
            "Miel",
            "Caramelo",
            "Azúcar",
            "Vainilla",
            "Canela",
            "Leche",
            "Lactosa",
            "Caseína",
            "Proteína",
            "Calcio",
            "Vitamina",
            "Nutriente",
            "Probiótica",
            "Fortificada",
            "Enriquecida",
        ],
    },
    BreedType.GYR_LECHERO: {
        "male": [
            "Ordeño",
            "Balde",
            "Tarro",
            "Cántaro",
            "Botella",
            "Bidón",
            "Tanque",
            "Cisterna",
            "Depósito",
            "Recipiente",
            "Pastor",
            "Vaquero",
            "Ganadero",
            "Ranchero",
            "Llanero",
            "Jinete",
            "Arriero",
            "Boyero",
            "Caporal",
            "Mayordomo",
        ],
        "female": [
            "Ordeña",
            "Vaca",
            "Nodriza",
            "Materna",
            "Nutriz",
            "Lactante",
            "Productora",
            "Donadora",
            "Dadora",
            "Proveedora",
            "Madre",
            "Mamá",
            "Mami",
            "Matriarca",
            "Abuela",
            "Nana",
            "Tata",
            "Yaya",
            "Ama",
            "Nodriza",
        ],
    },
    BreedType.SINDI: {
        "male": [
            "Rojo",
            "Bermejo",
            "Carmesí",
            "Escarlata",
            "Granate",
            "Rubí",
            "Coral",
            "Salmón",
            "Naranja",
            "Ámbar",
            "Compacto",
            "Pequeño",
            "Chico",
            "Bajito",
            "Petizo",
            "Enano",
            "Mini",
            "Tiny",
            "Diminuto",
            "Pigmeo",
        ],
        "female": [
            "Roja",
            "Bermeja",
            "Carmesí",
            "Escarlata",
            "Granate",
            "Rubí",
            "Coral",
            "Salmón",
            "Naranja",
            "Ámbar",
            "Compacta",
            "Pequeña",
            "Chica",
            "Bajita",
            "Petiza",
            "Enana",
            "Mini",
            "Tiny",
            "Diminuta",
            "Pigmea",
        ],
    },
}

# Distribución de razas (TOTAL: 300 animales)
# Proporciones: Nelore 35.39%, Brahman 21.07%, Guzerat 13.48%, Senepol 9.27%, Girolando 8.15%, Gyr Lechero 7.58%, Sindi 5.06%
BREED_DISTRIBUTION = {
    BreedType.NELORE: 126,  # 35.39% de 356
    BreedType.BRAHMAN: 75,  # 21.07% de 356
    BreedType.GUZERAT: 48,  # 13.48% de 356
    BreedType.SENEPOL: 33,  # 9.27% de 356
    BreedType.GIROLANDO: 29,  # 8.15% de 356
    BreedType.GYR_LECHERO: 27,  # 7.58% de 356
    BreedType.SINDI: 18,  # 5.06% de 356
}

# Colores por raza
BREED_COLORS = {
    BreedType.NELORE: ["Blanco", "Gris claro", "Blanco con manchas", "Gris"],
    BreedType.BRAHMAN: ["Gris", "Gris oscuro", "Blanco grisáceo", "Gris claro"],
    BreedType.GUZERAT: ["Gris", "Gris claro", "Blanco", "Gris con manchas"],
    BreedType.SENEPOL: ["Rojo", "Rojo oscuro", "Marrón rojizo", "Caoba"],
    BreedType.GIROLANDO: ["Blanco y negro", "Negro", "Blanco", "Manchado"],
    BreedType.GYR_LECHERO: ["Amarillo", "Amarillo claro", "Dorado", "Crema"],
    BreedType.SINDI: ["Rojo", "Marrón", "Rojo oscuro", "Castaño"],
}


class WeightDataLoader:
    """Carga y procesa datos de peso del CSV."""

    def __init__(self, csv_path: str):
        self.data: defaultdict[str, defaultdict[str, list[dict]]] = defaultdict(
            lambda: defaultdict(list)
        )
        self.load_csv(csv_path)

    def load_csv(self, csv_path: str):
        """Carga el CSV y organiza los datos por raza y categoría de edad."""
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                breed = row["breed"]
                age_in_year = float(row["age_in_year"])
                weight_kg = float(row["weight_kg"])
                sex = row["sex"]

                age_months = int(age_in_year * 12)
                if age_months < 8:
                    category = "terneros"
                elif age_months <= 18:
                    category = "vaquillonas_torillos"
                elif age_months <= 30:
                    category = "vaquillonas_toretes"
                else:
                    category = "vacas_toros"

                self.data[breed][category].append(
                    {"weight": weight_kg, "age_months": age_months, "sex": sex}
                )

    def get_sample_weight(self, breed: str, age_months: int, gender: str) -> float:
        """Obtiene un peso muestreado del CSV para una edad específica."""
        if age_months < 8:
            category = "terneros"
        elif age_months <= 18:
            category = "vaquillonas_torillos"
        elif age_months <= 30:
            category = "vaquillonas_toretes"
        else:
            category = "vacas_toros"

        sex_filter = "FEMALE" if gender == "female" else "MALE"
        candidates = [
            item for item in self.data[breed][category] if sex_filter in item["sex"]
        ]

        if not candidates:
            candidates = self.data[breed][category]

        if not candidates:
            return 200.0

        weights = sorted(candidates, key=lambda x: abs(x["age_months"] - age_months))
        selected = random.choice(weights[:5])
        variation = random.uniform(0.95, 1.05)
        return round(selected["weight"] * variation, 2)


async def create_roles() -> dict[str, RoleModel]:
    """Crea roles iniciales del sistema."""
    roles = {}

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


async def create_users(
    admin_role: RoleModel, user_role: RoleModel
) -> dict[str, UserModel]:
    """Crea usuarios del equipo Hacienda Gamelera."""
    users = {}

    bruno = UserModel(
        id=BRUNO_USER_ID,
        username="bruno_brito",
        email="bruno@haciendagamelera.com",
        hashed_password=get_password_hash("password123"),
        first_name="Bruno",
        last_name="Brito Macedo",
        role_id=admin_role.id,
        farm_id=FARM_ID,
        is_active=True,
        is_superuser=True,
    )
    await bruno.insert()
    users["bruno"] = bruno
    print(f"   ✅ Usuario creado: {bruno.first_name} {bruno.last_name} (Owner/Admin)")

    miguel = UserModel(
        id=MIGUEL_USER_ID,
        username="miguel_escobar",
        email="miguel@haciendagamelera.com",
        hashed_password=get_password_hash("password123"),
        first_name="Miguel Angel",
        last_name="Escobar Lazcano",
        role_id=admin_role.id,
        farm_id=FARM_ID,
        is_active=True,
        is_superuser=False,
    )
    await miguel.insert()
    users["miguel"] = miguel
    print(
        f"   ✅ Usuario creado: {miguel.first_name} {miguel.last_name} (Product Owner)"
    )

    rodrigo = UserModel(
        id=RODRIGO_USER_ID,
        username="rodrigo_escobar",
        email="rodrigo@haciendagamelera.com",
        hashed_password=get_password_hash("password123"),
        first_name="Rodrigo",
        last_name="Escobar Morón",
        role_id=user_role.id,
        farm_id=FARM_ID,
        is_active=True,
        is_superuser=False,
    )
    await rodrigo.insert()
    users["rodrigo"] = rodrigo
    print(
        f"   ✅ Usuario creado: {rodrigo.first_name} {rodrigo.last_name} (Scrum Master)"
    )

    return users


async def create_farm(owner: UserModel) -> FarmModel:
    """Crea la finca Hacienda Gamelera."""
    farm = FarmModel(
        id=FARM_ID,
        name=settings.HACIENDA_NAME,
        owner_id=owner.id,
        location={
            "type": "Point",
            "coordinates": [-60.797889, -15.859500],
        },
        capacity=settings.HACIENDA_CAPACITY,
        total_animals=0,
    )
    await farm.insert()
    print(f"   ✅ Finca creada: {farm.name}")
    print("      📍 Ubicación: San Ignacio de Velasco, Santa Cruz, Bolivia")
    print(f"      👤 Propietario: {owner.first_name} {owner.last_name}")
    print(f"      📊 Capacidad: {farm.capacity} animales")

    owner.farm_id = cast(UUID, farm.id)
    await owner.save()

    return farm


def generate_animals(
    farm_id: UUID,
    weight_loader: WeightDataLoader,
    images_by_breed: dict[str, dict[str, list[str]]],
) -> list[AnimalModel]:
    """Genera 200 animales con datos realistas y relaciones familiares validadas."""
    animals = []
    now = datetime.now(UTC)
    used_names: defaultdict[str, set[str]] = defaultdict(set)

    base_animals_by_breed: defaultdict[BreedType, dict[str, list[AnimalModel]]] = (
        defaultdict(lambda: {"males": [], "females": []})
    )
    base_counter = 1

    print("\n   📋 Generando animales base (potenciales reproductores)...")
    for breed in BreedType:
        num_females = random.randint(4, 8)
        num_males = random.randint(2, 4)

        for _ in range(num_females):
            birth_date = datetime(
                random.randint(2018, 2021),
                random.randint(1, 12),
                random.randint(1, 28),
                tzinfo=UTC,
            )
            name = get_unique_name(breed, "female", used_names)

            # Calcular edad para seleccionar imagen apropiada
            age_months = (now.year - birth_date.year) * 12 + (
                now.month - birth_date.month
            )
            photo_url = get_animal_photo_url(breed, age_months, images_by_breed)

            animal = AnimalModel(
                ear_tag=f"HG-{breed.value.upper()[:3]}-B{base_counter:03d}",
                breed=breed.value,
                birth_date=birth_date,
                gender="female",
                name=name,
                color=random.choice(BREED_COLORS[breed]),
                birth_weight_kg=round(random.uniform(25, 40), 1),
                photo_url=photo_url,
                status="active",
                farm_id=farm_id,
                registration_date=birth_date + timedelta(
                    days=random.randint(1, 30),
                    hours=random.randint(7, 10),
                    minutes=random.randint(0, 59)
                ),
                last_updated=now - timedelta(days=random.randint(0, 30)),
                observations=f"Vaca reproductora base - {BreedType.get_display_name(breed)}",
            )
            base_animals_by_breed[breed]["females"].append(animal)
            animals.append(animal)
            base_counter += 1

        for _ in range(num_males):
            birth_date = datetime(
                random.randint(2018, 2021),
                random.randint(1, 12),
                random.randint(1, 28),
                tzinfo=UTC,
            )
            name = get_unique_name(breed, "male", used_names)

            # Calcular edad para seleccionar imagen apropiada
            age_months = (now.year - birth_date.year) * 12 + (
                now.month - birth_date.month
            )
            photo_url = get_animal_photo_url(breed, age_months, images_by_breed)

            animal = AnimalModel(
                ear_tag=f"HG-{breed.value.upper()[:3]}-B{base_counter:03d}",
                breed=breed.value,
                birth_date=birth_date,
                gender="male",
                name=name,
                color=random.choice(BREED_COLORS[breed]),
                birth_weight_kg=round(random.uniform(28, 45), 1),
                photo_url=photo_url,
                status="active",
                farm_id=farm_id,
                registration_date=birth_date + timedelta(
                    days=random.randint(1, 30),
                    hours=random.randint(7, 10),
                    minutes=random.randint(0, 59)
                ),
                last_updated=now - timedelta(days=random.randint(0, 30)),
                observations=f"Toro reproductor base - {BreedType.get_display_name(breed)}",
            )
            base_animals_by_breed[breed]["males"].append(animal)
            animals.append(animal)
            base_counter += 1

    print(f"      ✓ {len(animals)} animales base creados")

    print("\n   📋 Generando animales del hato principal...")
    ear_tag_counter = 1

    for breed, count in BREED_DISTRIBUTION.items():
        base_count = len(base_animals_by_breed[breed]["males"]) + len(
            base_animals_by_breed[breed]["females"]
        )
        remaining = count - base_count

        if remaining <= 0:
            continue

        for _ in range(remaining):
            year = random.choices(
                [2021, 2022, 2023, 2024],
                weights=[10, 20, 35, 35],
            )[0]
            birth_date = datetime(
                year, random.randint(1, 12), random.randint(1, 28), tzinfo=UTC
            )

            if birth_date > now:
                birth_date = now - timedelta(days=random.randint(30, 365))

            gender = "female" if random.random() < 0.55 else "male"
            name = get_unique_name(breed, gender, used_names)

            # Calcular edad para seleccionar imagen apropiada
            age_months = (now.year - birth_date.year) * 12 + (
                now.month - birth_date.month
            )
            photo_url = get_animal_photo_url(breed, age_months, images_by_breed)

            mother_id = None
            father_id = None

            if birth_date.year >= 2022 and random.random() < 0.75:
                # Los padres deben tener al menos 24 meses (no pueden ser terneros/vaquillonas)
                # Esto significa al menos 24 meses + 9 meses gestación = 33 meses de diferencia mínima
                min_parent_age_days = 1005  # ~33 meses (24 meses + 9 gestación)

                potential_mothers = [
                    a
                    for a in base_animals_by_breed[breed]["females"]
                    if (birth_date - a.birth_date).days >= min_parent_age_days
                ]
                if potential_mothers:
                    mother_id = str(random.choice(potential_mothers).id)

                potential_fathers = [
                    a
                    for a in base_animals_by_breed[breed]["males"]
                    if (birth_date - a.birth_date).days >= min_parent_age_days
                ]
                if potential_fathers:
                    father_id = str(random.choice(potential_fathers).id)

            status = random.choices(
                ["active", "sold", "deceased"], weights=[0.85, 0.10, 0.05]
            )[0]

            # Calcular last_updated según estado
            days_alive = (now - birth_date).days

            if status == "deceased":
                # Muerte entre 30 días y la edad actual
                death_days = random.randint(30, max(31, days_alive))
                death_date = birth_date + timedelta(days=death_days)
                last_updated = death_date
            elif status == "sold":
                # Venta entre 180 días y la edad actual
                sold_days = random.randint(180, max(181, days_alive))
                sold_date = birth_date + timedelta(days=sold_days)
                last_updated = sold_date
            else:
                last_updated = now - timedelta(days=random.randint(0, 30))

            animal = AnimalModel(
                ear_tag=f"HG-{breed.value.upper()[:3]}-{ear_tag_counter:03d}",
                breed=breed.value,
                birth_date=birth_date,
                gender=gender,
                name=name,
                color=random.choice(BREED_COLORS[breed]),
                birth_weight_kg=round(random.uniform(25, 45), 1),
                photo_url=photo_url,
                mother_id=mother_id,
                father_id=father_id,
                status=status,
                farm_id=farm_id,
                registration_date=birth_date + timedelta(
                    days=random.randint(1, 30),
                    hours=random.randint(7, 10),
                    minutes=random.randint(0, 59)
                ),
                last_updated=last_updated,
                observations=f"Animal {BreedType.get_display_name(breed)}. "
                f"{'Con genealogía registrada.' if mother_id or father_id else 'Sin registro genealógico.'}",
            )
            animals.append(animal)
            ear_tag_counter += 1

    print(f"      ✓ {len(animals)} animales totales generados")
    return animals


def get_unique_name(
    breed: BreedType, gender: str, used_names: defaultdict[str, set[str]]
) -> str:
    """Genera un nombre único para el animal."""
    breed_key = breed.value
    available_names = [
        n for n in CATTLE_NAMES[breed][gender] if n not in used_names[breed_key]
    ]

    if not available_names:
        base_name = random.choice(CATTLE_NAMES[breed][gender])
        counter = 2
        while f"{base_name} {counter}" in used_names[breed_key]:
            counter += 1
        name = f"{base_name} {counter}"
    else:
        name = random.choice(available_names)

    used_names[breed_key].add(name)
    return name


def generate_weight_estimations(
    animals: list[AnimalModel],
    weight_loader: WeightDataLoader,
    images_by_breed: dict[str, dict[str, list[str]]],
) -> list[WeightEstimationModel]:
    """
    Genera estimaciones de peso con evolución temporal usando datos del CSV.
    Confianza entre 80-96%.

    Incluye:
    - Pérdida de peso aleatoria (10-15% de pesajes)
    - Decline progresivo para animales deceased
    """
    estimations = []
    now = datetime.now(UTC)

    print("\n   ⚖️  Generando estimaciones de peso con datos reales del CSV...")

    for animal in animals:
        end_date = animal.last_updated if animal.status in ("deceased", "sold") else now

        age_at_end = (end_date.year - animal.birth_date.year) * 12 + (
            end_date.month - animal.birth_date.month
        )

        if age_at_end < 6:
            num_weighings = random.randint(2, 4)
        elif age_at_end < 12:
            num_weighings = random.randint(4, 7)
        elif age_at_end < 24:
            num_weighings = random.randint(7, 12)
        else:
            num_weighings = random.randint(10, 18)

        weighing_dates = []
        start_date = animal.birth_date + timedelta(days=random.randint(30, 90))

        # Verificar que hay suficiente tiempo para generar pesajes
        if (end_date - start_date).days < 30:
            weighing_dates = [start_date] if start_date <= end_date else []
        else:
            days_span = (end_date - start_date).days
            interval = days_span / max(num_weighings, 1)
            for i in range(num_weighings):
                jitter = random.randint(-10, 10) if interval > 20 else 0
                date = start_date + timedelta(days=int(i * interval) + jitter)
                if start_date <= date <= end_date:
                    weighing_dates.append(date)

        weighing_dates.sort()

        # Rastrear el peso máximo alcanzado (para decline en deceased)
        max_weight = 0.0  # Tipo peso máximo: float
        previous_weight = 0.0  # Tipo peso anterior: float

        # Determinar si este animal tendrá decline (solo deceased)
        has_decline = animal.status == "deceased" and len(weighing_dates) > 3
        decline_start_index = (
            len(weighing_dates) - random.randint(2, 4)
            if has_decline
            else len(weighing_dates)
        )

        for i, weighing_date in enumerate(weighing_dates):
            age_months = (weighing_date.year - animal.birth_date.year) * 12 + (
                weighing_date.month - animal.birth_date.month
            )
            age_months = max(0, age_months)

            # Obtener peso base del CSV
            base_weight = weight_loader.get_sample_weight(
                animal.breed, age_months, animal.gender
            )

            # Aplicar lógica de peso según situación
            if has_decline and i >= decline_start_index:
                # DECLINE PROGRESIVO para animales deceased
                # Pérdida entre 5-15% del peso máximo por pesaje
                decline_factor = 1 - (
                    random.uniform(0.05, 0.15) * (i - decline_start_index + 1)
                )
                weight = max(
                    max_weight * decline_factor, base_weight * 0.5
                )  # No menos del 50% del base
            elif i > 0 and random.random() < 0.12:  # 12% de chance de pérdida de peso
                # PÉRDIDA DE PESO ALEATORIA (realismo)
                # Puede perder entre 3-8% del peso anterior
                loss_factor = random.uniform(0.92, 0.97)
                weight = previous_weight * loss_factor
            else:
                # CRECIMIENTO NORMAL
                weight = base_weight

            # Actualizar tracking
            max_weight = max(max_weight, weight)
            previous_weight = weight

            confidence = round(random.uniform(0.80, 0.96), 2)
            processing_time = random.randint(1200, 2800)

            # Obtener imagen real para la estimación
            breed_enum = BreedType(animal.breed)
            frame_image_path = get_estimation_frame_path(breed_enum, images_by_breed)

            estimation = WeightEstimationModel(
                animal_id=str(animal.id),
                breed=animal.breed,
                estimated_weight_kg=round(weight, 1),
                confidence=confidence,
                method="tflite",
                ml_model_version="1.0.0",
                processing_time_ms=processing_time,
                frame_image_path=frame_image_path,
                latitude=-15.859500 + random.uniform(-0.001, 0.001),
                longitude=-60.797889 + random.uniform(-0.001, 0.001),
                timestamp=weighing_date,
                created_at=weighing_date,
            )
            estimations.append(estimation)

    print(f"      ✓ {len(estimations)} estimaciones generadas")
    print(f"      ✓ Promedio: {len(estimations) / len(animals):.1f} pesajes por animal")

    return estimations


def generate_sample_alerts(
    user_id: UUID, farm_id: UUID, animals: list[AnimalModel]
) -> list[AlertModel]:
    """
    Genera alertas inteligentes programadas con límite de 20-25 animales.

    Criterios:
    - Por hato/potrero
    - Por especie/raza
    - Por edad/categoría
    - Por temporada
    - Por circunstancia (enfermedad, nacimiento, clima)
    - Combinaciones múltiples
    """
    alerts = []
    now = datetime.now(UTC)

    # Límite máximo de animales por alerta
    max_animals_per_alert = 25

    # ALERTA 1: Pesaje - Terneros Nelore (edad + raza)
    nelore_terneros = [
        a
        for a in animals
        if a.breed == "nelore"
        and a.calculate_age_category() == AgeCategory.TERNEROS
        and a.status == "active"
    ]
    if len(nelore_terneros) > 0:
        count = min(len(nelore_terneros), max_animals_per_alert)
        alerts.append(
            AlertModel(
                user_id=user_id,
                farm_id=farm_id,
                type=AlertType.SCHEDULED_WEIGHING,
                title="Control de Peso - Terneros Nelore",
                message=f"Pesar {count} terneros Nelore (<8 meses) del potrero norte",
                status=AlertStatus.PENDING,
                scheduled_at=now + timedelta(days=7),
                recurrence=RecurrenceType.MONTHLY,
                reminder_before_days=[7, 3, 1],
                filter_criteria={
                    "breed": "nelore",
                    "age_category": "terneros",
                    "count": count,
                    "location": "potrero_norte",
                },
                location={"type": "Point", "coordinates": [-60.797889, -15.859500]},
            )
        )

    # ALERTA 2: Vacunación - Vaquillonas (edad + género)
    vaquillonas_active = [
        a
        for a in animals
        if a.gender == "female"
        and a.calculate_age_category() == AgeCategory.VAQUILLONAS_TORILLOS
        and a.status == "active"
    ]
    if len(vaquillonas_active) > 0:
        count = min(len(vaquillonas_active), max_animals_per_alert)
        alerts.append(
            AlertModel(
                user_id=user_id,
                farm_id=farm_id,
                type=AlertType.VETERINARY_TREATMENT,
                title="Vacunación - Vaquillonas",
                message=f"Vacunar {count} vaquillonas (6-18 meses) - Programa sanitario trimestral",
                status=AlertStatus.PENDING,
                scheduled_at=now + timedelta(days=14),
                recurrence=RecurrenceType.QUARTERLY,
                reminder_before_days=[14, 7, 3, 1],
                filter_criteria={
                    "gender": "female",
                    "age_category": "vaquillonas_torillos",
                    "count": count,
                },
            )
        )

    # ALERTA 3: Tratamiento - Brahman adultos por temporada de lluvia
    brahman_adultos = [
        a
        for a in animals
        if a.breed == "brahman"
        and a.calculate_age_category()
        in [AgeCategory.VAQUILLONAS_TORETES, AgeCategory.VACAS_TOROS]
        and a.status == "active"
    ]
    if len(brahman_adultos) > 0:
        count = min(len(brahman_adultos), max_animals_per_alert)
        alerts.append(
            AlertModel(
                user_id=user_id,
                farm_id=farm_id,
                type=AlertType.VETERINARY_TREATMENT,
                title="Antiparasitario - Brahman Adultos (Temporada Lluvia)",
                message=f"Aplicar antiparasitario a {count} animales Brahman adultos por temporada de lluvias",
                status=AlertStatus.PENDING,
                scheduled_at=now + timedelta(days=5),
                recurrence=RecurrenceType.MONTHLY,
                reminder_before_days=[5, 2],
                filter_criteria={
                    "breed": "brahman",
                    "age_category": ["vaquillonas_toretes", "vacas_toros"],
                    "count": count,
                    "reason": "temporada_lluvia",
                },
            )
        )

    # ALERTA 4: Pesaje selectivo - Machos de múltiples razas (género + múltiples razas)
    machos_carne = [
        a
        for a in animals
        if a.gender == "male"
        and a.breed in ["nelore", "brahman", "guzerat"]
        and a.calculate_age_category()
        in [AgeCategory.VAQUILLONAS_TORETES, AgeCategory.VACAS_TOROS]
        and a.status == "active"
    ]
    if len(machos_carne) > 0:
        count = min(len(machos_carne), max_animals_per_alert)
        alerts.append(
            AlertModel(
                user_id=user_id,
                farm_id=farm_id,
                type=AlertType.SCHEDULED_WEIGHING,
                title="Evaluación Reproductores - Nelore/Brahman/Guzerat",
                message=f"Pesar y evaluar {count} toros reproductores (Nelore, Brahman, Guzerat)",
                status=AlertStatus.PENDING,
                scheduled_at=now + timedelta(days=10),
                recurrence=RecurrenceType.MONTHLY,
                reminder_before_days=[7, 1],
                filter_criteria={
                    "gender": "male",
                    "breed": ["nelore", "brahman", "guzerat"],
                    "age_category": ["vaquillonas_toretes", "vacas_toros"],
                    "count": count,
                    "purpose": "evaluacion_reproductiva",
                },
            )
        )

    # ALERTA 5: Control de gestación - Hembras adultas
    hembras_gestacion = [
        a
        for a in animals
        if a.gender == "female"
        and a.calculate_age_category() == AgeCategory.VACAS_TOROS
        and a.status == "active"
    ]
    if len(hembras_gestacion) > 0:
        count = min(len(hembras_gestacion), 20)  # Más selectivo: max 20
        alerts.append(
            AlertModel(
                user_id=user_id,
                farm_id=farm_id,
                type=AlertType.VETERINARY_TREATMENT,
                title="Control de Gestación - Vacas Adultas",
                message=f"Revisar {count} vacas adultas para control de gestación y preñez",
                status=AlertStatus.PENDING,
                scheduled_at=now + timedelta(days=21),
                recurrence=RecurrenceType.MONTHLY,
                reminder_before_days=[7, 3],
                filter_criteria={
                    "gender": "female",
                    "age_category": "vacas_toros",
                    "count": count,
                    "checkup": "gestacion",
                },
            )
        )

    # ALERTA 6: Pesaje post-sequía (circunstancia climática)
    animales_potrero_sur = random.sample(
        [a for a in animals if a.status == "active"],
        min(max_animals_per_alert, len([a for a in animals if a.status == "active"])),
    )
    if len(animales_potrero_sur) > 0:
        alerts.append(
            AlertModel(
                user_id=user_id,
                farm_id=farm_id,
                type=AlertType.SCHEDULED_WEIGHING,
                title="Control Post-Sequía - Potrero Sur",
                message=f"Evaluar peso de {len(animales_potrero_sur)} animales del potrero sur tras período de sequía",
                status=AlertStatus.PENDING,
                scheduled_at=now + timedelta(days=3),
                recurrence=RecurrenceType.NONE,  # Evento único
                reminder_before_days=[2, 1],
                filter_criteria={
                    "location": "potrero_sur",
                    "count": len(animales_potrero_sur),
                    "circumstance": "post_sequia",
                },
                location={"type": "Point", "coordinates": [-60.798000, -15.860000]},
            )
        )

    # ALERTA 7: Preparación exposición ganadera (evento específico)
    animales_exposicion = [
        a
        for a in animals
        if a.breed in ["nelore", "brahman"]
        and a.calculate_age_category()
        in [AgeCategory.VAQUILLONAS_TORETES, AgeCategory.VACAS_TOROS]
        and a.status == "active"
    ]
    if len(animales_exposicion) > 0:
        count = min(15, len(animales_exposicion))  # Solo los mejores ejemplares
        alerts.append(
            AlertModel(
                user_id=user_id,
                farm_id=farm_id,
                type=AlertType.CALENDAR_EVENT,
                title="Preparación Exposición ASOCEBU",
                message=f"Preparar {count} ejemplares (Nelore/Brahman) para exposición ganadera",
                status=AlertStatus.PENDING,
                scheduled_at=now + timedelta(days=30),
                recurrence=RecurrenceType.YEARLY,
                reminder_before_days=[30, 14, 7, 1],
                filter_criteria={
                    "breed": ["nelore", "brahman"],
                    "age_category": ["vaquillonas_toretes", "vacas_toros"],
                    "count": count,
                    "event": "exposicion_asocebu",
                },
            )
        )

    return alerts


async def seed_database():
    """Función principal para cargar datos iniciales mejorados."""
    print("🌱 Iniciando carga de datos MEJORADOS con CSV real...")
    print(f"📊 Base de datos: {settings.MONGODB_DB_NAME}")
    print(f"🔗 MongoDB URL: {settings.MONGODB_URL}\n")

    csv_path = Path(__file__).parent.parent / "uploads" / "metadata_estimada.csv"
    if not csv_path.exists():
        print(f"❌ Error: No se encontró el archivo CSV en {csv_path}")
        print("   Por favor coloca 'metadata_estimada.csv' en backend/uploads/")
        return

    print(f"📁 Cargando datos de peso desde: {csv_path}")
    weight_loader = WeightDataLoader(str(csv_path))
    print("   ✅ CSV cargado exitosamente\n")

    # Cargar imágenes disponibles
    uploads_dir = Path(__file__).parent.parent / "uploads"
    print("📸 Cargando imágenes disponibles por raza...")
    images_by_breed = load_available_images(uploads_dir)
    print("   ✅ Imágenes cargadas\n")

    client = AsyncIOMotorClient(settings.MONGODB_URL)

    try:
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

        print("🗑️  Limpiando datos existentes...")
        await AlertModel.delete_all()
        await AnimalModel.delete_all()
        await WeightEstimationModel.delete_all()
        await FarmModel.delete_all()
        await UserModel.delete_all()
        await RoleModel.delete_all()
        print("✅ Datos limpiados\n")

        print("👥 Creando roles iniciales...")
        roles = await create_roles()
        print(f"✅ {len(roles)} roles creados\n")

        print("👤 Creando usuarios del equipo Hacienda Gamelera...")
        users = await create_users(roles["admin"], roles["user"])
        print(f"✅ {len(users)} usuarios creados\n")

        print("🏢 Creando finca Hacienda Gamelera...")
        farm = await create_farm(users["bruno"])
        print("✅ Finca creada\n")

        print("🐄 Generando 300 animales con datos realistas...")
        animals = generate_animals(farm.id, weight_loader, images_by_breed)
        await AnimalModel.insert_many(animals)
        print(f"✅ {len(animals)} animales insertados\n")

        farm.total_animals = len(animals)
        await farm.save()

        estimations = generate_weight_estimations(
            animals, weight_loader, images_by_breed
        )
        await WeightEstimationModel.insert_many(estimations)
        print(f"✅ {len(estimations)} estimaciones insertadas\n")

        print("🔔 Generando alertas...")
        alerts = generate_sample_alerts(users["bruno"].id, farm.id, animals)
        if alerts:
            await AlertModel.insert_many(alerts)
            print(f"✅ {len(alerts)} alertas insertadas\n")

        print("=" * 70)
        print("📊 RESUMEN - DATOS MEJORADOS CARGADOS")
        print("=" * 70)
        print(f"👥 Roles: {len(roles)}")
        print(f"👤 Usuarios: {len(users)}")
        print("   - Bruno Brito Macedo (Owner/Superusuario)")
        print("   - Miguel Angel Escobar Lazcano (Product Owner)")
        print("   - Rodrigo Escobar Morón (Scrum Master)")
        print(f"🏢 Finca: {farm.name}")
        print(f"🐄 Animales: {len(animals)}")
        print(f"⚖️  Estimaciones: {len(estimations)}")
        print(f"📈 Promedio pesajes/animal: {len(estimations)/len(animals):.1f}")
        print(f"🔔 Alertas: {len(alerts)}")

        print("\n📋 Distribución por raza:")
        breed_counts = Counter(animal.breed for animal in animals)
        for breed, count in sorted(breed_counts.items()):
            percentage = (count / len(animals)) * 100
            print(
                f"   - {BreedType.get_display_name(BreedType(breed))}: "
                f"{count} ({percentage:.1f}%)"
            )

        with_parents = sum(1 for a in animals if a.mother_id or a.father_id)
        print(
            f"\n👨‍👩‍👧 Animales con genealogía: {with_parents} ({with_parents/len(animals)*100:.1f}%)"
        )

        confidences = [e.confidence for e in estimations]
        print(
            f"\n📊 Rango de confianza: {min(confidences):.2%} - {max(confidences):.2%}"
        )

        print("\n" + "=" * 70)
        print("✅ Seed data MEJORADO completado!")
        print("\n🔐 CREDENCIALES:")
        print("   Usuario: bruno_brito | Contraseña: password123")
        print("   Usuario: miguel_escobar | Contraseña: password123")
        print("   Usuario: rodrigo_escobar | Contraseña: password123")
        print("=" * 70)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        raise
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
