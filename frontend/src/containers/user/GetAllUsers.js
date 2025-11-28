// frontend/src/containers/user/GetAllUsers.js

import { useState, useEffect } from 'react';
import { getAllUsers } from '../../services/user/getAllUsers';

function GetAllUsers() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                const data = await getAllUsers();
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

export default GetAllUsers;

