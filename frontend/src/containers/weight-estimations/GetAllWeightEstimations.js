// frontend/src/containers/weight-estimations/GetAllWeightEstimations.js

import { useState, useEffect } from 'react';
import getAllWeightEstimations from '../../services/weight-estimations/getAllWeightEstimations';

function GetAllWeightEstimations() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const data = await getAllWeightEstimations();
                // El servicio puede retornar { weighings: [...] } o directamente el array
                const estimationsList = data.weighings || data || [];
                setItems(estimationsList);
            } catch (err) {
                setError(err.message);
                console.error('Error al obtener estimaciones:', err);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    return { items, loading, error };
}

export default GetAllWeightEstimations;

