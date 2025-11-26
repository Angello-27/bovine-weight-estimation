# Scripts de Utilidad - Backend

## Seed Data Script

Script para cargar datos iniciales en MongoDB para desarrollo y testing.

### 📋 Descripción

El script `seed_data.py` carga datos de ejemplo en la base de datos MongoDB con **TRAZABILIDAD COMPLETA**:

- **200 animales** distribuidos según porcentajes realistas de Hacienda Gamelera
- **Evolución temporal de peso** (múltiples pesajes por animal mostrando crecimiento)
- **Relaciones familiares** (madre/padre registrados)
- **Estados variados** (active/sold/deceased)
- **Datos controlados** para demostración de trazabilidad completa
- **Referencias a imágenes** (para descargar manualmente de Drive)

### 🚀 Uso

#### Opción 1: Ejecutar directamente

```bash
cd backend
python -m scripts.seed_data
```

#### Opción 2: Ejecutar desde la raíz del proyecto

```bash
python -m backend.scripts.seed_data
```

### ⚙️ Configuración

El script usa las mismas configuraciones que el backend principal:

- **MongoDB URL**: Desde `settings.MONGODB_URL` (por defecto: `mongodb://localhost:27017`)
- **Base de datos**: Desde `settings.MONGODB_DB_NAME` (por defecto: `bovine_weight_estimation`)

Puedes configurarlo mediante variables de entorno o archivo `.env`:

```bash
export MONGODB_URL="mongodb://localhost:27017"
export MONGODB_DB_NAME="bovine_weight_estimation"
```

### 📊 Datos Generados

#### Animales

- **Total**: 200 animales + 30 animales base (padres/madres) = 230 animales
- **Distribución realista** según Hacienda Gamelera:
  - Nelore: 84 animales (42%)
  - Brahman: 50 animales (25%)
  - Guzerat: 30 animales (15%)
  - Senepol: 16 animales (8%)
  - Girolando: 10 animales (5%)
  - Gyr Lechero: 6 animales (3%)
  - Sindi: 4 animales (2%)

**Características de los animales**:
- Caravanas únicas: `HG-{RAZA}-001`, `HG-{RAZA}-002`, etc.
- Fechas de nacimiento variadas (2018-2024)
  - Animales base: 2018-2020 (padres/madres)
  - Animales principales: 2020-2024 (más jóvenes)
- Géneros: 55% hembras, 45% machos
- Pesos al nacer realistas según la raza
- Estados: 85% active, 10% sold, 5% deceased
- **Relaciones familiares**: 70% tienen padre/madre registrados
- **Trazabilidad completa**: historial desde nacimiento

#### Estimaciones de Peso (Evolución Temporal)

- **Total**: ~1,500-2,000 estimaciones (promedio 7-10 por animal)
- **Distribución por edad**:
  - Animales muy jóvenes (<1 mes): 1-2 pesajes
  - Animales jóvenes (<12 meses): 3-5 pesajes
  - Animales en crecimiento (12-24 meses): 6-10 pesajes
  - Animales adultos (>24 meses): 10-15 pesajes

**Características de las estimaciones**:
- **Evolución temporal**: pesajes distribuidos a lo largo de la vida del animal
- **Curvas de crecimiento realistas**: peso aumenta según edad y raza
- Confidence scores: 85-98% (más alto para adultos)
- Método: `tflite`
- Modelo: `1.0.0`
- Tiempo de procesamiento: 1.2-2.5 segundos
- Fechas desde nacimiento hasta hoy (o fecha de muerte/venta)
- Coordenadas GPS: San Ignacio de Velasco
- **Rangos de peso por raza y categoría de edad**:
  - Terneros (<8 meses): 70-210 kg según raza
  - Vaquillonas/Torillos (6-18 meses): 180-400 kg según raza
  - Vaquillonas/Toretes (19-30 meses): 320-550 kg según raza
  - Vacas/Toros (>30 meses): 350-650 kg según raza

### 📸 Imágenes

El script incluye referencias a imágenes en Google Drive. Para usar imágenes reales:

1. **Descarga las imágenes** de Drive manualmente
2. **Actualiza los IDs** en el script `seed_data.py`:

