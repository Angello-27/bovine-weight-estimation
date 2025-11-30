// frontend/src/containers/dashboard/DashboardStatsContainer.js

import { useState, useEffect } from 'react';
import getAllCattle from '../../services/cattle/getAllCattle';
import getAllWeightEstimations from '../../services/weight-estimations/getAllWeightEstimations';

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
                
                // Obtener datos de animales con manejo de errores mejorado
                let cattleList = [];
                try {
                    const cattleData = await getAllCattle();
                    // El backend puede retornar { animals: [], total: 0 } o directamente []
                    cattleList = Array.isArray(cattleData) 
                        ? cattleData 
                        : (cattleData?.animals || []);
                } catch (cattleError) {
                    console.warn('Error al obtener animales (continuando):', cattleError);
                    // Continuar aunque falle, mostrar 0
                }

                // Obtener datos de estimaciones con manejo de errores mejorado
                let estimationsList = [];
                try {
                    const estimationsData = await getAllWeightEstimations();
                    // El backend puede retornar { weighings: [], total: 0 } o directamente []
                    estimationsList = Array.isArray(estimationsData)
                        ? estimationsData
                        : (estimationsData?.weighings || []);
                } catch (estimationsError) {
                    console.warn('Error al obtener estimaciones (continuando):', estimationsError);
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

