// frontend/src/services/alerts/getPendingAlerts.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene alertas pendientes
 * 
 * @param {Object} filters - Filtros opcionales
 * @param {string} filters.user_id - Filtrar por usuario (UUID) (opcional)
 * @param {string} filters.farm_id - Filtrar por finca (UUID) (opcional)
 * @returns {Promise<Array>} Lista de alertas pendientes
 */
const getPendingAlerts = async (filters = {}) => {
    try {
        const params = new URLSearchParams();
        
        if (filters.user_id) params.append('user_id', filters.user_id);
        if (filters.farm_id) params.append('farm_id', filters.farm_id);
        
        const queryString = params.toString();
        const url = `/api/v1/alerts/pending/list${queryString ? `?${queryString}` : ''}`;
        
        const response = await apiClient.get(url);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Error en los filtros proporcionados. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al obtener las alertas pendientes. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getPendingAlerts };

