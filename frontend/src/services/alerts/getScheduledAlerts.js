// frontend/src/services/alerts/getScheduledAlerts.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene alertas programadas
 * 
 * @param {Object} filters - Filtros opcionales
 * @param {string} filters.user_id - Filtrar por usuario (UUID) (opcional)
 * @param {string} filters.farm_id - Filtrar por hacienda (UUID) (opcional)
 * @returns {Promise<Array>} Lista de alertas programadas
 */
const getScheduledAlerts = async (filters = {}) => {
    try {
        const params = new URLSearchParams();
        
        if (filters.user_id) params.append('user_id', filters.user_id);
        if (filters.farm_id) params.append('farm_id', filters.farm_id);
        
        const queryString = params.toString();
        const url = `/api/v1/alerts/scheduled/list${queryString ? `?${queryString}` : ''}`;
        
        const response = await apiClient.get(url);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Error en los filtros proporcionados. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al obtener las alertas programadas. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getScheduledAlerts };

