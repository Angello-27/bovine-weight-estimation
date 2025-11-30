// frontend/src/services/role/updateRole.js

import apiClient from '../../api/axiosClient';

/**
 * Actualiza un rol existente
 * @param {string} roleId - ID del rol a actualizar
 * @param {Object} roleData - Datos actualizados del rol
 * @param {string} roleData.name - Nombre del rol
 * @param {string} roleData.priority - Prioridad (Administrador, Usuario, Invitado)
 * @returns {Promise<Object>} Rol actualizado
 */
const updateRole = async (roleId, roleData) => {
    try {
        const payload = {
            name: roleData.name,
            priority: roleData.priority,
        };
        
        const response = await apiClient.put(`/role/${roleId}`, payload);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Rol no encontrado');
        } else if (error.response && error.response.status === 400) {
            throw new Error('Los datos proporcionados son incorrectos. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar actualizar el rol. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { updateRole };

