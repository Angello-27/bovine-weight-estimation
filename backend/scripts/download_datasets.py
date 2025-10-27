#!/usr/bin/env python3
"""
Download Datasets Script - Descarga datasets críticos para entrenamiento ML
Sprint 1: Setup Infraestructura ML + Datasets

Objetivo: Descargar datasets críticos para entrenamiento de modelos ML
- CID Dataset (17,899 imgs con peso) - PRIORIDAD #1
- Kaggle Cattle Weight (12k imgs)
- Roboflow Cow Weight (390 imgs)
"""

import os
import sys
import subprocess
import requests
import zipfile
from pathlib import Path
from typing import Dict, List

# Configuración de datasets
DATASETS_CONFIG = {
    "cid_dataset": {
        "name": "CID Dataset",
        "description": "17,899 imágenes con peso - PRIORIDAD #1",
        "url": "https://www.kaggle.com/datasets/cattle-weight-estimation/cid-dataset",
        "size": "~2.5GB",
        "priority": 1
    },
    "kaggle_cattle_weight": {
        "name": "Kaggle Cattle Weight",
        "description": "12,000 imágenes con peso",
        "url": "https://www.kaggle.com/datasets/cattle-weight-estimation/kaggle-cattle-weight",
        "size": "~1.8GB",
        "priority": 2
    },
    "roboflow_cow_weight": {
        "name": "Roboflow Cow Weight",
        "description": "390 imágenes con peso",
        "url": "https://universe.roboflow.com/cow-weight-estimation/cow-weight-estimation",
        "size": "~150MB",
        "priority": 3
    }
}

# Directorios
BASE_DIR = Path(__file__).parent.parent
ML_TRAINING_DIR = BASE_DIR.parent / "ml-training"
DATASETS_DIR = ML_TRAINING_DIR / "datasets"
RAW_DATA_DIR = DATASETS_DIR / "raw"
PROCESSED_DATA_DIR = DATASETS_DIR / "processed"

