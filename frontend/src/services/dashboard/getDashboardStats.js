// frontend/src/services/dashboard/getDashboardStats.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene las estadísticas del dashboard
 * @returns {Promise<Object>} Objeto con totalCattle, averageWeight, totalBreeds, totalEstimations
 */
const getDashboardStats = async () => {
    try {
        const response = await apiClient.get('/api/v1/dashboard/stats');
        return response.data;
    } catch (error) {
        // Extraer mensaje del backend si está disponible
        let backendMessage = null;
        if (error.response?.data?.detail) {
            const detail = error.response.data.detail;
            if (typeof detail === 'string') {
                backendMessage = detail;
            } else if (Array.isArray(detail) && detail.length > 0) {
                backendMessage = detail[0]?.msg || detail[0]?.message || String(detail[0]);
            } else if (typeof detail === 'object') {
                backendMessage = detail.message || detail.msg || String(detail);
            }
        }
        
        if (error.response && error.response.status === 400) {
            const message = backendMessage || 'El usuario no tiene una finca asignada.';
            throw new Error(message);
        } else if (error.response && error.response.status === 401) {
            throw new Error('No autenticado. Por favor inicia sesión.');
        } else {
            throw new Error(backendMessage || 'Error al obtener estadísticas del dashboard.');
        }
    }
};

export { getDashboardStats };

