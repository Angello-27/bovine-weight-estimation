// frontend/src/services/weight-estimations/estimateWeightFromImage.js

import apiClient from '../../api/axiosClient';

/**
 * Estima el peso de un animal desde una imagen subida
 * 
 * @param {File} imageFile - Archivo de imagen del animal
 * @param {string|null} cattleId - ID del animal (opcional)
 * @param {string|null} breed - Raza del animal (opcional)
 * @returns {Promise<Object>} Resultado de la estimación
 */
const estimateWeightFromImage = async (imageFile, cattleId = null, breed = null) => {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    if (cattleId) {
      formData.append('cattle_id', cattleId);
    }
    
    if (breed) {
      formData.append('breed', breed);
    }

    const response = await apiClient.post('/api/v1/ml/estimate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    if (error.response) {
      // Error con respuesta del servidor
      const status = error.response.status;
      const message = error.response.data?.message || error.response.data?.detail || 'Error desconocido';
      
      if (status === 400) {
        throw new Error('Imagen inválida o formato no soportado. Por favor verifica e intenta de nuevo.');
      } else if (status === 422) {
        throw new Error('La imagen no contiene un animal detectable. Por favor intenta con otra imagen.');
      } else if (status === 500) {
        throw new Error('Error en el procesamiento. Por favor intenta de nuevo más tarde.');
      } else {
        throw new Error(message);
      }
    } else if (error.request) {
      // Error de red
      throw new Error('Error de conexión. Por favor verifica tu conexión a internet e intenta de nuevo.');
    } else {
      // Error desconocido
      throw new Error('Ocurrió un error inesperado. Por favor intenta de nuevo.');
    }
  }
};

export default estimateWeightFromImage;

