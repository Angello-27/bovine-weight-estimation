// frontend/src/services/user/getUserById.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene un usuario por su ID
 * @param {string} userId - ID del usuario
 * @returns {Promise<Object>} Datos del usuario
 */
const getUserById = async (userId) => {
    try {
        const response = await apiClient.get(`/user/${userId}`);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Usuario no encontrado');
        } else if (error.response && error.response.status === 400) {
            throw new Error('Error al obtener el usuario. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar obtener el usuario. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getUserById };

