// frontend/src/services/cattle/getAnimalTimeline.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene el timeline de eventos de un animal
 * @param {string} animalId - ID del animal
 * @returns {Promise<Object>} Timeline con events
 */
const getAnimalTimeline = async (animalId) => {
    try {
        const response = await apiClient.get(`/api/v1/animals/${animalId}/timeline`);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Animal no encontrado');
        } else if (error.response && error.response.status === 400) {
            throw new Error('Error al obtener el timeline. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar obtener el timeline. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getAnimalTimeline };

