// frontend/src/services/cattle/getCattleById.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene un animal por su ID
 * @param {string} id - ID del animal
 * @returns {Promise<Object>} Datos del animal
 */
const getCattleById = async (id) => {
    try {
        const response = await apiClient.get(`/api/v1/animals/${id}`);
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
        
        if (error.response && error.response.status === 404) {
            throw new Error('Animal no encontrado.');
        } else {
            throw new Error(backendMessage || 'Ocurrió un error al obtener el animal. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getCattleById };

