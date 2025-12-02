// frontend/src/utils/transformers/cattleToTimelineEvents.js

/**
 * Transforma los datos de un animal y sus estimaciones en eventos de timeline
 * @param {Object} cattle - Datos del animal
 * @param {Array} estimations - Lista de estimaciones de peso
 * @returns {Array} Lista de eventos ordenados por fecha
 */
export function cattleToTimelineEvents(cattle, estimations = []) {
    const events = [];

    if (!cattle) return events;

    // Evento de registro
    if (cattle.created_at || cattle.registration_date) {
        events.push({
            id: `registration-${cattle.id}`,
            type: 'registration',
            date: cattle.created_at || cattle.registration_date,
            title: 'Registro',
            description: 'Animal registrado en el sistema'
        });
    }

    // Evento de nacimiento
    if (cattle.birth_date) {
        events.push({
            id: `birth-${cattle.id}`,
            type: 'birth',
            date: cattle.birth_date,
            title: 'Nacimiento',
            description: `Peso al nacer: ${cattle.birth_weight_kg ? `${cattle.birth_weight_kg} kg` : 'No registrado'}`,
            metadata: {
                weight: cattle.birth_weight_kg,
                breed: cattle.breed,
                gender: cattle.gender
            }
        });
    }

    // Eventos de estimaciones de peso
    estimations.forEach((estimation, index) => {
        events.push({
            id: `estimation-${estimation.id}`,
            type: 'weight_estimation',
            date: estimation.timestamp,
            title: 'Estimación de Peso',
            description: `Peso: ${estimation.estimated_weight?.toFixed(1)} kg (Confianza: ${(estimation.confidence_score * 100).toFixed(0)}%)`,
            metadata: {
                weight: estimation.estimated_weight,
                confidence: estimation.confidence_score,
                gps: estimation.gps_latitude && estimation.gps_longitude 
                    ? { lat: estimation.gps_latitude, lng: estimation.gps_longitude }
                    : null,
                method: estimation.method
            }
        });
    });

    // Ordenar por fecha (más reciente primero)
    return events.sort((a, b) => new Date(b.date) - new Date(a.date));
}

