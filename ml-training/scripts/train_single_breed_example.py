#!/usr/bin/env python3
"""
Ejemplo de entrenamiento de un modelo para una raza específica.
Basado en ml-training-standards.md
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from models.cnn_architecture import BreedWeightEstimatorCNN
from models.export.tflite_converter import TFLiteExporter
from models.evaluation.metrics import MetricsCalculator
import tensorflow as tf


def train_single_breed_example():
    """
    Ejemplo de cómo entrenar un modelo para una raza específica.
    Este es un ejemplo simplificado - adaptar según tus datos reales.
    """
    print("\n" + "="*70)
    print("🐄 EJEMPLO: Entrenamiento de Modelo por Raza")
    print("="*70)
    
    # Configuración
    breed_name = 'brahman'
    base_architecture = 'mobilenetv2'  # Más rápido que EfficientNet
    
    # Directorio base
    BASE_DIR = Path(__file__).parent.parent
    MODELS_DIR = BASE_DIR / 'models' / breed_name / 'v1.0.0'
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📋 RAZA: {breed_name.upper()}")
    print(f"🏗️  Arquitectura: {base_architecture}")
    
    # ============================================================
    # 1. CONSTRUIR MODELO
    # ============================================================
    print(f"\n{'='*70}")
    print("1️⃣ CONSTRUIR MODELO")
    print(f"{'='*70}")
    
    model = BreedWeightEstimatorCNN.build_model(
        breed_name=breed_name,
        base_architecture=base_architecture
    )
    
    print(f"✅ Modelo construido: {model.name}")
    print(f"📊 Parámetros: {model.count_params():,}")
    
    # Mostrar arquitectura
    model.summary()
    
    # ============================================================
    # 2. ENTRENAR MODELO (PSEUDO-CÓDIGO)
    # ============================================================
    print(f"\n{'='*70}")
    print("2️⃣ ENTRENAR MODELO")
    print(f"{'='*70}")
    
    print("⚠️  NOTA: Este es código de ejemplo")
    print("📝 Implementar carga de datos real según tu dataset")
    print()
    
    # CÓDIGO DE EJEMPLO (comentado porque no hay datos reales):
    """
    # Configurar callbacks
    callbacks_list = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=10,
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(MODELS_DIR / 'best.h5'),
            monitor='val_loss',
            save_best_only=True
        ),
    ]
    
    # Entrenar
    history = model.fit(
        train_generator,
        epochs=50,
        validation_data=val_generator,
        callbacks=callbacks_list,
        verbose=1
    )
    """
    
    # Por ahora, guardamos modelo sin entrenar
    saved_model_path = MODELS_DIR / 'saved_model'
    model.save(str(saved_model_path))
    print(f"💾 Modelo guardado en: {saved_model_path}")
    
    # ============================================================
    # 3. EVALUAR MODELO (EJEMPLO CON DATOS SIMULADOS)
    # ============================================================
    print(f"\n{'='*70}")
    print("3️⃣ EVALUAR MODELO")
    print(f"{'='*70}")
    
    # Datos simulados para ejemplo
    import numpy as np
    y_true = np.array([450, 500, 380, 420, 600])  # Pesos reales (kg)
    y_pred = np.array([445, 505, 385, 418, 605])  # Pesos predichos (kg)
    
    # Calcular métricas
    metrics = MetricsCalculator.calculate_metrics(
        y_true=y_true,
        y_pred=y_pred,
        breed_type=breed_name
    )
    
    print(f"📊 MÉTRICAS:")
    print(f"   R²:  {metrics.r2_score:.4f}")
    print(f"   MAE: {metrics.mae_kg:.2f} kg")
    print(f"   MAPE: {metrics.mape_percent:.2f}%")
    print(f"   Bias: {metrics.bias_kg:.2f} kg")
    
    # Validar objetivos
    target_r2 = 0.95
    max_mae = 5.0
    
    print(f"\n🎯 VALIDACIÓN:")
    print(f"   R² ≥ {target_r2}: {'✅' if metrics.r2_score >= target_r2 else '❌'}")
    print(f"   MAE < {max_mae} kg: {'✅' if metrics.mae_kg < max_mae else '❌'}")
    
    # ============================================================
    # 4. EXPORTAR A TFLITE
    # ============================================================
    print(f"\n{'='*70}")
    print("4️⃣ EXPORTAR A TFLITE")
    print(f"{'='*70}")
    
    tflite_path = MODELS_DIR / f"{breed_name}-v1.0.0.tflite"
    
    try:
        size_bytes = TFLiteExporter.convert_to_tflite(
            saved_model_path=str(saved_model_path),
            output_path=str(tflite_path),
            optimization='default'  # FP16
        )
        
        print(f"✅ TFLite exportado: {tflite_path}")
        print(f"📏 Tamaño: {size_bytes / 1024:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error exportando: {e}")
        return
    
    # ============================================================
    # 5. GUARDAR MÉTRICAS
    # ============================================================
    import json
    
    metrics_data = {
        'breed_type': breed_name,
        'version': 'v1.0.0',
        'metrics': metrics.to_dict()
    }
    
    metrics_path = MODELS_DIR / 'metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics_data, f, indent=2)
    
    print(f"💾 Métricas guardadas: {metrics_path}")
    
    print(f"\n{'='*70}")
    print("✅ EJEMPLO COMPLETADO")
    print(f"{'='*70}")


if __name__ == '__main__':
    train_single_breed_example()

