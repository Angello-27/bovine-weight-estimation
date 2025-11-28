// frontend/src/containers/weight-estimations/GetWeightEstimationById.js

import { useState, useEffect } from 'react';
import getWeightEstimationById from '../../services/weight-estimations/getWeightEstimationById';

function GetWeightEstimationById(id) {
    const [estimation, setEstimation] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                setLoading(true);
                const data = await getWeightEstimationById(id);
                setEstimation(data);
            } catch (err) {
                setError(err.message);
                console.error(`Error al obtener estimación ${id}:`, err);
            } finally {
                setLoading(false);
            }
        }
        if (id) {
            fetchData();
        }
    }, [id]);

    return { estimation, loading, error };
}

export default GetWeightEstimationById;

