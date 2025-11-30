// frontend/src/services/reports/generateMovementReport.js

import apiClient from '../../api/axiosClient';

/**
 * Genera reporte de movimientos (ventas, fallecimientos) (PDF o Excel) desde el backend
 * 
 * @param {Object} params - Parámetros del reporte
 * @param {string} params.farm_id - ID de la finca (opcional)
 * @param {string} params.format - Formato: 'pdf' o 'excel' (default: 'pdf')
 * @param {string} params.movement_type - Tipo de movimiento: 'sold', 'deceased', o null (todos) (opcional)
 * @param {string} params.date_from - Fecha desde (ISO 8601) (opcional)
 * @param {string} params.date_to - Fecha hasta (ISO 8601) (opcional)
 * @returns {Promise<void>} Descarga el archivo automáticamente
 */
const generateMovementReport = async (params = {}) => {
    try {
        const { format = 'pdf', ...reportParams } = params;
        
        const response = await apiClient.post(
            '/api/v1/reports/movements',
            { format, ...reportParams },
            {
                responseType: 'blob', // Importante para descargar archivo
            }
        );

        // Crear nombre de archivo descriptivo
        const timestamp = new Date().toISOString().split('T')[0];
        const movementType = params.movement_type || 'todos';
        const filename = `movimientos_${params.farm_id || 'general'}_${movementType}_${timestamp}.${format}`;

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
        } else {
            throw new Error('Ocurrió un error al generar el reporte de movimientos. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { generateMovementReport };

