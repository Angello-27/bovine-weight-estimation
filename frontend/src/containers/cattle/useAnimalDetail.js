// frontend/src/containers/cattle/useAnimalDetail.js

import { useState, useEffect } from 'react';
import { getCattleById, getAnimalTimeline, getAnimalLineage } from '../../services/cattle';
import getWeightEstimationsByCattleId from '../../services/weight-estimations/getWeightEstimationsByCattleId';

/**
 * Hook para obtener datos de detalle de un animal y sus relaciones
 * Similar a useFarmDetail.js pero para animales
 * @param {string} animalId - ID del animal
 */
function useAnimalDetail(animalId) {
    const [cattle, setCattle] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    // Datos relacionados
    const [estimations, setEstimations] = useState([]);
    const [timeline, setTimeline] = useState(null);
    const [lineage, setLineage] = useState(null);
    
    // Estados de carga para cada recurso
    const [estimationsLoading, setEstimationsLoading] = useState(false);
    const [timelineLoading, setTimelineLoading] = useState(false);
    const [lineageLoading, setLineageLoading] = useState(false);

    useEffect(() => {
        async function fetchData() {
            if (!animalId) {
                setError('ID de animal no proporcionado');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                setError(null);

                // Obtener datos del animal
                const cattleData = await getCattleById(animalId);
                setCattle(cattleData);

                // Obtener datos relacionados en paralelo
                const promises = [];
                
                // Historial de estimaciones
                promises.push(
                    getWeightEstimationsByCattleId(animalId, 1, 100)
                        .then(data => {
                            // El servicio retorna { weighings: [...], total, page, page_size }
                            const estimationsList = data?.weighings || data?.estimations || (Array.isArray(data) ? data : []);
                            const sorted = estimationsList.sort((a, b) => {
                                const dateA = new Date(a.timestamp || a.created_at || 0);
                                const dateB = new Date(b.timestamp || b.created_at || 0);
                                return dateB - dateA;
                            });
                            setEstimations(sorted);
                            setEstimationsLoading(false);
                        })
                        .catch(err => {
                            console.warn('Error al obtener estimaciones:', err);
                            setEstimations([]);
                            setEstimationsLoading(false);
                        })
                );
                setEstimationsLoading(true);

                // Timeline (opcional - no debe bloquear la carga)
                promises.push(
                    getAnimalTimeline(animalId)
                        .then(data => {
                            // getAnimalTimeline ahora retorna null en caso de error
                            setTimeline(data || null);
                            setTimelineLoading(false);
                        })
                        .catch(err => {
                            // Fallback por si acaso (aunque getAnimalTimeline ya maneja errores)
                            console.warn('Error al obtener timeline:', err);
                            setTimeline(null);
                            setTimelineLoading(false);
                        })
                );
                setTimelineLoading(true);

                // Linaje
                promises.push(
                    getAnimalLineage(animalId)
                        .then(data => {
                            // El servicio retorna { animal, father, mother, descendants }
                            setLineage(data);
                            setLineageLoading(false);
                        })
                        .catch(err => {
                            console.warn('Error al obtener linaje:', err);
                            setLineage(null);
                            setLineageLoading(false);
                        })
                );
                setLineageLoading(true);

                // Esperar a que todas las promesas terminen (o fallen)
                await Promise.allSettled(promises);

            } catch (err) {
                setError(err?.message || 'Error al cargar los datos del animal');
                console.error('Error al cargar detalle de animal:', err);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [animalId]);

    // Determinar si hay alguna carga en progreso
    const isLoading = loading || estimationsLoading || timelineLoading || lineageLoading;

    return {
        cattle,
        estimations,
        timeline,
        lineage,
        loading: isLoading,
        error,
        animalId
    };
}

export default useAnimalDetail;

