// src/services/weight-estimations/getAllWeightEstimations.js
import apiClient from '../../api/axiosClient';

/**
 * Obtiene todas las estimaciones de peso
 * @param {Object} [params] - Parámetros de consulta opcionales
 * @param {string} [params.cattle_id] - Filtrar por ID de animal
 * @returns {Promise<Array>} Lista de estimaciones de peso
 */
const getAllWeightEstimations = async (params = {}) => {
    try {
        const response = await apiClient.get('/api/v1/weighings', { params });
        return response.data;
    } catch (error) {
        console.error('Error al obtener estimaciones de peso:', error);
        throw error;
    }
};

export default getAllWeightEstimations;