def setup_directories():
    """Crea directorios necesarios para datasets."""
    print("📁 Creando directorios para datasets...")
    
    directories = [DATASETS_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ Directorio creado: {directory}")
    
    # Crear subdirectorios por dataset
    for dataset_name in DATASETS_CONFIG.keys():
        dataset_dir = RAW_DATA_DIR / dataset_name
        dataset_dir.mkdir(exist_ok=True)
        print(f"✅ Directorio dataset: {dataset_dir}")

def check_kaggle_credentials():
    """Verifica que las credenciales de Kaggle estén configuradas."""
    print("🔑 Verificando credenciales de Kaggle...")
    
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_key = kaggle_dir / "kaggle.json"
    
    if not kaggle_key.exists():
        print("❌ Error: Archivo kaggle.json no encontrado")
        print("📋 Instrucciones:")
        print("1. Ve a https://www.kaggle.com/settings")
        print("2. Crea una nueva API token")
        print("3. Descarga kaggle.json")
        print("4. Colócalo en ~/.kaggle/kaggle.json")
        print("5. Ejecuta: chmod 600 ~/.kaggle/kaggle.json")
        return False
    
    print("✅ Credenciales de Kaggle encontradas")
    return True

def download_kaggle_dataset(dataset_name: str, dataset_config: Dict) -> bool:
    """Descarga dataset de Kaggle."""
    print(f"📥 Descargando {dataset_config['name']}...")
    
    try:
        # Comando para descargar dataset
        cmd = [
            "kaggle", "datasets", "download",
            "-d", dataset_name,
            "-p", str(RAW_DATA_DIR / dataset_name),
            "--unzip"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {dataset_config['name']} descargado exitosamente")
            return True
        else:
            print(f"❌ Error descargando {dataset_config['name']}: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error descargando {dataset_config['name']}: {e}")
        return False

def download_roboflow_dataset(dataset_config: Dict) -> bool:
    """Descarga dataset de Roboflow."""
    print(f"📥 Descargando {dataset_config['name']}...")
    
    try:
        # Para Roboflow necesitamos usar su API
        # Por ahora, creamos un placeholder
        dataset_dir = RAW_DATA_DIR / "roboflow_cow_weight"
        placeholder_file = dataset_dir / "README.md"
        
        with open(placeholder_file, "w") as f:
            f.write(f"# {dataset_config['name']}\n\n")
            f.write(f"**Descripción**: {dataset_config['description']}\n")
            f.write(f"**URL**: {dataset_config['url']}\n")
            f.write(f"**Tamaño**: {dataset_config['size']}\n\n")
            f.write("**Instrucciones de descarga**:\n")
            f.write("1. Ve a la URL del dataset\n")
            f.write("2. Descarga el dataset en formato YOLO\n")
            f.write("3. Extrae los archivos en este directorio\n")
        
        print(f"✅ Placeholder creado para {dataset_config['name']}")
        return True
        
    except Exception as e:
        print(f"❌ Error creando placeholder para {dataset_config['name']}: {e}")
        return False

def create_dataset_summary():
    """Crea resumen de datasets descargados."""
    print("📊 Creando resumen de datasets...")
    
    summary_file = DATASETS_DIR / "DATASETS_SUMMARY.md"
    
    with open(summary_file, "w") as f:
        f.write("# 📊 Resumen de Datasets - Sprint 1\n\n")
        f.write("**Proyecto**: Sistema de Estimación de Peso Bovino\n")
        f.write("**Hacienda**: Hacienda Gamelera - Bruno Brito Macedo\n")
        f.write("**Fecha**: Octubre 2024\n\n")
        
        f.write("## 🎯 Datasets Objetivo\n\n")
        f.write("| Dataset | Descripción | Tamaño | Prioridad | Estado |\n")
        f.write("|---------|-------------|--------|-----------|--------|\n")
        
        for dataset_name, config in DATASETS_CONFIG.items():
            dataset_dir = RAW_DATA_DIR / dataset_name
            status = "✅ Descargado" if dataset_dir.exists() and any(dataset_dir.iterdir()) else "⏳ Pendiente"
            
            f.write(f"| {config['name']} | {config['description']} | {config['size']} | {config['priority']} | {status} |\n")
        
        f.write("\n## 📁 Estructura de Directorios\n\n")
        f.write("```\n")
        f.write("ml-training/\n")
        f.write("├── datasets/\n")
        f.write("│   ├── raw/\n")
        f.write("│   │   ├── cid_dataset/\n")
        f.write("│   │   ├── kaggle_cattle_weight/\n")
        f.write("│   │   └── roboflow_cow_weight/\n")
        f.write("│   └── processed/\n")
        f.write("└── notebooks/\n")
        f.write("    └── colab_setup_ml.ipynb\n")
        f.write("```\n")
        
        f.write("\n## 🚀 Próximos Pasos\n\n")
        f.write("1. **Día 4**: Análisis Exploratorio de Datos (EDA)\n")
        f.write("2. **Día 5-6**: Preparar pipeline de datos optimizado\n")
        f.write("3. **Sprint 2**: Entrenamiento de modelos ML\n")
    
    print(f"✅ Resumen creado: {summary_file}")

def main():
    """Función principal para descargar datasets."""
    print("🐄 Sistema de Estimación de Peso Bovino - Descarga de Datasets")
    print("=" * 60)
    
    # 1. Crear directorios
    setup_directories()
    
    # 2. Verificar credenciales de Kaggle
    if not check_kaggle_credentials():
        print("\n⚠️ No se pueden descargar datasets de Kaggle sin credenciales")
        print("📋 Continuando con setup de directorios...")
    
    # 3. Descargar datasets (si las credenciales están disponibles)
    if check_kaggle_credentials():
        print("\n📥 Iniciando descarga de datasets...")
        
        # Ordenar por prioridad
        sorted_datasets = sorted(
            DATASETS_CONFIG.items(),
            key=lambda x: x[1]["priority"]
        )
        
        for dataset_name, dataset_config in sorted_datasets:
            if dataset_name == "roboflow_cow_weight":
                download_roboflow_dataset(dataset_config)
            else:
                download_kaggle_dataset(dataset_name, dataset_config)
    
    # 4. Crear resumen
    create_dataset_summary()
    
    print("\n🎉 Setup de datasets completado!")
    print(f"📁 Directorios creados en: {DATASETS_DIR}")
    print("📋 Revisa DATASETS_SUMMARY.md para más detalles")

if __name__ == "__main__":
    main()
