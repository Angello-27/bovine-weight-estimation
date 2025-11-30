// frontend/src/containers/farm/useFarmDetail.js

import { useState, useEffect } from 'react';
import { getFarmById } from '../../services/farm/getFarmById';
import getAllCattle from '../../services/cattle/getAllCattle';
import getAllWeightEstimations from '../../services/weight-estimations/getAllWeightEstimations';
import { getUserById } from '../../services/user/getUserById';

/**
 * Hook para obtener datos de detalle de una hacienda y sus relaciones
 * @param {string} farmId - ID de la hacienda
 */
function useFarmDetail(farmId) {
    const [farm, setFarm] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    // Estadísticas relacionadas
    const [stats, setStats] = useState({
        totalAnimals: 0,
        totalEstimations: 0,
        averageWeight: 0,
        totalBreeds: 0,
        activeAnimals: 0,
    });

    useEffect(() => {
        async function fetchData() {
            if (!farmId) {
                setError('ID de hacienda no proporcionado');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                setError(null);

                // Obtener datos de la hacienda
                const farmData = await getFarmById(farmId);
                
                // Si hay owner_id, obtener información del propietario
                if (farmData.owner_id) {
                    try {
                        const ownerData = await getUserById(farmData.owner_id);
                        farmData.owner = ownerData;
                    } catch (err) {
                        console.warn('No se pudo obtener información del propietario:', err);
                    }
                }
                
                setFarm(farmData);

                // Obtener estadísticas relacionadas
                try {
                    // Animales de la hacienda
                    const animalsData = await getAllCattle({ 
                        farm_id: farmId, 
                        page: 1, 
                        page_size: 100 
                    });
                    const animals = animalsData.animals || animalsData || [];
                    
                    // Intentar obtener todas las estimaciones primero (si el endpoint está disponible)
                    let farmEstimations = [];
                    const farmAnimalIds = new Set(animals.map(a => a.id));
                    
                    try {
                        const allEstimationsData = await getAllWeightEstimations({ 
                            page: 1,
                            page_size: 100
                        });
                        const allEstimations = allEstimationsData.weighings || allEstimationsData.estimations || allEstimationsData || [];
                        // Filtrar estimaciones de animales de esta hacienda
                        farmEstimations = allEstimations.filter(e => {
                            const animalId = e.animal_id || e.cattle_id;
                            return animalId && farmAnimalIds.has(animalId);
                        });
                    } catch (e) {
                        // Si el endpoint no está disponible, intentar obtener por animal (máximo 10 para evitar demasiadas llamadas)
                        console.warn('Endpoint getAllWeightEstimations no disponible, intentando obtener por animal');
                        try {
                            const getWeightEstimationsByCattleId = (await import('../../services/weight-estimations/getWeightEstimationsByCattleId')).default;
                            for (const animal of animals.slice(0, 10)) {
                                try {
                                    const estData = await getWeightEstimationsByCattleId(animal.id, 1, 50);
                                    const ests = estData.weighings || estData.estimations || estData || [];
                                    farmEstimations.push(...ests);
                                } catch (err) {
                                    // Continuar con el siguiente animal si falla
                                    console.warn(`Error al obtener estimaciones para animal ${animal.id}:`, err);
                                }
                            }
                        } catch (importErr) {
                            console.warn('No se pudieron obtener estimaciones:', importErr);
                        }
                    }

                    // Calcular estadísticas
                    const breeds = new Set(animals.map(a => a.breed).filter(Boolean));
                    const activeAnimals = animals.filter(a => a.status === 'active').length;
                    
                    let totalWeight = 0;
                    let weightCount = 0;
                    farmEstimations.forEach(est => {
                        const weight = est.estimated_weight_kg || est.estimated_weight;
                        if (weight && weight > 0) {
                            totalWeight += weight;
                            weightCount++;
                        }
                    });

                    setStats({
                        totalAnimals: animals.length,
                        totalEstimations: farmEstimations.length,
                        averageWeight: weightCount > 0 ? totalWeight / weightCount : 0,
                        totalBreeds: breeds.size,
                        activeAnimals: activeAnimals,
                    });
                } catch (statsError) {
                    console.warn('Error al obtener estadísticas:', statsError);
                    // No detenemos la carga si fallan las estadísticas
                }

            } catch (err) {
                setError(err?.message || 'Error al cargar los datos de la hacienda');
                console.error('Error al cargar detalle de hacienda:', err);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [farmId]);

    return {
        farm,
        stats,
        loading,
        error,
        farmId
    };
}

export default useFarmDetail;

