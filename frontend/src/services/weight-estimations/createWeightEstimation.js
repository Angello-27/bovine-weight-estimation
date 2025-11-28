// src/services/weight-estimations/createWeightEstimation.js
import apiClient from '../../api/axiosClient';

/**
 * Crea una nueva estimación de peso
 * @param {Object} estimationData - Datos de la estimación
 * @param {string} estimationData.breed - Raza (obligatorio)
 * @param {number} estimationData.estimated_weight - Peso estimado en kg (obligatorio)
 * @param {number} estimationData.confidence_score - Confianza 0-1 (obligatorio, mínimo 0.8)
 * @param {string} estimationData.frame_image_path - Path del fotograma (obligatorio)
 * @param {string} [estimationData.cattle_id] - ID del animal (opcional)
 * @param {number} [estimationData.gps_latitude] - Latitud GPS (opcional)
 * @param {number} [estimationData.gps_longitude] - Longitud GPS (opcional)
 * @param {string} [estimationData.method] - Método (default: "tflite")
 * @param {string} [estimationData.model_version] - Versión del modelo (opcional)
 * @param {number} estimationData.processing_time_ms - Tiempo de procesamiento en ms (obligatorio)
 * @returns {Promise<Object>} Estimación creada
 */
const createWeightEstimation = async (estimationData) => {
    try {
        const response = await apiClient.post('/api/v1/weighings', estimationData);
        return response.data;
    } catch (error) {
        console.error('Error al crear estimación de peso:', error);
        throw error;
    }
};

export default createWeightEstimation;

