// frontend/src/containers/weight-estimations/GetWeightHistoryByCattle.js

import { useState, useEffect } from 'react';
import getWeightEstimationsByCattleId from '../../services/weight-estimations/getWeightEstimationsByCattleId';

function GetWeightHistoryByCattle(cattleId) {
    const [estimations, setEstimations] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!cattleId) {
            setLoading(false);
            return;
        }

        async function fetchData() {
            try {
                const data = await getWeightEstimationsByCattleId(cattleId);
                // Ordenar por fecha (más reciente primero)
                const sorted = (data || []).sort((a, b) => 
                    new Date(b.timestamp) - new Date(a.timestamp)
                );
                setEstimations(sorted);
            } catch (err) {
                setError(err.message || 'Error al obtener el historial de pesos');
                console.error('Error al obtener historial:', err);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [cattleId]);

    return { estimations, loading, error };
}

export default GetWeightHistoryByCattle;

