"""
Script de Setup para Producción/Cloud

Prepara el backend para deployment en la nube:
- Verifica dependencias
- Crea directorios necesarios
- Valida configuración
- Prepara modelos ML

Uso:
    python scripts/setup_production.py
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings  # noqa: E402


def check_dependencies():
    """Verifica que todas las dependencias estén instaladas."""
    print("🔍 Verificando dependencias...")

    # Mapeo de nombres de paquetes pip a nombres de módulos Python
    required_packages = {
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "motor": "motor",
        "beanie": "beanie",
        "pydantic": "pydantic",
        "python-jose": "jose",  # El paquete se llama python-jose pero el módulo es jose
        "passlib": "passlib",
    }

    missing = []
    for package_name, module_name in required_packages.items():
        try:
            __import__(module_name)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - FALTA")
            missing.append(package_name)

    # Verificar tensorflow-lite-runtime (opcional pero recomendado)
    try:
        import tflite_runtime.interpreter as tflite  # type: ignore  # noqa: F401

        print("   ✅ tensorflow-lite-runtime")
    except ImportError:
        print("   ⚠️  tensorflow-lite-runtime - No instalado (opcional)")

    if missing:
        print(f"\n❌ Faltan dependencias: {', '.join(missing)}")
        print("   Instala con: pip install -r requirements.txt")
        return False

    print("✅ Todas las dependencias están instaladas\n")
    return True


def create_directories():
    """Crea directorios necesarios."""
    print("📁 Creando directorios necesarios...")

    directories = [
        "ml_models",
        "logs",
        "uploads",
    ]

    for dir_name in directories:
        dir_path = Path(dir_name)
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {dir_name}/")

    print("✅ Directorios creados\n")


def check_ml_models(download_if_missing: bool = False):
    """
    Verifica modelos ML.

    Args:
        download_if_missing: Si True, intenta descargar el modelo si no existe
    """
    print("🤖 Verificando modelos ML...")

    models_path = Path(settings.ML_MODELS_PATH)
    default_model = models_path / settings.ML_DEFAULT_MODEL

    if default_model.exists():
        file_size_mb = float(default_model.stat().st_size) / (1024 * 1024)  # MB
        print(f"   ✅ Modelo encontrado: {settings.ML_DEFAULT_MODEL}")
        print(f"      Tamaño: {file_size_mb:.2f} MB")
    else:
        print(f"   ⚠️  Modelo no encontrado: {default_model}")

        if download_if_missing:
            print("   📥 Intentando descargar modelo desde Google Drive...")
            try:
                from scripts.download_model_from_drive import download_model_from_drive

                download_model_from_drive()
                if default_model.exists():
                    file_size_mb = float(default_model.stat().st_size) / (1024 * 1024)
                    print(f"   ✅ Modelo descargado: {file_size_mb:.2f} MB")
                else:
                    print("   ❌ No se pudo descargar el modelo automáticamente")
                    print(
                        "      Ejecuta manualmente: python scripts/download_model_from_drive.py"
                    )
            except Exception as e:
                print(f"   ❌ Error al descargar: {e}")
                print(
                    "      Ejecuta manualmente: python scripts/download_model_from_drive.py"
                )
        else:
            print("      Descarga el modelo desde Colab/Drive")
            print("      Ejecuta: python scripts/download_model_from_drive.py")
            print("      Ver guía: backend/INTEGRATION_GUIDE.md")

    print()


def validate_config():
    """Valida configuración crítica."""
    print("⚙️  Validando configuración...")

    issues = []

    # Verificar MongoDB URL
    if (
        settings.MONGODB_URL == "mongodb://localhost:27017"
        and settings.ENVIRONMENT == "production"
    ):
        issues.append("⚠️  MONGODB_URL está en localhost (cambiar en producción)")

    # Verificar Secret Key
    if (
        settings.SECRET_KEY == "CHANGE_THIS_IN_PRODUCTION_USE_ENV_FILE"
        and settings.ENVIRONMENT == "production"
    ):
        issues.append("❌ SECRET_KEY no configurado (CRÍTICO en producción)")

    # Verificar CORS
    if "*" in settings.CORS_ORIGINS and settings.ENVIRONMENT == "production":
        issues.append("⚠️  CORS permite todos los orígenes (restringir en producción)")

    if issues:
        print("   Problemas encontrados:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("   ✅ Configuración válida")

    print()


def main():
    """Función principal."""
    import argparse

    parser = argparse.ArgumentParser(description="Setup de producción para el backend")
    parser.add_argument(
        "--download-model",
        action="store_true",
        help="Descargar modelo TFLite automáticamente si no existe",
    )
    args = parser.parse_args()

    print("=" * 70)
    print("🚀 Setup de Producción - Backend FastAPI")
    print("=" * 70)
    print()

    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)

    # Crear directorios
    create_directories()

    # Verificar modelos ML (con opción de descarga automática)
    check_ml_models(download_if_missing=args.download_model)

    # Validar configuración
    validate_config()

    print("=" * 70)
    print("✅ Setup completado")
    print()
    print("📝 Próximos pasos:")
    print("   1. Configurar variables de entorno (.env)")
    if not (Path(settings.ML_MODELS_PATH) / settings.ML_DEFAULT_MODEL).exists():
        print("   2. Descargar modelo TFLite:")
        print("      python scripts/download_model_from_drive.py")
        print(
            "      O ejecutar setup con: python scripts/setup_production.py --download-model"
        )
    print("   3. Ejecutar: python -m app.main")
    print("=" * 70)


if __name__ == "__main__":
    main()
