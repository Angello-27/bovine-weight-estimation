// src/services/weight-estimations/getAllWeightEstimations.js
import apiClient from '../../api/axiosClient';

/**
 * Obtiene todas las estimaciones de peso (lista general)
 * Nota: Según la API, el endpoint GET /api/v1/weighings puede no estar disponible.
 * Usa getWeightEstimationsByCattleId() para obtener estimaciones por animal.
 * 
 * @param {Object} [params] - Parámetros de consulta opcionales
 * @param {number} [params.page] - Número de página
 * @param {number} [params.page_size] - Tamaño de página
 * @returns {Promise<Object>} Lista de estimaciones de peso con paginación
 */
const getAllWeightEstimations = async (params = {}) => {
    try {
        const queryParams = new URLSearchParams();
        if (params.page) queryParams.append('page', params.page);
        if (params.page_size) queryParams.append('page_size', params.page_size);
        
        const queryString = queryParams.toString();
        const url = `/api/v1/weighings${queryString ? `?${queryString}` : ''}`;
        
        const response = await apiClient.get(url);
        return response.data;
    } catch (error) {
        console.error('Error al obtener estimaciones de peso:', error);
        if (error.response && error.response.status === 404) {
            throw new Error('Endpoint no disponible. Use getWeightEstimationsByCattleId() para obtener estimaciones por animal.');
        }
        throw error;
    }
};

export default getAllWeightEstimations;

