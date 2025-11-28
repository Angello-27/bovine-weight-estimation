// frontend/src/containers/farm/GetAllFarms.js

import { useState, useEffect } from 'react';
import { getAllFarms } from '../../services/farm/getAllFarms';

function GetAllFarms() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const data = await getAllFarms({ page: 1, page_size: 100 });
                // El backend devuelve { total, farms, page, page_size }
                setItems(data.farms || data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    return { items, loading, error };
}

export default GetAllFarms;

