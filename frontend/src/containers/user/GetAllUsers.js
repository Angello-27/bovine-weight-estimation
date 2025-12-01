// frontend/src/containers/user/GetAllUsers.js

import { useState, useEffect } from 'react';
import { getAllUsers } from '../../services/user/getAllUsers';
import { getUsersByCriteria } from '../../services/user/getUsersByCriteria';

function GetAllUsers() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [pagination, setPagination] = useState({
        page: 0,
        pageSize: 10,
        total: 0
    });

    const fetchData = async (page = 0, pageSize = 10, filters = {}) => {
        try {
            setLoading(true);
            
            // Convertir page y pageSize a skip y limit
            const skip = page * pageSize;
            const limit = pageSize;
            
            // Si hay filtros (como role_id, is_active, farm_id), usar getUsersByCriteria
            // De lo contrario, usar getAllUsers para obtener todos los usuarios
            let data;
            if (filters.role_id || filters.is_active !== undefined || filters.farm_id) {
                data = await getUsersByCriteria(
                    filters,
                    { skip, limit }
                );
            } else {
                data = await getAllUsers({ skip, limit });
            }
            
            // El backend devuelve { total, users, page, page_size }
            setItems(data.users || []);
            setPagination({
                page,
                pageSize,
                total: data.total || (data.users ? data.users.length : 0)
            });
            setError(null);
        } catch (err) {
            setError(err?.message || 'Error al cargar los usuarios');
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

    // Función para recargar con filtros opcionales
    const reloadWithFilters = (filters = {}) => {
        fetchData(pagination.page, pagination.pageSize, filters);
    };

    return { 
        items, 
        loading, 
        error,
        pagination,
        onPageChange: handlePageChange,
        onPageSizeChange: handlePageSizeChange,
        reloadWithFilters
    };
}

export default GetAllUsers;

