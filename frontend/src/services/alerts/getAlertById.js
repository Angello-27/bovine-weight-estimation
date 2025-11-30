// frontend/src/services/alerts/getAlertById.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene una alerta por su ID
 * 
 * @param {string} alertId - ID de la alerta
 * @returns {Promise<Object>} Datos de la alerta
 */
const getAlertById = async (alertId) => {
    try {
        const response = await apiClient.get(`/api/v1/alerts/${alertId}`);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Alerta no encontrada');
        } else if (error.response && error.response.status === 400) {
            throw new Error('Error al obtener la alerta. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar obtener la alerta. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getAlertById };

