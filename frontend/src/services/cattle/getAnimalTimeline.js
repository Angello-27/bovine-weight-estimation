// frontend/src/services/cattle/getAnimalTimeline.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene el timeline de eventos de un animal
 * @param {string} animalId - ID del animal
 * @returns {Promise<Object|null>} Timeline con events o null si hay error
 */
const getAnimalTimeline = async (animalId) => {
    try {
        // Validar que animalId sea un UUID válido
        if (!animalId || typeof animalId !== 'string') {
            console.warn('getAnimalTimeline: animalId inválido', animalId);
            return null;
        }

        // Validar formato UUID básico
        const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
        if (!uuidRegex.test(animalId)) {
            console.warn('getAnimalTimeline: animalId no es un UUID válido', animalId);
            return null;
        }

        const response = await apiClient.get(`/api/v1/animals/${animalId}/timeline`);
        return response.data;
    } catch (error) {
        // Para errores 400 o 404, retornar null en lugar de lanzar error
        // El timeline es opcional y no debe bloquear la carga de la página
        if (error.response) {
            if (error.response.status === 404) {
                console.warn('getAnimalTimeline: Animal no encontrado', animalId);
                return null;
            } else if (error.response.status === 400) {
                console.warn('getAnimalTimeline: Error 400 - Request inválido', error.response.data);
                return null;
            } else if (error.response.status >= 500) {
                console.error('getAnimalTimeline: Error del servidor', error.response.status);
                return null;
            }
        }
        // Para otros errores (red, timeout, etc.), también retornar null
        console.warn('getAnimalTimeline: Error al obtener timeline', error.message);
        return null;
    }
};

export { getAnimalTimeline };

