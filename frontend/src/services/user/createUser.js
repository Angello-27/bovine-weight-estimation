// frontend/src/services/user/createUser.js

import apiClient from '../../api/axiosClient';

/**
 * Crea un nuevo usuario
 * @param {Object} userData - Datos del usuario (username, email, password, role_id, farm_id, full_name)
 * @returns {Promise<Object>} Datos del usuario creado
 */
const createUser = async (userData) => {
    try {
        // Mapear los campos del frontend al backend
        const payload = {
            username: userData.username,
            email: userData.email,
            password: userData.password,
            role_id: userData.roleId || userData.role_id,
            farm_id: userData.farmId || userData.farm_id || null,
            first_name: userData.first_name || null,
            last_name: userData.last_name || null,
        };
        const response = await apiClient.post('/user', payload);
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

export { createUser };

