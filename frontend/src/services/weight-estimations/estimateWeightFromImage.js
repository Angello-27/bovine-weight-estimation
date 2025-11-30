// frontend/src/services/weight-estimations/estimateWeightFromImage.js

import apiClient from '../../api/axiosClient';

/**
 * Estima el peso de un animal desde una imagen subida
 * 
 * @param {File} imageFile - Archivo de imagen del animal
 * @param {string} breed - Raza del animal (requerido según API)
 * @param {string|null} animalId - ID del animal (opcional)
 * @returns {Promise<Object>} Resultado de la estimación
 */
const estimateWeightFromImage = async (imageFile, breed, animalId = null) => {
  try {
    if (!breed) {
      throw new Error('La raza es requerida para la estimación');
    }

    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('breed', breed);
    
    if (animalId) {
      formData.append('animal_id', animalId);
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

