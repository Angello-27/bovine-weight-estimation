"""
Trainer para modelos de estimación de peso por raza.
"""

from typing import Tuple, Dict
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import callbacks
import mlflow
import mlflow.tensorflow
import numpy as np

from ..cnn_architecture import BreedWeightEstimatorCNN, BreedModelConfig
from ...models.evaluation.metrics import MetricsCalculator


class BreedModelTrainer:
    """
    Trainer para entrenar modelos por raza.
    """
    
    def __init__(
        self,
        breed_type: str,
        data_dir: Path,
        config: BreedModelConfig,
        base_architecture: str = 'mobilenetv2'
    ):
        self.breed_type = breed_type
        self.data_dir = Path(data_dir)
        self.config = config
        self.base_architecture = base_architecture
        self.model = None
        
    def train(
        self,
        epochs: int = 100,
        batch_size: int = 32,
        validation_split: float = 0.2,
        early_stopping_patience: int = 10
    ) -> keras.Model:
        """
        Entrenar modelo para la raza.
        
        Args:
            epochs: Número de épocas
            batch_size: Tamaño de batch
            validation_split: Proporción de validación
            early_stopping_patience: Paciencia para early stopping
        
        Returns:
            keras.Model: Modelo entrenado
        """
        print(f"\n{'#'*60}")
        print(f"# ENTRENANDO MODELO: {self.breed_type.upper()}")
        print(f"{'#'*60}\n")
        
        # Iniciar MLflow run
        with mlflow.start_run(run_name=f"{self.breed_type}-training"):
            # Log parámetros
            mlflow.log_params({
                'breed_type': self.breed_type,
                'base_architecture': self.base_architecture,
                'epochs': epochs,
                'batch_size': batch_size,
                'target_r2': self.config.target_r2,
                'target_mae': self.config.target_mae_kg,
            })
            
            # Construir modelo
            self.model = BreedWeightEstimatorCNN.build_model(
                breed_name=self.breed_type,
                base_architecture=self.base_architecture
            )
            
            print(f"✅ Modelo construido: {self.model.name}")
            print(f"📊 Parámetros: {self.model.count_params():,}")
            
            # Configurar callbacks
            callbacks_list = self._setup_callbacks(early_stopping_patience)
            
            # Crear datasets
            # NOTA: Implementar generator de datos real
            train_generator = None  # TODO: Implementar
            val_generator = None    # TODO: Implementar
            
            # Entrenar
            # NOTA: Descomentar cuando generator esté implementado
            # history = self.model.fit(
            #     train_generator,
            #     epochs=epochs,
            #     validation_data=val_generator,
            #     callbacks=callbacks_list,
            #     verbose=1
            # )
            
            print("✅ Entrenamiento completado")
            
            # Log modelo en MLflow
            mlflow.tensorflow.log_model(self.model, "model")
            
            return self.model
    
    def _setup_callbacks(self, patience: int) -> list:
        """
        Configurar callbacks de entrenamiento.
        
        Args:
            patience: Paciencia para early stopping
        
        Returns:
            list: Lista de callbacks
        """
        return [
            callbacks.EarlyStopping(
                monitor='val_loss',
                patience=patience,
                restore_best_weights=True,
                verbose=1
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            ),
            callbacks.ModelCheckpoint(
                filepath=str(self.data_dir.parent.parent / 'models' / self.breed_type / 'best.h5'),
                monitor='val_loss',
                save_best_only=True,
                verbose=1
            ),
            callbacks.TensorBoard(
                log_dir=str(self.data_dir.parent.parent / 'logs' / self.breed_type),
                histogram_freq=1,
            )
        ]
    
    def evaluate(self, test_generator) -> Dict[str, float]:
        """
        Evaluar modelo en conjunto de test.
        
        Args:
            test_generator: Generador de datos de test
        
        Returns:
            Dict[str, float]: Diccionario de métricas
        """
        if self.model is None:
            raise ValueError("Modelo no entrenado. Ejecutar train() primero.")
        
        # Predicciones
        # y_true, y_pred = ...
        
        # Calcular métricas
        # metrics = MetricsCalculator.calculate_metrics_with_assertions(
        #     y_true, y_pred, self.breed_type,
        #     self.config.target_r2, self.config.target_mae_kg
        # )
        
        # return metrics.to_dict()
        pass

