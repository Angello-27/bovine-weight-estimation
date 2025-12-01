// frontend/src/services/role/getRoleById.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene un rol por su ID
 * @param {string} roleId - ID del rol
 * @returns {Promise<Object>} Datos del rol
 */
const getRoleById = async (roleId) => {
    try {
        const response = await apiClient.get(`/role/${roleId}`);
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
        
        if (error.response && error.response.status === 404) {
            throw new Error('Recurso no encontrado.');
        } else {
            throw new Error(backendMessage || 'Ocurrió un error. Por favor intenta de nuevo.');
        }
    }
};

export { getRoleById };

