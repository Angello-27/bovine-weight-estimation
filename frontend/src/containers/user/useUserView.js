// frontend/src/containers/user/useUserView.js

import { useState } from 'react';
import GetAllUsers from './GetAllUsers';
import GetAllRoles from '../role/GetAllRoles';
import GetAllFarms from '../farm/GetAllFarms';
import CreateNewUser from './CreateNewUser';
import ManageUserForm from './ManageUserForm';

/**
 * Hook para manejar la lógica de la vista de usuarios
 * @returns {Object} Estado y funciones para la vista de usuarios
 */
function useUserView() {
    const usersProps = GetAllUsers();
    const rolesProps = GetAllRoles();
    const farmsProps = GetAllFarms();
    const formProps = CreateNewUser();
    const formActions = ManageUserForm(formProps);
    
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
                showSuccess(formProps.formData.id ? 'Usuario actualizado exitosamente' : 'Usuario creado exitosamente');
                // Recargar la lista después de crear/editar
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            }
            // Si hay errores de validación, el formulario no se cierra y los errores se muestran en los campos
        } catch (error) {
            const errorMessage = error?.message || 'Ocurrió un error al guardar el usuario. Por favor intenta de nuevo.';
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
                showSuccess('Usuario eliminado exitosamente');
                // Recargar la lista después de eliminar
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            }
        } catch (error) {
            // Cerrar el dialog para que el usuario pueda ver el error
            formActions.handleCloseDeleteDialog();
            const errorMessage = error?.message || 'Ocurrió un error al eliminar el usuario. Por favor intenta de nuevo.';
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
        usersProps,
        rolesProps,
        farmsProps,
        
        // Props del formulario
        formProps,
        formActions,
        
        // Handlers
        handleSubmit,
        handleConfirmDelete,
        
        // Snackbars
        errorSnackbar,
        successSnackbar,
        closeErrorSnackbar,
        closeSuccessSnackbar,
    };
}

export default useUserView;

