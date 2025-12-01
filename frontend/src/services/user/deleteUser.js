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
            const message = backendMessage || 'No se puede eliminar el usuario.';
            throw new Error(message);
        } else if (error.response && error.response.status === 404) {
            throw new Error('Recurso no encontrado.');
        } else {
            throw new Error(backendMessage || 'Ocurrió un error. Por favor intenta de nuevo.');
        }
    }
};

export { deleteUser };

