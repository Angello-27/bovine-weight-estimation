// frontend/src/containers/cattle/GetAllCattle.js

import { useState, useEffect } from 'react';
import { getAllCattle } from '../../services/cattle/getAllCattle';

function GetAllCattle() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const data = await getAllCattle();
                // El servicio puede retornar { animals: [...] } o directamente el array
                const cattleList = data.animals || data || [];
                setItems(cattleList);
            } catch (err) {
                setError(err.message);
                console.error('Error al obtener animales:', err);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    return { items, loading, error };
}

export default GetAllCattle;

