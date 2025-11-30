# Frontend - Panel Administrativo Bovino

Panel administrativo web para el sistema de estimación de peso bovino desarrollado con React.

## 🚀 Inicio Rápido

### Prerrequisitos

- **Node.js**: v16.0.0 o superior
- **npm**: v7.0.0 o superior (o yarn)

### Instalación

1. **Navegar al directorio del frontend:**
```bash
cd frontend
```

2. **Instalar dependencias:**
```bash
npm install
```

O si usas yarn:
```bash
yarn install
```

### Configuración

1. **Crear archivo de variables de entorno:**
```bash
cp .env.example .env
```

2. **Editar `.env` y configurar la URL del backend:**
```env
REACT_APP_API_URL=http://localhost:8000
```

> **Nota**: Si el backend está en otro puerto o servidor, actualiza `REACT_APP_API_URL` en el archivo `.env`.

### Ejecutar en Desarrollo

```bash
npm run dev
```

O con yarn:
```bash
yarn dev
```

El proyecto se abrirá automáticamente en `http://localhost:3000` en tu navegador.

### Scripts Disponibles

- **`npm run dev`** o **`npm start`** - Inicia el servidor de desarrollo con Vite
- **`npm run build`** - Crea una versión de producción optimizada
- **`npm run preview`** - Previsualiza la build de producción
- **`npm test`** - Ejecuta los tests (con Vitest)

### Construir para Producción

```bash
npm run build
```

Esto crea una carpeta `build/` con los archivos optimizados listos para desplegar.

## 📁 Estructura del Proyecto

```
frontend/
├── public/              # Archivos estáticos
├── src/
│   ├── api/            # Configuración de axios (cliente HTTP con middleware)
│   │   └── axiosClient.js  # Cliente HTTP con interceptores (middleware)
│   ├── components/     # Componentes (Atomic Design)
│   │   ├── atoms/      # Componentes básicos (botones, inputs)
│   │   ├── molecules/  # Componentes compuestos (ProtectedRoute, formularios)
│   │   ├── organisms/  # Componentes complejos (listas, tablas, formularios completos)
│   │   ├── layout/     # Componentes de layout (Header, Sidebar, Footer)
│   │   └── auth/       # Componentes de autenticación (legacy, usar molecules/)
│   ├── config/         # Configuración centralizada
│   │   ├── routes.js          # Definición de rutas React Router
│   │   ├── routesConfig.js    # Configuración centralizada de rutas y sidebar
│   │   ├── constants.js       # Constantes de la aplicación (razas, estados)
│   │   ├── theme/             # Configuración de temas
│   │   └── themes.js          # Temas Material-UI
│   ├── containers/     # Hooks de lógica de negocio (casos de uso)
│   │   ├── auth/       # Casos de uso de autenticación
│   │   ├── cattle/     # Casos de uso de ganado
│   │   ├── weight-estimations/  # Casos de uso de estimaciones
│   │   ├── farm/       # Casos de uso de fincas
│   │   ├── user/       # Casos de uso de usuarios
│   │   ├── role/       # Casos de uso de roles
│   │   ├── sync/       # Casos de uso de sincronización
│   │   └── dashboard/  # Casos de uso del dashboard
│   ├── services/       # Servicios API (llamadas al backend)
│   │   ├── auth/       # Servicios de autenticación
│   │   │   ├── authService.js  # Casos de uso: login, logout, getCurrentUser
│   │   │   └── AuthContext.js  # Context API para estado de autenticación
│   │   ├── cattle/     # Servicios de ganado
│   │   ├── weight-estimations/  # Servicios de estimaciones
│   │   ├── farm/       # Servicios de fincas
│   │   ├── user/       # Servicios de usuarios
│   │   ├── role/       # Servicios de roles
│   │   ├── sync/       # Servicios de sincronización
│   │   └── reports/    # Servicios de reportes
│   ├── templates/      # Templates de páginas (layouts de vistas)
│   ├── utils/          # Utilidades (transformers, helpers)
│   └── views/          # Vistas principales (páginas de la aplicación)
└── package.json
```

### 📚 Organización por Responsabilidades

**API (`src/api/`)**: Cliente HTTP con middleware (interceptores)
- `axiosClient.js`: Configuración base, interceptores de request/response

**Services (`src/services/`)**: Casos de uso que interactúan con el backend
- Organizados por dominio: `auth/`, `cattle/`, `weight-estimations/`, etc.
- Cada servicio representa un caso de uso específico

**Containers (`src/containers/`)**: Hooks personalizados que orquestan servicios
- Organizados por dominio, igual que services
- Combinan múltiples servicios y lógica de estado local

**Components (`src/components/`)**: UI components siguiendo Atomic Design
- **Atoms**: Componentes básicos reutilizables
- **Molecules**: Componentes compuestos (ej: `ProtectedRoute`)
- **Organisms**: Componentes complejos con lógica propia
- **Layout**: Componentes estructurales (Header, Sidebar, Footer)

**Config (`src/config/`)**: Configuración centralizada
- `routesConfig.js`: Fuente única de verdad para rutas y sidebar
- `constants.js`: Constantes de la aplicación
- `routes.js`: Configuración de React Router

### 🔑 Principios de Organización

1. **Separación de Responsabilidades**: Services (API) → Containers (Lógica) → Components (UI)
2. **Atomic Design**: Componentes organizados por complejidad
3. **Single Source of Truth**: `routesConfig.js` centraliza rutas y sidebar
4. **Domain-Driven**: Services y Containers organizados por dominio de negocio

## 🔧 Configuración del Backend

El frontend se conecta al backend FastAPI. Asegúrate de que:

1. El backend esté corriendo en el puerto configurado (por defecto `http://localhost:8000`)
2. CORS esté habilitado en el backend para permitir peticiones desde `http://localhost:3000`

### Endpoints del Backend

- **Animals**: `/api/v1/animals`
- **Weight Estimations**: `/api/v1/weighings`
- **Sync**: `/api/v1/sync`

## 🐛 Solución de Problemas

### Error: "Module not found"
```bash
# Eliminar node_modules y reinstalar
rm -rf node_modules package-lock.json
npm install
```

### Error: "Port 3000 is already in use"
```bash
# Usar otro puerto
PORT=3001 npm start
```

### Error de conexión con el backend
- Verifica que el backend esté corriendo
- Revisa la URL en `.env` (REACT_APP_API_URL)
- Verifica CORS en el backend

## 📝 Notas

- El proyecto usa **Vite** como bundler (más rápido que Create React App)
- **Material-UI (MUI)** para componentes de UI
- **React Router** para navegación
- **Axios** para peticiones HTTP
- **Atomic Design** para estructura de componentes

## 📚 Documentación de Integración

> 📖 **Guía Completa de Integración**: Ver [`docs/integration/FRONTEND_INTEGRATION_GUIDE.md`](../docs/integration/FRONTEND_INTEGRATION_GUIDE.md)

Esta guía incluye:
- Integración completa con Backend FastAPI
- Uso de APIs REST
- Estimación de Peso desde Web (ML)
- Sistema de Trazabilidad
- Sistema de Reportes
- Autenticación y Autorización
- Checklist completo de implementación

## 🔗 Enlaces Útiles

- [React Documentation](https://react.dev/)
- [Material-UI Documentation](https://mui.com/)
- [React Router Documentation](https://reactrouter.com/)
- [Documentación API Backend](../docs/integration/API_INTEGRATION_GUIDE.md)

