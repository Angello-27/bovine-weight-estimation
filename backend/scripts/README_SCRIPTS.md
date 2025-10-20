# Backend Scripts

Scripts de utilidad para desarrollo y deployment del backend.

---

## 📋 Scripts Disponibles

### `train_generic_model.py` - Training ML MVP

**Propósito**: Entrena modelo genérico básico para demostración.

**Uso**:
```bash
cd backend
python scripts/train_generic_model.py
```

**Output**:
- `ml_models/generic-v1.0.0.tflite` - Modelo TFLite genérico
- `ml_models/generic/v1.0.0/saved_model/` - Modelo Keras completo

**Nota**: 
- Usa datos mock (no es modelo real)
- Para modelos reales, usar `ml-training/` con datasets
- Los 7 modelos específicos por raza se entrenarán después

---

## 🎯 Próximos Scripts a Crear

### `setup_mongodb.py` - Setup MongoDB Atlas
```bash
python scripts/setup_mongodb.py
```
- Crear base de datos
- Crear colecciones con índices
- Seed data inicial (Farm Gamelera, Usuario Bruno)

### `seed_data.py` - Datos de prueba
```bash
python scripts/seed_data.py --animals 500 --weighings 1000
```
- Generar animales de prueba (500 cabezas, 7 razas)
- Generar pesajes históricos

### `test_ml_endpoint.py` - Test ML API
```bash
python scripts/test_ml_endpoint.py --image test.jpg --breed brahman
```
- Probar endpoint /ml/predict
- Validar respuesta y métricas

---

**Última actualización**: 20 Oct 2024

