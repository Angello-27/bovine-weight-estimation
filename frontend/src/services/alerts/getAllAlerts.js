// frontend/src/services/alerts/getAllAlerts.js

import apiClient from '../../api/axiosClient';

/**
 * Lista alertas con filtros y paginación
 * 
 * @param {Object} filters - Filtros opcionales
 * @param {number} filters.page - Número de página (default: 1)
 * @param {number} filters.page_size - Tamaño de página (default: 50, max: 100)
 * @param {string} filters.user_id - Filtrar por usuario (UUID) (opcional)
 * @param {string} filters.farm_id - Filtrar por finca (UUID) (opcional)
 * @param {string} filters.type - Filtrar por tipo (opcional)
 * @param {string} filters.status - Filtrar por estado (opcional)
 * @param {string} filters.scheduled_from - Fecha desde (ISO 8601) (opcional)
 * @param {string} filters.scheduled_to - Fecha hasta (ISO 8601) (opcional)
 * @returns {Promise<Object>} Lista de alertas paginada
 */
const getAllAlerts = async (filters = {}) => {
    try {
        const params = new URLSearchParams();
        
        if (filters.page) params.append('page', filters.page);
        if (filters.page_size) params.append('page_size', filters.page_size);
        if (filters.user_id) params.append('user_id', filters.user_id);
        if (filters.farm_id) params.append('farm_id', filters.farm_id);
        if (filters.type) params.append('type', filters.type);
        if (filters.status) params.append('status', filters.status);
        if (filters.scheduled_from) params.append('scheduled_from', filters.scheduled_from);
        if (filters.scheduled_to) params.append('scheduled_to', filters.scheduled_to);
        
        const queryString = params.toString();
        const url = `/api/v1/alerts${queryString ? `?${queryString}` : ''}`;
        
        const response = await apiClient.get(url);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Error en los filtros proporcionados. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al obtener las alertas. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getAllAlerts };

