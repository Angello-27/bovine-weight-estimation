// frontend/src/services/alerts/getUpcomingAlerts.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene alertas programadas para los próximos N días
 * 
 * @param {Object} filters - Filtros opcionales
 * @param {number} filters.days_ahead - Días hacia adelante (default: 7, max: 30)
 * @param {string} filters.user_id - Filtrar por usuario (UUID) (opcional)
 * @param {string} filters.farm_id - Filtrar por finca (UUID) (opcional)
 * @returns {Promise<Array>} Lista de alertas próximas
 */
const getUpcomingAlerts = async (filters = {}) => {
    try {
        const params = new URLSearchParams();
        
        if (filters.days_ahead) params.append('days_ahead', filters.days_ahead);
        if (filters.user_id) params.append('user_id', filters.user_id);
        if (filters.farm_id) params.append('farm_id', filters.farm_id);
        
        const queryString = params.toString();
        const url = `/api/v1/alerts/upcoming${queryString ? `?${queryString}` : ''}`;
        
        const response = await apiClient.get(url);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Error en los filtros proporcionados. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al obtener las alertas próximas. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getUpcomingAlerts };

