"""
Script para descargar modelo TFLite desde Google Drive

Uso:
    python scripts/download_model_from_drive.py --file-id FILE_ID

Requisitos:
    pip install gdown

El script usa la configuración del proyecto (settings.ML_MODELS_PATH y ML_DEFAULT_MODEL)
para descargar el modelo en la ubicación correcta.
"""

import argparse
import sys
from pathlib import Path

try:
    import gdown  # type: ignore
except ImportError:
    print("❌ Error: gdown no está instalado")
    print("   Instala con: pip install gdown")
    sys.exit(1)

# Agregar path del backend para importar settings
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from app.core.config import settings
except ImportError:
    print("⚠️  No se pudo importar settings, usando valores por defecto")
    settings = None  # type: ignore


def download_model_from_drive(
    file_id: str, output_dir: str | None = None, filename: str | None = None
):
    """
    Descarga un modelo TFLite desde Google Drive.

    Args:
        file_id: ID del archivo en Google Drive
        output_dir: Directorio de salida (opcional, usa settings si no se proporciona)
        filename: Nombre del archivo (opcional, usa settings si no se proporciona)
    """
    # Usar configuración del proyecto si está disponible
    if settings is not None:
        output_path = (
            Path(settings.ML_MODELS_PATH) if output_dir is None else Path(output_dir)
        )
        model_filename = settings.ML_DEFAULT_MODEL if filename is None else filename
        print("📋 Usando configuración del proyecto:")
        print(f"   ML_MODELS_PATH: {settings.ML_MODELS_PATH}")
        print(f"   ML_DEFAULT_MODEL: {settings.ML_DEFAULT_MODEL}")
    else:
        output_path = Path(output_dir or "ml_models")
        model_filename = filename or "generic-cattle-v1.0.0.tflite"

    # Crear directorio si no existe
    output_path.mkdir(parents=True, exist_ok=True)

    # Construir URL de descarga
    url = f"https://drive.google.com/uc?id={file_id}"

    output_file = output_path / model_filename

    print("\n📥 Descargando modelo desde Google Drive...")
    print(f"   File ID: {file_id}")
    print(f"   Output: {output_file}")

    try:
        # Descargar archivo
        gdown.download(url, str(output_file), quiet=False)

        if output_file.exists():
            file_size = output_file.stat().st_size / (1024 * 1024)  # MB
            print("\n✅ Modelo descargado exitosamente")
            print(f"   Tamaño: {file_size:.2f} MB")
            print(f"   Ubicación: {output_file.absolute()}")
            print("\n💡 El modelo está listo para usar en el backend.")
            print(
                f"   El sistema cargará automáticamente el modelo desde: {output_path.absolute()}"
            )
        else:
            print("❌ Error: El archivo no se descargó correctamente")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error al descargar modelo: {e}")
        print("\n💡 Consejos:")
        print("   1. Verifica que el archivo esté compartido públicamente o con acceso")
        print("   2. Verifica que el FILE_ID sea correcto")
        print("   3. Extrae el FILE_ID del link compartido:")
        print("      https://drive.google.com/file/d/FILE_ID_AQUI/view?usp=sharing")
        print("   4. Intenta descargar manualmente desde Drive")
        sys.exit(1)


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="Descarga modelo TFLite desde Google Drive"
    )
    parser.add_argument(
        "--file-id",
        type=str,
        required=True,
        help="ID del archivo en Google Drive (extraer del link compartido)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Directorio de salida (default: usa ML_MODELS_PATH de settings)",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default=None,
        help="Nombre del archivo (default: usa ML_DEFAULT_MODEL de settings)",
    )

    args = parser.parse_args()

    download_model_from_drive(args.file_id, args.output, args.filename)


if __name__ == "__main__":
    main()
