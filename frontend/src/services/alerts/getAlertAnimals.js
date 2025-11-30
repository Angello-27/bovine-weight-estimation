// frontend/src/services/alerts/getAlertAnimals.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene los animales relacionados con una alerta
 * 
 * @param {string} alertId - ID de la alerta
 * @returns {Promise<Array>} Lista de animales relacionados
 */
const getAlertAnimals = async (alertId) => {
    try {
        const response = await apiClient.get(`/api/v1/alerts/${alertId}/animals`);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Alerta no encontrada');
        } else if (error.response && error.response.status === 400) {
            throw new Error('Error al obtener los animales de la alerta. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al obtener los animales. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getAlertAnimals };

