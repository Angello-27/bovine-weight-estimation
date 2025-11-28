// frontend\src\services\user\createUser.js

import apiClient from '../../api/axiosClient';

/**
 * Crea un nuevo usuario
 * @param {Object} userData - Datos del usuario (username, email, password, role_id, farm_id)
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
        };
        const response = await apiClient.post('/user', payload);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Los datos proporcionados son incorrectos. Por favor verifica e intenta de nuevo.');
        } else if (error.response && error.response.status === 404) {
            throw new Error('El rol o la finca especificada no existe.');
        } else {
            throw new Error('Ocurrió un error al intentar crear el usuario. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { createUser };

