// frontend/src/containers/cattle/GenerateCattleReport.js

import { useState } from 'react';
import { generateTraceabilityReport } from '../../services/reports/generateTraceabilityReport';

/**
 * GenerateCattleReport container hook - Maneja la generación de reportes PDF desde el backend
 * @param {Object} cattle - Datos del animal
 * @param {Array} estimations - Lista de estimaciones (no usado, el backend obtiene los datos)
 * @param {Array} timelineEvents - Eventos del timeline (no usado, el backend obtiene los datos)
 * @param {Object} father - Datos del padre (no usado, el backend obtiene los datos)
 * @param {Object} mother - Datos de la madre (no usado, el backend obtiene los datos)
 * @returns {Object} { loading, error, handleGenerateReport }
 */
function GenerateCattleReport(cattle, estimations, timelineEvents, father, mother) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleGenerateReport = async (format) => {
        if (!cattle || !cattle.id) {
            setError('No hay datos del animal para generar el reporte');
            return;
        }

        // Si no se especifica formato, usar PDF por defecto
        // Asegurarse de que sea un string válido
        const reportFormat = (format && (format === 'pdf' || format === 'excel')) ? format : 'pdf';
        
        console.log('handleGenerateReport llamado:', { format, reportFormat, animalId: cattle.id });

        setLoading(true);
        setError(null);

        try {
            // Llamar al endpoint del backend que genera el reporte
            await generateTraceabilityReport(cattle.id, reportFormat);
            // Si llegamos aquí, la descarga fue exitosa
            // No hay necesidad de mostrar un mensaje de éxito ya que el archivo se descarga automáticamente
        } catch (err) {
            const errorMessage = err?.message || 'Error al generar el reporte. Por favor intenta de nuevo más tarde.';
            setError(errorMessage);
            console.error('Error al generar reporte:', err);
        } finally {
            setLoading(false);
        }
    };

    return {
        loading,
        error,
        handleGenerateReport
    };
}

export default GenerateCattleReport;

