# Sistema de Estimación Automática del Peso de Ganado Bovino

## 📋 Información del Proyecto

### Cliente
- **Nombre**: Hacienda Gamelera
- **Propietario**: Bruno Brito Macedo
- **Ubicación**: San Ignacio de Velasco, Santa Cruz, Bolivia
- **Capacidad**: 500 cabezas de ganado bovino

### Equipo de Desarrollo
- **Product Owner**: Miguel Angel Escobar Lazcano
- **Scrum Master**: Rodrigo Escobar Morón
- **Equipo**: 3 estudiantes trabajando con programación asistida por IA

### Características del Proyecto
- **Tipo**: Proyecto académico final de carrera
- **Fecha límite**: Finales noviembre / inicio diciembre 2024
- **Sprint actual**: Sprint 2 (mitad del sprint)
- **Semanas restantes**: 4-5 semanas hasta presentación final
- **Estado**: Arquitectura 83% completa, FALTA core ML

## 🐄 Razas Bovinas Soportadas (8 razas)

### Razas Prioritarias (más datos disponibles)
1. **Brahman** - Bos indicus, muy común en Chiquitanía
2. **Nelore** - Bos indicus, 80% del Pantanal
3. **Angus** - Bos taurus, carne de calidad

### Razas Adicionales
4. **Cebuinas** - Bos indicus general (agrupa varias razas zebu)
5. **Criollo** - Criollo Chaqueño, adaptado local
6. **Pardo Suizo** - Bos taurus grande
7. **Guzerat** - Bos indicus, lechero y carne (reemplaza Jersey)
8. **Holstein** - Lechera, común en región

## 🛠️ Stack Tecnológico

### Backend
- **Python**: 3.11+
- **Framework**: FastAPI
- **Base de Datos**: MongoDB con Beanie ODM
- **ML Framework**: TensorFlow 2.19+

### Mobile
- **Framework**: Flutter 3.35+
- **Lenguaje**: Dart 3.9+
- **Base de Datos Local**: SQLite
- **ML Mobile**: TensorFlow Lite

### Machine Learning
- **Framework**: TensorFlow 2.19+
- **Entrenamiento**: Google Colab (GPU gratuita)
- **Experiment Tracking**: MLflow
- **Data Augmentation**: Albumentations

## 🏗️ Arquitectura del Sistema

### Strategy Pattern Implementado
El sistema utiliza el patrón Strategy para manejar diferentes métodos de estimación:

1. **ML Strategy**: Modelos entrenados específicos por raza (prioridad alta)
2. **Hybrid Strategy**: YOLO + fórmulas morfométricas (fallback)

### Principios SOLID Aplicados
- **Single Responsibility**: Cada estrategia tiene una responsabilidad específica
- **Open/Closed**: Fácil agregar nuevas estrategias sin modificar código existente
- **Liskov Substitution**: Todas las estrategias son intercambiables
- **Interface Segregation**: Interfaces específicas para cada tipo de estrategia
- **Dependency Inversion**: Dependencias hacia abstracciones, no implementaciones

## 📊 Métricas Objetivo

- **Precisión**: ≥95% (R² ≥0.95)
- **Error**: <5 kg
- **Tiempo de procesamiento**: <3 segundos
- **Confianza mínima**: ≥80%

## 🚀 Próximos Pasos

1. **Entrenar modelos ML** para las 3 razas prioritarias
2. **Calibrar sistema híbrido** con datos reales de la hacienda
3. **Implementar core ML** (83% arquitectura completa)
4. **Testing y validación** del sistema completo
5. **Preparación para presentación final**

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── ml/
│   │   ├── strategies/          # Sistema de estrategias
│   │   ├── strategy_context.py  # Contexto de selección
│   │   └── inference.py         # Motor de inferencia
│   ├── core/
│   │   └── constants/
│   │       └── breeds.py        # 8 razas bovinas
│   └── api/routes/
│       └── ml.py                # Endpoints ML
└── scripts/
    ├── ml_training/             # Entrenamiento
    ├── data_generation/         # Datos sintéticos
    ├── calibration/             # Calibración híbrida
    └── testing/                 # Pruebas
```

## 📝 Notas Importantes

- **Prioridad**: Enfocar esfuerzos en las 3 razas principales (Brahman, Nelore, Angus)
- **Datos**: Necesarios datos reales de la hacienda para calibración
- **Tiempo**: 4-5 semanas restantes para completar el proyecto
- **Arquitectura**: Sistema modular y extensible siguiendo Clean Architecture
