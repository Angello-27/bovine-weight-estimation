// frontend/src/services/reports/generateGrowthReport.js

import apiClient from '../../api/axiosClient';

/**
 * Genera reporte de crecimiento y GDP (PDF o Excel) desde el backend
 * 
 * @param {Object} params - Parámetros del reporte
 * @param {string} params.animal_id - ID del animal (opcional, si no se proporciona farm_id)
 * @param {string} params.farm_id - ID de la hacienda (opcional, si no se proporciona animal_id)
 * @param {string} params.format - Formato: 'pdf' o 'excel' (default: 'excel')
 * @returns {Promise<void>} Descarga el archivo automáticamente
 */
const generateGrowthReport = async (params = {}) => {
    try {
        const { format = 'excel', ...reportParams } = params;
        
        if (!params.animal_id && !params.farm_id) {
            throw new Error('Debe proporcionar animal_id o farm_id');
        }
        
        const response = await apiClient.post(
            '/api/v1/reports/growth',
            { format, ...reportParams },
            {
                responseType: 'blob', // Importante para descargar archivo
            }
        );

        // Crear nombre de archivo descriptivo
        const timestamp = new Date().toISOString().split('T')[0];
        const id = params.animal_id || params.farm_id;
        const type = params.animal_id ? 'animal' : 'hacienda';
        const filename = `crecimiento_${type}_${id}_${timestamp}.${format}`;

        // Crear URL del blob y descargar
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Datos inválidos. Por favor verifica los parámetros e intenta de nuevo.');
        } else if (error.message && error.message.includes('Debe proporcionar')) {
            throw error;
        } else {
            throw new Error('Ocurrió un error al generar el reporte de crecimiento. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { generateGrowthReport };

