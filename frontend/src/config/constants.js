// src/config/constants.js
/**
 * Constantes de la aplicación
 * 
 * Nota: Para configuración de rutas y sidebar, ver routesConfig.js
 */

export const drawer = {
    width: 304,
};

export const radioButtonsRoles = [
    { id: "Administrador", label: "Administrador" },
    { id: "Usuario", label: "Usuario" },
    { id: "Invitado", label: "Invitado" }
];

import { getAllSidebarItems } from './routesConfig';
export const sidebarItems = getAllSidebarItems();

// Razas válidas de bovinos (7 razas exactas del sistema)
export const BREEDS = [
    'nelore',
    'brahman',
    'guzerat',
    'senepol',
    'girolando',
    'gyr_lechero',
    'sindi',
];

// Estados posibles de un animal
export const ANIMAL_STATUS = ['active', 'inactive', 'sold', 'deceased'];

// Géneros posibles de un animal
export const GENDERS = ['male', 'female'];

// Configuración de API
export const API_VERSION = 'v1';
export const API_BASE_URL = import.meta.env.REACT_APP_API_URL || 'http://localhost:8000';

