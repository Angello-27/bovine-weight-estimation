"""
Seed Data Script - Cargar datos iniciales en MongoDB

Ejecutar: python -m scripts.seed_data

Carga datos de ejemplo para desarrollo y testing con TRAZABILIDAD COMPLETA:
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
from uuid import UUID

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings
from app.core.constants import AgeCategory
from app.core.constants import BreedType
from app.models import AnimalModel
from app.models import WeightEstimationModel


# ID de la hacienda (usar el mismo para todos los animales)
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
    BreedType.NELORE: 84,      # 42% de 200
    BreedType.BRAHMAN: 50,     # 25% de 200
    BreedType.GUZERAT: 30,     # 15% de 200
    BreedType.SENEPOL: 16,     # 8% de 200
    BreedType.GIROLANDO: 10,   # 5% de 200
    BreedType.GYR_LECHERO: 6,  # 3% de 200
    BreedType.SINDI: 4,        # 2% de 200
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


def generate_animals() -> list[AnimalModel]:
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
            birth_weight_kg=round(
                random.uniform(*BIRTH_WEIGHTS[breed]), 1
            ),
            status="active",
            farm_id=FARM_ID,
            registration_date=birth_date + timedelta(days=random.randint(1, 30)),
            last_updated=now - timedelta(days=random.randint(0, 30)),
            photo_url=IMAGE_REFERENCES.get(breed.value),
            observations=f"Animal base para reproducción. Raza {BreedType.get_display_name(breed)}.",
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
            birth_date = datetime(year, 1, 1) + timedelta(
                days=random.randint(0, 364)
            )

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
                name=f"{BreedType.get_display_name(breed)} {ear_tag_counter}",
                color=random.choice(BREED_COLORS[breed]),
                birth_weight_kg=round(
                    random.uniform(*BIRTH_WEIGHTS[breed]), 1
                ),
                mother_id=mother_id,
                father_id=father_id,
                status=status,
                farm_id=FARM_ID,
                registration_date=birth_date + timedelta(days=random.randint(1, 30)),
                last_updated=last_updated,
                photo_url=IMAGE_REFERENCES.get(breed.value),
                observations=f"Animal de raza {BreedType.get_display_name(breed)}. "
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
        birth_weight = animal.birth_weight_kg or random.uniform(
            *BIRTH_WEIGHTS[breed]
        )

        # Generar pesajes distribuidos a lo largo de la vida del animal
        weighing_dates = []
        start_date = animal.birth_date + timedelta(days=random.randint(30, 90))

        if (end_date - start_date).days < 30:
            # Si el período es muy corto, solo un pesaje
            weighing_dates = [start_date + timedelta(days=random.randint(0, (end_date - start_date).days))]
        else:
            # Distribuir pesajes uniformemente
            days_span = (end_date - start_date).days
            interval = days_span / max(num_weighings, 1)
            for i in range(num_weighings):
                date = start_date + timedelta(days=int(i * interval) + random.randint(-7, 7))
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
                AnimalModel,
                WeightEstimationModel,
            ],
        )
        print("✅ Conectado a MongoDB\n")

        # Limpiar datos existentes
        print("🗑️  Limpiando datos existentes...")
        await AnimalModel.delete_all()
        await WeightEstimationModel.delete_all()
        print("✅ Datos limpiados\n")

        # Generar animales
        print("🐄 Generando 200 animales con trazabilidad completa...")
        animals = generate_animals()
        print(f"   📝 {len(animals)} animales generados")

        # Insertar animales
        await AnimalModel.insert_many(animals)
        print(f"✅ {len(animals)} animales insertados en MongoDB\n")

        # Generar estimaciones de peso con evolución temporal
        print("⚖️  Generando estimaciones de peso con evolución temporal...")
        estimations = generate_weight_estimations(animals)
        print(f"   📝 {len(estimations)} estimaciones generadas")

        # Insertar estimaciones
        await WeightEstimationModel.insert_many(estimations)
        print(f"✅ {len(estimations)} estimaciones insertadas en MongoDB\n")

        # Resumen detallado
        print("=" * 70)
        print("📊 RESUMEN DE DATOS CARGADOS - TRAZABILIDAD COMPLETA")
        print("=" * 70)
        print(f"🐄 Animales totales: {len(animals)}")
        print(f"⚖️  Estimaciones totales: {len(estimations)}")
        print(f"📈 Promedio de pesajes por animal: {len(estimations) / len(animals):.1f}")
        print(f"🏢 Hacienda ID: {FARM_ID}\n")

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
        animals_with_parents = sum(
            1 for a in animals if a.mother_id or a.father_id
        )
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
        print("\n📸 NOTA: Las referencias a imágenes están en IMAGE_REFERENCES")
        print("   Descarga las imágenes de Drive y actualiza los IDs en el script.")
        print("\n🔍 TRAZABILIDAD:")
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
