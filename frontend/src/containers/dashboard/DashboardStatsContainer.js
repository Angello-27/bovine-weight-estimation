// frontend/src/containers/dashboard/DashboardStatsContainer.js

import { useState, useEffect } from 'react';
import { getDashboardStats } from '../../services/dashboard/getDashboardStats';
import {
    getCachedDashboardStats,
    setCachedDashboardStats,
    clearDashboardCache
} from '../../utils/cache/dashboardCache';

function DashboardStatsContainer() {

    const [stats, setStats] = useState({
        totalCattle: 0,
        averageWeight: 0,
        totalBreeds: 0,
        totalEstimations: 0,
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchStats = async (forceRefresh = false) => {
        try {
            setError(null);

            // Intentar obtener del caché primero (si no es refresh forzado)
            if (!forceRefresh) {
                const cached = getCachedDashboardStats();
                if (cached && typeof cached === 'object') {
                    setStats(cached);
                    setLoading(false);
                    return;
                }
            }

            // Obtener estadísticas del backend
            const statsData = await getDashboardStats();

            const finalStats = {
                totalCattle: statsData.totalCattle || 0,
                averageWeight: statsData.averageWeight || 0,
                totalBreeds: statsData.totalBreeds || 0,
                totalEstimations: statsData.totalEstimations || 0,
            };

            setStats(finalStats);
            
            // Guardar en caché
            setCachedDashboardStats(finalStats);
        } catch (err) {
            // Solo establecer error si es un error crítico
            const errorMessage = err.message || 'Error al obtener estadísticas';
            setError(errorMessage);
            console.error('Error crítico al obtener estadísticas:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchStats();
    }, []);

    // Función para refrescar datos (invalidar caché y recargar)
    const refreshStats = () => {
        clearDashboardCache();
        fetchStats(true);
    };

    return { stats, loading, error, refreshStats };
}

export default DashboardStatsContainer;

