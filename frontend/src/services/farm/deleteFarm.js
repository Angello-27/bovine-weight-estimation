// frontend/src/services/farm/deleteFarm.js

import apiClient from '../../api/axiosClient';

/**
 * Elimina una hacienda
 * @param {string} farmId - ID de la hacienda
 * @returns {Promise<void>}
 */
const deleteFarm = async (farmId) => {
    try {
        await apiClient.delete(`/api/v1/farms/${farmId}`);
    } catch (error) {
        // Extraer mensaje del backend si está disponible
        // FastAPI puede enviar: string, array de errores, o objeto
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
            // Usar mensaje del backend si está disponible, sino usar mensaje por defecto
            const message = backendMessage || 'No se puede eliminar la hacienda porque tiene animales registrados.';
            throw new Error(message);
        } else if (error.response && error.response.status === 404) {
            throw new Error('Hacienda no encontrada.');
        } else {
            throw new Error(backendMessage || 'Ocurrió un error al intentar eliminar la hacienda. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { deleteFarm };

