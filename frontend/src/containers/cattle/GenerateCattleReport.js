// frontend/src/containers/cattle/GenerateCattleReport.js

import { useState } from 'react';
import generateCattleTraceabilityReport from '../../services/reports/generateCattleTraceabilityReport';

/**
 * GenerateCattleReport container hook - Maneja la generación de reportes PDF
 * @param {Object} cattle - Datos del animal
 * @param {Array} estimations - Lista de estimaciones
 * @param {Array} timelineEvents - Eventos del timeline
 * @param {Object} father - Datos del padre
 * @param {Object} mother - Datos de la madre
 * @returns {Object} { loading, error, handleGenerateReport }
 */
function GenerateCattleReport(cattle, estimations, timelineEvents, father, mother) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleGenerateReport = async () => {
        if (!cattle) {
            setError('No hay datos del animal para generar el reporte');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            await generateCattleTraceabilityReport(
                cattle,
                estimations || [],
                timelineEvents || [],
                father,
                mother
            );
        } catch (err) {
            setError(err.message || 'Error al generar el reporte');
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

