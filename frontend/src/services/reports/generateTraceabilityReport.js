// frontend/src/services/reports/generateTraceabilityReport.js

import apiClient from '../../api/axiosClient';

/**
 * Genera reporte de trazabilidad individual (PDF o Excel) desde el backend
 * 
 * @param {string} animalId - ID del animal
 * @param {string} format - Formato del reporte: 'pdf' o 'excel' (default: 'pdf')
 * @returns {Promise<void>} Descarga el archivo automáticamente
 */
const generateTraceabilityReport = async (animalId, format = 'pdf') => {
    // Asegurar que el formato tenga un valor por defecto válido
    const reportFormat = format || 'pdf';
    
    // Validar formato
    if (reportFormat !== 'pdf' && reportFormat !== 'excel') {
        console.error('Formato inválido recibido:', { format, reportFormat, animalId });
        throw new Error(`Formato inválido: "${reportFormat}". Use "pdf" o "excel"`);
    }

    // Validar animalId
    if (!animalId) {
        throw new Error('ID de animal es requerido');
    }

    try {
        console.log('Generando reporte:', { animalId, format });
        
        const response = await apiClient.post(
            `/api/v1/reports/traceability/${animalId}`,
            { format: reportFormat },
            {
                responseType: 'blob', // Importante para descargar archivo
                timeout: 60000, // 60 segundos para reportes grandes
            }
        );

        console.log('Respuesta recibida:', {
            status: response.status,
            headers: response.headers,
            dataType: typeof response.data,
            dataSize: response.data?.size || 0
        });

        // Verificar que tenemos datos
        if (!response.data) {
            throw new Error('El servidor no retornó datos del reporte');
        }

        // Crear URL del blob y descargar
        const blob = new Blob([response.data], {
            type: response.headers['content-type'] || 'application/pdf'
        });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `trazabilidad_${animalId}.${reportFormat}`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
        
        console.log('Reporte descargado exitosamente');
    } catch (error) {
        console.error('Error completo al generar reporte:', {
            message: error.message,
            response: error.response,
            status: error.response?.status,
            data: error.response?.data,
            config: error.config
        });

        if (error.response) {
            // El servidor respondió con un código de error
            if (error.response.status === 404) {
                throw new Error('Animal no encontrado');
            } else if (error.response.status === 400) {
                const detail = error.response.data?.detail || 'Formato inválido. Use "pdf" o "excel"';
                throw new Error(detail);
            } else if (error.response.status === 401) {
                throw new Error('No autorizado. Por favor inicia sesión nuevamente.');
            } else if (error.response.status === 500) {
                throw new Error('Error interno del servidor. Por favor intenta más tarde.');
            } else {
                throw new Error(`Error del servidor (${error.response.status}): ${error.response.data?.detail || 'Error desconocido'}`);
            }
        } else if (error.request) {
            // La petición se hizo pero no hubo respuesta
            throw new Error('No se pudo conectar con el servidor. Verifica tu conexión a internet.');
        } else {
            // Algo más pasó al configurar la petición
            throw new Error(`Error al configurar la petición: ${error.message}`);
        }
    }
};

export { generateTraceabilityReport };

