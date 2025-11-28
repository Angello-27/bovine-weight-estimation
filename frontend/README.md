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
│   ├── api/            # Configuración de axios
│   ├── components/     # Componentes (Atomic Design)
│   ├── config/         # Configuración (rutas, temas, constantes)
│   ├── containers/     # Lógica de negocio
│   ├── services/       # Servicios API
│   ├── templates/       # Templates de páginas
│   ├── utils/          # Utilidades
│   └── views/          # Vistas principales
└── package.json
```

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

## 🔗 Enlaces Útiles

- [React Documentation](https://react.dev/)
- [Material-UI Documentation](https://mui.com/)
- [React Router Documentation](https://reactrouter.com/)

