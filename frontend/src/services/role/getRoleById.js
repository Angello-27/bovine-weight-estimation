// frontend/src/services/role/getRoleById.js

import apiClient from '../../api/axiosClient';

/**
 * Obtiene un rol por su ID
 * @param {string} roleId - ID del rol
 * @returns {Promise<Object>} Datos del rol
 */
const getRoleById = async (roleId) => {
    try {
        const response = await apiClient.get(`/role/${roleId}`);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Rol no encontrado');
        } else if (error.response && error.response.status === 400) {
            throw new Error('Error al obtener el rol. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar obtener el rol. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { getRoleById };

