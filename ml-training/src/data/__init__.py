"""Módulos de datos."""

from .augmentation import (
    get_training_transform,
    get_aggressive_augmentation,
    get_validation_transform,
)

__all__ = [
    'get_training_transform',
    'get_aggressive_augmentation',
    'get_validation_transform',
]

