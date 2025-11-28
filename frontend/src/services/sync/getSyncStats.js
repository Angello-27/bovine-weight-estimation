// src/services/sync/getSyncStats.js
import apiClient from '../../api/axiosClient';

/**
 * Obtiene estadísticas del servicio de sincronización
 * @returns {Promise<Object>} Estadísticas de sincronización
 */
const getSyncStats = async () => {
    try {
        const response = await apiClient.get('/api/v1/sync/stats');
        return response.data;
    } catch (error) {
        console.error('Error al obtener estadísticas de sincronización:', error);
        throw error;
    }
};

export default getSyncStats;

