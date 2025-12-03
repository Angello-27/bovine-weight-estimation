// frontend/src/services/farm/getAllFarms.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene todas las haciendas del sistema
 * @param {Object} params - Parámetros opcionales (skip, limit)
 * @returns {Promise<Object>} Objeto con total, farms, page, page_size
 */
const getAllFarms = async (params = {}) => {
    try {
        const response = await apiClient.get('/api/v1/farms', { params });
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
            const message = backendMessage || 'Error al obtener las haciendas. Por favor verifica e intenta de nuevo.';
            throw new Error(message);
        } else {
            throw new Error(backendMessage || 'Ocurrió un error al intentar obtener las haciendas. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getAllFarms };

