// frontend/src/services/cattle/createCattle.js

import apiClient from '../../api/axiosClient';

/**
 * Crea un nuevo animal
 * @param {Object} cattleData - Datos del animal a crear
 * @param {string} cattleData.ear_tag - Número de caravana (obligatorio)
 * @param {string} cattleData.breed - Raza (obligatorio)
 * @param {string} cattleData.birth_date - Fecha de nacimiento (obligatorio)
 * @param {string} cattleData.gender - Género: "male" | "female" (obligatorio)
 * @param {string} [cattleData.name] - Nombre del animal (opcional)
 * @param {string} [cattleData.color] - Color (opcional)
 * @param {number} [cattleData.birth_weight_kg] - Peso al nacer en kg (opcional)
 * @param {string} [cattleData.observations] - Observaciones (opcional)
 * @param {string} [cattleData.farm_id] - ID de la hacienda (obligatorio)
 * @returns {Promise<Object>} Animal creado
 */
const createCattle = async (cattleData) => {
    try {
        console.log('Enviando datos al backend (POST /api/v1/animals):', JSON.stringify(cattleData, null, 2));
        const response = await apiClient.post('/api/v1/animals', cattleData);
        console.log('Respuesta del backend:', JSON.stringify(response.data, null, 2));
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
            const message = backendMessage || 'Los datos proporcionados son incorrectos. Por favor verifica e intenta de nuevo.';
            throw new Error(message);
        } else if (error.response && error.response.status === 404) {
            throw new Error('Recurso no encontrado.');
        } else {
            throw new Error(backendMessage || 'Ocurrió un error al intentar crear el animal. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { createCattle };

