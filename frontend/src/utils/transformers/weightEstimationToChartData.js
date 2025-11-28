// frontend/src/utils/transformers/weightEstimationToChartData.js

/**
 * Transforma estimaciones de peso a formato para gráficos
 * @param {Array} estimations - Lista de estimaciones
 * @param {string} birthDate - Fecha de nacimiento del animal (opcional)
 * @param {number} birthWeight - Peso al nacer (opcional)
 * @returns {Object} Datos formateados para gráfico
 */
export function weightEstimationToChartData(estimations = [], birthDate = null, birthWeight = null) {
    const data = [];

    // Agregar punto de nacimiento si está disponible
    if (birthDate && birthWeight !== null) {
        data.push({
            date: new Date(birthDate),
            weight: birthWeight,
            type: 'birth',
            label: 'Nacimiento'
        });
    }

    // Agregar estimaciones
    estimations.forEach(estimation => {
        if (estimation.timestamp && estimation.estimated_weight) {
            data.push({
                date: new Date(estimation.timestamp),
                weight: estimation.estimated_weight,
                type: 'estimation',
                confidence: estimation.confidence_score,
                label: new Date(estimation.timestamp).toLocaleDateString()
            });
        }
    });

    // Ordenar por fecha
    data.sort((a, b) => a.date - b.date);

    return {
        data,
        labels: data.map(d => d.label),
        weights: data.map(d => d.weight),
        dates: data.map(d => d.date)
    };
}

