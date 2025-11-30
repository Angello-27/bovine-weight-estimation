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

try:
    import requests  # type: ignore
except ImportError:
    requests = None  # type: ignore

# Agregar path del backend para importar settings
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from app.core.config import settings
except ImportError:
    print("⚠️  No se pudo importar settings, usando valores por defecto")
    settings = None  # type: ignore


def download_model_from_drive(
    file_id: str | None = None,
    output_dir: str | None = None,
    filename: str | None = None,
):
    """
    Descarga un modelo TFLite desde Google Drive.

    Args:
        file_id: ID del archivo en Google Drive (opcional, usa ML_MODEL_FILE_ID de settings si no se proporciona)
        output_dir: Directorio de salida (opcional, usa settings si no se proporciona)
        filename: Nombre del archivo (opcional, usa settings si no se proporciona)
    """
    # Usar configuración del proyecto si está disponible
    if settings is not None:
        # Usar FILE_ID de settings si no se proporciona
        file_id_from_env = None
        if file_id is None:
            file_id = settings.ML_MODEL_FILE_ID
            file_id_from_env = True
        output_path = (
            Path(settings.ML_MODELS_PATH) if output_dir is None else Path(output_dir)
        )
        model_filename = settings.ML_DEFAULT_MODEL if filename is None else filename
        print("📋 Usando configuración del proyecto:")
        print(f"   ML_MODELS_PATH: {settings.ML_MODELS_PATH}")
        print(f"   ML_DEFAULT_MODEL: {settings.ML_DEFAULT_MODEL}")
        if file_id_from_env:
            print(f"   ML_MODEL_FILE_ID: {file_id} (desde .env)")
        else:
            print(f"   ML_MODEL_FILE_ID: {file_id} (proporcionado)")
    else:
        output_path = Path(output_dir or "ml_models")
        model_filename = filename or "generic-cattle-v1.0.0.tflite"
        # Si no hay settings y no se proporciona file_id, mostrar error
        if file_id is None:
            print(
                "❌ Error: No se proporcionó FILE_ID y no se pudo obtener de configuración"
            )
            print("   Usa: --file-id FILE_ID o configura ML_MODEL_FILE_ID en .env")
            sys.exit(1)

    # Validar que tenemos file_id
    if file_id is None:
        print("❌ Error: No se proporcionó FILE_ID")
        print("   Usa: --file-id FILE_ID o configura ML_MODEL_FILE_ID en .env")
        sys.exit(1)

    # Crear directorio si no existe
    output_path.mkdir(parents=True, exist_ok=True)

    output_file = output_path / model_filename

    print("\n📥 Descargando modelo desde Google Drive...")
    print(f"   File ID: {file_id}")
    print(f"   Output: {output_file}")

    try:
        # Método 1: Intentar con gdown (puede fallar con algunos archivos)
        url = f"https://drive.google.com/uc?id={file_id}"
        print(f"   URL: {url}")

        try:
            # Intentar descarga con fuzzy=True para manejar archivos grandes
            gdown.download(url, str(output_file), quiet=False, fuzzy=True)

            # Verificar que el archivo se descargó correctamente
            if output_file.exists():
                file_size = output_file.stat().st_size
                # Si el archivo es muy pequeño (< 1KB), probablemente es un error HTML
                if file_size < 1024:
                    output_file.unlink()  # Eliminar archivo pequeño
                    raise Exception(
                        f"El archivo descargado es muy pequeño ({file_size} bytes). "
                        "Verifica que el archivo esté compartido públicamente."
                    )
        except Exception as gdown_error:
            # Si gdown falla, intentar con requests directamente
            if requests is None:
                raise gdown_error

            print("   ⚠️ gdown falló, intentando método alternativo con requests...")

            # Método alternativo: Descargar directamente usando requests
            # Primero obtener el link de descarga real
            share_url = f"https://drive.google.com/uc?export=download&id={file_id}"

            # Hacer request con sesión para manejar cookies
            session = requests.Session()
            response = session.get(share_url, stream=True, allow_redirects=True)

            # Si Google Drive muestra página de confirmación (archivos grandes)
            # Buscar el link de descarga real en la respuesta
            if (
                "virus scan warning" in response.text.lower()
                or "confirm" in response.text.lower()
            ):
                # Extraer el link de confirmación
                import re

                confirm_match = re.search(
                    r'href="(/uc\?export=download[^"]+)', response.text
                )
                if confirm_match:
                    confirm_url = "https://drive.google.com" + confirm_match.group(1)
                    response = session.get(confirm_url, stream=True)

            # Verificar que la respuesta es exitosa
            response.raise_for_status()

            # Descargar archivo en chunks
            total_size = 0
            with open(output_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        total_size += len(chunk)

            if total_size < 1024:
                output_file.unlink()
                raise Exception(
                    f"El archivo descargado es muy pequeño ({total_size} bytes). "
                    "Verifica que el archivo esté compartido públicamente."
                )

            print(
                f"   ✅ Descargado {total_size / (1024*1024):.2f} MB usando método alternativo"
            )

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
        error_msg = str(e)
        print(f"❌ Error al descargar modelo: {error_msg}")

        # Intentar método alternativo si el primero falló
        if "groups" in error_msg.lower() or "none" in error_msg.lower():
            print("\n🔄 Intentando método alternativo de descarga...")
            try:
                # Método alternativo: usar formato de link compartido
                share_url = (
                    f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
                )
                gdown.download(share_url, str(output_file), quiet=False, fuzzy=True)

                if output_file.exists() and output_file.stat().st_size > 1024:
                    file_size = output_file.stat().st_size / (1024 * 1024)  # MB
                    print("\n✅ Modelo descargado exitosamente (método alternativo)")
                    print(f"   Tamaño: {file_size:.2f} MB")
                    print(f"   Ubicación: {output_file.absolute()}")
                    print("\n💡 El modelo está listo para usar en el backend.")
                    print(
                        f"   El sistema cargará automáticamente el modelo desde: {output_path.absolute()}"
                    )
                    return
            except Exception as e2:
                print(f"   ❌ Método alternativo también falló: {e2}")

        print("\n💡 Consejos para resolver el problema:")
        print(
            "   1. Verifica que el archivo esté compartido con 'Cualquiera con el enlace'"
        )
        print(
            "   2. Abre el link en el navegador para verificar que el archivo sea accesible:"
        )
        print(f"      https://drive.google.com/file/d/{file_id}/view?usp=sharing")
        print("   3. Verifica que el FILE_ID sea correcto")
        print("   4. Intenta descargar manualmente desde Drive y copiar a ml_models/")
        print("   5. Verifica que tengas conexión a internet estable")
        print("\n📝 Si el problema persiste, puedes descargar manualmente:")
        print(f"   - Abre: https://drive.google.com/file/d/{file_id}/view?usp=sharing")
        print(f"   - Descarga el archivo")
        print(f"   - Copia a: {output_file.absolute()}")
        sys.exit(1)


def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="Descarga modelo TFLite desde Google Drive"
    )
    parser.add_argument(
        "--file-id",
        type=str,
        required=False,
        default=None,
        help="ID del archivo en Google Drive (opcional, usa ML_MODEL_FILE_ID de .env si no se proporciona)",
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
