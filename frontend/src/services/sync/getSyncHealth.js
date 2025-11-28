// src/services/sync/getSyncHealth.js
import apiClient from '../../api/axiosClient';

/**
 * Verifica el estado de salud del servicio de sincronización
 * @returns {Promise<Object>} Estado del servicio
 */
const getSyncHealth = async () => {
    try {
        const response = await apiClient.get('/api/v1/sync/health');
        return response.data;
    } catch (error) {
        console.error('Error al verificar salud de sincronización:', error);
        throw error;
    }
};

export default getSyncHealth;

