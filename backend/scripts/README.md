# Scripts del Sistema de Estimación de Peso Bovino

Este directorio contiene scripts utilitarios para el sistema de estimación de peso bovino con IA.

## Estructura Organizada

```
scripts/
├── ml_training/           # Scripts de entrenamiento de modelos ML
│   └── train_generic_model.py
├── data_generation/       # Scripts de generación de datos
│   ├── generate_synthetic_data.py
│   └── example_weights.json
├── calibration/           # Scripts de calibración del sistema híbrido
│   └── calibrate_hybrid.py
├── testing/              # Scripts de pruebas y validación
│   └── test_hybrid_system.py
└── README.md            # Este archivo
```

## Scripts Disponibles

### 🧠 ML Training (`ml_training/`)

- **`train_generic_model.py`**: Entrena modelo genérico de estimación de peso
  - Entrada: Dataset de imágenes bovinas etiquetadas
  - Salida: Modelo TFLite optimizado
  - Uso: `python ml_training/train_generic_model.py`

### 📊 Data Generation (`data_generation/`)

- **`generate_synthetic_data.py`**: Genera datos sintéticos para entrenamiento
  - Crea imágenes sintéticas de bovinos con pesos conocidos
  - Útil para aumentar dataset cuando hay pocos datos reales
  - Uso: `python data_generation/generate_synthetic_data.py`

- **`example_weights.json`**: Archivo de ejemplo con pesos típicos por raza
  - Contiene rangos de peso para las 7 razas soportadas
  - Usado como referencia para validación

### ⚙️ Calibration (`calibration/`)

- **`calibrate_hybrid.py`**: Calibra parámetros del sistema híbrido
  - Ajusta coeficientes de fórmulas morfométricas por raza
  - Requiere ~20 fotos reales por raza para calibración
  - Uso: `python calibration/calibrate_hybrid.py`

### 🧪 Testing (`testing/`)

- **`test_hybrid_system.py`**: Prueba el sistema de estrategias
  - Valida funcionamiento de estrategias ML e híbrida
  - Genera reportes de precisión y rendimiento
  - Uso: `python testing/test_hybrid_system.py`

## Arquitectura del Sistema

El sistema utiliza **Strategy Pattern** para manejar diferentes métodos de estimación:

1. **ML Strategy**: Modelos entrenados específicos por raza (prioridad alta)
2. **Hybrid Strategy**: YOLO + fórmulas morfométricas (fallback)

### Principios SOLID Aplicados

- **Single Responsibility**: Cada script tiene una responsabilidad específica
- **Open/Closed**: Fácil agregar nuevas estrategias sin modificar código existente
- **Liskov Substitution**: Todas las estrategias son intercambiables
- **Interface Segregation**: Interfaces específicas para cada tipo de estrategia
- **Dependency Inversion**: Dependencias hacia abstracciones, no implementaciones

## Requisitos

Todos los scripts requieren las dependencias del proyecto:

```bash
pip install -r ../requirements.txt
```

## Uso Recomendado

1. **Desarrollo**: Usar `generate_synthetic_data.py` para crear datos de prueba
2. **Entrenamiento**: Ejecutar `train_generic_model.py` con datos reales
3. **Calibración**: Usar `calibrate_hybrid.py` con fotos reales de la hacienda
4. **Validación**: Ejecutar `test_hybrid_system.py` para verificar funcionamiento

## Notas Importantes

- Los scripts están diseñados para funcionar con la arquitectura Clean Architecture del proyecto
- Todos los scripts respetan las 7 razas bovinas definidas en el sistema
- Los modelos generados son compatibles con TensorFlow Lite para despliegue móvil
- La calibración híbrida requiere datos reales de la hacienda para máxima precisión