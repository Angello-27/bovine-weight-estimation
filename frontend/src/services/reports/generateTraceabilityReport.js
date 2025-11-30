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
    try {
        const response = await apiClient.post(
            `/api/v1/reports/traceability/${animalId}`,
            { format },
            {
                responseType: 'blob', // Importante para descargar archivo
            }
        );

        // Crear URL del blob y descargar
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `trazabilidad_${animalId}.${format}`);
        document.body.appendChild(link);
        link.click();
        link.remove();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        if (error.response && error.response.status === 404) {
            throw new Error('Animal no encontrado');
        } else if (error.response && error.response.status === 400) {
            throw new Error('Formato inválido. Use "pdf" o "excel"');
        } else {
            throw new Error('Ocurrió un error al generar el reporte. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { generateTraceabilityReport };

