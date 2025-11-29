# 📋 Scripts de Utilidad - Backend

Scripts de utilidad para desarrollo, testing y deployment del backend FastAPI.

**Última actualización**: Diciembre 2024

---

## ✅ Scripts Disponibles

### 1. `setup_production.py` - Setup para Producción/Cloud

**Propósito**: Prepara el backend para deployment en la nube.

**Funcionalidades**:
- ✅ Verifica dependencias instaladas
- ✅ Crea directorios necesarios (ml_models, logs, uploads)
- ✅ Valida configuración crítica (MongoDB URL, Secret Key, CORS)
- ✅ Verifica modelos ML disponibles

**Uso**:
```bash
cd backend
python scripts/setup_production.py
```

**Output**:
- Verificación de dependencias
- Directorios creados
- Validación de configuración
- Estado de modelos ML

---

### 2. `seed_data.py` - Datos Iniciales para Testing

**Propósito**: Carga datos iniciales en MongoDB para desarrollo y testing.

**Funcionalidades**:
- ✅ Crea roles iniciales (Administrador, Usuario, Invitado)
- ✅ Crea usuario principal: **Bruno Brito Macedo**
  - Usuario: `bruno_brito`
  - Email: `bruno@haciendagamelera.com`
  - Contraseña: `password123` ⚠️ **Cambiar en producción**
- ✅ Crea finca: **Hacienda Gamelera**
- ✅ Genera 200 animales con trazabilidad completa
- ✅ Genera estimaciones de peso con evolución temporal (~1,500-2,000 pesajes)

**Uso**:
```bash
cd backend
python -m scripts.seed_data
```

**⚠️ Advertencia**: El script **limpia datos existentes** antes de cargar nuevos datos.

**Datos Generados**:

#### Animales (200 + 30 base = 230 total)
- **Distribución realista** según Hacienda Gamelera:
  - Nelore: 84 animales (42%)
  - Brahman: 50 animales (25%)
  - Guzerat: 30 animales (15%)
  - Senepol: 16 animales (8%)
  - Girolando: 10 animales (5%)
  - Gyr Lechero: 6 animales (3%)
  - Sindi: 4 animales (2%)

**Características**:
- Caravanas únicas: `HG-{RAZA}-001`, `HG-{RAZA}-002`, etc.
- Fechas de nacimiento variadas (2018-2024)
- Géneros: 55% hembras, 45% machos
- Estados: 85% active, 10% sold, 5% deceased
- **Relaciones familiares**: 70% tienen padre/madre registrados
- **Trazabilidad completa**: historial desde nacimiento

#### Estimaciones de Peso (~1,500-2,000)
- **Evolución temporal**: pesajes distribuidos a lo largo de la vida del animal
- **Curvas de crecimiento realistas**: peso aumenta según edad y raza
- Confidence scores: 85-98% (más alto para adultos)
- Método: `tflite`
- Modelo: `1.0.0`
- Tiempo de procesamiento: 1.2-2.5 segundos

**Distribución por edad**:
- Animales muy jóvenes (<1 mes): 1-2 pesajes
- Animales jóvenes (<12 meses): 3-5 pesajes
- Animales en crecimiento (12-24 meses): 6-10 pesajes
- Animales adultos (>24 meses): 10-15 pesajes

**Rangos de peso por raza y categoría**:
- Terneros (<8 meses): 70-210 kg según raza
- Vaquillonas/Torillos (6-18 meses): 180-400 kg según raza
- Vaquillonas/Toretes (19-30 meses): 320-550 kg según raza
- Vacas/Toros (>30 meses): 350-650 kg según raza

**Verificación**:
```bash
# Usando la API
curl http://localhost:8000/api/v1/animals
curl http://localhost:8000/api/v1/weighings
```

---

### 3. `download_model_from_drive.py` - Descargar Modelo TFLite

**Propósito**: Descarga modelo TFLite desde Google Drive.

**Funcionalidades**:
- ✅ Descarga modelo desde Google Drive usando `gdown`
- ✅ Valida que el archivo se descargó correctamente
- ✅ Muestra tamaño del archivo

**Uso**:
```bash
cd backend
python scripts/download_model_from_drive.py --file-id FILE_ID --output ml_models/
```

**Requisitos**:
```bash
pip install gdown
```

**Ejemplo**:
```bash
# Obtener FILE_ID del link de Google Drive:
# https://drive.google.com/file/d/FILE_ID_AQUI/view?usp=sharing

python scripts/download_model_from_drive.py \
  --file-id FILE_ID_AQUI \
  --output ml_models/ \
  --filename generic-cattle-v1.0.0.tflite
```

**Output**:
- Modelo descargado en `ml_models/`
- Tamaño del archivo mostrado
- Ubicación del archivo

---

## 🚀 Flujo Recomendado

### 1. Setup Inicial
```bash
# Verificar dependencias y configuración
python scripts/setup_production.py
```

### 2. Descargar Modelo ML
```bash
# Descargar modelo TFLite desde Colab/Drive
python scripts/download_model_from_drive.py --file-id FILE_ID
```

### 3. Cargar Datos de Prueba
```bash
# Cargar datos iniciales en MongoDB
python -m scripts.seed_data
```

### 4. Iniciar Backend
```bash
# Iniciar servidor
python -m app.main
```

---

## ⚙️ Configuración

Los scripts usan las mismas configuraciones que el backend principal:

- **MongoDB URL**: Desde `settings.MONGODB_URL` (por defecto: `mongodb://localhost:27017`)
- **Base de datos**: Desde `settings.MONGODB_DB_NAME` (por defecto: `bovine_weight_estimation`)

Puedes configurarlo mediante variables de entorno o archivo `.env`:

```bash
export MONGODB_URL="mongodb://localhost:27017"
export MONGODB_DB_NAME="bovine_weight_estimation"
```

---

## 🛠️ Troubleshooting

### Error: "No module named 'app'"
- Asegúrate de ejecutar desde el directorio `backend/` o desde la raíz del proyecto

### Error: "Connection refused"
- Verifica que MongoDB esté corriendo: `mongosh` o `mongo`

### Error: "Database not found"
- El script crea la base de datos automáticamente si no existe

### Error: "gdown no está instalado"
- Instala con: `pip install gdown`

---

## 📝 Notas Importantes

### Seed Data
- ⚠️ **El script limpia datos existentes** antes de cargar nuevos datos
- Si quieres mantener datos existentes, comenta las líneas de limpieza en `seed_data.py`
- Las referencias a imágenes están en `IMAGE_REFERENCES` (descargar manualmente de Drive)

### Modelo TFLite
- El modelo debe estar compartido públicamente o con acceso en Google Drive
- Verifica que el `FILE_ID` sea correcto
- El modelo se descarga en `ml_models/` por defecto

---

**Última actualización**: Diciembre 2024
