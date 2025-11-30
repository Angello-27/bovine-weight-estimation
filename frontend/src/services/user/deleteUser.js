// frontend/src/services/user/deleteUser.js

import apiClient from '../../api/axiosClient';

/**
 * Elimina un usuario
 * @param {string} userId - ID del usuario a eliminar
 * @returns {Promise<void>}
 */
const deleteUser = async (userId) => {
    try {
        await apiClient.delete(`/user/${userId}`);
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Usuario no encontrado');
        } else if (error.response && error.response.status === 400) {
            throw new Error('No se puede eliminar el usuario. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar eliminar el usuario. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { deleteUser };

