// frontend/src/services/role/getAllRoles.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene todos los roles del sistema
 * @param {Object} params - Parámetros opcionales (skip, limit)
 * @returns {Promise<Object>} Objeto con total, roles, page, page_size
 */
const getAllRoles = async (params = {}) => {
    try {
        const response = await apiClient.get('/role', { params });
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Error al obtener los roles. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar obtener los roles. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getAllRoles };

