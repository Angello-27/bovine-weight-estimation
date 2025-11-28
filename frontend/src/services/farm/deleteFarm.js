// frontend/src/services/farm/deleteFarm.js

import apiClient from '../../api/axiosClient';

/**
 * Elimina una finca
 * @param {string} farmId - ID de la finca
 * @returns {Promise<void>}
 */
const deleteFarm = async (farmId) => {
    try {
        await apiClient.delete(`/farm/${farmId}`);
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('No se puede eliminar la finca porque tiene animales registrados.');
        } else if (error.response && error.response.status === 404) {
            throw new Error('Finca no encontrada.');
        } else {
            throw new Error('Ocurrió un error al intentar eliminar la finca. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { deleteFarm };

