// src/services/weight-estimations/getWeightEstimationsByCattleId.js
import apiClient from '../../api/axiosClient';

/**
 * Obtiene el historial completo de pesajes de un animal específico
 * @param {string} animalId - ID del animal
 * @param {number} page - Número de página (default: 1)
 * @param {number} pageSize - Tamaño de página (default: 50, max: 100)
 * @returns {Promise<Object>} Objeto con total, weighings, page, page_size
 */
const getWeightEstimationsByCattleId = async (animalId, page = 1, pageSize = 50) => {
    try {
        const params = new URLSearchParams();
        params.append('page', page);
        params.append('page_size', pageSize);
        
        const response = await apiClient.get(
            `/api/v1/weighings/animal/${animalId}?${params.toString()}`
        );
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Animal no encontrado');
        } else {
            throw new Error('Ocurrió un error al obtener el historial de pesajes. Por favor intenta de nuevo más tarde.');
        }
    }
};

export default getWeightEstimationsByCattleId;

