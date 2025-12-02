// frontend/src/containers/cattle/TransformCattleDetailData.js

import { useMemo } from 'react';
import { cattleToTimelineEvents } from '../../utils/transformers/cattleToTimelineEvents';
import { weightEstimationToChartData } from '../../utils/transformers/weightEstimationToChartData';

/**
 * TransformCattleDetailData container hook - Transforma datos para la vista de detalle
 * @param {Object} cattle - Datos del animal
 * @param {Array} estimations - Lista de estimaciones de peso
 * @param {Object} timeline - Timeline del backend (opcional)
 * @returns {Object} { timelineEvents, chartData, galleryImages }
 */
function TransformCattleDetailData(cattle, estimations, timeline = null) {
    // Transformar datos para timeline
    const timelineEvents = useMemo(() => {
        if (!cattle) return [];
        
        // Si hay timeline del backend, usarlo y ordenarlo
        if (timeline && timeline.events && Array.isArray(timeline.events)) {
            // Ordenar eventos del backend por fecha (más reciente primero)
            const sortedEvents = [...timeline.events].sort((a, b) => {
                const dateA = new Date(a.timestamp || a.date || 0);
                const dateB = new Date(b.timestamp || b.date || 0);
                return dateB - dateA; // Más reciente primero
            });
            return sortedEvents;
        }
        
        // Si no hay timeline del backend, usar el transformador local
        const events = cattleToTimelineEvents(cattle, estimations);
        // Ya está ordenado en cattleToTimelineEvents (más reciente primero)
        return events;
    }, [cattle, estimations, timeline]);

    // Transformar datos para gráfico
    const chartData = useMemo(() => {
        if (!estimations || estimations.length === 0) {
            return null;
        }
        return weightEstimationToChartData(
            estimations,
            cattle?.birth_date,
            cattle?.birth_weight_kg
        );
    }, [estimations, cattle?.birth_date, cattle?.birth_weight_kg]);

    // Extraer imágenes de las estimaciones para la galería
    const galleryImages = useMemo(() => {
        if (!estimations) return [];
        return estimations
            .filter(est => est.frame_image_path)
            .map(est => ({
                id: est.id,
                url: est.frame_image_path,
                title: `Estimación de Peso - ${est.estimated_weight?.toFixed(1)} kg`,
                date: est.timestamp
            }));
    }, [estimations]);

    return {
        timelineEvents,
        chartData,
        galleryImages
    };
}

export default TransformCattleDetailData;

