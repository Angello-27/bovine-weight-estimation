// frontend/src/services/role/updateRole.js

import apiClient from '../../api/axiosClient';

/**
 * Actualiza un rol existente
 * @param {string} roleId - ID del rol a actualizar
 * @param {Object} roleData - Datos actualizados del rol
 * @returns {Promise<Object>} Rol actualizado
 */
const updateRole = async (roleId, roleData) => {
    try {
        const payload = {};
        
        if (roleData.name !== undefined) payload.name = roleData.name;
        if (roleData.description !== undefined) payload.description = roleData.description || null;
        if (roleData.priority !== undefined) payload.priority = roleData.priority;
        if (roleData.permissions !== undefined) payload.permissions = roleData.permissions || [];
        
        const response = await apiClient.put(`/api/v1/roles/${roleId}`, payload);
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

export { updateRole };

