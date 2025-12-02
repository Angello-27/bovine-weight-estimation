// frontend/src/containers/weight-estimations/GetAllWeightEstimations.js

import { useState, useEffect } from 'react';
import getAllWeightEstimations from '../../services/weight-estimations/getAllWeightEstimations';

function GetAllWeightEstimations() {
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
            setError(null);
            
            // Convertir page a formato de API (page 1-based)
            const apiPage = page + 1;
            const data = await getAllWeightEstimations({ 
                page: apiPage, 
                page_size: pageSize 
            });
            
            // El backend devuelve { total, weighings, page, page_size }
            // Asegurar que items siempre sea un array
            const estimationsList = Array.isArray(data.weighings) 
                ? data.weighings 
                : Array.isArray(data) 
                    ? data 
                    : [];
            
            setItems(estimationsList);
            setPagination({
                page,
                pageSize,
                total: data.total || estimationsList.length
            });
        } catch (err) {
            setError(err?.message || 'Error al cargar las estimaciones de peso');
            setItems([]);
            console.error('Error al obtener estimaciones:', err);
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

export default GetAllWeightEstimations;

