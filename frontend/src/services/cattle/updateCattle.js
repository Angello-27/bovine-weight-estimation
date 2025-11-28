// src/services/cattle/updateCattle.js
import apiClient from '../../api/axiosClient';

/**
 * Actualiza un animal existente
 * @param {string} id - ID del animal a actualizar
 * @param {Object} cattleData - Datos actualizados del animal
 * @returns {Promise<Object>} Animal actualizado
 */
const updateCattle = async (id, cattleData) => {
    try {
        const response = await apiClient.put(`/api/v1/animals/${id}`, cattleData);
        return response.data;
    } catch (error) {
        console.error(`Error al actualizar animal ${id}:`, error);
        throw error;
    }
};

export default updateCattle;