```python
IMAGE_REFERENCES = {
    "nelore": "https://drive.google.com/file/d/TU_FILE_ID_AQUI/view",
    "brahman": "https://drive.google.com/file/d/TU_FILE_ID_AQUI/view",
    # ... etc
}
```

3. **Opcional**: Sube las imágenes a un servidor/CDN y actualiza las URLs

### ⚠️ Advertencias

- **El script limpia datos existentes** antes de cargar nuevos datos
- Si quieres mantener datos existentes, comenta las líneas de limpieza:

```python
# await AnimalModel.delete_all()
# await WeightEstimationModel.delete_all()
```

### 🔍 Verificación

Después de ejecutar el script, puedes verificar los datos:

1. **Usando MongoDB Compass** o cualquier cliente MongoDB
2. **Usando la API**:
   ```bash
   curl http://localhost:8000/api/v1/animals
   curl http://localhost:8000/api/v1/weighings
   ```

### 📝 Ejemplo de Salida

```
🌱 Iniciando carga de datos iniciales con TRAZABILIDAD COMPLETA...
📊 Base de datos: bovine_weight_estimation
🔗 MongoDB URL: mongodb://localhost:27017

✅ Conectado a MongoDB

🗑️  Limpiando datos existentes...
✅ Datos limpiados

🐄 Generando 200 animales con trazabilidad completa...
   📝 230 animales generados
✅ 230 animales insertados en MongoDB

⚖️  Generando estimaciones de peso con evolución temporal...
   📝 1850 estimaciones generadas
✅ 1850 estimaciones insertadas en MongoDB

======================================================================
📊 RESUMEN DE DATOS CARGADOS - TRAZABILIDAD COMPLETA
======================================================================
🐄 Animales totales: 230
⚖️  Estimaciones totales: 1850
📈 Promedio de pesajes por animal: 8.0
🏢 Hacienda ID: 550e8400-e29b-41d4-a716-446655440000

📋 Distribución por raza:
   - Brahman: 50 animales (25.0%)
   - Girolando: 10 animales (5.0%)
   - Guzerat: 30 animales (15.0%)
   - Gyr Lechero: 6 animales (3.0%)
   - Nelore: 84 animales (42.0%)
   - Senepol: 16 animales (8.0%)
   - Sindi: 4 animales (2.0%)

📊 Distribución por estado:
   - Active: 195 animales (84.8%)
   - Deceased: 12 animales (5.2%)
   - Sold: 23 animales (10.0%)

👶 Distribución por categoría de edad:
   - terneros: 45 animales (19.6%)
   - vaquillonas_torillos: 68 animales (29.6%)
   - vaquillonas_toretes: 52 animales (22.6%)
   - vacas_toros: 65 animales (28.3%)

👨‍👩‍👧 Animales con padre/madre registrados: 161 (70.0%)

📅 Rango de fechas de nacimiento: 2018-01-15 a 2024-11-20
📅 Rango de fechas de pesajes: 2018-04-10 a 2024-12-15

======================================================================
✅ Seed data completado exitosamente!

📸 NOTA: Las referencias a imágenes están en IMAGE_REFERENCES
   Descarga las imágenes de Drive y actualiza los IDs en el script.

🔍 TRAZABILIDAD:
   - Cada animal tiene historial completo de pesajes
   - Relaciones familiares (madre/padre) registradas
   - Estados variados (active/sold/deceased)
   - Evolución temporal de peso documentada
======================================================================
```

### 🛠️ Troubleshooting

**Error: "No module named 'app'"**
- Asegúrate de ejecutar desde el directorio `backend/` o desde la raíz del proyecto

**Error: "Connection refused"**
- Verifica que MongoDB esté corriendo: `mongosh` o `mongo`

**Error: "Database not found"**
- El script crea la base de datos automáticamente si no existe

### 📚 Próximos Pasos

1. Ejecutar el script de seed data
2. Verificar los datos en MongoDB
3. Probar los endpoints de la API
4. Descargar imágenes de Drive y actualizar referencias
5. Personalizar datos según necesidades específicas
