// src/services/weight-estimations/getWeightEstimationById.js
import apiClient from '../../api/axiosClient';

/**
 * Obtiene una estimación de peso por su ID
 * @param {string} id - ID de la estimación
 * @returns {Promise<Object>} Datos de la estimación
 */
const getWeightEstimationById = async (id) => {
    try {
        const response = await apiClient.get(`/api/v1/weighings/${id}`);
        return response.data;
    } catch (error) {
        console.error(`Error al obtener estimación ${id}:`, error);
        throw error;
    }
};

export default getWeightEstimationById;

