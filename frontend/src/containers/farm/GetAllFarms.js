// frontend/src/containers/farm/GetAllFarms.js

import { useState, useEffect } from 'react';
import { getAllFarms } from '../../services/farm/getAllFarms';
import { getFarmsByCriteria } from '../../services/farm/getFarmsByCriteria';

function GetAllFarms() {
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
            
            // Si hay filtros (como owner_id), usar getFarmsByCriteria
            // De lo contrario, usar getAllFarms para obtener todas las farms
            let data;
            if (filters.owner_id) {
                // Convertir page a skip para el endpoint by-criteria
                const skip = page * pageSize;
                data = await getFarmsByCriteria(
                    filters,
                    { skip, limit: pageSize }
                );
            } else {
                // Convertir page a skip para el endpoint get_all
                const skip = page * pageSize;
                data = await getAllFarms({ skip, limit: pageSize });
            }
            
            // El backend devuelve { total, farms, page, page_size }
            // Asegurar que items siempre sea un array
            const farmsArray = Array.isArray(data.farms) 
                ? data.farms 
                : Array.isArray(data) 
                    ? data 
                    : [];
            
            setItems(farmsArray);
            setPagination({
                page,
                pageSize,
                total: data.total || farmsArray.length
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

export default GetAllFarms;

