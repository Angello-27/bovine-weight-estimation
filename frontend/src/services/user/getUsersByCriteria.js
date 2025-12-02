// frontend/src/services/user/getUsersByCriteria.js

import apiClient from '../../api/axiosClient';

/**
 * Busca usuarios por criterios de filtrado
 * @param {Object} filters - Criterios de filtrado (role_id, is_active, farm_id)
 * @param {Object} pagination - Parámetros de paginación (skip, limit)
 * @returns {Promise<Object>} Objeto con total, users, page, page_size
 */
const getUsersByCriteria = async (filters = {}, pagination = {}) => {
    try {
        const params = {
            ...pagination,
            ...filters,
        };
        
        const response = await apiClient.get('/user/by-criteria', { params });
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
        
        if (error.response && (error.response.status === 400 || error.response.status === 422)) {
            const message = backendMessage || 'Los datos proporcionados son incorrectos.';
            throw new Error(message);
        } else {
            throw new Error(backendMessage || 'Ocurrió un error. Por favor intenta de nuevo.');
        }
    }
};

export { getUsersByCriteria };

