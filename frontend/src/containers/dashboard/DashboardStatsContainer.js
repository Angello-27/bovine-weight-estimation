// frontend/src/containers/dashboard/DashboardStatsContainer.js

import { useState, useEffect } from 'react';
import { getAllCattle } from '../../services/cattle/getAllCattle';
import { getAllWeightEstimations } from '../../services/weight-estimations/getAllWeightEstimations';

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
                // Obtener datos de animales
                const cattleData = await getAllCattle();
                const cattleList = cattleData.animals || cattleData || [];

                // Obtener datos de estimaciones
                const estimationsData = await getAllWeightEstimations();
                const estimationsList = estimationsData.weighings || estimationsData || [];

                // Calcular estadísticas
                const totalCattle = cattleList.length;
                
                // Calcular peso promedio (de estimaciones más recientes por animal)
                const weights = estimationsList
                    .map(est => est.estimated_weight)
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
                setError(err.message);
                console.error('Error al obtener estadísticas:', err);
            } finally {
                setLoading(false);
            }
        }

        fetchStats();
    }, []);

    return { stats, loading, error };
}

export default DashboardStatsContainer;

