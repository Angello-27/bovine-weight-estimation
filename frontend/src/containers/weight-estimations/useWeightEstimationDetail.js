// frontend/src/containers/weight-estimations/useWeightEstimationDetail.js

import { useState, useEffect } from 'react';
import GetWeightEstimationById from './GetWeightEstimationById';
import GetCattleById from '../cattle/GetCattleById';
import getWeightEstimationsByCattleId from '../../services/weight-estimations/getWeightEstimationsByCattleId';

/**
 * Hook para obtener todos los datos necesarios para el detalle de una estimación
 * @param {string} estimationId - ID de la estimación
 * @returns {Object} Objeto con estimation, cattle, previousEstimations, loading, error
 */
function useWeightEstimationDetail(estimationId) {
    const estimationProps = GetWeightEstimationById(estimationId);
    
    // Obtener información del animal asociado si existe
    // Según API: GET /api/v1/weighings/{id} devuelve 'animal_id' (no 'cattle_id')
    const animalId = estimationProps.estimation?.animal_id || estimationProps.estimation?.cattle_id;
    const cattleProps = GetCattleById(animalId);

    // Estado para historial de estimaciones del animal (solo anteriores a la fecha actual)
    const [previousEstimations, setPreviousEstimations] = useState([]);
    const [loadingHistory, setLoadingHistory] = useState(false);

    // Obtener historial de estimaciones del animal (solo anteriores a la fecha actual)
    useEffect(() => {
        const loadHistory = async () => {
            // El endpoint GET /api/v1/weighings/animal/{animal_id} ya filtra por animal
            // Según API: el endpoint devuelve 'animal_id', no 'cattle_id'
            const animalIdForHistory = estimationProps.estimation?.animal_id || estimationProps.estimation?.cattle_id;
            
            if (!animalIdForHistory || !estimationProps.estimation) {
                console.log('No hay animal_id o estimación:', { animalIdForHistory, estimation: estimationProps.estimation });
                return;
            }

            setLoadingHistory(true);
            try {
                // El endpoint GET /api/v1/weighings/animal/{animal_id} ya devuelve solo estimaciones del animal especificado
                const response = await getWeightEstimationsByCattleId(animalIdForHistory, 1, 100);
                console.log('Respuesta del historial:', response);
                
                if (response.weighings && Array.isArray(response.weighings)) {
                    const currentTimestamp = new Date(estimationProps.estimation.timestamp);
                    const currentEstimationId = estimationProps.estimation.id;
                    
                    console.log('Filtrando estimaciones:', {
                        total: response.weighings.length,
                        currentTimestamp,
                        currentEstimationId
                    });
                    
                    // Filtrar solo estimaciones anteriores a la fecha de la estimación actual
                    // El endpoint ya filtra por animal, así que solo necesitamos filtrar por fecha
                    const filtered = response.weighings
                        .filter(w => {
                            // Excluir la estimación actual por ID y por fecha
                            const isNotCurrent = w.id !== currentEstimationId;
                            const wTimestamp = new Date(w.timestamp);
                            const isBeforeCurrent = wTimestamp < currentTimestamp;
                            const shouldInclude = isNotCurrent && isBeforeCurrent;
                            
                            if (!shouldInclude) {
                                console.log('Estimación excluida:', {
                                    id: w.id,
                                    timestamp: w.timestamp,
                                    isNotCurrent,
                                    isBeforeCurrent
                                });
                            }
                            
                            return shouldInclude;
                        })
                        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)); // Más reciente primero
                    
                    console.log('Estimaciones filtradas:', filtered.length, filtered);
                    setPreviousEstimations(filtered);
                } else {
                    console.log('No hay weighings en la respuesta:', response);
                    setPreviousEstimations([]);
                }
            } catch (error) {
                console.error('Error al cargar historial de estimaciones:', error);
                setPreviousEstimations([]);
            } finally {
                setLoadingHistory(false);
            }
        };

        loadHistory();
    }, [estimationProps.estimation?.id, estimationProps.estimation?.timestamp, estimationProps.estimation?.animal_id, estimationProps.estimation?.cattle_id]);

    return {
        estimation: estimationProps.estimation,
        cattle: cattleProps.cattle,
        previousEstimations,
        loading: estimationProps.loading || cattleProps.loading || loadingHistory,
        error: estimationProps.error || cattleProps.error
    };
}

export default useWeightEstimationDetail;

