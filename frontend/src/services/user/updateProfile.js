// frontend/src/services/user/updateProfile.js

import apiClient from '../../api/axiosClient';
import { getCurrentUser } from '../auth/authService';

/**
 * Actualiza el perfil del usuario actual
 * @param {Object} profileData - Datos del perfil (email, first_name, last_name)
 * @returns {Promise<Object>} Usuario actualizado
 */
const updateProfile = async (profileData) => {
    try {
        const currentUser = getCurrentUser();
        if (!currentUser || !currentUser.id) {
            throw new Error('Usuario no autenticado');
        }

        const payload = {
            email: profileData.email,
            first_name: profileData.first_name || null,
            last_name: profileData.last_name || null,
        };

        const response = await apiClient.put(`/api/v1/users/${currentUser.id}`, payload);
        
        // Actualizar datos del usuario en localStorage
        const updatedUser = {
            ...currentUser,
            ...response.data,
        };
        localStorage.setItem('user', JSON.stringify(updatedUser));

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
            throw new Error(backendMessage || 'Ocurrió un error. Por favor intenta de nuevo.');
        }
    }
};

export { updateProfile };

