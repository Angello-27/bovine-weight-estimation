# 🎨 Guía de Integración Frontend - Panel Web React

**Objetivo**: Guía completa de integración del Panel Web React con el Backend FastAPI, incluyendo ML, APIs REST, trazabilidad, reportes y estimación de peso.

**Estado**: ✅ **TODOS LOS SERVICIOS API IMPLEMENTADOS** (100%)  
**Frontend**: React + Material-UI  
**Backend**: FastAPI (Python 3.11+)  
**Base URL API**: `http://localhost:8000` (desarrollo) | `https://api.haciendagamelera.com` (producción)

---

## 📋 Índice

1. [Configuración Inicial](#configuración-inicial)
2. [Arquitectura del Frontend](#arquitectura-del-frontend)
3. [Integración con APIs REST](#integración-con-apis-rest)
4. [Estimación de Peso desde Web](#estimación-de-peso-desde-web)
5. [Trazabilidad del Ganado](#trazabilidad-del-ganado)
6. [Sistema de Reportes](#sistema-de-reportes)
7. [Autenticación y Autorización](#autenticación-y-autorización)
8. [Checklist de Implementación](#checklist-de-implementación)

---

## 🔧 Configuración Inicial

### 1. Variables de Entorno

**Archivo:** `.env` o `.env.local`

```env
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_API_VERSION=v1
REACT_APP_APP_NAME=Bovine Weight Estimation
```

### 2. Configuración de Axios

**Archivo:** `src/api/axiosClient.js`

```javascript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token JWT
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para manejar errores
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

### 3. Constantes de la Aplicación

**Archivo:** `src/config/constants.js`

```javascript
// Rutas del sidebar
export const sidebarItems = [
  {
    text: 'Dashboard',
    icon: <DashboardIcon />,
    to: '/dashboard',
    roles: ['Administrador', 'Usuario', 'Invitado'],
  },
  {
    text: 'Ganado',
    icon: <PetsIcon />,
    to: '/cattle',
    roles: ['Administrador', 'Usuario'],
  },
  {
    text: 'Estimaciones',
    icon: <ScaleIcon />,
    to: '/weight-estimations',
    roles: ['Administrador', 'Usuario'],
  },
  {
    text: 'Estimar Peso',
    icon: <AddCircleIcon />,
    to: '/weight-estimations/estimate',
    roles: ['Administrador', 'Usuario'],
  },
  {
    text: 'Reportes',
    icon: <DescriptionIcon />,
    to: '/reports',
    roles: ['Administrador', 'Usuario'],
  },
  {
    text: 'Usuarios',
    icon: <PeopleIcon />,
    to: '/users',
    roles: ['Administrador'],
  },
  {
    text: 'Roles',
    icon: <SecurityIcon />,
    to: '/roles',
    roles: ['Administrador'],
  },
  {
    text: 'Sincronización',
    icon: <SyncIcon />,
    to: '/sync',
    roles: ['Administrador'],
  },
];

// Razas válidas
export const BREEDS = [
  'nelore',
  'brahman',
  'guzerat',
  'senepol',
  'girolando',
  'gyr_lechero',
  'sindi',
];

// Estados de animales
export const ANIMAL_STATUS = ['active', 'inactive', 'sold', 'deceased'];

// Géneros
export const GENDERS = ['male', 'female'];
```

### 4. Rutas de la Aplicación

**Archivo:** `src/config/routes.js`

```javascript
import { Routes, Route, Navigate } from 'react-router-dom';
import LoginView from '../views/LoginView';
import DashboardView from '../views/DashboardView';
import CattleView from '../views/CattleView';
import CattleDetailView from '../views/CattleDetailView';
import WeightEstimationsView from '../views/WeightEstimationsView';
import WeightEstimationFromWebView from '../views/WeightEstimationFromWebView';
import SyncStatusView from '../views/SyncStatusView';
import UserView from '../views/UserView';
import RoleView from '../views/RoleView';
import FarmView from '../views/FarmView';

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginView />} />
      <Route path="/dashboard" element={<DashboardView />} />
      <Route path="/cattle" element={<CattleView />} />
      <Route path="/cattle/:id" element={<CattleDetailView />} />
      <Route path="/weight-estimations" element={<WeightEstimationsView />} />
      <Route
        path="/weight-estimations/estimate"
        element={<WeightEstimationFromWebView />}
      />
      <Route path="/sync" element={<SyncStatusView />} />
      <Route path="/users" element={<UserView />} />
      <Route path="/roles" element={<RoleView />} />
      <Route path="/farms" element={<FarmView />} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
};

export default AppRoutes;
```

---

## 🏗️ Arquitectura del Frontend

### Estructura de Carpetas

```
src/
├── api/
│   └── axiosClient.js          # Cliente HTTP configurado
├── config/
│   ├── constants.js            # Constantes de la app
│   └── routes.js               # Configuración de rutas
├── services/                   # Servicios API
│   ├── auth/
│   │   ├── AuthContext.js
│   │   └── authService.js ✅
│   ├── cattle/
│   │   ├── getAllCattle.js ✅ (con filtros y paginación)
│   │   ├── getCattleById.js ✅
│   │   ├── createCattle.js ✅
│   │   ├── updateCattle.js ✅
│   │   ├── deleteCattle.js ✅
│   │   ├── getAnimalTimeline.js ✅
│   │   └── getAnimalLineage.js ✅
│   ├── weight-estimations/
│   │   ├── getAllWeightEstimations.js ✅ (con paginación)
│   │   ├── getWeightEstimationById.js ✅
│   │   ├── getWeightEstimationsByCattleId.js ✅ (con paginación)
│   │   ├── estimateWeightFromImage.js ✅ # ⭐ ML desde web
│   │   └── createWeightEstimation.js ✅
│   ├── ml/
│   │   ├── getModelsStatus.js ✅
│   │   └── getMLHealth.js ✅
│   ├── reports/
│   │   ├── generateTraceabilityReport.js ✅ (desde backend)
│   │   ├── generateInventoryReport.js ✅ (desde backend)
│   │   ├── generateMovementReport.js ✅ (desde backend)
│   │   └── generateGrowthReport.js ✅ (desde backend)
│   ├── alerts/
│   │   ├── createAlert.js ✅
│   │   ├── getAllAlerts.js ✅ (con filtros y paginación)
│   │   ├── getAlertById.js ✅
│   │   ├── updateAlert.js ✅
│   │   ├── deleteAlert.js ✅
│   │   ├── getTodayAlerts.js ✅
│   │   ├── getUpcomingAlerts.js ✅
│   │   ├── getPendingAlerts.js ✅
│   │   ├── getScheduledAlerts.js ✅
│   │   └── getAlertAnimals.js ✅
│   ├── sync/
│   │   ├── getSyncHealth.js ✅
│   │   ├── getSyncStats.js ✅
│   │   ├── syncCattleBatch.js ✅
│   │   └── syncWeightEstimationsBatch.js ✅
│   ├── user/
│   │   ├── getAllUsers.js ✅ (con paginación)
│   │   ├── getUserById.js ✅
│   │   ├── createUser.js ✅
│   │   ├── updateUser.js ✅
│   │   └── deleteUser.js ✅
│   ├── role/
│   │   ├── getAllRoles.js ✅ (con paginación)
│   │   ├── getRoleById.js ✅
│   │   ├── createRole.js ✅
│   │   ├── updateRole.js ✅
│   │   └── deleteRole.js ✅
│   └── farm/
│       ├── getAllFarms.js ✅ (con paginación)
│       ├── getFarmById.js ✅
│       ├── createFarm.js ✅
│       ├── updateFarm.js ✅
│       └── deleteFarm.js ✅
├── containers/                 # Lógica de negocio
│   ├── auth/
│   ├── cattle/
│   ├── weight-estimations/
│   ├── reports/
│   └── sync/
├── components/
│   ├── atoms/                  # Componentes básicos
│   ├── molecules/              # Componentes compuestos
│   └── organisms/              # Componentes complejos
│       ├── CreateCattle/
│       ├── CreateWeightEstimation/
│       ├── CattleList/
│       ├── CattleTraceabilityTimeline/
│       ├── CattleLineageTree/
│       ├── CattleWeightHistoryChart/
│       └── CattleReportGenerator/
├── views/                      # Vistas principales
│   ├── LoginView.js
│   ├── DashboardView.js
│   ├── CattleView.js
│   ├── CattleDetailView.js
│   ├── WeightEstimationsView.js
│   ├── WeightEstimationFromWebView.js
│   ├── SyncStatusView.js
│   ├── UserView.js
│   └── RoleView.js
├── templates/                  # Templates de layout
│   ├── DashboardTemplate.js
│   ├── CattleTemplate.js
│   ├── WeightEstimationTemplate.js
│   └── SyncStatusTemplate.js
└── utils/
    └── transformers/
        ├── breedToComboBox.js
        ├── cattleToTableRow.js
        ├── weightEstimationToChartData.js
        └── cattleToTimelineEvents.js
```

---

## 🔌 Integración con APIs REST

### Autenticación

**Servicio:** `src/services/auth/login.js`

```javascript
import apiClient from '../../api/axiosClient';

export const login = async (username, password) => {
  const response = await apiClient.post('/api/v1/auth/login', {
    username,
    password,
  });
  
  // Guardar token
  localStorage.setItem('access_token', response.data.access_token);
  localStorage.setItem('user', JSON.stringify(response.data));
  
  return response.data;
};
```

**Uso en LoginView:**
```javascript
const handleLogin = async (username, password) => {
  try {
    const userData = await login(username, password);
    navigate('/dashboard');
  } catch (error) {
    setError('Credenciales inválidas');
  }
};
```

### Gestión de Animales (Cattle)

**Servicio:** `src/services/cattle/getAllCattle.js`

```javascript
import apiClient from '../../api/axiosClient';

export const getAllCattle = async (filters = {}) => {
  const params = new URLSearchParams();
  
  if (filters.farm_id) params.append('farm_id', filters.farm_id);
  if (filters.breed) params.append('breed', filters.breed);
  if (filters.gender) params.append('gender', filters.gender);
  if (filters.status) params.append('status', filters.status);
  if (filters.page) params.append('page', filters.page);
  if (filters.page_size) params.append('page_size', filters.page_size);
  
  const response = await apiClient.get(`/api/v1/animals?${params.toString()}`);
  return response.data;
};
```

**Endpoint Backend:** `GET /api/v1/animals`

**Response:**
```json
{
  "total": 100,
  "animals": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "ear_tag": "HG-BRA-001",
      "name": "Brahman #1",
      "breed": "brahman",
      "birth_date": "2022-03-15T00:00:00Z",
      "gender": "male",
      "status": "active",
      "farm_id": "770e8400-e29b-41d4-a716-446655440000"
    }
  ],
  "page": 1,
  "page_size": 50
}
```

### Gestión de Estimaciones de Peso

**Servicio:** `src/services/weight-estimations/getWeightEstimationsByCattleId.js`

```javascript
import apiClient from '../../api/axiosClient';

export const getWeightEstimationsByCattleId = async (cattleId, page = 1, pageSize = 50) => {
  const response = await apiClient.get(
    `/api/v1/weighings/animal/${cattleId}?page=${page}&page_size=${pageSize}`
  );
  return response.data;
};
```

**Endpoint Backend:** `GET /api/v1/weighings/animal/{animal_id}`

---

## 🤖 Estimación de Peso desde Web

### Descripción

Permitir hacer estimaciones de peso desde el panel web subiendo imágenes. El backend procesa la imagen con el modelo ML TFLite y retorna la estimación.

### Endpoint Backend

**POST** `/api/v1/ml/estimate`

**Autenticación:** Requerida (JWT Bearer Token)

**Content-Type:** `multipart/form-data`

**Request:**
- `image` (File, required): Imagen del bovino (JPEG/PNG/WEBP)
- `breed` (string, required): Raza
- `animal_id` (UUID, optional): ID del animal si existe

**Response:**
```json
{
  "id": "2e0a53d6-86c0-4ae8-b402-ae09233861b7",
  "animal_id": "550e8400-e29b-41d4-a716-446655440000",
  "breed": "nelore",
  "estimated_weight": 289.25,
  "estimated_weight_kg": 289.25,
  "confidence_score": 0.92,
  "confidence": 0.92,
  "ml_model_version": "1.0.0-deep_learning_tflite",
  "processing_time_ms": 397,
  "image_path": "web_uploads/550e8400.../cow.jpg",
  "method": "strategy_based",
  "meets_quality_criteria": true,
  "timestamp": "2025-11-30T14:54:25.964158"
}
```

### Servicio Frontend

**Archivo:** `src/services/weight-estimations/estimateWeightFromImage.js`

```javascript
import apiClient from '../../api/axiosClient';

export const estimateWeightFromImage = async (imageFile, breed, animalId = null) => {
  const formData = new FormData();
  formData.append('image', imageFile);
  formData.append('breed', breed);
  if (animalId) {
    formData.append('animal_id', animalId);
  }

  const response = await apiClient.post('/api/v1/ml/estimate', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};
```

### Vista: WeightEstimationFromWebView

**Flujo:**
1. Usuario selecciona imagen (drag & drop o botón)
2. Usuario selecciona raza (opcional, pero recomendado)
3. Usuario selecciona animal (opcional)
4. Click en "Estimar"
5. Mostrar resultado: peso, confianza, tiempo de procesamiento
6. Opción de guardar estimación

**Componente:**
```javascript
import React, { useState } from 'react';
import { estimateWeightFromImage } from '../../services/weight-estimations/estimateWeightFromImage';
import ImageUploader from '../../components/organisms/CreateWeightEstimation/ImageUploader';
import EstimationResult from '../../components/organisms/CreateWeightEstimation/EstimationResult';

const WeightEstimationFromWebView = () => {
  const [imageFile, setImageFile] = useState(null);
  const [breed, setBreed] = useState('');
  const [animalId, setAnimalId] = useState(null);
  const [estimation, setEstimation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleEstimate = async () => {
    if (!imageFile || !breed) {
      setError('Por favor selecciona una imagen y una raza');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await estimateWeightFromImage(imageFile, breed, animalId);
      setEstimation(result);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al estimar peso');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <ImageUploader
        onImageSelected={setImageFile}
        selectedImage={imageFile}
      />
      <BreedSelector value={breed} onChange={setBreed} />
      <CattleSelector value={animalId} onChange={setAnimalId} />
      <Button onClick={handleEstimate} disabled={loading}>
        {loading ? 'Estimando...' : 'Estimar Peso'}
      </Button>
      {estimation && <EstimationResult estimation={estimation} />}
      {error && <Alert severity="error">{error}</Alert>}
    </div>
  );
};
```

### Componentes Requeridos

#### ImageUploader
- Drag & drop para imágenes
- Preview de imagen
- Validación de formato (JPEG, PNG, WEBP)
- Validación de tamaño (máx. 10MB)

#### EstimationResult
- Muestra peso estimado destacado
- Barra de confianza
- Información de ML (versión, método)
- Tiempo de procesamiento
- Botón para guardar estimación

---

## 🐄 Trazabilidad del Ganado

### Vista de Detalle: CattleDetailView

**Endpoint Backend:** `GET /api/v1/animals/{animal_id}`

**Información Mostrada:**
1. **Datos Generales**
   - Caravana, nombre, raza, género
   - Fecha de nacimiento, edad
   - Estado actual
   - Foto del animal

2. **Timeline de Eventos**
   - Registro del animal
   - Nacimiento
   - Estimaciones de peso
   - Cambios de estado
   - Observaciones

3. **Linaje**
   - Padre (si existe)
   - Madre (si existe)
   - Descendientes (hijos)

4. **Historial de Pesos**
   - Gráfico de evolución
   - Tabla de estimaciones
   - Cálculo de GDP (Ganancia Diaria Promedio)

### Timeline de Eventos

**Endpoint Backend:** `GET /api/v1/animals/{animal_id}/timeline`

**Response:**
```json
{
  "animal_id": "550e8400-e29b-41d4-a716-446655440000",
  "events": [
    {
      "type": "registration",
      "date": "2024-12-20T10:00:00Z",
      "description": "Animal registrado"
    },
    {
      "type": "weight_estimation",
      "date": "2024-12-20T10:25:00Z",
      "description": "Peso estimado: 487.3 kg",
      "weight_kg": 487.3,
      "confidence": 0.97
    }
  ]
}
```

**Componente:** `CattleTraceabilityTimeline`
- Visualización cronológica de eventos
- Filtros por tipo de evento
- Iconos por tipo de evento
- Enlaces a detalles (ej: ver estimación completa)

### Linaje

**Endpoint Backend:** `GET /api/v1/animals/{animal_id}/lineage`

**Response:**
```json
{
  "animal_id": "550e8400-e29b-41d4-a716-446655440000",
  "father": {
    "id": "aa0e8400-e29b-41d4-a716-446655440000",
    "ear_tag": "HG-NEL-001",
    "breed": "nelore"
  },
  "mother": {
    "id": "bb0e8400-e29b-41d4-a716-446655440000",
    "ear_tag": "HG-BRA-002",
    "breed": "brahman"
  },
  "offspring": []
}
```

**Componente:** `CattleLineageTree`
- Árbol genealógico visual
- Navegación a padres/hijos
- Información de razas

### Historial de Pesos

**Endpoint Backend:** `GET /api/v1/weighings/animal/{animal_id}`

**Componente:** `CattleWeightHistoryChart`
- Gráfico de línea (recharts)
- Tabla de estimaciones
- Filtros por fecha
- Cálculo de GDP

**Transformador:** `src/utils/transformers/weightEstimationToChartData.js`

```javascript
export const weightEstimationToChartData = (estimations) => {
  return estimations.map((est) => ({
    date: new Date(est.timestamp),
    weight: est.estimated_weight_kg,
    confidence: est.confidence,
    label: `${est.estimated_weight_kg} kg`,
  }));
};
```

---

## 📊 Sistema de Reportes

### Endpoints Backend

Todos los reportes requieren autenticación y retornan archivos como `StreamingResponse`.

#### 1. Reporte de Trazabilidad Individual

**POST** `/api/v1/reports/traceability/{animal_id}`

**Request:**
```json
{
  "format": "pdf"  // o "excel"
}
```

**Response:** Archivo PDF o Excel descargable

**Servicio:** `src/services/reports/generateTraceabilityReport.js`

```javascript
import apiClient from '../../api/axiosClient';

export const generateTraceabilityReport = async (animalId, format = 'pdf') => {
  const response = await apiClient.post(
    `/api/v1/reports/traceability/${animalId}`,
    { format },
    {
      responseType: 'blob', // Importante para descargar archivo
    }
  );

  // Crear URL del blob y descargar
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `trazabilidad_${animalId}.${format}`);
  document.body.appendChild(link);
  link.click();
  link.remove();
};
```

#### 2. Reporte de Inventario

**POST** `/api/v1/reports/inventory`

**Request:**
```json
{
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "format": "excel",
  "status": "active",
  "breed": "brahman",
  "date_from": "2024-01-01T00:00:00Z",
  "date_to": "2024-12-31T23:59:59Z"
}
```

#### 3. Reporte de Movimientos

**POST** `/api/v1/reports/movements`

**Request:**
```json
{
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",
  "format": "pdf",
  "movement_type": "sold",  // "sold", "deceased", o null (todos)
  "date_from": "2024-01-01T00:00:00Z",
  "date_to": "2024-12-31T23:59:59Z"
}
```

#### 4. Reporte de Crecimiento

**POST** `/api/v1/reports/growth`

**Request:**
```json
{
  "animal_id": "550e8400-e29b-41d4-a716-446655440000",  // Opcional
  "farm_id": "770e8400-e29b-41d4-a716-446655440000",  // Opcional (si no animal_id)
  "format": "excel"
}
```

### Componente: CattleReportGenerator

**Uso en CattleDetailView:**

```javascript
import { generateTraceabilityReport } from '../../services/reports/generateTraceabilityReport';

const handleGenerateReport = async (format) => {
  try {
    await generateTraceabilityReport(animalId, format);
    showSuccess('Reporte generado exitosamente');
  } catch (error) {
    showError('Error al generar reporte');
  }
};

// En el componente
<Button
  onClick={() => handleGenerateReport('pdf')}
  startIcon={<PictureAsPdfIcon />}
>
  Generar Reporte PDF
</Button>
```

---

## 🔐 Autenticación y Autorización

### Roles del Sistema

- **Administrador**: Acceso completo
- **Usuario**: Dashboard, Ganado, Estimaciones, Reportes
- **Invitado**: Solo Dashboard (lectura)

### Protección de Rutas

**Archivo:** `src/components/auth/ProtectedRoute.js`

```javascript
import { Navigate } from 'react-router-dom';
import { useSelector } from 'react-redux'; // O tu sistema de estado

const ProtectedRoute = ({ children, requiredRoles = [] }) => {
  const user = useSelector((state) => state.auth.user);

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (requiredRoles.length > 0 && !requiredRoles.includes(user.role.name)) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};
```

---

## ✅ Checklist de Implementación

### Fase 1: Configuración y Autenticación ✅ COMPLETADO
- [x] Configurar axiosClient con interceptors
- [x] Implementar servicio de login
- [x] Protección de rutas
- [x] Manejo de tokens JWT
- [x] Variables de entorno configuradas
- [x] Constantes (BREEDS, STATUS, GENDERS)

### Fase 2: Vistas Principales ✅ COMPLETADO
- [x] DashboardView con estadísticas
- [x] CattleView con lista de animales
- [x] CattleDetailView con trazabilidad completa
- [x] WeightEstimationsView
- [x] WeightEstimationFromWebView
- [x] SyncStatusView (solo visualización)
- [x] UserView y RoleView
- [x] FarmView

### Fase 3: Servicios API ✅ COMPLETADO
- [x] Servicios de autenticación (login, logout, getCurrentUser, isAuthenticated)
- [x] Servicios de animales (CRUD completo + filtros + paginación)
  - [x] getAllCattle (con filtros y paginación)
  - [x] getCattleById
  - [x] createCattle
  - [x] updateCattle
  - [x] deleteCattle
  - [x] getAnimalTimeline
  - [x] getAnimalLineage
- [x] Servicios de estimaciones
  - [x] getAllWeightEstimations (con paginación)
  - [x] getWeightEstimationById
  - [x] getWeightEstimationsByCattleId (con paginación)
  - [x] estimateWeightFromImage (ML desde web)
  - [x] createWeightEstimation
- [x] Servicios ML
  - [x] estimateWeightFromImage (corregido con animal_id)
  - [x] getModelsStatus
  - [x] getMLHealth
- [x] Servicios de reportes (4 tipos desde backend)
  - [x] generateTraceabilityReport
  - [x] generateInventoryReport
  - [x] generateMovementReport
  - [x] generateGrowthReport
- [x] Servicios de sincronización (solo lectura)
  - [x] getSyncHealth
  - [x] getSyncStats
- [x] Servicios de Farms (CRUD completo)
  - [x] getAllFarms (con paginación)
  - [x] getFarmById
  - [x] createFarm
  - [x] updateFarm
  - [x] deleteFarm
- [x] Servicios de Users (CRUD completo)
  - [x] getAllUsers (con paginación)
  - [x] getUserById
  - [x] createUser
  - [x] updateUser
  - [x] deleteUser
- [x] Servicios de Roles (CRUD completo)
  - [x] getAllRoles (con paginación)
  - [x] getRoleById
  - [x] createRole
  - [x] updateRole
  - [x] deleteRole
- [x] Servicios de Alertas (CRUD completo)
  - [x] createAlert
  - [x] getAllAlerts (con filtros y paginación)
  - [x] getAlertById
  - [x] updateAlert
  - [x] deleteAlert
  - [x] getTodayAlerts
  - [x] getUpcomingAlerts
  - [x] getPendingAlerts
  - [x] getScheduledAlerts
  - [x] getAlertAnimals

### Fase 4: Componentes de Trazabilidad ✅ COMPLETADO
- [x] CattleTraceabilityTimeline
- [x] CattleLineageTree
- [x] CattleWeightHistoryChart (tabla implementada)
- [x] Servicios de timeline y lineage implementados
- [ ] Gráfico de evolución de peso (recharts) - Opcional para mejoras visuales

### Fase 5: Componentes de Estimación ML ✅ COMPLETADO
- [x] ImageUploader
- [x] EstimationResult
- [x] CreateWeightEstimation organism
- [x] Integración con backend `/api/v1/ml/estimate`
- [x] Manejo de errores robusto
- [x] Validación de imágenes

### Fase 6: Sistema de Reportes ✅ COMPLETADO
- [x] Generador de reporte de trazabilidad (desde backend)
- [x] Generador de reporte de inventario (desde backend)
- [x] Generador de reporte de movimientos (desde backend)
- [x] Generador de reporte de crecimiento (desde backend)
- [x] Manejo de descarga de archivos (blob download)

### Fase 7: Búsqueda y Filtros Avanzados ⚠️ PARCIAL
- [x] Filtros múltiples implementados en servicios (raza, género, estado, farm_id)
- [x] Paginación implementada en todos los listados
- [ ] Búsqueda avanzada en CattleView (UI pendiente)
- [ ] Ordenamiento (UI pendiente)
- [x] Filtros disponibles en backend y servicios

### Fase 8: Endpoints de Recursos ✅ COMPLETADO
- [x] GET `/api/v1/resources/images/{image_path}` - Implementado en backend
- [x] Utilidad `getImageUrl()` para construir URLs de imágenes
- [x] Integración en componentes: ImageGallery, EstimationImageCard, EstimationImage
- [x] Configuración de Nginx para servir recursos con caché

### Fase 9: Mejoras y Optimizaciones ⚠️ PARCIAL
- [x] Manejo de errores robusto (implementado en todos los servicios)
- [x] Loading states (implementados en varios componentes)
- [x] Caché de datos para dashboard (15 minutos TTL)
- [x] Caché de estimaciones de peso
- [x] Invalidación de caché sincronizada entre módulos
- [ ] Optimización de imágenes (mejora futura)
- [ ] Testing (pendiente)

---

## 📝 Notas Importantes

1. **Sincronización**: Los endpoints de sincronización (`/api/v1/sync/*`) son principalmente para la app móvil. El panel web solo muestra estado (health check, stats).

2. **Estimación ML**: 
   - Mobile usa `/api/v1/ml/predict` (sin guardar)
   - Web usa `/api/v1/ml/estimate` (con guardado automático)

3. **Timestamps**: Todos los timestamps están en formato ISO 8601 UTC

4. **UUIDs**: Todos los IDs son UUIDs v4

5. **Formatos de Imagen**: JPEG, PNG, WEBP (para estimaciones ML)

6. **Razas Válidas**: Solo las 7 razas definidas en el backend

---

## 🔗 Referencias

- **Documentación API Backend**: [`API_INTEGRATION_GUIDE.md`](./API_INTEGRATION_GUIDE.md)
- **Documentación Modelo ML**: [`../backend/INTEGRATION_GUIDE.md`](../../backend/INTEGRATION_GUIDE.md)
- **Documentación Mobile Sync**: [`FLUTTER_SYNC_GUIDE.md`](./FLUTTER_SYNC_GUIDE.md)

---

---

## 📊 Análisis de Cobertura de Endpoints (Excluyendo Reportes)

### ✅ Endpoints Implementados (100% de cobertura para Web)

#### Autenticación
- ✅ POST `/api/v1/auth/login` - Implementado en `authService.js`

#### Machine Learning (Web)
- ✅ POST `/api/v1/ml/estimate` - Implementado en `estimateWeightFromImage.js`
- ✅ GET `/api/v1/ml/models/status` - Implementado en `getModelsStatus.js`
- ✅ GET `/api/v1/ml/health` - Implementado en `getMLHealth.js`

#### Gestión de Animales
- ✅ POST `/api/v1/animals` - Implementado en `createCattle.js`
- ✅ GET `/api/v1/animals` - Implementado en `getAllCattle.js` y `getAnimalsByCriteria.js`
- ✅ GET `/api/v1/animals/{animal_id}` - Implementado en `getCattleById.js`
- ✅ PUT `/api/v1/animals/{animal_id}` - Implementado en `updateCattle.js`
- ✅ DELETE `/api/v1/animals/{animal_id}` - Implementado en `deleteCattle.js`
- ✅ GET `/api/v1/animals/{animal_id}/timeline` - Implementado en `getAnimalTimeline.js`
- ✅ GET `/api/v1/animals/{animal_id}/lineage` - Implementado en `getAnimalLineage.js`

#### Historial de Pesajes
- ✅ GET `/api/v1/weighings/animal/{animal_id}` - Implementado en `getWeightEstimationsByCattleId.js`
- ✅ GET `/api/v1/weighings/{weighing_id}` - Implementado en `getWeightEstimationById.js`
- ✅ GET `/api/v1/weighings` - Implementado en `getAllWeightEstimations.js` y `getWeightEstimationsByCriteria.js`
- ✅ POST `/api/v1/weighings` - Implementado en `createWeightEstimation.js`
- ✅ DELETE `/api/v1/weighings/{weighing_id}` - Implementado en `deleteWeightEstimation.js`

#### Gestión de Fincas
- ✅ POST `/api/v1/farms` - Implementado en `createFarm.js`
- ✅ GET `/api/v1/farms` - Implementado en `getAllFarms.js` y `getFarmsByCriteria.js`
- ✅ GET `/api/v1/farms/{farm_id}` - Implementado en `getFarmById.js`
- ✅ PUT `/api/v1/farms/{farm_id}` - Implementado en `updateFarm.js`
- ✅ DELETE `/api/v1/farms/{farm_id}` - Implementado en `deleteFarm.js`

#### Gestión de Usuarios
- ✅ POST `/api/v1/users` - Implementado en `createUser.js`
- ✅ GET `/api/v1/users` - Implementado en `getAllUsers.js` y `getUsersByCriteria.js`
- ✅ GET `/api/v1/users/{user_id}` - Implementado en `getUserById.js`
- ✅ PUT `/api/v1/users/{user_id}` - Implementado en `updateUser.js`
- ✅ DELETE `/api/v1/users/{user_id}` - Implementado en `deleteUser.js`

#### Gestión de Roles
- ✅ POST `/api/v1/roles` - Implementado en `createRole.js`
- ✅ GET `/api/v1/roles` - Implementado en `getAllRoles.js`
- ✅ GET `/api/v1/roles/{role_id}` - Implementado en `getRoleById.js`
- ✅ PUT `/api/v1/roles/{role_id}` - Implementado en `updateRole.js`
- ✅ DELETE `/api/v1/roles/{role_id}` - Implementado en `deleteRole.js`

#### Alertas y Cronograma
- ✅ POST `/api/v1/alerts` - Implementado en `createAlert.js`
- ✅ GET `/api/v1/alerts` - Implementado en `getAllAlerts.js`
- ✅ GET `/api/v1/alerts/{alert_id}` - Implementado en `getAlertById.js`
- ✅ PUT `/api/v1/alerts/{alert_id}` - Implementado en `updateAlert.js`
- ✅ DELETE `/api/v1/alerts/{alert_id}` - Implementado en `deleteAlert.js`
- ✅ GET `/api/v1/alerts/today` - Implementado en `getTodayAlerts.js`
- ✅ GET `/api/v1/alerts/upcoming` - Implementado en `getUpcomingAlerts.js`
- ✅ GET `/api/v1/alerts/pending` - Implementado en `getPendingAlerts.js`
- ✅ GET `/api/v1/alerts/scheduled` - Implementado en `getScheduledAlerts.js`
- ✅ GET `/api/v1/alerts/{alert_id}/animals` - Implementado en `getAlertAnimals.js`

#### Sincronización (Solo lectura para Web)
- ✅ GET `/api/v1/sync/health` - Implementado en `getSyncHealth.js`
- ✅ GET `/api/v1/sync/stats` - Implementado en `getSyncStats.js`
- ✅ POST `/api/v1/sync/cattle` - Implementado en `syncCattleBatch.js` (para administración)
- ✅ POST `/api/v1/sync/weight-estimations` - Implementado en `syncWeightEstimationsBatch.js` (para administración)

#### Recursos Estáticos
- ✅ GET `/api/v1/resources/images/{image_path}` - Implementado en backend, usado a través de `getImageUrl.js`

### ⚠️ Endpoints No Aplicables al Frontend Web
- ❌ POST `/api/v1/ml/predict` - Solo para Mobile (sin guardar en BD)
- ❌ Endpoints de sincronización POST - Principalmente para Mobile, pero implementados para administración

### 📝 Notas sobre Implementación

1. **Dashboard**: No existe un endpoint específico `/api/v1/dashboard`. Las estadísticas se calculan desde múltiples llamadas a:
   - `getAnimalsByCriteria()` para obtener total de animales y razas
   - `getWeightEstimationsByCriteria()` para obtener total de estimaciones y peso promedio
   - ✅ Implementación correcta y eficiente con caché

2. **Recursos de Imágenes**: El endpoint `/api/v1/resources/images/{image_path}` está implementado en el backend y se utiliza a través de la utilidad `getImageUrl.js` en todos los componentes que muestran imágenes.

3. **Caché**: Se ha implementado un sistema de caché para:
   - Dashboard (TTL: 15 minutos)
   - Estimaciones de peso
   - Invalidación automática cuando se crean/actualizan estimaciones

4. **Filtros y Búsqueda**: Todos los servicios soportan filtros y paginación. La UI de búsqueda avanzada está pendiente pero los servicios están listos.

---

**Última actualización**: 2025-01-02  
**Versión Frontend**: 1.0.0  
**React Version**: 18+  
**Material-UI Version**: 5+  
**Estado**: ✅ **TODOS LOS ENDPOINTS WEB IMPLEMENTADOS** (100% - Excluyendo reportes como solicitado)

