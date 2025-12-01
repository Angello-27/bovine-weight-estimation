// frontend/src/services/user/updateUser.js

import apiClient from '../../api/axiosClient';

/**
 * Actualiza un usuario existente
 * @param {string} userId - ID del usuario a actualizar
 * @param {Object} userData - Datos actualizados del usuario
 * @returns {Promise<Object>} Usuario actualizado
 */
const updateUser = async (userId, userData) => {
    try {
        const payload = {
            email: userData.email,
            role_id: userData.roleId || userData.role_id,
            farm_id: userData.farmId || userData.farm_id || null,
            first_name: userData.first_name || null,
            last_name: userData.last_name || null,
            is_active: userData.is_active !== undefined ? userData.is_active : true,
        };
        
        // Solo incluir password si se proporciona
        if (userData.password && userData.password.trim() !== '') {
            payload.password = userData.password;
        }
        
        const response = await apiClient.put(`/user/${userId}`, payload);
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
            throw new Error('Recurso no encontrado.');
        } else {
            throw new Error(backendMessage || 'Ocurrió un error. Por favor intenta de nuevo.');
        }
    }
};

export { updateUser };

