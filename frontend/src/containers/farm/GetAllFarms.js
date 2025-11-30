// frontend/src/containers/farm/GetAllFarms.js

import { useState, useEffect } from 'react';
import { getAllFarms } from '../../services/farm/getAllFarms';

function GetAllFarms() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [pagination, setPagination] = useState({
        page: 0,
        pageSize: 10,
        total: 0
    });

    const fetchData = async (page = 0, pageSize = 10) => {
        try {
            setLoading(true);
            const data = await getAllFarms({ page: page + 1, page_size: pageSize });
            // El backend devuelve { total, farms, page, page_size }
            setItems(data.farms || data || []);
            setPagination({
                page,
                pageSize,
                total: data.total || (data.farms ? data.farms.length : 0)
            });
            setError(null);
        } catch (err) {
            setError(err?.message || 'Error al cargar las haciendas');
            setItems([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData(0, 10);
    }, []);

    const handlePageChange = (newPage, newPageSize) => {
        fetchData(newPage, newPageSize);
    };

    const handlePageSizeChange = (newPageSize) => {
        fetchData(0, newPageSize);
    };

    return { 
        items, 
        loading, 
        error, 
        pagination,
        onPageChange: handlePageChange,
        onPageSizeChange: handlePageSizeChange
    };
}

export default GetAllFarms;

