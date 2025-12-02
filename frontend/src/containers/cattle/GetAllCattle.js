// frontend/src/containers/cattle/GetAllCattle.js

import { useState, useEffect, useMemo } from 'react';
import { getAnimalsByCriteria } from '../../services/cattle';
import { getCurrentUser } from '../../services/auth/authService';
import { getAllFarms } from '../../services/farm/getAllFarms';

/**
 * Hook para obtener todos los animales con filtros y búsqueda
 * @param {Object} filters - Filtros { breed, gender, status, farm_id }
 * @param {string} searchQuery - Texto de búsqueda (caravana, nombre)
 */
function GetAllCattle(filters = {}, searchQuery = '') {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(0);
    const [pageSize, setPageSize] = useState(10);
    const [totalItems, setTotalItems] = useState(0);

    // Memoizar valores de filtros para evitar renders innecesarios
    const breedFilter = filters?.breed || '';
    const genderFilter = filters?.gender || '';
    const statusFilter = filters?.status || '';
    const farmIdFilter = filters?.farm_id || '';
    const searchText = searchQuery || '';

    const fetchData = async () => {
        try {
            setLoading(true);
            setError(null);

            // Intentar obtener farm_id del usuario
            const currentUser = getCurrentUser();
            let farmId = filters.farm_id || currentUser?.farm_id;
            
            // Si el usuario no tiene farm_id, obtener la primera hacienda disponible
            if (!farmId) {
                try {
                    const farmsResponse = await getAllFarms({ limit: 1 });
                    if (farmsResponse?.farms && farmsResponse.farms.length > 0) {
                        farmId = farmsResponse.farms[0].id;
                    }
                } catch (e) {
                    console.warn('No se pudo obtener haciendas:', e);
                }
            }
            
            // Llamar al servicio con farm_id
            if (!farmId) {
                throw new Error('No se encontró una hacienda. Por favor, contacta al administrador para asignarte una hacienda.');
            }
            
            // Construir filtros para el backend
            const backendFilters = {
                farm_id: farmId,
            };

            // Agregar filtros opcionales solo si tienen valor
            if (breedFilter) backendFilters.breed = breedFilter;
            if (genderFilter) backendFilters.gender = genderFilter;
            if (statusFilter) backendFilters.status = statusFilter;

            // Si hay búsqueda por texto, agregarla como filtro
            // Nota: El backend puede necesitar un parámetro específico para búsqueda
            // Por ahora, si el backend no soporta búsqueda, se filtrará en el frontend
            if (searchText && searchText.trim()) {
                // Si el backend soporta búsqueda, agregar aquí
                // backendFilters.search = searchText.trim();
            }
            
            const data = await getAnimalsByCriteria(
                backendFilters,
                { page: page + 1, page_size: pageSize } // Backend usa página basada en 1
            );
            
            // El servicio retorna { animals: [...], total, page, page_size }
            let cattleList = data?.animals || [];

            // Filtrar por búsqueda en el frontend si el backend no lo soporta
            if (searchText && searchText.trim()) {
                const query = searchText.toLowerCase().trim();
                cattleList = cattleList.filter(animal => 
                    animal.ear_tag?.toLowerCase().includes(query) ||
                    animal.name?.toLowerCase().includes(query) ||
                    animal.breed?.toLowerCase().includes(query)
                );
            }

            setItems(cattleList);
            setTotalItems(data?.total || 0);
        } catch (err) {
            const errorMessage = err?.message || err?.toString() || 'Error al obtener animales';
            setError(errorMessage);
            console.error('Error al obtener animales:', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [page, pageSize, breedFilter, genderFilter, statusFilter, farmIdFilter, searchText]);

    const pagination = {
        page,
        pageSize,
        total: totalItems,
    };

    const onPageChange = (newPage) => {
        // DataTable pasa (newPage) desde handleChangePage
        setPage(newPage);
    };

    const onPageSizeChange = (newPageSize) => {
        // DataTable pasa (newPageSize) desde handleChangeRowsPerPage
        setPageSize(newPageSize);
        setPage(0);
    };

    return { 
        items, 
        loading, 
        error,
        pagination,
        onPageChange,
        onPageSizeChange,
        refetch: fetchData
    };
}

export default GetAllCattle;

