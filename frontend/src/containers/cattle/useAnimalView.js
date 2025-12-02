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
    const [searchInput, setSearchInput] = useState(''); // Valor del input (no aplicado aún)
    const [searchQuery, setSearchQuery] = useState(''); // Búsqueda aplicada
    
    // Obtener animales con filtros y búsqueda
    const animalsProps = GetAllCattle(filters, searchQuery);
    const formProps = CreateNewCattle();
    const formActions = ManageCattleForm(formProps);
    
    // Handlers para filtros y búsqueda
    const handleFilterChange = (name, value) => {
        setFilters(prev => ({
            ...prev,
            [name]: value
        }));
    };
    
    const handleSearchInputChange = (event) => {
        // Solo actualizar el valor del input, no aplicar búsqueda
        setSearchInput(event.target.value);
    };
    
    const handleSearchApply = (value) => {
        // Aplicar la búsqueda cuando se presiona el botón
        const searchValue = value !== undefined ? value : searchInput;
        setSearchInput(searchValue);
        setSearchQuery(searchValue);
    };
    
    const handleSearchClear = () => {
        // Limpiar búsqueda
        setSearchInput('');
        setSearchQuery('');
    };
    
    const handleSearchChange = (event) => {
        // Manejar tanto cambios en el input como acciones (buscar/limpiar)
        if (event.type === 'clear') {
            handleSearchClear();
        } else if (event.type === 'search') {
            // Aplicar búsqueda con el valor del evento
            handleSearchApply(event.target.value);
        } else {
            // Cambio normal en el input - solo actualizar el valor del input
            handleSearchInputChange(event);
        }
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
        searchQuery: searchInput, // Pasar el valor del input para mostrar en el campo
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

