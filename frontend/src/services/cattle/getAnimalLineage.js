// frontend/src/services/cattle/getAnimalLineage.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene el linaje (padre, madre, descendientes) de un animal
 * @param {string} animalId - ID del animal
 * @returns {Promise<Object>} Linaje con father, mother, offspring
 */
const getAnimalLineage = async (animalId) => {
    try {
        const response = await apiClient.get(`/api/v1/animals/${animalId}/lineage`);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Animal no encontrado');
        } else if (error.response && error.response.status === 400) {
            throw new Error('Error al obtener el linaje. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar obtener el linaje. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getAnimalLineage };

