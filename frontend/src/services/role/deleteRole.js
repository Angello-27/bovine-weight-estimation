// frontend/src/services/role/deleteRole.js

import apiClient from '../../api/axiosClient';

/**
 * Elimina un rol
 * @param {string} roleId - ID del rol a eliminar
 * @returns {Promise<void>}
 */
const deleteRole = async (roleId) => {
    try {
        await apiClient.delete(`/role/${roleId}`);
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Rol no encontrado');
        } else if (error.response && error.response.status === 400) {
            throw new Error('No se puede eliminar el rol. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar eliminar el rol. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { deleteRole };

