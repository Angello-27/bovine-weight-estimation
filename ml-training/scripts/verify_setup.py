#!/usr/bin/env python3
"""
Script de verificación del setup del proyecto.
Verifica que todos los componentes estén correctamente configurados.
"""

import sys
from pathlib import Path

# Agregar src al path
SRC_DIR = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(SRC_DIR))

def check_init_files() -> tuple[bool, list]:
    """Verifica que todos los __init__.py existan."""
    required_init_files = [
        'src/__init__.py',
        'src/data/__init__.py',
        'src/models/__init__.py',
        'src/models/evaluation/__init__.py',
        'src/models/export/__init__.py',
        'src/models/training/__init__.py',
        'src/utils/__init__.py',
        'src/features/__init__.py',
    ]
    
    base_dir = Path(__file__).parent.parent
    missing = []
    
    for file_path in required_init_files:
        full_path = base_dir / file_path
        if not full_path.exists():
            missing.append(file_path)
    
    success = len(missing) == 0
    return success, missing


def check_imports() -> tuple[bool, str]:
    """Verifica que todos los imports funcionen."""
    errors = []
    
    try:
        from data.augmentation import get_training_transform
    except Exception as e:
        errors.append(f"data.augmentation: {e}")
    
    try:
        from models.cnn_architecture import BreedWeightEstimatorCNN, BREED_CONFIGS
    except Exception as e:
        errors.append(f"models.cnn_architecture: {e}")
    
    try:
        from models.evaluation.metrics import MetricsCalculator
    except Exception as e:
        errors.append(f"models.evaluation.metrics: {e}")
    
    try:
        from models.export.tflite_converter import TFLiteExporter
    except Exception as e:
        errors.append(f"models.export.tflite_converter: {e}")
    
    try:
        from data.data_loader import CattleDataGenerator
    except Exception as e:
        errors.append(f"data.data_loader: {e}")
    
    success = len(errors) == 0
    error_msg = '\n'.join(errors) if errors else ''
    return success, error_msg


def check_breed_configs() -> tuple[bool, int]:
    """Verifica que haya 8 razas configuradas."""
    try:
        from models.cnn_architecture import BREED_CONFIGS
        num_breeds = len(BREED_CONFIGS)
        expected = 8
        success = num_breeds == expected
        return success, num_breeds
    except Exception as e:
        return False, 0


def check_metrics() -> tuple[bool, str]:
    """Verifica que las métricas sean realistas."""
    try:
        from models.cnn_architecture import BreedModelConfig
        
        # Crear instancia de prueba
        config = BreedModelConfig('test', (200.0, 800.0))
        
        issues = []
        if config.target_r2 > 0.90:
            issues.append(f"target_r2={config.target_r2} es demasiado optimista (esperado ≤0.90)")
        
        if config.target_mae_kg < 10:
            issues.append(f"target_mae_kg={config.target_mae_kg} es demasiado optimista (esperado ≥10)")
        
        success = len(issues) == 0
        error_msg = '\n'.join(issues) if issues else ''
        return success, error_msg
        
    except Exception as e:
        return False, str(e)


def check_directory_structure() -> tuple[bool, list]:
    """Verifica estructura de directorios."""
    base_dir = Path(__file__).parent.parent
    required_dirs = [
        'src',
        'src/data',
        'src/models',
        'src/models/evaluation',
        'src/models/export',
        'src/models/training',
        'src/utils',
        'src/features',
        'scripts',
        'config',
    ]
    
    missing = []
    for dir_path in required_dirs:
        if not (base_dir / dir_path).exists():
            missing.append(dir_path)
    
    success = len(missing) == 0
    return success, missing


def check_requirements() -> bool:
    """Verifica que requirements.txt exista."""
    base_dir = Path(__file__).parent.parent
    requirements_file = base_dir / 'requirements.txt'
    return requirements_file.exists()


def main():
    """Ejecuta todas las verificaciones."""
    print("🔍 VERIFICACIÓN DE SETUP DEL PROYECTO")
    print("=" * 60)
    
    checks = []
    
    # 1. Archivos __init__.py
    print("\n1️⃣ Verificando archivos __init__.py...")
    success, missing = check_init_files()
    if success:
        print("   ✅ Todos los __init__.py existen")
    else:
        print(f"   ❌ Faltan: {missing}")
    checks.append(success)
    
    # 2. Imports
    print("\n2️⃣ Verificando imports...")
    success, error_msg = check_imports()
    if success:
        print("   ✅ Todos los imports funcionan")
    else:
        print(f"   ❌ Errores:\n{error_msg}")
    checks.append(success)
    
    # 3. Configuración de razas
    print("\n3️⃣ Verificando configuración de razas...")
    success, num_breeds = check_breed_configs()
    if success:
        print(f"   ✅ {num_breeds} razas configuradas correctamente")
    else:
        print(f"   ❌ Configuradas {num_breeds} razas (esperado 8)")
    checks.append(success)
    
    # 4. Métricas realistas
    print("\n4️⃣ Verificando métricas realistas...")
    success, error_msg = check_metrics()
    if success:
        print("   ✅ Métricas configuradas correctamente")
    else:
        print(f"   ⚠️ Avisos:\n{error_msg}")
    checks.append(success)
    
    # 5. Estructura de directorios
    print("\n5️⃣ Verificando estructura de directorios...")
    success, missing = check_directory_structure()
    if success:
        print("   ✅ Estructura correcta")
    else:
        print(f"   ❌ Faltan directorios: {missing}")
    checks.append(success)
    
    # 6. Requirements.txt
    print("\n6️⃣ Verificando requirements.txt...")
    success = check_requirements()
    if success:
        print("   ✅ requirements.txt existe")
    else:
        print("   ❌ requirements.txt no existe")
    checks.append(success)
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN")
    print("=" * 60)
    
    passed = sum(checks)
    total = len(checks)
    
    print(f"✅ Checks pasados: {passed}/{total}")
    print(f"❌ Checks fallidos: {total - passed}/{total}")
    
    if all(checks):
        print("\n🎉 ¡SETUP COMPLETO Y VERIFICADO!")
        return 0
    else:
        print("\n⚠️ HAY PROBLEMAS QUE RESOLVER")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

