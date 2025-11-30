// frontend/src/config/routesConfig.js
/**
 * Configuración centralizada de rutas y sidebar
 * 
 * Esta configuración unifica:
 * - Definición de rutas con sus roles requeridos
 * - Configuración del sidebar con íconos y roles
 * - Evita duplicación entre routes.js y constants.js
 */

import DashboardIcon from '@mui/icons-material/Dashboard';
import PetsIcon from '@mui/icons-material/Pets';
import ScaleIcon from '@mui/icons-material/Scale';
import SyncIcon from '@mui/icons-material/Sync';
import BarChartIcon from '@mui/icons-material/BarChart';
import PeopleIcon from '@mui/icons-material/People';
import SecurityIcon from '@mui/icons-material/Security';
import FarmIcon from '@mui/icons-material/Business'; 
import AddCircleIcon from '@mui/icons-material/AddCircle';

/**
 * Definición de rutas de la aplicación
 * Cada ruta incluye: path, roles requeridos, y configuración para sidebar
 */
export const appRoutes = [
    {
        path: '/home',
        roles: ['Administrador', 'Usuario', 'Invitado'],
        sidebar: {
            text: 'Dashboard',
            icon: <DashboardIcon />,
            to: '/home',
        },
    },
    {
        path: '/cattle',
        roles: ['Administrador', 'Usuario'],
        sidebar: {
            text: 'Ganado',
            icon: <PetsIcon />,
            to: '/cattle',
        },
    },
    {
        path: '/weight-estimations',
        roles: ['Administrador', 'Usuario'],
        sidebar: {
            text: 'Estimaciones de Peso',
            icon: <ScaleIcon />,
            to: '/weight-estimations',
        },
    },
    {
        path: '/weight-estimations/estimate',
        roles: ['Administrador', 'Usuario'],
        sidebar: {
            text: 'Estimar Peso',
            icon: <AddCircleIcon />,
            to: '/weight-estimations/estimate',
        },
    },
    {
        path: '/sync',
        roles: ['Administrador'],
        sidebar: {
            text: 'Sincronización',
            icon: <SyncIcon />,
            to: '/sync',
        },
    },
    {
        path: '/users',
        roles: ['Administrador'],
        sidebar: {
            text: 'Usuarios',
            icon: <PeopleIcon />,
            to: '/users',
        },
    },
    {
        path: '/roles',
        roles: ['Administrador'],
        sidebar: {
            text: 'Roles',
            icon: <SecurityIcon />,
            to: '/roles',
        },
    },
    {
        path: '/farms',
        roles: ['Administrador'],
        sidebar: {
            text: 'Fincas',
            icon: <FarmIcon />,
            to: '/farms',
        },
    },
    {
        path: '/statistics',
        roles: ['Administrador', 'Usuario'],
        sidebar: {
            text: 'Estadísticas',
            icon: <BarChartIcon />,
            to: '/statistics',
        },
    },
];

/**
 * Obtiene los items del sidebar filtrados por rol
 * @param {string} userRole - Rol del usuario actual
 * @returns {Array} Items del sidebar visibles para el rol
 */
export const getSidebarItems = (userRole) => {
    return appRoutes
        .filter(route => route.sidebar && route.roles.includes(userRole))
        .map(route => route.sidebar)
        // Eliminar duplicados basados en 'to'
        .filter((item, index, self) => 
            index === self.findIndex(t => t.to === item.to)
        );
};

/**
 * Obtiene la configuración de una ruta específica
 * @param {string} path - Path de la ruta
 * @returns {Object|null} Configuración de la ruta o null si no existe
 */
export const getRouteConfig = (path) => {
    return appRoutes.find(route => route.path === path) || null;
};

/**
 * Verifica si un usuario tiene acceso a una ruta
 * @param {string} path - Path de la ruta
 * @param {string} userRole - Rol del usuario
 * @returns {boolean} true si tiene acceso
 */
export const hasAccess = (path, userRole) => {
    const route = getRouteConfig(path);
    return route ? route.roles.includes(userRole) : false;
};

/**
 * Obtiene todos los items del sidebar (sin filtrar por rol)
 * Útil para componentes que necesitan la lista completa
 */
export const getAllSidebarItems = () => {
    return appRoutes
        .filter(route => route.sidebar)
        .map(route => ({
            ...route.sidebar,
            roles: route.roles, // Incluir roles para validación en Sidebar component
        }))
        // Eliminar duplicados basados en 'to'
        .filter((item, index, self) => 
            index === self.findIndex(t => t.to === item.to)
        );
};

