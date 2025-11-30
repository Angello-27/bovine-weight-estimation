// frontend/src/services/alerts/deleteAlert.js

import apiClient from '../../api/axiosClient';

/**
 * Elimina una alerta
 * 
 * @param {string} alertId - ID de la alerta a eliminar
 * @returns {Promise<void>}
 */
const deleteAlert = async (alertId) => {
    try {
        await apiClient.delete(`/api/v1/alerts/${alertId}`);
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Alerta no encontrada');
        } else if (error.response && error.response.status === 400) {
            throw new Error('No se puede eliminar la alerta. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar eliminar la alerta. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { deleteAlert };

