// src/services/cattle/getAllCattle.js
import apiClient from '../../api/axiosClient';

/**
 * Obtiene todos los animales (ganado) registrados con filtros y paginación
 * 
 * @param {Object} filters - Filtros opcionales
 * @param {string} filters.farm_id - Filtrar por hacienda (UUID)
 * @param {string} filters.breed - Filtrar por raza
 * @param {string} filters.gender - Filtrar por género (male/female)
 * @param {string} filters.status - Filtrar por estado (active/inactive/sold/deceased)
 * @param {number} filters.page - Número de página (default: 1)
 * @param {number} filters.page_size - Tamaño de página (default: 50, max: 100)
 * @returns {Promise<Object>} Objeto con total, animals, page, page_size
 */
const getAllCattle = async (filters = {}) => {
    try {
        const params = new URLSearchParams();
        
        // farm_id es requerido por el backend (Query(...))
        // Intentar obtenerlo de los filtros o del usuario autenticado
        let farmId = filters.farm_id;
        
        // Si no se proporciona farm_id en filtros, intentar obtenerlo del usuario actual
        if (!farmId) {
            try {
                const userStr = localStorage.getItem('user');
                if (userStr) {
                    const user = JSON.parse(userStr);
                    farmId = user.farm_id || user.farm?.id;
                }
            } catch (e) {
                console.warn('No se pudo obtener farm_id del usuario:', e);
            }
        }
        
        // Si aún no hay farm_id, lanzar un error descriptivo
        // El backend requiere farm_id como parámetro obligatorio
        if (!farmId) {
            throw new Error('Se requiere farm_id para listar animales. Por favor, proporciona un farm_id en los filtros o asegúrate de que tu usuario tenga una hacienda asignada.');
        }
        
        // Agregar farm_id como requerido
        params.append('farm_id', farmId);
        
        // Agregar filtros opcionales
        if (filters.breed) params.append('breed', filters.breed);
        if (filters.gender) params.append('gender', filters.gender);
        if (filters.status) params.append('status', filters.status);
        if (filters.page) params.append('page', filters.page);
        if (filters.page_size) params.append('page_size', filters.page_size);
        
        const queryString = params.toString();
        const url = `/api/v1/animals${queryString ? `?${queryString}` : ''}`;
        
        const response = await apiClient.get(url);
        return response.data;
    } catch (error) {
        console.error('Error al obtener animales:', error);
        if (error.response) {
            // Manejar diferentes tipos de errores de respuesta
            const errorData = error.response.data;
            let errorMessage = 'Error al obtener animales';
            
            if (typeof errorData === 'string') {
                errorMessage = errorData;
            } else if (errorData?.detail) {
                // Si detail es un string, usarlo directamente
                if (typeof errorData.detail === 'string') {
                    errorMessage = errorData.detail;
                } else if (Array.isArray(errorData.detail)) {
                    // Si detail es un array (errores de validación), extraer mensajes
                    errorMessage = errorData.detail.map(err => err.msg || JSON.stringify(err)).join(', ');
                } else {
                    errorMessage = JSON.stringify(errorData.detail);
                }
            } else if (errorData?.message) {
                errorMessage = errorData.message;
            }
            
            throw new Error(errorMessage);
        }
        // Si no hay response, puede ser un error de red
        throw new Error(error?.message || 'Error de conexión al obtener animales');
    }
};

export { getAllCattle };

