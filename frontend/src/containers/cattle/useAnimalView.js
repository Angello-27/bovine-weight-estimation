// frontend/src/containers/cattle/useAnimalView.js

import { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import GetAllCattle from './GetAllCattle';
import CreateNewCattle from './CreateNewCattle';
import ManageCattleForm from './ManageCattleForm';

/**
 * Hook para manejar la lógica de la vista de animales
 * @returns {Object} Estado y funciones para la vista de animales
 */
function useAnimalView() {
    const navigate = useNavigate();
    
    // Estado para filtros y búsqueda
    const [filters, setFilters] = useState({
        breed: '',
        gender: '',
        status: ''
    });
    const [searchQuery, setSearchQuery] = useState('');
    const [debouncedSearchQuery, setDebouncedSearchQuery] = useState('');
    
    // Debounce para búsqueda (300ms)
    const searchTimeoutRef = useRef(null);
    useEffect(() => {
        if (searchTimeoutRef.current) {
            clearTimeout(searchTimeoutRef.current);
        }
        
        searchTimeoutRef.current = setTimeout(() => {
            setDebouncedSearchQuery(searchQuery);
        }, 300);
        
        return () => {
            if (searchTimeoutRef.current) {
                clearTimeout(searchTimeoutRef.current);
            }
        };
    }, [searchQuery]);
    
    // Obtener animales con filtros y búsqueda (usando debouncedSearchQuery)
    const animalsProps = GetAllCattle(filters, debouncedSearchQuery);
    const formProps = CreateNewCattle();
    const formActions = ManageCattleForm(formProps);
    
    // Handlers para filtros y búsqueda
    const handleFilterChange = (name, value) => {
        setFilters(prev => ({
            ...prev,
            [name]: value
        }));
    };
    
    const handleSearchChange = (event) => {
        setSearchQuery(event.target.value);
    };
    
    const [errorSnackbar, setErrorSnackbar] = useState({
        open: false,
        message: ''
    });
    const [successSnackbar, setSuccessSnackbar] = useState({
        open: false,
        message: ''
    });

    const showError = (message) => {
        setErrorSnackbar({ open: true, message });
    };

    const showSuccess = (message) => {
        setSuccessSnackbar({ open: true, message });
    };

    const handleSubmit = async (e) => {
        try {
            const success = await formProps.handleSubmit(e);
            // Solo cerrar el dialog y mostrar éxito si la validación fue exitosa
            if (success) {
                formActions.handleCloseForm();
                showSuccess(formProps.formData.id ? 'Animal actualizado exitosamente' : 'Animal creado exitosamente');
                // Recargar la lista después de crear/editar
                if (animalsProps.refetch) {
                    animalsProps.refetch();
                } else {
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                }
            }
            // Si hay errores de validación, el formulario no se cierra y los errores se muestran en los campos
        } catch (error) {
            const errorMessage = error?.message || 'Ocurrió un error al guardar el animal. Por favor intenta de nuevo.';
            showError(errorMessage);
            console.error('Error al guardar:', error);
        }
    };

    const handleConfirmDelete = async () => {
        try {
            if (formActions.deleteItem) {
                await formProps.handleDelete(formActions.deleteItem.id);
                // Cerrar el dialog antes de mostrar el éxito
                formActions.handleCloseDeleteDialog();
                showSuccess('Animal eliminado exitosamente');
                // Recargar la lista después de eliminar
                if (animalsProps.refetch) {
                    animalsProps.refetch();
                } else {
                    setTimeout(() => {
                        window.location.reload();
                    }, 1500);
                }
            }
        } catch (error) {
            // Cerrar el dialog para que el usuario pueda ver el error
            formActions.handleCloseDeleteDialog();
            const errorMessage = error?.message || 'Ocurrió un error al eliminar el animal. Por favor intenta de nuevo.';
            showError(errorMessage);
            console.error('Error al eliminar:', error);
        }
    };

    const closeErrorSnackbar = () => {
        setErrorSnackbar({ open: false, message: '' });
    };

    const closeSuccessSnackbar = () => {
        setSuccessSnackbar({ open: false, message: '' });
    };

    return {
        // Props de las listas
        animalsProps,
        
        // Props del formulario
        formProps,
        formActions,
        
        // Filtros y búsqueda
        filters,
        searchQuery,
        handleFilterChange,
        handleSearchChange,
        
        // Handlers
        handleSubmit,
        handleConfirmDelete,
        handleViewClick: (animalId) => navigate(`/animals/${animalId}`),
        
        // Snackbars
        errorSnackbar,
        successSnackbar,
        closeErrorSnackbar,
        closeSuccessSnackbar,
    };
}

export default useAnimalView;

