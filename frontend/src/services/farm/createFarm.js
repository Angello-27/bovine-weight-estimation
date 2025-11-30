// frontend/src/services/farm/createFarm.js

import apiClient from '../../api/axiosClient';

/**
 * Crea una nueva hacienda
 * @param {Object} farmData - Datos de la hacienda (name, owner_id, latitude, longitude, capacity)
 * @returns {Promise<Object>} Datos de la hacienda creada
 */
const createFarm = async (farmData) => {
    try {
        const response = await apiClient.post('/farm', farmData);
        return response.data;
    } catch (error) {
        // Extraer mensaje del backend si está disponible
        let backendMessage = null;
        if (error.response?.data?.detail) {
            const detail = error.response.data.detail;
            if (typeof detail === 'string') {
                backendMessage = detail;
            } else if (Array.isArray(detail) && detail.length > 0) {
                // Si es un array, tomar el primer mensaje
                backendMessage = detail[0]?.msg || detail[0]?.message || String(detail[0]);
            } else if (typeof detail === 'object') {
                backendMessage = detail.message || detail.msg || String(detail);
            }
        }
        
        if (error.response && error.response.status === 400) {
            const message = backendMessage || 'Los datos proporcionados son incorrectos. Por favor verifica e intenta de nuevo.';
            throw new Error(message);
        } else if (error.response && error.response.status === 404) {
            throw new Error('El propietario especificado no existe.');
        } else {
            throw new Error(backendMessage || 'Ocurrió un error al intentar crear la hacienda. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { createFarm };

