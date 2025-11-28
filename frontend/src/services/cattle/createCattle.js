// src/services/cattle/createCattle.js
import apiClient from '../../api/axiosClient';

/**
 * Crea un nuevo animal
 * @param {Object} cattleData - Datos del animal a crear
 * @param {string} cattleData.ear_tag - Número de caravana (obligatorio)
 * @param {string} cattleData.breed - Raza (obligatorio)
 * @param {string} cattleData.birth_date - Fecha de nacimiento (obligatorio)
 * @param {string} cattleData.gender - Género: "male" | "female" (obligatorio)
 * @param {string} [cattleData.name] - Nombre del animal (opcional)
 * @param {string} [cattleData.color] - Color (opcional)
 * @param {number} [cattleData.birth_weight_kg] - Peso al nacer en kg (opcional)
 * @param {string} [cattleData.observations] - Observaciones (opcional)
 * @returns {Promise<Object>} Animal creado
 */
const createCattle = async (cattleData) => {
    try {
        const response = await apiClient.post('/api/v1/animals', cattleData);
        return response.data;
    } catch (error) {
        console.error('Error al crear animal:', error);
        throw error;
    }
};

export default createCattle;

