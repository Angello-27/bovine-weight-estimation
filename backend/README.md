# Backend API - Sistema de Estimación de Peso Bovino

API FastAPI para sincronización y análisis avanzado - Hacienda Gamelera.

## 🏗️ Arquitectura

```
app/
├── api/            # Routes, Dependencies
├── core/           # Config, Constants, Errors
├── models/         # MongoDB Models (Beanie ODM)
├── schemas/        # Pydantic Schemas
├── services/       # Business Logic
└── utils/          # Utilidades
```

## 🎯 Características

- Sincronización bidireccional con MongoDB
- Endpoints REST para análisis y reportes
- Integración con entidades regulatorias (SENASAG, REGENSA, ASOCEBU)

## 📋 Requisitos

- Python 3.11+
- MongoDB 5.0+

## 🚀 Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python -m app.main
```

## 🧪 Testing

```bash
pytest tests/ -v
pytest --cov=app tests/
```

## 🔧 Configuración

Copiar `.env.example` a `.env` y configurar variables.

## 📊 Datos Críticos

**7 Razas**: Brahman, Nelore, Angus, Cebuinas, Criollo, Pardo Suizo, Jersey  
**Owner**: Bruno Brito Macedo  
**Ubicación**: San Ignacio de Velasco, Santa Cruz, Bolivia

