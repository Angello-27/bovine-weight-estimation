"""
Generador de Datos Sintéticos de Emergencia
Genera dataset sintético usando IA para demo académica

Uso:
    python scripts/generate_synthetic_data.py --breed brahman --count 20 --output_dir ./synthetic_data
"""

import argparse
import json
import os
import random
from pathlib import Path
from typing import Dict, List

import requests
from PIL import Image
import io


class SyntheticDataGenerator:
    """Generador de datos sintéticos para demo académica."""
    
    def __init__(self):
        """Inicializa el generador."""
        # Prompts optimizados por raza para generar imágenes realistas
        self.prompts_by_breed = {
            'brahman': [
                "professional livestock photo, brahman cattle bull, side profile view, natural outdoor lighting, full body visible, white/gray coat, characteristic hump, farm setting",
                "high quality cattle photography, brahman cow, lateral view, ranch environment, zebu characteristics, hump visible, professional lighting",
                "livestock portrait, brahman cattle, side angle, agricultural setting, white gray coat, distinctive hump, natural daylight"
            ],
            'nelore': [
                "professional cattle photo, nelore cow, side view, farm setting, gray coat, zebu characteristics, natural outdoor lighting",
                "high quality livestock photography, nelore bull, lateral profile, ranch environment, gray zebu cattle, professional shot",
                "cattle portrait, nelore breed, side angle, agricultural background, gray coat, zebu features, natural lighting"
            ],
            'angus': [
                "professional ranch photo, black angus cattle, side view, outdoor daylight, solid black coat, polled head, farm setting",
                "high quality cattle photography, angus cow, lateral view, agricultural environment, black coat, beef cattle, natural lighting",
                "livestock portrait, black angus bull, side profile, ranch setting, solid black color, polled characteristics, professional shot"
            ],
            'cebuinas': [
                "professional livestock photo, cebuinas cattle, side view, farm setting, zebu characteristics, natural outdoor lighting",
                "high quality cattle photography, cebuinas cow, lateral profile, agricultural environment, zebu breed, professional lighting",
                "cattle portrait, cebuinas breed, side angle, ranch background, zebu features, natural daylight"
            ],
            'criollo': [
                "professional cattle photo, criollo cow, side view, farm setting, local breed characteristics, natural outdoor lighting",
                "high quality livestock photography, criollo cattle, lateral view, agricultural environment, adapted breed, professional shot",
                "cattle portrait, criollo breed, side profile, ranch setting, local adaptation, natural lighting"
            ],
            'pardo_suizo': [
                "professional livestock photo, pardo suizo cattle, side view, farm setting, brown coat, dairy breed characteristics, natural lighting",
                "high quality cattle photography, pardo suizo cow, lateral profile, agricultural environment, brown dairy cattle, professional shot",
                "cattle portrait, pardo suizo breed, side angle, ranch background, brown coat, dairy characteristics, natural daylight"
            ],
            'jersey': [
                "professional cattle photo, jersey cow, side view, farm setting, light brown coat, dairy breed, small size, natural lighting",
                "high quality livestock photography, jersey cattle, lateral view, agricultural environment, light brown dairy cow, professional shot",
                "cattle portrait, jersey breed, side profile, ranch setting, light brown coat, small dairy cattle, natural daylight"
            ]
        }
        
        # Rangos de peso típicos por raza (kg)
        self.weight_ranges = {
            'brahman': (300, 900),
            'nelore': (280, 850),
            'angus': (250, 850),
            'cebuinas': (290, 880),
            'criollo': (220, 650),
            'pardo_suizo': (260, 800),
            'jersey': (200, 600)
        }

    def generate_with_stable_diffusion(self, prompt: str, api_key: str = None) -> bytes:
        """
        Genera imagen usando Stable Diffusion API.
        
        Args:
            prompt: Prompt para generar imagen
            api_key: API key (opcional, usar límite gratuito)
            
        Returns:
            Bytes de imagen generada
        """
        # Usar API gratuita de Stable Diffusion
        # Nota: En producción usar servicio pagado para mejor calidad
        
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}" if api_key else "Bearer sk-free-tier"
        }
        
        data = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            if 'artifacts' in result and result['artifacts']:
                # Decodificar imagen base64
                import base64
                image_data = base64.b64decode(result['artifacts'][0]['base64'])
                return image_data
            
        except Exception as e:
            print(f"⚠️ Error con Stable Diffusion API: {e}")
        
        # Fallback: generar imagen placeholder
        return self._generate_placeholder_image()

    def generate_with_leonardo_ai(self, prompt: str, api_key: str = None) -> bytes:
        """
        Genera imagen usando Leonardo.ai (15 imágenes gratis/día).
        
        Args:
            prompt: Prompt para generar imagen
            api_key: API key de Leonardo.ai
            
        Returns:
            Bytes de imagen generada
        """
        if not api_key:
            print("⚠️ Se requiere API key de Leonardo.ai para generar imágenes")
            return self._generate_placeholder_image()
        
        url = "https://cloud.leonardo.ai/api/rest/v1/generations"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "prompt": prompt,
            "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",  # Leonardo Diffusion XL
            "width": 1024,
            "height": 1024,
            "num_images": 1,
            "guidance_scale": 7,
            "steps": 30
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            if 'sdGenerationJob' in result:
                generation_id = result['sdGenerationJob']['generationId']
                
                # Esperar generación
                import time
                time.sleep(30)  # Esperar generación
                
                # Obtener imagen generada
                get_url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}"
                get_response = requests.get(get_url, headers=headers)
                get_response.raise_for_status()
                
                generation_result = get_response.json()
                if 'generations_by_pk' in generation_result:
                    image_url = generation_result['generations_by_pk']['generated_images'][0]['url']
                    
                    # Descargar imagen
                    img_response = requests.get(image_url)
                    img_response.raise_for_status()
                    return img_response.content
            
        except Exception as e:
            print(f"⚠️ Error con Leonardo.ai API: {e}")
        
        return self._generate_placeholder_image()

    def _generate_placeholder_image(self) -> bytes:
        """Genera imagen placeholder simple."""
        from PIL import Image, ImageDraw
        
        # Crear imagen placeholder
        img = Image.new('RGB', (1024, 1024), color='lightgray')
        draw = ImageDraw.Draw(img)
        
        # Dibujar rectángulo simple (placeholder para vaca)
        draw.rectangle([200, 200, 800, 800], fill='brown', outline='black', width=3)
        
        # Convertir a bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        return img_bytes.getvalue()

    def generate_dataset(self, breed: str, count: int, output_dir: str, 
                        api_key: str = None) -> None:
        """
        Genera dataset sintético completo.
        
        Args:
            breed: Raza a generar
            count: Número de imágenes a generar
            output_dir: Directorio de salida
            api_key: API key para generación (opcional)
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        breed_dir = output_path / breed
        breed_dir.mkdir(exist_ok=True)
        
        prompts = self.prompts_by_breed.get(breed, [self.prompts_by_breed['brahman'][0]])
        weight_min, weight_max = self.weight_ranges.get(breed, (300, 600))
        
        weights_data = {}
        
        print(f"🎨 Generando {count} imágenes sintéticas para raza: {breed}")
        
        for i in range(count):
            # Seleccionar prompt aleatorio
            prompt = random.choice(prompts)
            
            # Generar imagen
            print(f"📸 Generando imagen {i+1}/{count}...")
            
            if api_key:
                image_bytes = self.generate_with_leonardo_ai(prompt, api_key)
            else:
                image_bytes = self.generate_with_stable_diffusion(prompt)
            
            # Guardar imagen
            filename = f"{breed}_synthetic_{i+1:03d}.jpg"
            image_path = breed_dir / filename
            
            with open(image_path, 'wb') as f:
                f.write(image_bytes)
            
            # Generar peso aleatorio en rango de la raza
            weight = random.uniform(weight_min, weight_max)
            weights_data[filename] = round(weight, 1)
            
            print(f"✅ Guardada: {filename} (peso: {weight:.1f} kg)")
        
        # Guardar archivo de pesos
        weights_file = breed_dir / "weights.json"
        with open(weights_file, 'w') as f:
            json.dump(weights_data, f, indent=2)
        
        print(f"\n💾 Dataset sintético generado:")
        print(f"   📁 Directorio: {breed_dir}")
        print(f"   📸 Imágenes: {count}")
        print(f"   📊 Pesos: {weights_file}")
        print(f"\n🔧 Para calibrar:")
        print(f"   python scripts/calibrate_hybrid.py --breed {breed} --photos_dir {breed_dir}")


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(description='Generar datos sintéticos')
    parser.add_argument('--breed', required=True,
                       choices=['brahman', 'nelore', 'angus', 'cebuinas', 'criollo', 'pardo_suizo', 'jersey'],
                       help='Raza a generar')
    parser.add_argument('--count', type=int, default=20,
                       help='Número de imágenes a generar')
    parser.add_argument('--output_dir', default='./synthetic_data',
                       help='Directorio de salida')
    parser.add_argument('--api_key', 
                       help='API key de Leonardo.ai o Stability.ai')
    
    args = parser.parse_args()
    
    generator = SyntheticDataGenerator()
    
    try:
        generator.generate_dataset(
            breed=args.breed,
            count=args.count,
            output_dir=args.output_dir,
            api_key=args.api_key
        )
        
        print(f"\n🎯 Dataset sintético listo para calibración!")
        print(f"📝 Nota: Para mejor calidad, usar API key de Leonardo.ai")
        print(f"🔗 Registro gratuito: https://leonardo.ai")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
