// frontend/src/services/ml/getMLHealth.js

import apiClient from '../../api/axiosClient';

/**
 * Verifica que el servicio ML esté operativo (health check)
 * 
 * @returns {Promise<Object>} Estado de salud del servicio ML
 * @returns {string} returns.status - Estado ('healthy')
 * @returns {string} returns.service - Nombre del servicio ('ml_inference')
 * @returns {string} returns.method - Método usado ('strategy_based')
 * @returns {string} returns.description - Descripción del sistema
 */
const getMLHealth = async () => {
    try {
        const response = await apiClient.get('/api/v1/ml/health');
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 500) {
            throw new Error('El servicio ML no está disponible. Por favor intenta de nuevo más tarde.');
        } else {
            throw new Error('Error de conexión al verificar el estado del servicio ML.');
        }
    }
};

export { getMLHealth };

