// frontend/src/containers/dashboard/DashboardStatsContainer.js

import { useState, useEffect } from 'react';
import { getAnimalsByCriteria } from '../../services/cattle/getAnimalsByCriteria';
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
                    const animalIds = Array.from(new Set(cattleList.map(animal => animal.id)));
                    console.log(`📊 Obteniendo estimaciones para ${animalIds.length} animales...`);

                    if (animalIds.length > 0) {
                        // Procesar en lotes para no sobrecargar el servidor
                        const batchSize = 10; // Procesar 10 animales a la vez

                        for (let i = 0; i < animalIds.length; i += batchSize) {
                            const batch = animalIds.slice(i, i + batchSize);
                            console.log(`📦 Procesando lote ${Math.floor(i / batchSize) + 1}/${Math.ceil(animalIds.length / batchSize)} (${batch.length} animales)`);

                            const batchPromises = batch.map(async (animalId) => {
                                try {
                                    // Obtener todas las estimaciones de este animal con paginación
                                    let animalEstimations = [];
                                    let page = 1;
                                    let hasMore = true;
                                    const pageSize = 100;

                                    while (hasMore) {
                                        const result = await getWeightEstimationsByCriteria(
                                            { animal_id: animalId },
                                            { page, page_size: pageSize }
                                        );

                                        const weighings = result?.weighings || [];
                                        animalEstimations = [...animalEstimations, ...weighings];

                                        const total = result?.total || 0;
                                        hasMore = animalEstimations.length < total;
                                        page++;
                                    }

                                    return animalEstimations;
                                } catch (error) {
                                    console.error(`❌ Error obteniendo estimaciones para animal ${animalId}:`, error.message);
                                    return []; // Continuar si falla para un animal
                                }
                            });

                            const batchResults = await Promise.all(batchPromises);
                            estimationsList = [...estimationsList, ...batchResults.flat()];
                        }
                    }

                    console.log(`✅ Total de estimaciones obtenidas: ${estimationsList.length}`);
                } catch (estimationsError) {
                    console.error('Error al obtener estimaciones:', estimationsError);
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

