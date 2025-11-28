// src/services/cattle/getAllCattle.js
import apiClient from '../../api/axiosClient';

/**
 * Obtiene todos los animales (ganado) registrados
 * @returns {Promise<Array>} Lista de animales
 */
const getAllCattle = async () => {
    try {
        const response = await apiClient.get('/api/v1/animals');
        return response.data;
    } catch (error) {
        console.error('Error al obtener animales:', error);
        throw error;
    }
};

export default getAllCattle;

