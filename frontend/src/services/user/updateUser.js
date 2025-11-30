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
            username: userData.username,
            email: userData.email,
            role_id: userData.roleId || userData.role_id,
            farm_id: userData.farmId || userData.farm_id || null,
            full_name: userData.full_name,
            is_active: userData.is_active,
        };
        
        // Solo incluir password si se proporciona
        if (userData.password) {
            payload.password = userData.password;
        }
        
        const response = await apiClient.put(`/user/${userId}`, payload);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Usuario no encontrado');
        } else if (error.response && error.response.status === 400) {
            throw new Error('Los datos proporcionados son incorrectos. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar actualizar el usuario. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { updateUser };

