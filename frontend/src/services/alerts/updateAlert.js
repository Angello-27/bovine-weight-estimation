// frontend/src/services/alerts/updateAlert.js

import apiClient from '../../api/axiosClient';

/**
 * Actualiza una alerta existente
 * 
 * @param {string} alertId - ID de la alerta a actualizar
 * @param {Object} alertData - Datos actualizados de la alerta
 * @param {string} alertData.title - Título de la alerta (opcional)
 * @param {string} alertData.description - Descripción de la alerta (opcional)
 * @param {string} alertData.type - Tipo de alerta (opcional)
 * @param {string} alertData.status - Estado: 'pending', 'completed', 'cancelled' (opcional)
 * @param {string} alertData.scheduled_date - Fecha programada (ISO 8601) (opcional)
 * @param {string} alertData.user_id - ID del usuario (opcional)
 * @param {string} alertData.farm_id - ID de la hacienda (opcional)
 * @returns {Promise<Object>} Alerta actualizada
 */
const updateAlert = async (alertId, alertData) => {
    try {
        const payload = {};
        
        if (alertData.title !== undefined) payload.title = alertData.title;
        if (alertData.description !== undefined) payload.description = alertData.description;
        if (alertData.type !== undefined) payload.type = alertData.type;
        if (alertData.status !== undefined) payload.status = alertData.status;
        if (alertData.scheduled_date !== undefined) payload.scheduled_date = alertData.scheduled_date;
        if (alertData.user_id !== undefined) payload.user_id = alertData.user_id;
        if (alertData.farm_id !== undefined) payload.farm_id = alertData.farm_id;
        
        const response = await apiClient.put(`/api/v1/alerts/${alertId}`, payload);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Alerta no encontrada');
        } else if (error.response && error.response.status === 400) {
            throw new Error('Los datos proporcionados son incorrectos. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al actualizar la alerta. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { updateAlert };

