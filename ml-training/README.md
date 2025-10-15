# ML Training - Sistema de Estimación de Peso Bovino

Entrenamiento de modelos TensorFlow/Keras para estimación de peso - Hacienda Gamelera.

## 🏗️ Estructura

```
src/
├── data/           # Raw, Processed, Augmented
├── models/         # Training, Evaluation, Export
├── features/       # Feature Engineering
└── utils/          # Utilidades
```

## 🎯 Objetivo

Entrenar **7 modelos TFLite** (uno por raza) con:
- **Precisión**: R² ≥ 0.95
- **Error**: MAE < 5 kg
- **Velocidad**: Inferencia < 3 segundos

## 📋 Requisitos

- Python 3.11+
- TensorFlow 2.15+
- MLflow (tracking)
- DVC (versionado de datos)

## 🚀 Entrenamiento

```bash
# Instalar dependencias
pip install -r requirements.txt

# Entrenar modelo
python src/models/training/train.py --breed brahman

# Evaluar modelo
python src/models/evaluation/evaluate.py --breed brahman

# Exportar a TFLite
python src/models/export/export_tflite.py --breed brahman
```

## 📊 Tracking

```bash
# Abrir MLflow UI
mlflow ui --backend-store-uri ./experiments/mlflow
```

## 🔧 Configuración

Ver `config/config.yaml` para configuración completa.

## 📦 Modelos

**7 Razas**: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey  
**Formato**: TFLite cuantizado  
**Entrada**: Imagen 224x224x3  
**Salida**: Peso estimado (kg)

