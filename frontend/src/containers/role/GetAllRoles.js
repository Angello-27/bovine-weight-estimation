// frontend/src/containers/role/GetAllRoles.js

import { useState, useEffect } from 'react';
import { getAllRoles } from '../../services/role/getAllRoles';

function GetAllRoles() {
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
            const data = await getAllRoles({ page: page + 1, page_size: pageSize });
            // El backend devuelve { total, roles, page, page_size }
            setItems(data.roles || []);
            setPagination({
                page,
                pageSize,
                total: data.total || (data.roles ? data.roles.length : 0)
            });
            setError(null);
        } catch (err) {
            setError(err?.message || 'Error al cargar los roles');
            setItems([]);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData(pagination.page, pagination.pageSize);
    }, [pagination.page, pagination.pageSize]); // Dependencias para recargar al cambiar página/tamaño

    const handlePageChange = (event, newPage) => {
        setPagination(prev => ({ ...prev, page: newPage }));
    };

    const handlePageSizeChange = (event) => {
        setPagination(prev => ({ ...prev, pageSize: parseInt(event.target.value, 10), page: 0 }));
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

export default GetAllRoles;