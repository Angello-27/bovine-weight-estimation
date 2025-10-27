"""
Sistema de logging para el proyecto.
Configura loggers que escriben a archivo y consola.
"""

import logging
from pathlib import Path
from datetime import datetime


def setup_logger(
    name: str,
    log_dir: Path,
    level: int = logging.INFO
) -> logging.Logger:
    """
    Configura un logger que escribe a archivo y consola.
    
    Args:
        name: Nombre del logger
        log_dir: Directorio donde guardar logs
        level: Nivel de logging (default INFO)
    
    Returns:
        logging.Logger configurado
    """
    # Crear directorio de logs si no existe
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evitar duplicados
    if logger.handlers:
        return logger
    
    # Formato de logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para archivo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f"{name}_{timestamp}.log"
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Agregar handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logger '{name}' configurado - Log file: {log_file}")
    
    return logger


def setup_project_logger(log_dir: Path = None) -> logging.Logger:
    """
    Configura el logger principal del proyecto.
    
    Args:
        log_dir: Directorio donde guardar logs (default: ./logs)
    
    Returns:
        logging.Logger configurado
    """
    if log_dir is None:
        log_dir = Path('./logs')
    
    return setup_logger('bovine-weight-estimation', log_dir)

