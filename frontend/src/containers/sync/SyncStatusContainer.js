// frontend/src/containers/sync/SyncStatusContainer.js

import { useState, useEffect } from 'react';
import { getSyncHealth } from '../../services/sync/getSyncHealth';
import { getSyncStats } from '../../services/sync/getSyncStats';

function SyncStatusContainer() {
    const [health, setHealth] = useState({
        status: 'unknown',
        database: 'unknown',
    });
    const [stats, setStats] = useState({
        totalSynced: 0,
        pendingItems: 0,
        lastSync: null,
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchSyncData() {
            try {
                // Obtener estado de salud
                const healthData = await getSyncHealth();
                setHealth({
                    status: healthData.status || 'unknown',
                    database: healthData.database || 'unknown',
                });

                // Obtener estadísticas
                const statsData = await getSyncStats();
                setStats({
                    totalSynced: statsData.total_synced || 0,
                    pendingItems: statsData.pending_items || 0,
                    lastSync: statsData.last_sync || null,
                });
            } catch (err) {
                setError(err.message);
                console.error('Error al obtener estado de sincronización:', err);
            } finally {
                setLoading(false);
            }
        }

        fetchSyncData();
    }, []);

    return { health, stats, loading, error };
}

export default SyncStatusContainer;

