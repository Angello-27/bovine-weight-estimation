"""
Arquitecturas CNN para estimación de peso bovino.
Transfer Learning con modelos pre-entrenados ImageNet.
"""

from dataclasses import dataclass
from typing import Tuple, Optional
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2, EfficientNetB1


@dataclass
class BreedModelConfig:
    """Configuración de modelo por raza"""
    breed_type: str
    expected_weight_range_kg: Tuple[float, float]
    target_r2: float = 0.85  # Realista para proyecto académico
    target_mae_kg: float = 22.0  # Realista según literatura 2023-2024


class BreedWeightEstimatorCNN:
    """
    CNN con transfer learning MobileNetV2 para estimación de peso.
    
    Arquitectura:
    - MobileNetV2 (frozen, ImageNet) 
    - GlobalAvgPooling2D
    - Dense(256, relu) + Dropout(0.3)
    - Dense(128, relu) + Dropout(0.2)
    - Dense(1, linear) → Peso kg
    """
    
    @staticmethod
    def build_model(
        breed_name: str,
        input_shape: Tuple[int, int, int] = (224, 224, 3),
        base_architecture: str = 'mobilenetv2'
    ) -> keras.Model:
        """
        Construir modelo para estimación de peso por raza.
        
        Args:
            breed_name: Nombre de la raza
            input_shape: Forma de entrada (height, width, channels)
            base_architecture: 'mobilenetv2' o 'efficientnetb1'
        
        Returns:
            keras.Model: Modelo compilado
        """
        # Seleccionar base model
        if base_architecture == 'mobilenetv2':
            base = MobileNetV2(
                input_shape=input_shape,
                include_top=False,
                weights='imagenet',
            )
        elif base_architecture == 'efficientnetb1':
            base = EfficientNetB1(
                input_shape=input_shape,
                include_top=False,
                weights='imagenet',
            )
        else:
            raise ValueError(f"Arquitectura no soportada: {base_architecture}")
        
        # Congelar capas base (transfer learning)
        base.trainable = False
        
        # Preprocessing específico del modelo base
        inputs = keras.Input(shape=input_shape)
        
        if base_architecture == 'mobilenetv2':
            x = keras.applications.mobilenet_v2.preprocess_input(inputs)
        else:  # efficientnetb1
            x = keras.applications.efficientnet.preprocess_input(inputs)
        
        x = base(x, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        
        # Custom head para regresión
        x = layers.Dense(256, activation='relu', name='dense_1')(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(128, activation='relu', name='dense_2')(x)
        x = layers.Dropout(0.2)(x)
        
        # Salida: peso en kg
        outputs = layers.Dense(1, activation='linear', name='weight_output')(x)
        
        # Crear modelo
        model = keras.Model(inputs, outputs, name=f"{breed_name}_estimator")
        
        # Compilar
        model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae', 'mse'],
        )
        
        return model
    
    @staticmethod
    def build_generic_model(
        input_shape: Tuple[int, int, int] = (224, 224, 3),
        base_architecture: str = 'efficientnetb1'
    ) -> keras.Model:
        """
        Construir modelo genérico multi-raza.
        Usado en Fase 1 del entrenamiento.
        """
        return BreedWeightEstimatorCNN.build_model(
            breed_name='generic_cattle',
            input_shape=input_shape,
            base_architecture=base_architecture
        )
    
    @staticmethod
    def unfreeze_for_finetuning(
        model: keras.Model,
        n_layers_to_unfreeze: int = 3
    ) -> keras.Model:
        """
        Descongelar últimas capas para fine-tuning.
        
        Args:
            model: Modelo pre-entrenado
            n_layers_to_unfreeze: Número de capas base a descongelar
        
        Returns:
            keras.Model: Modelo listo para fine-tuning
        """
        base_layers = [
            layer for layer in model.layers 
            if layer.name in ['mobilenetv2_1.00_224', 'efficientnetb1']
        ]
        
        if not base_layers:
            raise ValueError("No se encontraron capas base para fine-tuning")
        
        base_model = base_layers[0]
        base_model.trainable = True
        
        # Descongelar últimas n capas
        for layer in base_model.layers[:-n_layers_to_unfreeze]:
            layer.trainable = False
        
        # Re-compilar con learning rate bajo para fine-tuning
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=1e-5),
            loss='mse',
            metrics=['mae', 'mse'],
        )
        
        print(f"✅ {n_layers_to_unfreeze} capas descongeladas para fine-tuning")
        
        return model


# Configuraciones por raza (7 razas tropicales priorizadas - alineadas con entrenamiento)
BREED_CONFIGS = {
    'nelore': BreedModelConfig(
        breed_type='nelore',
        expected_weight_range_kg=(250.0, 650.0),  # novillo: 250-380, vaca: 380-520, toro: 480-650
    ),
    'brahman': BreedModelConfig(
        breed_type='brahman',
        expected_weight_range_kg=(260.0, 680.0),  # novillo: 260-400, vaca: 390-540, toro: 500-680
    ),
    'guzerat': BreedModelConfig(
        breed_type='guzerat',
        expected_weight_range_kg=(240.0, 650.0),  # novillo: 240-360, vaca: 360-520, toro: 480-650
    ),
    'senepol': BreedModelConfig(
        breed_type='senepol',
        expected_weight_range_kg=(280.0, 620.0),  # novillo: 280-400, vaca: 360-480, toro: 500-620
    ),
    'girolando': BreedModelConfig(
        breed_type='girolando',
        expected_weight_range_kg=(240.0, 640.0),  # novilla: 240-340, vaca: 420-580, toro: 500-640
    ),
    'gyr_lechero': BreedModelConfig(
        breed_type='gyr_lechero',
        expected_weight_range_kg=(220.0, 620.0),  # novilla: 220-320, vaca: 380-520, toro: 470-620
    ),
    'sindi': BreedModelConfig(
        breed_type='sindi',
        expected_weight_range_kg=(150.0, 380.0),  # novilla: 150-230, vaca: 260-380
    ),
}

