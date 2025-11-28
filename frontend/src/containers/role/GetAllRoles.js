// frontend\src\containers\role\GetAllRoles.js

import { useState, useEffect } from 'react';
import { getAllRoles } from '../../services/role/getAllRoles';

function GetAllRoles() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const data = await getAllRoles();
                setItems(data);
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

export default GetAllRoles;