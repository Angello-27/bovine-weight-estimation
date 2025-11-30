// frontend/src/services/ml/getModelsStatus.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene información sobre el estado de los modelos ML cargados
 * 
 * @returns {Promise<Object>} Estado de los modelos ML
 * @returns {string} returns.status - Estado general ('ok')
 * @returns {number} returns.total_loaded - Total de modelos cargados
 * @returns {Array<string>} returns.breeds_loaded - Razas con modelos cargados
 * @returns {Array<string>} returns.all_breeds - Todas las razas disponibles
 * @returns {Array<string>} returns.missing_breeds - Razas sin modelos cargados
 * @returns {Object} returns.strategies - Información de estrategias disponibles
 * @returns {Array<string>} returns.available_strategies - Estrategias disponibles
 */
const getModelsStatus = async () => {
    try {
        const response = await apiClient.get('/api/v1/ml/models/status');
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 500) {
            throw new Error('Error al obtener el estado de los modelos ML. Por favor intenta de nuevo más tarde.');
        } else {
            throw new Error('Error de conexión al obtener el estado de los modelos ML.');
        }
    }
};

export { getModelsStatus };

