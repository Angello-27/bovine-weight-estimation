"""
Data Augmentation con Albumentations 2.0.8
Simula condiciones reales de Hacienda Gamelera
"""

import albumentations as A
from typing import Tuple, List
import numpy as np

def get_training_transform(image_size: Tuple[int, int] = (224, 224)) -> A.Compose:
    """
    Transformaciones de augmentation para entrenamiento.
    Simula condiciones Hacienda Gamelera (luz solar, ángulos, ruido).
    
    Args:
        image_size: Tamaño de imagen de salida (height, width)
    
    Returns:
        A.Compose: Pipeline de augmentation
    """
    return A.Compose([
        # Variaciones de iluminación (condiciones campo)
        A.RandomBrightnessContrast(
            brightness_limit=0.2, 
            contrast_limit=0.2, 
            p=0.7
        ),
        
        # Ruido gaussiano (simula condiciones luz variable)
        A.GaussNoise(var_limit=(10, 50), p=0.3),
        
        # Flip horizontal (simetría bovina)
        A.HorizontalFlip(p=0.5),
        
        # Rotaciones sutiles
        A.Rotate(limit=15, p=0.4),
        
        # Resize y normalización
        A.Resize(image_size[0], image_size[1]),
        A.Normalize(
            mean=[0.485, 0.456, 0.406], 
            std=[0.229, 0.224, 0.225]
        ),
    ])

def get_aggressive_augmentation(image_size: Tuple[int, int] = (224, 224)) -> A.Compose:
    """
    Augmentation agresiva para datasets pequeños (Escenario B/C).
    Aumenta dataset 10-15x.
    """
    return A.Compose([
        # Variaciones de iluminación más agresivas
        A.RandomBrightnessContrast(
            brightness_limit=0.3, 
            contrast_limit=0.3, 
            p=0.7
        ),
        A.HueSaturationValue(
            hue_shift_limit=15, 
            sat_shift_limit=25, 
            p=0.5
        ),
        
        # Ruido y desenfoque
        A.GaussNoise(var_limit=(5, 15), p=0.3),
        A.Blur(blur_limit=3, p=0.25),
        
        # Efectos atmosféricos
        A.RandomShadow(shadow_roi=(0, 0.5, 1, 1), p=0.4),
        A.RandomFog(fog_coef_lower=0.1, fog_coef_upper=0.3, p=0.2),
        
        # Transformaciones geométricas
        A.RandomRotate90(p=0.3),
        A.HorizontalFlip(p=0.5),
        A.ShiftScaleRotate(
            shift_limit=0.1, 
            scale_limit=0.15, 
            rotate_limit=15, 
            border_mode=A.BORDER_REFLECT, 
            p=0.5
        ),
        
        # Augmentation específico ganado
        A.RandomCrop(height=200, width=200, p=0.3),
        A.ElasticTransform(alpha=1, sigma=50, p=0.2),
        A.GridDistortion(num_steps=5, distort_limit=0.3, p=0.2),
        
        # Resize y normalización
        A.Resize(image_size[0], image_size[1]),
        A.Normalize(
            mean=[0.485, 0.456, 0.406], 
            std=[0.229, 0.224, 0.225]
        ),
    ])

def get_validation_transform(image_size: Tuple[int, int] = (224, 224)) -> A.Compose:
    """
    Transformación para validación (sin augmentation agresivo).
    Solo resize y normalización.
    """
    return A.Compose([
        A.Resize(image_size[0], image_size[1]),
        A.Normalize(
            mean=[0.485, 0.456, 0.406], 
            std=[0.229, 0.224, 0.225]
        ),
    ])

def apply_augmentation(image: np.ndarray, transform: A.Compose) -> np.ndarray:
    """
    Aplica transformación de augmentation a una imagen.
    
    Args:
        image: Imagen en formato numpy array (H, W, C)
        transform: Pipeline de augmentation
    
    Returns:
        np.ndarray: Imagen transformada
    """
    augmented = transform(image=image)
    return augmented['image']

