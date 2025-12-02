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

    const fetchAllData = async () => {
        try {
            setLoading(true);
            setError(null);
            
            // Cargar todos los registros usando paginación iterativa (como en dashboard)
            let allEstimations = [];
            let page = 1;
            let hasMore = true;
            const pageSize = 100;

            while (hasMore) {
                try {
                    const data = await getAllWeightEstimations({ 
                        page, 
                        page_size: pageSize 
                    });

                    if (!data || typeof data !== 'object') {
                        console.warn(`⚠️ Respuesta inválida en página ${page}:`, data);
                        break;
                    }

                    const weighings = Array.isArray(data.weighings) 
                        ? data.weighings 
                        : Array.isArray(data) 
                            ? data 
                            : [];
                    
                    allEstimations = [...allEstimations, ...weighings];

                    const total = data.total || 0;

                    // Verificar si hay más páginas
                    hasMore = total > 0 && allEstimations.length < total;
                    
                    // Prevenir loops infinitos
                    if (page > 1000) {
                        console.warn(`⚠️ Límite de páginas alcanzado (1000)`);
                        break;
                    }
                    
                    page++;
                } catch (pageError) {
                    console.error(`❌ Error obteniendo página ${page} de estimaciones:`, {
                        message: pageError.message,
                        response: pageError.response?.data
                    });
                    break;
                }
            }

            setItems(allEstimations);
            setPagination({
                page: 0,
                pageSize: allEstimations.length,
                total: allEstimations.length
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
        fetchAllData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    // Paginación del lado del cliente cuando todos los datos están cargados
    const [currentPage, setCurrentPage] = useState(0);
    const [currentPageSize, setCurrentPageSize] = useState(10);

    // Calcular items paginados del lado del cliente
    const paginatedItems = items.slice(
        currentPage * currentPageSize,
        currentPage * currentPageSize + currentPageSize
    );

    const handlePageChange = (newPage, newPageSize) => {
        // Cuando se cargan todos los registros, la paginación es solo visual (lado del cliente)
        setCurrentPage(newPage);
        if (newPageSize !== currentPageSize) {
            setCurrentPageSize(newPageSize);
        }
    };

    const handlePageSizeChange = (newPageSize) => {
        // Cambiar el tamaño de página solo afecta la visualización
        setCurrentPageSize(newPageSize);
        setCurrentPage(0);
    };

    // Paginación para el DataTable
    const tablePagination = {
        page: currentPage,
        pageSize: currentPageSize,
        total: items.length
    };

    return { 
        items: paginatedItems, 
        loading, 
        error,
        pagination: tablePagination,
        onPageChange: handlePageChange,
        onPageSizeChange: handlePageSizeChange
    };
}

export default GetAllWeightEstimations;

