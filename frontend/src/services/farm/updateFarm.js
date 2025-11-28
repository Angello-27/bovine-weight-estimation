// frontend/src/services/farm/updateFarm.js

import apiClient from '../../api/axiosClient';

/**
 * Actualiza una finca existente
 * @param {string} farmId - ID de la finca
 * @param {Object} farmData - Datos a actualizar (name, latitude, longitude, capacity)
 * @returns {Promise<Object>} Datos de la finca actualizada
 */
const updateFarm = async (farmId, farmData) => {
    try {
        const response = await apiClient.put(`/farm/${farmId}`, farmData);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Los datos proporcionados son incorrectos. Por favor verifica e intenta de nuevo.');
        } else if (error.response && error.response.status === 404) {
            throw new Error('Finca no encontrada.');
        } else {
            throw new Error('Ocurrió un error al intentar actualizar la finca. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { updateFarm };

