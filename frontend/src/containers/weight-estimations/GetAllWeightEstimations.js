// frontend/src/containers/weight-estimations/GetAllWeightEstimations.js

import { useState, useEffect } from 'react';
import { getWeightEstimationsByCriteria } from '../../services/weight-estimations/getWeightEstimationsByCriteria';
import { deleteWeightEstimation } from '../../services/weight-estimations/deleteWeightEstimation';
import {
    getCachedEstimations,
    setCachedEstimations,
    clearCache,
    removeEstimationFromCache
} from '../../utils/cache/weightEstimationsCache';

function GetAllWeightEstimations() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [pagination, setPagination] = useState({
        page: 0,
        pageSize: 10,
        total: 0
    });

    const fetchAllData = async (forceRefresh = false) => {
        try {
            setLoading(true);
            setError(null);
            
            // Intentar obtener del caché primero (si no es refresh forzado)
            if (!forceRefresh) {
                const cached = getCachedEstimations();
                if (cached && Array.isArray(cached) && cached.length > 0) {
                    setItems(cached);
                    setPagination({
                        page: 0,
                        pageSize: cached.length,
                        total: cached.length
                    });
                    setLoading(false);
                    return;
                }
            }
            
            // Cargar todos los registros usando paginación iterativa (como en dashboard)
            let allEstimations = [];
            let page = 1;
            let hasMore = true;
            const pageSize = 500;

            while (hasMore) {
                try {
                    // Usar getWeightEstimationsByCriteria como en el dashboard (sin filtros)
                    const data = await getWeightEstimationsByCriteria(
                        {}, // Sin filtros
                        { page, page_size: pageSize }
                    );

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

                    console.log(`📊 Página ${page}: Obtenidos ${weighings.length} registros, Total acumulado: ${allEstimations.length}, Total del backend: ${total}`);

                    // Verificar si hay más páginas
                    hasMore = total > 0 && allEstimations.length < total;
                    
                    // Si no hay más registros en esta página, detener
                    if (weighings.length === 0) {
                        console.log(`✅ No hay más registros en la página ${page}, deteniendo carga`);
                        break;
                    }
                    
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

            console.log(`✅ Carga completa: ${allEstimations.length} estimaciones cargadas`);

            // Guardar en caché
            setCachedEstimations(allEstimations, 30); // 30 minutos de TTL

            // La información del animal ya viene en la respuesta del backend
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

    // Estado del diálogo de eliminación
    const [showDeleteDialog, setShowDeleteDialog] = useState(false);
    const [deleteItem, setDeleteItem] = useState(null);

    const handleDeleteClick = (estimationId, estimation) => {
        setDeleteItem({ id: estimationId, estimation });
        setShowDeleteDialog(true);
    };

    const handleCloseDeleteDialog = () => {
        setShowDeleteDialog(false);
        setDeleteItem(null);
    };

    const handleConfirmDelete = async () => {
        if (!deleteItem) return;

        try {
            await deleteWeightEstimation(deleteItem.id);
            
            // Eliminar del caché inmediatamente (actualización optimista)
            removeEstimationFromCache(deleteItem.id);
            
            // Actualizar el estado local sin recargar todo
            setItems(prevItems => prevItems.filter(item => item.id !== deleteItem.id));
            setPagination(prev => ({
                ...prev,
                total: prev.total - 1
            }));
            
            // Cerrar el diálogo
            handleCloseDeleteDialog();
        } catch (error) {
            // Cerrar el diálogo para que el usuario pueda ver el error
            handleCloseDeleteDialog();
            alert(`Error al eliminar la estimación: ${error.message}`);
            console.error('Error al eliminar estimación:', error);
            
            // Si falla, recargar desde el servidor para sincronizar
            await fetchAllData(true);
        }
    };

    // Función para refrescar datos (útil para invalidar caché manualmente)
    const refreshData = () => {
        clearCache();
        fetchAllData(true);
    };

    return { 
        items: paginatedItems, 
        loading, 
        error,
        pagination: tablePagination,
        onPageChange: handlePageChange,
        onPageSizeChange: handlePageSizeChange,
        onDeleteClick: handleDeleteClick,
        showDeleteDialog,
        deleteItem,
        onCloseDeleteDialog: handleCloseDeleteDialog,
        onConfirmDelete: handleConfirmDelete,
        refreshData // Exportar función de refresh
    };
}

export default GetAllWeightEstimations;

