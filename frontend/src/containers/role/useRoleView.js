// frontend/src/containers/role/useRoleView.js

import { useState } from 'react';
import GetAllRoles from './GetAllRoles';
import CreateNewRole from './CreateNewRole';
import ManageRoleForm from './ManageRoleForm';

/**
 * Hook para manejar la lógica de la vista de roles
 * @returns {Object} Estado y funciones para la vista de roles
 */
function useRoleView() {
    const rolesProps = GetAllRoles();
    const formProps = CreateNewRole();
    const formActions = ManageRoleForm(formProps);
    
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
                showSuccess(formProps.formData.id ? 'Rol actualizado exitosamente' : 'Rol creado exitosamente');
                // Recargar la lista después de crear/editar
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            }
            // Si hay errores de validación, el formulario no se cierra y los errores se muestran en los campos
        } catch (error) {
            const errorMessage = error?.message || 'Ocurrió un error al guardar el rol. Por favor intenta de nuevo.';
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
                showSuccess('Rol eliminado exitosamente');
                // Recargar la lista después de eliminar
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            }
        } catch (error) {
            // Cerrar el dialog para que el usuario pueda ver el error
            formActions.handleCloseDeleteDialog();
            const errorMessage = error?.message || 'Ocurrió un error al eliminar el rol. Por favor intenta de nuevo.';
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
        rolesProps,
        
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

export default useRoleView;

