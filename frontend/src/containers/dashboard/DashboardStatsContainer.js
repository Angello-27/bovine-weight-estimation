// frontend/src/containers/dashboard/DashboardStatsContainer.js

import { useState, useEffect } from 'react';
import { getAnimalsByCriteria } from '../../services/cattle';
import { getWeightEstimationsByCriteria } from '../../services/weight-estimations/getWeightEstimationsByCriteria';
import { getCurrentUser } from '../../services/auth/authService';

function DashboardStatsContainer() {

    const [stats, setStats] = useState({
        totalCattle: 0,
        averageWeight: 0,
        totalBreeds: 0,
        totalEstimations: 0,
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchStats() {
            try {
                setError(null);

                // Obtener farm_id del usuario logueado
                const currentUser = getCurrentUser();
                const farmId = currentUser?.farm_id;

                if (!farmId) {
                    // Si el usuario no tiene farm_id asignado, mostrar estadísticas vacías
                    setStats({
                        totalCattle: 0,
                        averageWeight: 0,
                        totalBreeds: 0,
                        totalEstimations: 0,
                    });
                    setLoading(false);
                    return;
                }

                // Obtener datos de animales filtrados por farm_id
                let cattleList = [];
                try {
                    // Obtener todos los animales usando paginación
                    let page = 1;
                    let hasMore = true;
                    const pageSize = 100;

                    while (hasMore) {
                        const cattleData = await getAnimalsByCriteria(
                            { farm_id: farmId },
                            { page, page_size: pageSize }
                        );

                        const animals = cattleData?.animals || [];
                        cattleList = [...cattleList, ...animals];

                        // Verificar si hay más páginas
                        const total = cattleData?.total || 0;
                        hasMore = cattleList.length < total;
                        page++;
                    }
                } catch (cattleError) {
                    console.error('Error al obtener animales:', cattleError);
                    // Continuar aunque falle, mostrar 0
                }

                // Obtener datos de estimaciones filtradas por los animales de la farm
                let estimationsList = [];
                try {
                    const animalIds = new Set(cattleList.map(animal => animal.id));

                    // Obtener todas las estimaciones sin filtrar por animal_id
                    // Esto es más eficiente que hacer una consulta por cada animal
                    let allEstimations = [];
                                    let page = 1;
                                    let hasMore = true;
                                    const pageSize = 100;

                                    while (hasMore) {
                        try {
                            // Obtener estimaciones sin filtro de animal_id
                                        const result = await getWeightEstimationsByCriteria(
                                {}, // Sin filtros
                                            { page, page_size: pageSize }
                                        );

                            if (!result || typeof result !== 'object') {
                                console.warn(`⚠️ Respuesta inválida en página ${page}:`, result);
                                break;
                            }

                                        const weighings = result?.weighings || [];
                            allEstimations = [...allEstimations, ...weighings];

                                        const total = result?.total || 0;

                            // Verificar si hay más páginas
                            hasMore = total > 0 && allEstimations.length < total;
                            
                            // Prevenir loops infinitos
                            if (page > 1000) {
                                console.warn(`⚠️ Límite de páginas alcanzado (1000)`);
                                break;
                            }
                            
                            page++;
                        } catch (pageError) {
                            console.error(`❌ Error obteniendo página ${page} de estimaciones:`, {
                                message: pageError.message,
                                response: pageError.response?.data
                            });
                            break;
                        }
                    }

                    // Filtrar estimaciones por los animales de la farm
                    estimationsList = allEstimations.filter(estimation => {
                        const estAnimalId = estimation?.animal_id || estimation?.animalId;
                        return estAnimalId && animalIds.has(estAnimalId);
                    });
                } catch (estimationsError) {
                    console.error('Error al obtener estimaciones:', {
                        message: estimationsError.message,
                        stack: estimationsError.stack,
                        response: estimationsError.response?.data
                    });
                    // Continuar aunque falle, mostrar 0
                }

                // Calcular estadísticas
                const totalCattle = cattleList.length;

                // Calcular peso promedio (de estimaciones más recientes por animal)
                const weights = estimationsList
                    .map(est => est.estimated_weight_kg || est.estimated_weight)
                    .filter(w => w && w > 0);
                const averageWeight = weights.length > 0
                    ? weights.reduce((sum, w) => sum + w, 0) / weights.length
                    : 0;

                // Contar razas únicas
                const uniqueBreeds = new Set(cattleList.map(c => c.breed).filter(Boolean));
                const totalBreeds = uniqueBreeds.size;

                const totalEstimations = estimationsList.length;



                setStats({
                    totalCattle,
                    averageWeight: Math.round(averageWeight * 10) / 10, // Redondear a 1 decimal
                    totalBreeds,
                    totalEstimations,
                });
            } catch (err) {
                // Solo establecer error si es un error crítico
                const errorMessage = err.response?.data?.detail || err.message || 'Error al obtener estadísticas';
                setError(errorMessage);
                console.error('Error crítico al obtener estadísticas:', err);
            } finally {
                setLoading(false);
            }
        }

        fetchStats();
    }, []);

    return { stats, loading, error };
}

export default DashboardStatsContainer;

