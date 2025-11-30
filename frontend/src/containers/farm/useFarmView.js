// frontend/src/containers/farm/useFarmView.js

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import GetAllFarms from './GetAllFarms';
import GetAllUsers from '../user/GetAllUsers';
import CreateNewFarm from './CreateNewFarm';
import ManageFarmForm from './ManageFarmForm';

/**
 * Hook para manejar la lógica de la vista de haciendas
 * @returns {Object} Estado y funciones para la vista de haciendas
 */
function useFarmView() {
    const navigate = useNavigate();
    const farmsProps = GetAllFarms();
    const usersProps = GetAllUsers();
    const formProps = CreateNewFarm();
    const formActions = ManageFarmForm(formProps);
    
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
                showSuccess(formProps.formData.id ? 'Hacienda actualizada exitosamente' : 'Hacienda creada exitosamente');
                // Recargar la lista después de crear/editar
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            }
            // Si hay errores de validación, el formulario no se cierra y los errores se muestran en los campos
        } catch (error) {
            const errorMessage = error?.message || 'Ocurrió un error al guardar la hacienda. Por favor intenta de nuevo.';
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
                showSuccess('Hacienda eliminada exitosamente');
                // Recargar la lista después de eliminar
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            }
        } catch (error) {
            // Cerrar el dialog para que el usuario pueda ver el error
            formActions.handleCloseDeleteDialog();
            const errorMessage = error?.message || 'Ocurrió un error al eliminar la hacienda. Por favor intenta de nuevo.';
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
        farmsProps,
        usersProps,
        
        // Props del formulario
        formProps,
        formActions,
        
        // Handlers
        handleSubmit,
        handleConfirmDelete,
        handleViewClick: (farmId) => navigate(`/farms/${farmId}`),
        
        // Snackbars
        errorSnackbar,
        successSnackbar,
        closeErrorSnackbar,
        closeSuccessSnackbar,
    };
}

export default useFarmView;

