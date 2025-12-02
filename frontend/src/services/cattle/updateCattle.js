// frontend/src/services/cattle/updateCattle.js

import apiClient from '../../api/axiosClient';

/**
 * Actualiza un animal existente
 * @param {string} id - ID del animal a actualizar
 * @param {Object} cattleData - Datos actualizados del animal
 * @returns {Promise<Object>} Animal actualizado
 */
const updateCattle = async (id, cattleData) => {
    try {
        const response = await apiClient.put(`/api/v1/animals/${id}`, cattleData);
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
            const message = backendMessage || 'Los datos proporcionados son incorrectos. Por favor verifica e intenta de nuevo.';
            throw new Error(message);
        } else if (error.response && error.response.status === 404) {
            throw new Error('Animal no encontrado.');
        } else {
            throw new Error(backendMessage || 'Ocurrió un error al intentar actualizar el animal. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { updateCattle };

