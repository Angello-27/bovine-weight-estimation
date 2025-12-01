// frontend/src/services/weight-estimations/getWeightEstimationsByCriteria.js

import apiClient from '../../api/axiosClient';

/**
 * Busca estimaciones de peso por criterios de filtrado
 * @param {Object} filters - Criterios de filtrado (animal_id, breed)
 * @param {Object} pagination - Parámetros de paginación (page, page_size)
 * @returns {Promise<Object>} Objeto con total, weighings, page, page_size
 */
const getWeightEstimationsByCriteria = async (filters = {}, pagination = {}) => {
    try {
        const params = {
            ...pagination,
        };
        
        // Agregar filtros opcionales solo si están presentes
        if (filters.animal_id) params.animal_id = filters.animal_id;
        if (filters.breed) params.breed = filters.breed;

        const response = await apiClient.get('/api/v1/weighings/by-criteria', { params });
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
        } else {
            throw new Error(backendMessage || 'Ocurrió un error. Por favor intenta de nuevo.');
        }
    }
};

export { getWeightEstimationsByCriteria };

