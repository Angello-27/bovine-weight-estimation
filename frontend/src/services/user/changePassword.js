// frontend/src/services/user/changePassword.js

import apiClient from '../../api/axiosClient';
import { getCurrentUser } from '../auth/authService';

/**
 * Cambia la contraseña del usuario actual
 * @param {Object} passwordData - { currentPassword, newPassword, confirmPassword }
 * @returns {Promise<Object>} Usuario actualizado
 */
const changePassword = async (passwordData) => {
    try {
        const currentUser = getCurrentUser();
        if (!currentUser || !currentUser.id) {
            throw new Error('Usuario no autenticado');
        }

        // Validar que las contraseñas coincidan
        if (passwordData.newPassword !== passwordData.confirmPassword) {
            throw new Error('Las contraseñas no coinciden');
        }

        // Validar longitud mínima
        if (passwordData.newPassword.length < 6) {
            throw new Error('La contraseña debe tener al menos 6 caracteres');
        }

        const payload = {
            password: passwordData.newPassword,
        };

        const response = await apiClient.put(`/api/v1/users/${currentUser.id}`, payload);
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
        } else if (error.response && error.response.status === 404) {
            throw new Error('Usuario no encontrado.');
        } else {
            throw new Error(backendMessage || error.message || 'Ocurrió un error. Por favor intenta de nuevo.');
        }
    }
};

export { changePassword };

