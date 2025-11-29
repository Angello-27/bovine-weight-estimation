"""
Script para descargar modelo TFLite desde Google Drive

Uso:
    python scripts/download_model_from_drive.py --file-id FILE_ID --output ml_models/

Requisitos:
    pip install gdown
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


def download_model_from_drive(
    file_id: str, output_dir: str, filename: str | None = None
):
    """
    Descarga un modelo TFLite desde Google Drive.

    Args:
        file_id: ID del archivo en Google Drive
        output_dir: Directorio de salida
        filename: Nombre del archivo (opcional)
    """
    # Crear directorio si no existe
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Construir URL de descarga
    url = f"https://drive.google.com/uc?id={file_id}"

    # Nombre del archivo
    if filename is None:
        filename = "generic-cattle-v1.0.0.tflite"

    output_file = output_path / filename

    print("📥 Descargando modelo desde Google Drive...")
    print(f"   File ID: {file_id}")
    print(f"   Output: {output_file}")

    try:
        # Descargar archivo
        gdown.download(url, str(output_file), quiet=False)

        if output_file.exists():
            file_size = output_file.stat().st_size / (1024 * 1024)  # MB
            print("✅ Modelo descargado exitosamente")
            print(f"   Tamaño: {file_size:.2f} MB")
            print(f"   Ubicación: {output_file.absolute()}")
        else:
            print("❌ Error: El archivo no se descargó correctamente")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error al descargar modelo: {e}")
        print("\n💡 Consejos:")
        print("   1. Verifica que el archivo esté compartido públicamente o con acceso")
        print("   2. Verifica que el FILE_ID sea correcto")
        print("   3. Intenta descargar manualmente desde Drive")
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
        default="ml_models",
        help="Directorio de salida (default: ml_models)",
    )
    parser.add_argument(
        "--filename",
        type=str,
        default=None,
        help="Nombre del archivo (default: generic-cattle-v1.0.0.tflite)",
    )

    args = parser.parse_args()

    download_model_from_drive(args.file_id, args.output, args.filename)


if __name__ == "__main__":
    main()
