// frontend/src/services/farm/getAllFarms.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene todas las haciendas del sistema
 * @param {Object} params - Parámetros opcionales (skip, limit, owner_id)
 * @returns {Promise<Object>} Objeto con total, farms, page, page_size
 */
const getAllFarms = async (params = {}) => {
    try {
        const response = await apiClient.get('/farm', { params });
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Error al obtener las haciendas. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar obtener las haciendas. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getAllFarms };

