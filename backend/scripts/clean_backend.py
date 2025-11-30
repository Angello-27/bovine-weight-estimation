"""
Script de Limpieza del Backend

Elimina archivos y directorios temporales, caches y el entorno virtual
para empezar con un entorno limpio.

Uso:
    python scripts/clean_backend.py

⚠️  ADVERTENCIA: Este script elimina:
- venv/ (entorno virtual)
- __pycache__/ (caché de Python)
- logs/ (archivos de logs)
- .pytest_cache/, .mypy_cache/, .ruff_cache/ (cachés de herramientas)
- uploads/ (archivos subidos temporalmente)
- Archivos .pyc, .pyo
- Archivos temporales (*.tmp, *.swp, etc.)
"""

import os
import shutil
import sys
from pathlib import Path


def remove_directory(path: Path, description: str) -> bool:
    """Elimina un directorio si existe."""
    if path.exists() and path.is_dir():
        try:
            shutil.rmtree(path)
            print(f"   ✅ Eliminado: {description}")
            return True
        except Exception as e:
            print(f"   ❌ Error al eliminar {description}: {e}")
            return False
    return False


def remove_file(path: Path, description: str) -> bool:
    """Elimina un archivo si existe."""
    if path.exists() and path.is_file():
        try:
            path.unlink()
            print(f"   ✅ Eliminado: {description}")
            return True
        except Exception as e:
            print(f"   ❌ Error al eliminar {description}: {e}")
            return False
    return False


def find_and_remove_patterns(root_dir: Path, patterns: list[str]) -> int:
    """Busca y elimina archivos/directorios que coinciden con patrones."""
    removed_count = 0
    for pattern in patterns:
        for path in root_dir.rglob(pattern):
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                    removed_count += 1
                elif path.is_file():
                    path.unlink()
                    removed_count += 1
            except Exception as e:
                print(f"   ⚠️  No se pudo eliminar {path}: {e}")
    return removed_count


def clean_backend():
    """Función principal de limpieza."""
    print("=" * 70)
    print("🧹 Limpieza del Backend - Preparando entorno limpio")
    print("=" * 70)
    print()

    # Directorio raíz del backend
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    print(f"📁 Directorio: {backend_dir}")
    print()

    removed_items = []

    # 1. Eliminar entorno virtual
    print("🗑️  Eliminando entorno virtual...")
    venv_path = backend_dir / "venv"
    if remove_directory(venv_path, "venv/ (entorno virtual)"):
        removed_items.append("venv/")

    # 2. Eliminar directorios de caché y temporales
    print("\n🗑️  Eliminando directorios de caché y temporales...")
    directories_to_remove = [
        (backend_dir / "logs", "logs/ (archivos de logs)"),
        (backend_dir / ".pytest_cache", ".pytest_cache/ (caché de pytest)"),
        (backend_dir / ".mypy_cache", ".mypy_cache/ (caché de mypy)"),
        (backend_dir / ".ruff_cache", ".ruff_cache/ (caché de ruff)"),
        (backend_dir / "uploads", "uploads/ (archivos subidos temporalmente)"),
    ]

    for dir_path, description in directories_to_remove:
        remove_directory(dir_path, description)
        if dir_path.exists():
            removed_items.append(str(dir_path.relative_to(backend_dir)))

    # 3. Eliminar archivos temporales y modelos descargados (opcional)
    print("\n🗑️  Eliminando archivos temporales...")
    files_to_remove = [
        (backend_dir / "yolov8n.pt", "yolov8n.pt (modelo YOLO descargado)"),
        (backend_dir / ".coverage", ".coverage (cobertura de tests)"),
        (backend_dir / "coverage.xml", "coverage.xml (reporte de cobertura)"),
    ]

    for file_path, description in files_to_remove:
        remove_file(file_path, description)
        if file_path.exists():
            removed_items.append(str(file_path.relative_to(backend_dir)))

    # 4. Buscar y eliminar __pycache__ en todo el proyecto
    print("\n🗑️  Eliminando directorios __pycache__...")
    pycache_count = find_and_remove_patterns(backend_dir, ["__pycache__"])
    if pycache_count > 0:
        print(f"   ✅ Eliminados {pycache_count} directorios __pycache__")
        removed_items.append(f"{pycache_count} directorios __pycache__")

    # 5. Eliminar archivos .pyc, .pyo
    print("\n🗑️  Eliminando archivos compilados (.pyc, .pyo)...")
    compiled_count = find_and_remove_patterns(backend_dir, ["*.pyc", "*.pyo"])
    if compiled_count > 0:
        print(f"   ✅ Eliminados {compiled_count} archivos compilados")
        removed_items.append(f"{compiled_count} archivos .pyc/.pyo")

    # 6. Eliminar archivos temporales del editor
    print("\n🗑️  Eliminando archivos temporales de editores...")
    temp_count = find_and_remove_patterns(
        backend_dir, ["*.tmp", "*.swp", "*.swo", "*~", ".DS_Store"]
    )
    if temp_count > 0:
        print(f"   ✅ Eliminados {temp_count} archivos temporales")
        removed_items.append(f"{temp_count} archivos temporales")

    # Resumen
    print("\n" + "=" * 70)
    print("✅ Limpieza completada")
    print("=" * 70)
    print("\n📝 Items eliminados:")
    if removed_items:
        for item in removed_items:
            print(f"   - {item}")
    else:
        print("   (No había nada que limpiar)")

    print("\n📝 NOTAS:")
    print("   - ml_models/ se mantiene (puede contener modelos necesarios)")
    print("   - .env debe estar presente para configuración")
    print("   - Archivos de código fuente no fueron modificados")
    print("\n🚀 Próximos pasos:")
    print("   1. Crear nuevo entorno virtual: python3 -m venv venv")
    print("   2. Activar entorno: source venv/bin/activate")
    print("   3. Instalar dependencias: pip install -r requirements.txt")
    print("   4. Configurar .env con tus variables")
    print("   5. Ejecutar setup: python scripts/setup_production.py")
    print("=" * 70)


if __name__ == "__main__":
    try:
        clean_backend()
    except KeyboardInterrupt:
        print("\n\n⚠️  Limpieza cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error durante la limpieza: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
