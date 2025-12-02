// src/services/weight-estimations/createWeightEstimation.js
import apiClient from '../../api/axiosClient';

/**
 * Crea una nueva estimación de peso
 * @param {Object} estimationData - Datos de la estimación
 * @param {string} estimationData.breed - Raza (obligatorio)
 * @param {number} estimationData.estimated_weight_kg - Peso estimado en kg (obligatorio)
 * @param {number} estimationData.confidence - Confianza 0-1 (obligatorio, mínimo 0.8)
 * @param {string} estimationData.frame_image_path - Path del fotograma (obligatorio)
 * @param {number} estimationData.processing_time_ms - Tiempo de procesamiento en ms (obligatorio)
 * @param {string} [estimationData.animal_id] - ID del animal (opcional)
 * @param {number} [estimationData.latitude] - Latitud GPS (opcional)
 * @param {number} [estimationData.longitude] - Longitud GPS (opcional)
 * @param {string} [estimationData.method] - Método (default: "tflite")
 * @param {string} [estimationData.ml_model_version] - Versión del modelo (opcional)
 * @param {string} [estimationData.device_id] - ID del dispositivo (opcional)
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

