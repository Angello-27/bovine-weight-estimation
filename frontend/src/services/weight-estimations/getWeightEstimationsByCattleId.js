// src/services/weight-estimations/getWeightEstimationsByCattleId.js
import getAllWeightEstimations from './getAllWeightEstimations';

/**
 * Obtiene todas las estimaciones de peso de un animal específico
 * @param {string} cattleId - ID del animal
 * @returns {Promise<Array>} Lista de estimaciones del animal
 */
const getWeightEstimationsByCattleId = async (cattleId) => {
    try {
        return await getAllWeightEstimations({ cattle_id: cattleId });
    } catch (error) {
        console.error(`Error al obtener estimaciones del animal ${cattleId}:`, error);
        throw error;
    }
};

export default getWeightEstimationsByCattleId;

