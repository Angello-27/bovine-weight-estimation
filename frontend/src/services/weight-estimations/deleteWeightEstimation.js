// frontend/src/services/weight-estimations/deleteWeightEstimation.js

import apiClient from '../../api/axiosClient';

/**
 * Elimina una estimación de peso
 * @param {string} estimationId - ID de la estimación a eliminar
 * @returns {Promise<void>}
 */
const deleteWeightEstimation = async (estimationId) => {
    try {
        await apiClient.delete(`/api/v1/weighings/${estimationId}`);
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
            const message = backendMessage || 'La estimación no fue encontrada.';
            throw new Error(message);
        } else if (error.response && error.response.status === 400) {
            const message = backendMessage || 'Los datos proporcionados son incorrectos.';
            throw new Error(message);
        } else {
            throw new Error(backendMessage || 'Ocurrió un error al eliminar la estimación. Por favor intenta de nuevo.');
        }
    }
};

export { deleteWeightEstimation };

