// frontend/src/services/alerts/createAlert.js

import apiClient from '../../api/axiosClient';

/**
 * Crea una nueva alerta o evento programado
 * 
 * @param {Object} alertData - Datos de la alerta
 * @param {string} alertData.title - Título de la alerta
 * @param {string} alertData.description - Descripción de la alerta
 * @param {string} alertData.type - Tipo de alerta (ej: 'scheduled_weighing')
 * @param {string} alertData.status - Estado: 'pending', 'completed', 'cancelled' (default: 'pending')
 * @param {string} alertData.scheduled_date - Fecha programada (ISO 8601)
 * @param {string} alertData.user_id - ID del usuario (opcional)
 * @param {string} alertData.farm_id - ID de la finca (opcional)
 * @returns {Promise<Object>} Alerta creada
 */
const createAlert = async (alertData) => {
    try {
        const payload = {
            title: alertData.title,
            description: alertData.description,
            type: alertData.type,
            status: alertData.status || 'pending',
            scheduled_date: alertData.scheduled_date,
            user_id: alertData.user_id || null,
            farm_id: alertData.farm_id || null,
        };
        
        const response = await apiClient.post('/api/v1/alerts', payload);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Los datos proporcionados son incorrectos. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al crear la alerta. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { createAlert };

