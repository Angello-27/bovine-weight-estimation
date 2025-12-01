// frontend/src/services/role/createRole.js

import apiClient from '../../api/axiosClient';

/**
 * Crea un nuevo rol
 * @param {Object} roleData - Datos del rol (name, description, priority, permissions)
 * @returns {Promise<Object>} Datos del rol creado
 */
const createRole = async (roleData) => {
    try {
        const payload = {
            name: roleData.name,
            description: roleData.description || null,
            priority: roleData.priority || 'Invitado',
            permissions: roleData.permissions || [],
        };
        const response = await apiClient.post('/role', payload);
        return response.data;
    } catch (error) {
        // Extraer mensaje del backend si está disponible
        let backendMessage = null;
        if (error.response?.data?.detail) {
            const detail = error.response.data.detail;
            if (typeof detail === 'string') {
                backendMessage = detail;
            } else if (Array.isArray(detail) && detail.length > 0) {
                backendMessage = detail[0]?.msg || detail[0]?.message || String(detail[0]);
            } else if (typeof detail === 'object') {
                backendMessage = detail.message || detail.msg || String(detail);
            }
        }
        
        if (error.response && error.response.status === 400) {
            const message = backendMessage || 'Los datos proporcionados son incorrectos.';
            throw new Error(message);
        } else if (error.response && error.response.status === 404) {
            throw new Error('Recurso no encontrado.');
        } else {
            throw new Error(backendMessage || 'Ocurrió un error. Por favor intenta de nuevo.');
        }
    }
};

export { createRole };

