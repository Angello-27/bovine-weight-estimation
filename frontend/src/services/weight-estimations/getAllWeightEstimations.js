// src/services/weight-estimations/getAllWeightEstimations.js
import apiClient from '../../api/axiosClient';

/**
 * Obtiene todas las estimaciones de peso (lista general)
 * 
 * @param {Object} [params] - Parámetros de consulta opcionales
 * @param {number} [params.page] - Número de página (1-based)
 * @param {number} [params.page_size] - Tamaño de página (default: 50, max: 100)
 * @returns {Promise<Object>} Objeto con { total, weighings, page, page_size }
 */
const getAllWeightEstimations = async (params = {}) => {
    try {
        const queryParams = new URLSearchParams();
        if (params.page) queryParams.append('page', params.page);
        if (params.page_size) queryParams.append('page_size', params.page_size);
        
        const queryString = queryParams.toString();
        const url = `/api/v1/weighings${queryString ? `?${queryString}` : ''}`;
        
        const response = await apiClient.get(url);
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
            throw new Error(backendMessage || 'Endpoint no disponible. El endpoint para listar todas las estimaciones puede no estar implementado.');
        } else if (error.response && error.response.status === 400) {
            throw new Error(backendMessage || 'Error al obtener las estimaciones. Por favor verifica los parámetros e intenta de nuevo.');
        } else {
            throw new Error(backendMessage || 'Ocurrió un error al intentar obtener las estimaciones. Por favor intenta de nuevo más tarde.');
        }
    }
};

export default getAllWeightEstimations;

