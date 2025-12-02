// frontend/src/services/cattle/getAnimalsByCriteria.js

import apiClient from '../../api/axiosClient';

/**
 * Busca animales por criterios de filtrado
 * @param {Object} filters - Criterios de filtrado (farm_id requerido, breed, status, gender, age_category)
 * @param {Object} pagination - Parámetros de paginación (page, page_size)
 * @returns {Promise<Object>} Objeto con total, animals, page, page_size
 */
const getAnimalsByCriteria = async (filters = {}, pagination = {}) => {
    try {
        // farm_id es requerido por el backend
        if (!filters.farm_id) {
            // Intentar obtenerlo del usuario autenticado
            try {
                const userStr = localStorage.getItem('user');
                if (userStr) {
                    const user = JSON.parse(userStr);
                    filters.farm_id = user.farm_id || user.farm?.id;
                }
            } catch (e) {
                console.warn('No se pudo obtener farm_id del usuario:', e);
            }

            if (!filters.farm_id) {
                throw new Error('Se requiere farm_id para buscar animales. Por favor, proporciona un farm_id en los filtros o asegúrate de que tu usuario tenga una hacienda asignada.');
            }
        }

        // Asegurar que farm_id sea un string válido
        const farmId = String(filters.farm_id).trim();

        const params = {
            ...pagination,
            farm_id: farmId,
        };

        // Agregar filtros opcionales solo si están presentes
        if (filters.breed) params.breed = filters.breed;
        if (filters.status) params.status = filters.status;
        if (filters.gender) params.gender = filters.gender;
        if (filters.age_category) params.age_category = filters.age_category;

        const response = await apiClient.get('/api/v1/animals', { params });
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
            const message = backendMessage || 'Los datos proporcionados son incorrectos.';
            throw new Error(message);
        } else {
            throw new Error(backendMessage || error?.message || 'Ocurrió un error. Por favor intenta de nuevo.');
        }
    }
};

export { getAnimalsByCriteria };

