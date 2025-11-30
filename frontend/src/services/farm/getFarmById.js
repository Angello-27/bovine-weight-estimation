// frontend/src/services/farm/getFarmById.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene una hacienda por su ID
 * @param {string} farmId - ID de la hacienda
 * @returns {Promise<Object>} Datos de la hacienda
 */
const getFarmById = async (farmId) => {
    try {
        const response = await apiClient.get(`/farm/${farmId}`);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Hacienda no encontrada.');
        } else {
            throw new Error('Ocurrió un error al intentar obtener la hacienda. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getFarmById };

