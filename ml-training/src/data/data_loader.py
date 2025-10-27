"""
Data Loader para entrenamiento de modelos de estimación de peso.
Clase CattleDataGenerator que hereda de tf.keras.utils.Sequence.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional, Tuple
import cv2
import albumentations as A
from tensorflow.keras.utils import Sequence


class CattleDataGenerator(Sequence):
    """
    Generador de datos para entrenamiento de modelos CNN.
    
    Lee imágenes, aplica augmentation y retorna batches de datos.
    Compatible con tf.keras.Model.fit()
    """
    
    def __init__(
        self,
        annotations_df: pd.DataFrame,
        images_dir: Path,
        batch_size: int = 32,
        image_size: Tuple[int, int] = (224, 224),
        transform: Optional[A.Compose] = None,
        shuffle: bool = True
    ):
        """
        Inicializar generador de datos.
        
        Args:
            annotations_df: DataFrame con columnas 'image_filename', 'weight_kg', 'breed'
            images_dir: Directorio con las imágenes
            batch_size: Tamaño del batch
            image_size: Tamaño de las imágenes (height, width)
            transform: Pipeline de Albumentations (opcional)
            shuffle: Si True, shuffle de índices después de cada época
        """
        self.annotations_df = annotations_df.copy()
        self.images_dir = Path(images_dir)
        self.batch_size = batch_size
        self.image_size = image_size
        self.transform = transform
        self.shuffle = shuffle
        
        # Validar columnas requeridas
        required_cols = ['image_filename', 'weight_kg', 'breed']
        missing_cols = [col for col in required_cols if col not in annotations_df.columns]
        if missing_cols:
            raise ValueError(f"Faltan columnas requeridas: {missing_cols}")
        
        # Índices de los datos
        self.indices = np.arange(len(annotations_df))
        
        if self.shuffle:
            np.random.shuffle(self.indices)
        
        print(f"✅ CattleDataGenerator inicializado")
        print(f"   📊 Datos: {len(annotations_df)} imágenes")
        print(f"   📦 Batch size: {batch_size}")
        print(f"   📏 Image size: {image_size}")
        print(f"   🔀 Shuffle: {shuffle}")
    
    def __len__(self) -> int:
        """Retorna número de batches por época."""
        return int(np.ceil(len(self.annotations_df) / self.batch_size))
    
    def __getitem__(self, idx: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Retorna un batch de datos.
        
        Args:
            idx: Índice del batch
        
        Returns:
            Tuple[X_batch, y_batch]:
                - X_batch: numpy array shape (batch_size, H, W, 3)
                - y_batch: numpy array shape (batch_size,) con pesos en kg
        """
        # Obtener índices del batch actual
        batch_indices = self.indices[idx * self.batch_size:(idx + 1) * self.batch_size]
        
        # Inicializar arrays
        X_batch = []
        y_batch = []
        
        # Procesar cada imagen del batch
        for i in batch_indices:
            row = self.annotations_df.iloc[i]
            
            try:
                # Cargar y procesar imagen
                image = self._load_and_process_image(
                    image_path=self.images_dir / row['image_filename'],
                    image_size=self.image_size,
                    transform=self.transform
                )
                
                X_batch.append(image)
                y_batch.append(row['weight_kg'])
                
            except Exception as e:
                print(f"⚠️ Error cargando imagen {row['image_filename']}: {e}")
                # Si hay error, usar imagen cero o saltar
                continue
        
        # Convertir a numpy arrays
        X_batch = np.array(X_batch, dtype=np.float32)
        y_batch = np.array(y_batch, dtype=np.float32)
        
        return X_batch, y_batch
    
    def on_epoch_end(self):
        """Callback al final de cada época."""
        if self.shuffle:
            np.random.shuffle(self.indices)
    
    @staticmethod
    def _load_and_process_image(
        image_path: Path,
        image_size: Tuple[int, int],
        transform: Optional[A.Compose] = None
    ) -> np.ndarray:
        """
        Cargar y procesar una imagen.
        
        Args:
            image_path: Ruta a la imagen
            image_size: Tamaño objetivo (height, width)
            transform: Pipeline de Albumentations
        
        Returns:
            np.ndarray: Imagen procesada shape (H, W, 3), valores 0-1
        """
        # Leer imagen con OpenCV
        image = cv2.imread(str(image_path))
        
        if image is None:
            raise ValueError(f"No se pudo cargar imagen: {image_path}")
        
        # Convertir BGR a RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Aplicar transformaciones
        if transform is not None:
            # Albumentations espera dict con key 'image'
            transformed = transform(image=image)
            image = transformed['image']
        else:
            # Solo resize y normalizar si no hay transform
            image = cv2.resize(image, (image_size[1], image_size[0]))
            # Normalizar a 0-1
            image = image.astype(np.float32) / 255.0
        
        return image
    
    def get_stats(self) -> dict:
        """
        Obtener estadísticas del dataset.
        
        Returns:
            dict con estadísticas
        """
        return {
            'total_images': len(self.annotations_df),
            'num_batches': len(self),
            'batch_size': self.batch_size,
            'breeds': self.annotations_df['breed'].value_counts().to_dict(),
            'weight_stats': {
                'mean': self.annotations_df['weight_kg'].mean(),
                'std': self.annotations_df['weight_kg'].std(),
                'min': self.annotations_df['weight_kg'].min(),
                'max': self.annotations_df['weight_kg'].max(),
            }
        }

