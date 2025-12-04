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
from app.domain.shared.constants.breeds import (
    DAIRY_BREEDS,
    DUAL_PURPOSE_BREEDS,
    MEAT_BREEDS,
)

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
CARLOS_USER_ID = UUID("770e8400-e29b-41d4-a716-446655440003")
NELSON_USER_ID = UUID("880e8400-e29b-41d4-a716-446655440004")
ANDRES_USER_ID = UUID("990e8400-e29b-41d4-a716-446655440005")
TECNICO_USER_ID = UUID("aa0e8400-e29b-41d4-a716-446655440006")
FARM_ID = UUID("bb0e8400-e29b-41d4-a716-446655440000")

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

# Distribución de razas (TOTAL: 373 animales)
# Proporciones: Nelore 39.14%, Brahman 19.03%, Guzerat 12.87%, Senepol 9.12%, Girolando 7.77%, Gyr Lechero 7.24%, Sindi 4.83%
BREED_DISTRIBUTION = {
    BreedType.NELORE: 146,  # 39.14% de 373
    BreedType.BRAHMAN: 71,  # 19.03% de 373
    BreedType.GUZERAT: 48,  # 12.87% de 373
    BreedType.SENEPOL: 34,  # 9.12% de 373
    BreedType.GIROLANDO: 29,  # 7.77% de 373
    BreedType.GYR_LECHERO: 27,  # 7.24% de 373
    BreedType.SINDI: 18,  # 4.83% de 373
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


def get_birth_year_range(
    breed: BreedType, gender: str, is_base_animal: bool = False
) -> tuple[int, int]:
    """
    Determina el rango de años de nacimiento según el propósito de la raza.

    Consideraciones:
    - Animales base (reproductores): pueden ser más viejos (2018-2021)
    - Razas de carne: más recientes (2022-2024), se fanean rápido
    - Razas lecheras: ciclo de producción (2021-2024)
    - Doble propósito: más longevos (2020-2024)

    Args:
        breed: Raza del animal
        gender: Género (male/female)
        is_base_animal: Si es animal base (reproductor)

    Returns:
        Tupla (año_minimo, año_maximo)
    """
    purpose = get_breed_purpose(breed)

    # Animales base (reproductores): se mantienen más tiempo
    if is_base_animal:
        # Reproductores pueden ser de 2018-2021 (más viejos pero activos)
        return 2018, 2021

    # Animales del hato principal según propósito
    if purpose == "meat":
        # Razas de carne: se fanean rápido (2-3 años), mayoría recientes
        if gender == "male":
            # Terneros de carne: nacidos 2022-2024 (se fanean a los 2-3 años)
            return 2022, 2024
        # Hembras de carne: algunas se mantienen como reproductoras
        return 2021, 2024

    if purpose == "dairy":
        # Razas lecheras: ciclo de producción 4-6 partos
        # Vacas lecheras se descartan después del 4-6 parto (48-84 meses)
        # Mayoría nacidas 2021-2024 para tener animales en producción activa
        return 2021, 2024

    if purpose == "dual_purpose":
        # Doble propósito: más longevos pero también con límites
        return 2020, 2024

    # Default: razas de carne
    return 2022, 2024


def get_breed_purpose(breed: BreedType) -> str:
    """
    Determina el propósito de la raza: 'meat', 'dairy', o 'dual_purpose'.

    Args:
        breed: Raza del animal

    Returns:
        Propósito de la raza
    """
    if breed in MEAT_BREEDS:
        return "meat"
    if breed in DAIRY_BREEDS:
        return "dairy"
    if breed in DUAL_PURPOSE_BREEDS:
        return "dual_purpose"
    return "meat"  # Default


def should_cull_animal(
    breed: BreedType,
    gender: str,
    age_months: int,
    purpose: str,
    random_factor: float,
) -> tuple[bool, str]:
    """
    Determina si un animal debe ser descartado (faneado) según su raza, propósito y edad.

    Basado en contexto ganadero:
    - Vacas lecheras: descarte al 4-6 parto (producción láctea decrece)
    - Razas de carne: terneros se levantan antes de 2.5-3 años
    - Doble propósito: más longevas, no se descartan pronto
    - Vacas de 5+ años tienen carne de menor calidad

    Args:
        breed: Raza del animal
        gender: Género (male/female)
        age_months: Edad en meses
        purpose: Propósito de la raza (meat/dairy/dual_purpose)
        random_factor: Factor aleatorio para variación (0-1)

    Returns:
        Tupla (debe_descartar, razon)
    """
    # RAZAS LECHERAS (Girolando, Gyr Lechero, Sindi)
    if purpose == "dairy":
        if gender == "female":
            # Vacas lecheras: descarte al 4-6 parto
            # Asumiendo primer parto a ~24 meses, cada parto cada 12 meses
            # 4-6 partos = 48-72 meses (4-6 años)
            # Jersey alcanza madurez después del 3er parto, pero Girolando/Gyr similar a Holstein
            # Gyr Lechero: descarte después del 3er-5to parto (36-60 meses)
            if (
                breed == BreedType.GYR_LECHERO
                and 36 <= age_months <= 72
                and random_factor < 0.15
            ):
                return True, "descarte_produccion_lechera"
            # Girolando/Sindi: descarte al 4-6 parto (48-72 meses)
            if (
                breed != BreedType.GYR_LECHERO
                and 48 <= age_months <= 84
                and random_factor < 0.20
            ):
                return True, "descarte_produccion_lechera"
        # Machos lecheros: se descartan más temprano (no son reproductores principales)
        elif gender == "male" and age_months >= 30 and random_factor < 0.10:
            return True, "descarte_macho_lechero"

    # RAZAS DE CARNE (Nelore, Brahman, Senepol)
    elif purpose == "meat":
        # Terneros de carne: se levantan antes de 2.5-3 años (30-36 meses)
        if gender == "male" and 24 <= age_months <= 42 and random_factor < 0.25:
            return True, "destinado_faneo_carne"
        # Hembras de carne: pueden mantenerse más tiempo si son reproductoras
        # Pero algunas se descartan temprano si no son productivas
        if gender == "female" and 30 <= age_months <= 48 and random_factor < 0.12:
            return True, "descarte_hembra_carne"

    # DOBLE PROPÓSITO (Guzerat)
    elif purpose == "dual_purpose" and age_months >= 84 and random_factor < 0.08:
        # Doble propósito: más longevas, no se descartan pronto
        # Solo descarte por edad avanzada (7+ años = 84+ meses)
        return True, "descarte_edad_avanzada"

    # DESCARTE GENERAL POR EDAD (todas las razas)
    # Vacas de 5+ años (60+ meses) tienen carne de menor calidad
    if age_months >= 60 and random_factor < 0.05:
        return True, "descarte_calidad_carne"

    return False, ""


def determine_animal_status(
    breed: BreedType,
    gender: str,
    age_months: int,
    random_factor: float,
) -> tuple[str, str]:
    """
    Determina el status final del animal considerando descarte (faneo) según propósito.

    Args:
        breed: Raza del animal
        gender: Género (male/female)
        age_months: Edad en meses
        random_factor: Factor aleatorio para variación

    Returns:
        Tupla (status, razon)
    """
    purpose = get_breed_purpose(breed)

    # Verificar si debe ser descartado (faneado)
    should_cull, cull_reason = should_cull_animal(
        breed, gender, age_months, purpose, random_factor
    )

    if should_cull:
        return "culled", cull_reason

    # Si no es descarte, usar lógica normal
    status_choice = random.choices(
        ["active", "sold", "deceased"],
        weights=[0.85, 0.10, 0.05],
    )[0]

    return status_choice, ""


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
    admin_role: RoleModel, user_role: RoleModel, guest_role: RoleModel
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
        is_superuser=True,
    )
    await miguel.insert()
    users["miguel"] = miguel
    print(
        f"   ✅ Usuario creado: {miguel.first_name} {miguel.last_name} (Administrador/Product Owner)"
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
        f"   ✅ Usuario creado: {rodrigo.first_name} {rodrigo.last_name} (Usuario/Scrum Master)"
    )

    # Técnico de medición (Usuario)
    tecnico = UserModel(
        id=TECNICO_USER_ID,
        username="sara_montero",
        email="sara.montero@haciendagamelera.com",
        hashed_password=get_password_hash("password123"),
        first_name="Sara Luz",
        last_name="Montero",
        role_id=user_role.id,
        farm_id=FARM_ID,
        is_active=True,
        is_superuser=False,
    )
    await tecnico.insert()
    users["tecnico"] = tecnico
    print(
        f"   ✅ Usuario creado: {tecnico.first_name} {tecnico.last_name} (Usuario - Técnico de Medición)"
    )

    # Capataces/Asistentes (Invitados - solo lectura)
    carlos = UserModel(
        id=CARLOS_USER_ID,
        username="carlos_ferrufino",
        email="carlos@haciendagamelera.com",
        hashed_password=get_password_hash("password123"),
        first_name="Carlos",
        last_name="Ferrufino",
        role_id=guest_role.id,
        farm_id=FARM_ID,
        is_active=True,
        is_superuser=False,
    )
    await carlos.insert()
    users["carlos"] = carlos
    print(
        f"   ✅ Usuario creado: {carlos.first_name} {carlos.last_name} (Invitado - Capataz)"
    )

    nelson = UserModel(
        id=NELSON_USER_ID,
        username="nelson_farel",
        email="nelson@haciendagamelera.com",
        hashed_password=get_password_hash("password123"),
        first_name="Nelson",
        last_name="Farel",
        role_id=guest_role.id,
        farm_id=FARM_ID,
        is_active=True,
        is_superuser=False,
    )
    await nelson.insert()
    users["nelson"] = nelson
    print(
        f"   ✅ Usuario creado: {nelson.first_name} {nelson.last_name} (Invitado - Capataz)"
    )

    andres = UserModel(
        id=ANDRES_USER_ID,
        username="andres_saravia",
        email="andres@haciendagamelera.com",
        hashed_password=get_password_hash("password123"),
        first_name="Andres",
        last_name="Saravia",
        role_id=guest_role.id,
        farm_id=FARM_ID,
        is_active=True,
        is_superuser=False,
    )
    await andres.insert()
    users["andres"] = andres
    print(
        f"   ✅ Usuario creado: {andres.first_name} {andres.last_name} (Invitado - Asistente)"
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
            # Animales base: reproductores que se mantienen más tiempo
            min_year, max_year = get_birth_year_range(
                breed, "female", is_base_animal=True
            )
            birth_date = datetime(
                random.randint(min_year, max_year),
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
                registration_date=birth_date
                + timedelta(
                    days=random.randint(1, 30),
                    hours=random.randint(7, 10),
                    minutes=random.randint(0, 59),
                ),
                last_updated=now - timedelta(days=random.randint(0, 30)),
                observations=f"Vaca reproductora base - {BreedType.get_display_name(breed)}",
            )
            base_animals_by_breed[breed]["females"].append(animal)
            animals.append(animal)
            base_counter += 1

        for _ in range(num_males):
            # Animales base: reproductores que se mantienen más tiempo
            min_year, max_year = get_birth_year_range(
                breed, "male", is_base_animal=True
            )
            birth_date = datetime(
                random.randint(min_year, max_year),
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
                registration_date=birth_date
                + timedelta(
                    days=random.randint(1, 30),
                    hours=random.randint(7, 10),
                    minutes=random.randint(0, 59),
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
            gender: str = "female" if random.random() < 0.55 else "male"

            # Determinar rango de años según propósito de la raza
            min_year, max_year = get_birth_year_range(breed, gender)

            # Asegurar que max_year no exceda el año actual
            max_year = min(max_year, now.year)

            # Generar año con distribución: más peso a años recientes
            available_years = list(range(min_year, max_year + 1))
            if len(available_years) == 1:
                year = available_years[0]
            else:
                # Más peso a años recientes (últimos 2 años tienen más probabilidad)
                weights: list[int] = []
                for y in available_years:
                    if y == max_year:
                        weights.append(35)  # Año más reciente: 35%
                    elif y == max_year - 1:
                        weights.append(35)  # Segundo más reciente: 35%
                    elif y == max_year - 2:
                        weights.append(20)  # Tercero: 20%
                    else:
                        weights.append(10)  # Más antiguos: 10%

                # Normalizar pesos
                total_weight = sum(weights)
                normalized_weights: list[float] = [w / total_weight for w in weights]
                year = random.choices(available_years, weights=normalized_weights)[0]

            birth_date = datetime(
                year, random.randint(1, 12), random.randint(1, 28), tzinfo=UTC
            )

            if birth_date > now:
                birth_date = now - timedelta(days=random.randint(30, 365))
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

            # Calcular edad actual para determinar descarte
            age_months = (now.year - birth_date.year) * 12 + (
                now.month - birth_date.month
            )
            age_months = max(0, age_months)

            # Determinar status considerando descarte según propósito de raza
            status, status_reason = determine_animal_status(
                breed, gender, age_months, random.random()
            )

            # Calcular last_updated según estado
            days_alive = (now - birth_date).days

            if status == "culled":
                # Descarte (faneo): entre edad mínima de descarte y la edad actual
                # Para razas de carne: 24-42 meses, lecheras: 36-84 meses
                purpose = get_breed_purpose(breed)
                if purpose == "meat" and gender == "male":
                    min_cull_age = 24 * 30  # 24 meses en días
                    max_cull_age = min(42 * 30, days_alive)
                elif purpose == "dairy" and gender == "female":
                    min_cull_age = 36 * 30  # 36 meses en días
                    max_cull_age = min(84 * 30, days_alive)
                else:
                    min_cull_age = 30 * 30  # 30 meses en días
                    max_cull_age = min(60 * 30, days_alive)

                if max_cull_age > min_cull_age:
                    cull_days = random.randint(min_cull_age, max_cull_age)
                else:
                    cull_days = random.randint(30, max(31, days_alive))

                cull_date = birth_date + timedelta(days=cull_days)
                last_updated = cull_date
            elif status == "deceased":
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
                registration_date=birth_date
                + timedelta(
                    days=random.randint(1, 30),
                    hours=random.randint(7, 10),
                    minutes=random.randint(0, 59),
                ),
                last_updated=last_updated,
                observations=(
                    f"Animal {BreedType.get_display_name(breed)}. "
                    f"{'Con genealogía registrada.' if mother_id or father_id else 'Sin registro genealógico.'}"
                    f"{f' Destinado al faneo: {status_reason}.' if status == 'culled' and status_reason else ''}"
                ),
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


def get_season(month: int) -> str:
    """
    Determina la época del año en Bolivia (San Ignacio de Velasco).

    Args:
        month: Mes (1-12)

    Returns:
        'dry' (seca) o 'rainy' (lluviosa)
    """
    # Época seca: mayo-octubre (5-10)
    # Época lluviosa: noviembre-abril (11-12, 1-4)
    if 5 <= month <= 10:
        return "dry"
    return "rainy"


def get_seasonal_weight_factor(month: int, random_factor: float) -> float:
    """
    Calcula factor de ajuste de peso según época del año.

    Época seca (mayo-octubre): pérdida de peso (-2% a -8%)
    Época lluviosa (noviembre-abril): ganancia de peso (+1% a +5%)

    Args:
        month: Mes del pesaje (1-12)
        random_factor: Factor aleatorio para variación

    Returns:
        Factor multiplicador (ej: 0.95 = -5%, 1.03 = +3%)
    """
    season = get_season(month)
    if season == "dry":
        # Pérdida de peso: -2% a -8% (0.92 a 0.98)
        return random.uniform(0.92, 0.98)
    # Época lluviosa: ganancia de peso: +1% a +5% (1.01 a 1.05)
    return random.uniform(1.01, 1.05)


def get_growth_curve_factor(age_months: int) -> float:
    """
    Aplica curva de crecimiento realista según edad.

    Terneros (0-12 meses): crecimiento acelerado (factor 1.0-1.15)
    Jóvenes (12-24 meses): crecimiento moderado (factor 0.95-1.05)
    Adultos (24+ meses): crecimiento lento o mantenimiento (factor 0.90-1.0)

    Args:
        age_months: Edad en meses

    Returns:
        Factor multiplicador de crecimiento
    """
    if age_months < 12:
        # Terneros: crecimiento acelerado
        # Más crecimiento al inicio, disminuye con la edad
        growth_rate = 1.0 + (12 - age_months) * 0.012  # 1.0 a 1.144
        return random.uniform(growth_rate * 0.98, growth_rate * 1.02)
    if age_months < 24:
        # Jóvenes: crecimiento moderado
        return random.uniform(0.95, 1.05)
    # Adultos: crecimiento lento o mantenimiento
    return random.uniform(0.90, 1.0)


def get_confidence_by_conditions(hour: int, random_factor: float) -> float:
    """
    Calcula confianza según condiciones de captura.

    Día soleado (8-16h): 0.90-0.96
    Día nublado: 0.85-0.92
    Atardecer/amanecer (6-8h, 16-18h): 0.80-0.88
    Condiciones adversas (noche/temprano): 0.80-0.85

    Args:
        hour: Hora del día (0-23)
        random_factor: Factor aleatorio para variación

    Returns:
        Nivel de confianza (0.80-0.96)
    """
    # Determinar condiciones según hora
    if 8 <= hour <= 16:
        # Día: 70% soleado, 30% nublado
        if random_factor < 0.7:
            return round(random.uniform(0.90, 0.96), 2)  # Día soleado
        return round(random.uniform(0.85, 0.92), 2)  # Día nublado
    if 6 <= hour < 8 or 16 < hour <= 18:
        # Atardecer/amanecer
        return round(random.uniform(0.80, 0.88), 2)
    # Noche o muy temprano: condiciones adversas
    return round(random.uniform(0.80, 0.85), 2)


def simulate_life_events(
    animal: AnimalModel,
    weighing_date: datetime,
    age_months: int,
    previous_weight: float,
) -> tuple[float, str]:
    """
    Simula eventos de vida que afectan el peso.

    - Enfermedades: pérdida temporal de peso (5-15%)
    - Tratamientos veterinarios: pérdida inicial, luego recuperación
    - Partos (hembras): pérdida post-parto (8-15%), luego recuperación
    - Toros en servicio: mantenimiento de peso

    Args:
        animal: Animal
        weighing_date: Fecha del pesaje
        age_months: Edad en meses
        previous_weight: Peso anterior

    Returns:
        Tupla (peso_ajustado, evento_descripcion)
    """
    event_description = ""
    adjusted_weight = previous_weight

    # Hembras: simular partos (solo si tienen más de 24 meses)
    # 15% de chance de estar preñada o haber parido recientemente
    if animal.gender == "female" and age_months >= 24 and random.random() < 0.15:
        days_since_birth = random.randint(0, 120)  # 0-4 meses post-parto
        if days_since_birth < 30:
            # Recién parido: pérdida de peso 8-15%
            loss_factor = random.uniform(0.85, 0.92)
            adjusted_weight = previous_weight * loss_factor
            event_description = f"Post-parto reciente ({days_since_birth} días)"
        elif days_since_birth < 60:
            # Recuperación post-parto: peso intermedio
            recovery_factor = random.uniform(0.92, 0.98)
            adjusted_weight = previous_weight * recovery_factor
            event_description = f"Recuperación post-parto ({days_since_birth} días)"
        elif days_since_birth < 90:
            # Preñada: ganancia de peso 2-5%
            gain_factor = random.uniform(1.02, 1.05)
            adjusted_weight = previous_weight * gain_factor
            event_description = f"Preñada (aprox {days_since_birth} días)"
        else:
            # Lactante: posible pérdida leve 2-5%
            loss_factor = random.uniform(0.95, 0.98)
            adjusted_weight = previous_weight * loss_factor
            event_description = f"Lactante ({days_since_birth} días)"

    # Enfermedades: 8% de chance (afecta a cualquier animal)
    if random.random() < 0.08:
        # Pérdida de peso por enfermedad: 5-15%
        illness_factor = random.uniform(0.85, 0.95)
        adjusted_weight = previous_weight * illness_factor
        if event_description:
            event_description += f" | Enfermedad (-{int((1-illness_factor)*100)}%)"
        else:
            event_description = f"Enfermedad (-{int((1-illness_factor)*100)}%)"

    # Tratamientos veterinarios: 5% de chance
    if random.random() < 0.05 and not event_description:
        # Pérdida inicial por tratamiento, luego recuperación
        treatment_factor = random.uniform(0.92, 0.97)
        adjusted_weight = previous_weight * treatment_factor
        event_description = "Tratamiento veterinario reciente"

    # Toros en servicio: mantenimiento de peso (si es toro adulto)
    if (
        animal.gender == "male"
        and age_months >= 30
        and random.random() < 0.20
        and not event_description
    ):
        # 20% de chance de estar en servicio activo
        # Mantenimiento: peso estable (±2%)
        maintenance_factor = random.uniform(0.98, 1.02)
        adjusted_weight = previous_weight * maintenance_factor
        event_description = "Toro en servicio activo"

    return adjusted_weight, event_description


def get_gender_weight_adjustment(gender: str, base_weight: float) -> float:
    """
    Ajusta peso según género.

    Machos: generalmente 5-10% más pesados
    Hembras: ligeramente más ligeras (usar peso base)

    Args:
        gender: Género (male/female)
        base_weight: Peso base del CSV

    Returns:
        Peso ajustado según género
    """
    if gender == "male":
        # Machos: 5-10% más pesados
        return base_weight * random.uniform(1.05, 1.10)
    # Hembras: usar peso base (ya viene ajustado del CSV)
    return base_weight


def apply_weight_correction_for_seeder(
    raw_weight: float, breed: BreedType, gender: str
) -> float:
    """
    Aplica corrección post-procesamiento para pesos fuera del rango del modelo.

    Misma lógica que deep_learning_strategy.py pero adaptada para el seeder.
    Detecta cuando el peso está subestimado y aplica corrección basada en:
    - Posición en el rango del modelo
    - Distancia al máximo real conocido
    - Diferenciación entre hembras y toros de élite

    Args:
        raw_weight: Peso calculado (después de todos los ajustes)
        breed: Raza del animal
        gender: Género (male/female)

    Returns:
        Peso corregido (puede ser igual al raw_weight si no necesita corrección)
    """
    # Rangos de entrenamiento del modelo (lo que el modelo "conoce")
    model_training_ranges = {
        BreedType.NELORE: (250, 650),
        BreedType.BRAHMAN: (260, 680),
        BreedType.GUZERAT: (240, 650),
        BreedType.SENEPOL: (280, 620),
        BreedType.GIROLANDO: (240, 640),
        BreedType.GYR_LECHERO: (220, 620),
        BreedType.SINDI: (150, 380),
    }

    # Rangos máximos reales conocidos para cada raza
    real_max_ranges = {
        BreedType.NELORE: 1150,
        BreedType.BRAHMAN: 1100,
        BreedType.GUZERAT: 1000,
        BreedType.SENEPOL: 950,
        BreedType.GIROLANDO: 900,
        BreedType.GYR_LECHERO: 850,
        BreedType.SINDI: 550,
    }

    # Rangos típicos para hembras adultas
    female_ranges = {
        BreedType.NELORE: (380, 520),
        BreedType.BRAHMAN: (390, 540),
        BreedType.GUZERAT: (360, 520),
        BreedType.SENEPOL: (360, 480),
        BreedType.GIROLANDO: (420, 580),
        BreedType.GYR_LECHERO: (380, 520),
        BreedType.SINDI: (260, 380),
    }

    weight_min, weight_max = model_training_ranges.get(breed, (300, 700))
    real_max = real_max_ranges.get(breed, 1000)
    female_min, female_max = female_ranges.get(breed, (300, 500))

    # Calcular posición en el rango del modelo
    range_size = weight_max - weight_min
    position_in_range = (raw_weight - weight_min) / range_size if range_size > 0 else 0

    should_correct = False
    correction_factor = 1.0

    # Caso 1: Peso muy por debajo del mínimo del modelo (< 90% del mínimo)
    if raw_weight < weight_min * 0.9:
        base_factor = real_max / weight_max
        extreme_factor = 1.3 if raw_weight < weight_min * 0.7 else 1.1
        correction_factor = base_factor * extreme_factor
        should_correct = True

    # Caso 2: Peso en el rango muy bajo del modelo (primeros 25% del rango)
    elif position_in_range < 0.25:
        # Para hembras: corrección conservadora
        if gender == "female":
            is_likely_female = (
                female_min * 0.85 <= raw_weight <= female_max * 1.1
            ) and (raw_weight >= weight_min * 1.1)

            if is_likely_female and raw_weight < female_min:
                target_weight = female_min
                distance_to_target = target_weight - raw_weight
                max_distance = female_min - weight_min
                if max_distance > 0:
                    correction_ratio = min(distance_to_target / max_distance, 1.0)
                    correction_factor = 1.1 + (correction_ratio * 0.5)
                else:
                    correction_factor = 1.2
                correction_factor = min(correction_factor, 1.6)
                should_correct = True
        else:
            # Toros: corrección más agresiva
            base_factor = real_max / weight_max
            position_factor = 1.0 + (0.25 - position_in_range) * 2.0
            correction_factor = base_factor * position_factor
            should_correct = True

    # Caso 3: Peso en el rango bajo-medio (25-40% del rango)
    elif position_in_range < 0.4:
        base_factor = (real_max / weight_max) * 0.7
        position_factor = 1.0 + (0.4 - position_in_range) * 0.3
        correction_factor = base_factor * position_factor
        correction_factor = min(correction_factor, 1.5)
        should_correct = True

    # Caso 4: Peso en el rango medio-bajo (40-60% del rango)
    elif position_in_range < 0.6 and (real_max / weight_max) > 1.4:
        base_factor = real_max / weight_max
        position_factor = 1.0 + (0.6 - position_in_range) * 0.2
        correction_factor = base_factor * position_factor * 0.85
        should_correct = True

    # Caso 5: Peso en el rango medio (60-80% del rango) pero subestimado para toro de élite
    elif (
        position_in_range >= 0.6
        and position_in_range < 0.8
        and raw_weight < weight_max * 0.75
        and (real_max / weight_max) > 1.5
    ):
        # Solo aplicar si es macho (toros de élite)
        if gender == "male":
            is_likely_female = female_min * 0.9 <= raw_weight <= female_max * 1.1

            if not is_likely_female:
                target_weight_elite = float(real_max) * 0.85
                distance_to_target = target_weight_elite - raw_weight
                max_possible_distance = float(real_max) - float(weight_min)

                if max_possible_distance > 0:
                    correction_ratio = min(
                        distance_to_target / max_possible_distance, 1.0
                    )
                    base_factor = real_max / weight_max
                    distance_factor = 1.0 + (correction_ratio * 0.3)
                    correction_factor = base_factor * distance_factor
                else:
                    base_factor = real_max / weight_max
                    position_factor = 1.0 + (0.8 - position_in_range) * 0.3
                    correction_factor = base_factor * position_factor * 0.9

                correction_factor = min(correction_factor, 2.8)
                should_correct = True

    if should_correct:
        # Limitar el factor de corrección a un máximo razonable
        correction_factor = min(correction_factor, 3.5)

        # Asegurar que no exceda el máximo real conocido
        max_allowed = real_max * 1.1
        return min(raw_weight * correction_factor, max_allowed)

    # Si el peso está por encima del máximo del modelo pero dentro de lo razonable, aceptarlo
    if raw_weight > weight_max and raw_weight <= real_max:
        return raw_weight

    # Si el peso está por encima del máximo real conocido, limitarlo
    if raw_weight > real_max:
        return real_max

    return raw_weight


def generate_weight_estimations(
    animals: list[AnimalModel],
    weight_loader: WeightDataLoader,
    images_by_breed: dict[str, dict[str, list[str]]],
) -> list[WeightEstimationModel]:
    """
    Genera estimaciones de peso con evolución temporal usando datos del CSV.
    Confianza entre 80-96%.

    Incluye:
    - Variaciones estacionales (época seca vs lluviosa)
    - Curvas de crecimiento realistas según edad
    - Variaciones en confianza según condiciones
    - Eventos de vida (enfermedades, partos, tratamientos)
    - Ajustes por género y estado reproductivo
    - Pérdida de peso aleatoria (10-15% de pesajes)
    - Decline progresivo para animales deceased
    """
    estimations = []
    now = datetime.now(UTC)

    print("\n   ⚖️  Generando estimaciones de peso con datos reales del CSV...")

    for animal in animals:
        end_date = (
            animal.last_updated
            if animal.status in ("deceased", "sold", "culled")
            else now
        )

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

        weighing_dates: list[datetime] = []
        # Primer pesaje entre 30-90 días después del nacimiento
        current_date = animal.birth_date + timedelta(days=random.randint(30, 90))

        # Verificar que hay suficiente tiempo para generar pesajes
        if current_date > end_date:
            # Si el primer pesaje ya excede la fecha de fin, no generar pesajes
            weighing_dates = []
        else:
            # Intervalo entre pesajes: 4-6 meses (120-180 días)
            min_interval_days = 120  # 4 meses
            max_interval_days = 180  # 6 meses

            while current_date <= end_date and len(weighing_dates) < num_weighings:
                weighing_dates.append(current_date)

                # Calcular siguiente pesaje: 4-6 meses después del actual
                interval_days = random.randint(min_interval_days, max_interval_days)
                current_date = current_date + timedelta(days=interval_days)

        weighing_dates.sort()

        # Rastrear el peso máximo alcanzado (para decline en deceased)
        max_weight = 0.0  # Tipo peso máximo: float
        previous_weight = 0.0  # Tipo peso anterior: float

        # Determinar si este animal tendrá decline (deceased o culled)
        has_decline = (
            animal.status in ("deceased", "culled") and len(weighing_dates) > 3
        )
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

            # 1. AJUSTE POR GÉNERO (machos más pesados)
            weight = get_gender_weight_adjustment(animal.gender, base_weight)

            # 2. APLICAR CURVA DE CRECIMIENTO según edad
            growth_factor = get_growth_curve_factor(age_months)
            weight = weight * growth_factor

            # 3. VARIACIONES ESTACIONALES (época seca vs lluviosa)
            seasonal_factor = get_seasonal_weight_factor(
                weighing_date.month, random.random()
            )
            weight = weight * seasonal_factor

            # 4. APLICAR LÓGICA DE PESO según situación
            if has_decline and i >= decline_start_index:
                # DECLINE PROGRESIVO para animales deceased/culled
                decline_factor = 1 - (
                    random.uniform(0.05, 0.15) * (i - decline_start_index + 1)
                )
                weight = max(
                    max_weight * decline_factor, base_weight * 0.5
                )  # No menos del 50% del base
            elif i > 0 and random.random() < 0.12:  # 12% de chance de pérdida de peso
                # PÉRDIDA DE PESO ALEATORIA (realismo)
                loss_factor = random.uniform(0.92, 0.97)
                weight = previous_weight * loss_factor
            # Si no hay decline ni pérdida aleatoria, usar peso calculado con todos los factores

            # 5. SIMULAR EVENTOS DE VIDA (enfermedades, partos, tratamientos)
            if i > 0:  # Solo aplicar eventos después del primer pesaje
                event_weight, event_description = simulate_life_events(
                    animal, weighing_date, age_months, previous_weight
                )
                # Combinar peso calculado con eventos (promedio ponderado)
                weight = (weight * 0.7) + (event_weight * 0.3)

            # 6. APLICAR CORRECCIÓN POST-PROCESAMIENTO (misma lógica que ML)
            # Esto corrige pesos subestimados para toros de élite y hembras
            breed_enum = BreedType(animal.breed)
            weight = apply_weight_correction_for_seeder(
                weight, breed_enum, animal.gender
            )

            # Actualizar tracking
            max_weight = max(max_weight, weight)
            previous_weight = weight

            # 7. VARIACIONES EN CONFIANZA según condiciones
            # Generar hora realista (mayoría en mañana: 6-10 AM)
            if random.random() < 0.70:  # 70% en mañana
                hour = random.randint(6, 10)
            elif random.random() < 0.85:  # 15% en tarde
                hour = random.randint(14, 17)
            else:  # 15% otros horarios
                hour = random.randint(11, 13)

            confidence = get_confidence_by_conditions(hour, random.random())
            # Processing time relacionado con confianza (menor confianza = más tiempo)
            if confidence < 0.85:
                processing_time = random.randint(2000, 2800)
            elif confidence < 0.90:
                processing_time = random.randint(1500, 2200)
            else:
                processing_time = random.randint(1200, 2000)

            # Obtener imagen real para la estimación
            breed_enum = BreedType(animal.breed)
            frame_image_path = get_estimation_frame_path(breed_enum, images_by_breed)

            # Ajustar timestamp con hora realista
            weighing_datetime = weighing_date.replace(
                hour=hour, minute=random.randint(0, 59), second=random.randint(0, 59)
            )

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
                timestamp=weighing_datetime,
                created_at=weighing_datetime,
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
        users = await create_users(roles["admin"], roles["user"], roles["guest"])
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
        print("   Administradores:")
        print("   - Bruno Brito Macedo (Owner/Superusuario)")
        print("   - Miguel Angel Escobar Lazcano (Administrador/Product Owner)")
        print("   Usuarios:")
        print("   - Rodrigo Escobar Morón (Usuario/Scrum Master)")
        print("   - Sara Luz Montero (Usuario - Técnico de Medición)")
        print("   Invitados (Capataces/Asistentes):")
        print("   - Carlos Ferrufino (Invitado - Capataz)")
        print("   - Nelson Farel (Invitado - Capataz)")
        print("   - Andres Saravia (Invitado - Asistente)")
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
        print("   Administradores:")
        print("   - bruno_brito | password123 (Owner/Superusuario)")
        print("   - miguel_escobar | password123 (Administrador)")
        print("   Usuarios:")
        print("   - rodrigo_escobar | password123 (Usuario)")
        print("   - sara_montero | password123 (Técnico de Medición)")
        print("   Invitados (solo lectura):")
        print("   - carlos_ferrufino | password123 (Capataz)")
        print("   - nelson_farel | password123 (Capataz)")
        print("   - andres_saravia | password123 (Asistente)")
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
