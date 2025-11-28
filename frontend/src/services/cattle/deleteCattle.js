// src/services/cattle/deleteCattle.js
import apiClient from '../../api/axiosClient';

/**
 * Elimina un animal
 * @param {string} id - ID del animal a eliminar
 * @returns {Promise<void>}
 */
const deleteCattle = async (id) => {
    try {
        await apiClient.delete(`/api/v1/animals/${id}`);
    } catch (error) {
        console.error(`Error al eliminar animal ${id}:`, error);
        throw error;
    }
};

export default deleteCattle;

