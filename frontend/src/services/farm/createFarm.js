// frontend/src/services/farm/createFarm.js

import apiClient from '../../api/axiosClient';

/**
 * Crea una nueva finca
 * @param {Object} farmData - Datos de la finca (name, owner_id, latitude, longitude, capacity)
 * @returns {Promise<Object>} Datos de la finca creada
 */
const createFarm = async (farmData) => {
    try {
        const response = await apiClient.post('/farm', farmData);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Los datos proporcionados son incorrectos. Por favor verifica e intenta de nuevo.');
        } else if (error.response && error.response.status === 404) {
            throw new Error('El propietario especificado no existe.');
        } else {
            throw new Error('Ocurrió un error al intentar crear la finca. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { createFarm };

