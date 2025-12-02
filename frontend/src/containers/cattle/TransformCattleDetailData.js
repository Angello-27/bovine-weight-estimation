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
        
        // Si hay timeline del backend, transformarlo al formato esperado
        if (timeline && timeline.events && Array.isArray(timeline.events)) {
            // Transformar eventos del backend al formato esperado por TimelineEvent
            const transformedEvents = timeline.events.map((event, index) => ({
                id: event.id || `timeline-${event.type}-${index}`,
                type: event.type,
                date: event.timestamp || event.date,
                timestamp: event.timestamp || event.date,
                title: event.type === 'registration' ? 'Registro' :
                       event.type === 'birth' ? 'Nacimiento' :
                       event.type === 'weight_estimation' ? 'Estimación de Peso' :
                       event.type === 'update' ? 'Actualización' :
                       event.type === 'status_change' ? 'Cambio de Estado' :
                       'Evento',
                description: event.description || '',
                metadata: event.data || {}
            }));
            
            // Ordenar eventos por fecha (más reciente primero)
            const sortedEvents = [...transformedEvents].sort((a, b) => {
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

