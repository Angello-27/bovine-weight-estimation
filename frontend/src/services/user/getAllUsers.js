// frontend/src/services/user/getAllUsers.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene todos los usuarios del sistema
 * @param {Object} params - Parámetros opcionales (page, page_size)
 * @returns {Promise<Object>} Objeto con total, users, page, page_size
 */
const getAllUsers = async (params = {}) => {
    try {
        const response = await apiClient.get('/user', { params });
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Error al obtener los usuarios. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar obtener los usuarios. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getAllUsers };

