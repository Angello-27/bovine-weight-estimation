// src/services/cattle/getCattleById.js
import apiClient from '../../api/axiosClient';

/**
 * Obtiene un animal por su ID
 * @param {string} id - ID del animal
 * @returns {Promise<Object>} Datos del animal
 */
const getCattleById = async (id) => {
    try {
        const response = await apiClient.get(`/api/v1/animals/${id}`);
        return response.data;
    } catch (error) {
        console.error(`Error al obtener animal ${id}:`, error);
        throw error;
    }
};

export default getCattleById;

