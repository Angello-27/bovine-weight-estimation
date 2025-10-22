#!/usr/bin/env python3
"""
Script de Prueba - Sistema Híbrido de Estimación de Peso
Demuestra el funcionamiento del estimador híbrido

Uso:
    python scripts/test_hybrid_system.py --image foto_vaca.jpg --breed brahman
"""

import argparse
import sys
from pathlib import Path

# Agregar el directorio backend al path
sys.path.append(str(Path(__file__).parent.parent))

from app.core.constants import BreedType
from app.ml.hybrid_estimator import HybridWeightEstimator


def test_hybrid_system(image_path: str, breed: str) -> None:
    """
    Prueba el sistema híbrido con una imagen.
    
    Args:
        image_path: Ruta a la imagen
        breed: Raza del animal
    """
    print(f"🧪 Probando Sistema Híbrido de Estimación de Peso")
    print(f"📸 Imagen: {image_path}")
    print(f"🐄 Raza: {breed}")
    print("-" * 50)
    
    try:
        # Validar que la imagen existe
        if not Path(image_path).exists():
            print(f"❌ Error: Imagen no encontrada: {image_path}")
            return
        
        # Validar raza
        try:
            breed_enum = BreedType(breed.lower())
        except ValueError:
            print(f"❌ Error: Raza inválida '{breed}'")
            print(f"Razas válidas: {[b.value for b in BreedType]}")
            return
        
        # Cargar imagen
        print("📥 Cargando imagen...")
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        print(f"✅ Imagen cargada: {len(image_bytes)} bytes")
        
        # Inicializar estimador híbrido
        print("🤖 Inicializando estimador híbrido...")
        estimator = HybridWeightEstimator()
        
        print("🔍 Ejecutando detección YOLO + estimación morfométrica...")
        
        # Ejecutar estimación
        result = estimator.estimate_weight(image_bytes, breed_enum)
        
        # Mostrar resultados
        print("\n" + "="*50)
        print("📊 RESULTADOS DE ESTIMACIÓN")
        print("="*50)
        print(f"🐄 Raza: {breed_enum.value}")
        print(f"⚖️  Peso estimado: {result['weight']} kg")
        print(f"🎯 Confianza: {result['confidence']:.1%}")
        print(f"🔧 Método: {result['method']}")
        print(f"📐 Calidad detección: {result['detection_quality']}")
        print(f"📏 Área normalizada: {result['normalized_area']:.3f}")
        print(f"🎯 Confianza YOLO: {result['detection_confidence']:.2f}")
        print(f"📏 Penalización tamaño: {result['size_penalty']:.2f}")
        
        # Mostrar bounding box
        bbox = result['bbox']
        print(f"📦 Bounding box: ({bbox[0]}, {bbox[1]}) → ({bbox[2]}, {bbox[3]})")
        
        # Interpretación de confianza
        confidence = result['confidence']
        if confidence >= 0.90:
            print("🟢 Alta confianza - Estimación muy confiable")
        elif confidence >= 0.80:
            print("🟡 Confianza media - Estimación aceptable")
        else:
            print("🔴 Baja confianza - Considerar nueva foto")
        
        # Mostrar coeficientes usados
        print("\n" + "="*50)
        print("🔧 COEFICIENTES UTILIZADOS")
        print("="*50)
        breed_coeffs = estimator.get_breed_coefficients()[breed_enum.value]
        print(f"📈 Coeficiente 'a': {breed_coeffs['a']:.3f}")
        print(f"📈 Coeficiente 'b': {breed_coeffs['b']:.1f}")
        print(f"📏 Peso mínimo: {breed_coeffs['min']} kg")
        print(f"📏 Peso máximo: {breed_coeffs['max']} kg")
        
        print("\n✅ Prueba completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()


def test_all_breeds(image_path: str) -> None:
    """
    Prueba el sistema con todas las razas.
    
    Args:
        image_path: Ruta a la imagen
    """
    print(f"🧪 Probando Sistema Híbrido con Todas las Razas")
    print(f"📸 Imagen: {image_path}")
    print("="*60)
    
    try:
        # Cargar imagen una sola vez
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        estimator = HybridWeightEstimator()
        
        # Probar con cada raza
        for breed in BreedType:
            print(f"\n🐄 Probando raza: {breed.value}")
            print("-" * 30)
            
            try:
                result = estimator.estimate_weight(image_bytes, breed)
                print(f"⚖️  Peso: {result['weight']} kg")
                print(f"🎯 Confianza: {result['confidence']:.1%}")
                print(f"📐 Calidad: {result['detection_quality']}")
                
            except Exception as e:
                print(f"❌ Error con {breed.value}: {e}")
        
        print("\n✅ Prueba con todas las razas completada!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(description='Probar sistema híbrido')
    parser.add_argument('--image', required=True,
                       help='Ruta a la imagen del bovino')
    parser.add_argument('--breed', 
                       choices=[b.value for b in BreedType],
                       help='Raza específica a probar')
    parser.add_argument('--all-breeds', action='store_true',
                       help='Probar con todas las razas')
    
    args = parser.parse_args()
    
    if args.all_breeds:
        test_all_breeds(args.image)
    elif args.breed:
        test_hybrid_system(args.image, args.breed)
    else:
        print("❌ Error: Especificar --breed o --all-breeds")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
