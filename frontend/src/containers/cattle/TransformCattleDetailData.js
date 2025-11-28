// frontend/src/containers/cattle/TransformCattleDetailData.js

import { useMemo } from 'react';
import { cattleToTimelineEvents } from '../../utils/transformers/cattleToTimelineEvents';
import { weightEstimationToChartData } from '../../utils/transformers/weightEstimationToChartData';

/**
 * TransformCattleDetailData container hook - Transforma datos para la vista de detalle
 * @param {Object} cattle - Datos del animal
 * @param {Array} estimations - Lista de estimaciones de peso
 * @returns {Object} { timelineEvents, chartData, galleryImages }
 */
function TransformCattleDetailData(cattle, estimations) {
    // Transformar datos para timeline
    const timelineEvents = useMemo(() => {
        if (!cattle) return [];
        return cattleToTimelineEvents(cattle, estimations);
    }, [cattle, estimations]);

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

