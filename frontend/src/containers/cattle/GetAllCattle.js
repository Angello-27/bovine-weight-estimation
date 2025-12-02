// frontend/src/containers/cattle/GetAllCattle.js

import { useState, useEffect } from 'react';
import { getAnimalsByCriteria } from '../../services/cattle';
import { getCurrentUser } from '../../services/auth/authService';
import { getAllFarms } from '../../services/farm/getAllFarms';

function GetAllCattle() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [page, setPage] = useState(0);
    const [pageSize, setPageSize] = useState(10);
    const [totalItems, setTotalItems] = useState(0);

    const fetchData = async () => {
        try {
            setLoading(true);
            setError(null);

            // Intentar obtener farm_id del usuario
            const currentUser = getCurrentUser();
            let farmId = currentUser?.farm_id;
            
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
            
            const data = await getAnimalsByCriteria(
                { farm_id: farmId },
                { page: page + 1, page_size: pageSize } // Backend usa página basada en 1
            );
            
            // El servicio retorna { animals: [...], total, page, page_size }
            const cattleList = data?.animals || [];
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
    }, [page, pageSize]);

    const pagination = {
        page,
        pageSize,
        total: totalItems,
    };

    const onPageChange = (newPage, pageSize) => {
        // DataTable pasa (newPage, pageSize) desde handleChangePage
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

