"""
Script de Calibración para Estimador Híbrido
Calibra coeficientes por raza usando fotos reales con peso conocido

Uso:
    python scripts/calibrate_hybrid.py --breed brahman --photos_dir ./photos/brahman
"""

import argparse
import json
import os
from pathlib import Path
from typing import List, Tuple

import numpy as np
from scipy.optimize import minimize

from app.core.constants import BreedType
from app.ml.hybrid_estimator import HybridWeightEstimator


def load_photo_weight_pairs(photos_dir: str) -> List[Tuple[str, float]]:
    """
    Carga pares (ruta_foto, peso_real) desde directorio.
    
    Formato esperado:
    - Fotos: *.jpg, *.jpeg, *.png
    - Pesos: archivo weights.json con {"foto.jpg": 450.5, ...}
    
    Args:
        photos_dir: Directorio con fotos y weights.json
        
    Returns:
        Lista de tuplas (ruta_foto, peso_kg)
    """
    photos_path = Path(photos_dir)
    weights_file = photos_path / "weights.json"
    
    if not weights_file.exists():
        raise FileNotFoundError(f"No se encontró {weights_file}")
    
    # Cargar pesos desde JSON
    with open(weights_file, 'r') as f:
        weights_data = json.load(f)
    
    # Crear pares (foto, peso)
    pairs = []
    for filename, weight_kg in weights_data.items():
        photo_path = photos_path / filename
        if photo_path.exists():
            pairs.append((str(photo_path), weight_kg))
        else:
            print(f"⚠️ Foto no encontrada: {filename}")
    
    print(f"📸 Cargados {len(pairs)} pares foto-peso")
    return pairs


def estimate_with_params(image_bytes: bytes, a: float, b: float, 
                        breed: BreedType) -> float:
    """
    Estima peso usando parámetros específicos (para optimización).
    
    Args:
        image_bytes: Bytes de imagen
        a: Coeficiente lineal
        b: Coeficiente constante
        breed: Raza del animal
        
    Returns:
        Peso estimado en kg
    """
    estimator = HybridWeightEstimator()
    
    # Temporalmente actualizar parámetros
    original_params = estimator.breed_params[breed].copy()
    estimator.breed_params[breed] = {
        'a': a, 'b': b, 
        'min': original_params['min'], 
        'max': original_params['max']
    }
    
    try:
        result = estimator.estimate_weight(image_bytes, breed)
        return result['weight']
    finally:
        # Restaurar parámetros originales
        estimator.breed_params[breed] = original_params


def calibrate_breed(breed: BreedType, photo_weight_pairs: List[Tuple[str, float]]) -> dict:
    """
    Calibra coeficientes para una raza específica.
    
    Args:
        breed: Raza a calibrar
        photo_weight_pairs: Lista de (ruta_foto, peso_real)
        
    Returns:
        Dict con mejores parámetros y métricas
    """
    print(f"\n🔧 Calibrando raza: {breed.value}")
    print(f"📊 Usando {len(photo_weight_pairs)} fotos")
    
    def error_function(params):
        """Función de error para minimizar (MAE)."""
        a, b = params
        predictions = []
        actuals = []
        
        for photo_path, real_weight in photo_weight_pairs:
            try:
                with open(photo_path, 'rb') as f:
                    img_bytes = f.read()
                
                estimated = estimate_with_params(img_bytes, a, b, breed)
                predictions.append(estimated)
                actuals.append(real_weight)
                
            except Exception as e:
                print(f"⚠️ Error procesando {photo_path}: {e}")
                continue
        
        if not predictions:
            return float('inf')
        
        # Calcular MAE (Mean Absolute Error)
        mae = np.mean(np.abs(np.array(predictions) - np.array(actuals)))
        return mae
    
    # Parámetros iniciales (valores por defecto)
    initial_params = [0.50, 150]
    
    # Límites de búsqueda
    bounds = [
        (0.3, 0.7),    # Coeficiente 'a'
        (100, 200)     # Coeficiente 'b'
    ]
    
    # Optimizar usando scipy
    print("🔍 Optimizando parámetros...")
    result = minimize(
        error_function, 
        x0=initial_params,
        bounds=bounds,
        method='L-BFGS-B'
    )
    
    if not result.success:
        print(f"❌ Optimización falló: {result.message}")
        return None
    
    best_a, best_b = result.x
    mae = result.fun
    
    # Calcular métricas adicionales
    predictions = []
    actuals = []
    
    for photo_path, real_weight in photo_weight_pairs:
        try:
            with open(photo_path, 'rb') as f:
                img_bytes = f.read()
            
            estimated = estimate_with_params(img_bytes, best_a, best_b, breed)
            predictions.append(estimated)
            actuals.append(real_weight)
            
        except Exception:
            continue
    
    if predictions:
        # R² (coeficiente de determinación)
        ss_res = np.sum((np.array(actuals) - np.array(predictions)) ** 2)
        ss_tot = np.sum((np.array(actuals) - np.mean(actuals)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # RMSE (Root Mean Square Error)
        rmse = np.sqrt(np.mean((np.array(predictions) - np.array(actuals)) ** 2))
        
        print(f"✅ Calibración completada:")
        print(f"   📈 Mejor 'a': {best_a:.3f}")
        print(f"   📈 Mejor 'b': {best_b:.1f}")
        print(f"   📊 MAE: {mae:.1f} kg")
        print(f"   📊 RMSE: {rmse:.1f} kg")
        print(f"   📊 R²: {r_squared:.3f}")
        
        return {
            'breed': breed.value,
            'a': best_a,
            'b': best_b,
            'mae': mae,
            'rmse': rmse,
            'r_squared': r_squared,
            'samples': len(predictions)
        }
    
    return None


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(description='Calibrar estimador híbrido')
    parser.add_argument('--breed', required=True, 
                       choices=[b.value for b in BreedType],
                       help='Raza a calibrar')
    parser.add_argument('--photos_dir', required=True,
                       help='Directorio con fotos y weights.json')
    parser.add_argument('--output', default='calibration_results.json',
                       help='Archivo de salida con resultados')
    
    args = parser.parse_args()
    
    try:
        # Cargar datos
        photo_weight_pairs = load_photo_weight_pairs(args.photos_dir)
        
        if len(photo_weight_pairs) < 5:
            print(f"⚠️ Pocas fotos ({len(photo_weight_pairs)}). Se recomiendan al menos 10-15.")
        
        # Calibrar
        breed = BreedType(args.breed)
        results = calibrate_breed(breed, photo_weight_pairs)
        
        if results:
            # Guardar resultados
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            
            print(f"\n💾 Resultados guardados en: {args.output}")
            
            # Mostrar código para actualizar
            print(f"\n🔧 Código para actualizar HybridWeightEstimator:")
            print(f"estimator.update_breed_coefficients(")
            print(f"    BreedType.{breed.value.upper()},")
            print(f"    a={results['a']:.3f},")
            print(f"    b={results['b']:.1f},")
            print(f"    min_weight=200,  # Ajustar según raza")
            print(f"    max_weight=800   # Ajustar según raza")
            print(f")")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
