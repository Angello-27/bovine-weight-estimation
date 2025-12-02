// frontend/src/containers/cattle/GetCattleById.js

import { useState, useEffect } from 'react';
import { getCattleById } from '../../services/cattle';

function GetCattleById(cattleId) {
    const [cattle, setCattle] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!cattleId) {
            setLoading(false);
            return;
        }

        async function fetchData() {
            try {
                const data = await getCattleById(cattleId);
                setCattle(data);
            } catch (err) {
                setError(err.message || 'Error al obtener el animal');
                console.error('Error al obtener animal:', err);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [cattleId]);

    return { cattle, loading, error };
}

export default GetCattleById;

