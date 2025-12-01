// frontend/src/containers/user/ManageUserForm.js

import { useState } from 'react';

/**
 * ManageUserForm container hook - Maneja el estado y acciones del formulario de usuarios
 * @param {Object} formProps - Props del formulario de CreateNewUser
 * @returns {Object} { showForm, showDeleteDialog, deleteItem, handleCreateClick, handleEditClick, handleDeleteClick, handleCloseForm, handleCloseDeleteDialog, handleConfirmDelete }
 */
function ManageUserForm(formProps) {
    const [showForm, setShowForm] = useState(false);
    const [showDeleteDialog, setShowDeleteDialog] = useState(false);
    const [deleteItem, setDeleteItem] = useState(null);

    const resetForm = () => {
        formProps.handleChange({ target: { name: 'id', value: '' } });
        formProps.handleChange({ target: { name: 'username', value: '' } });
        formProps.handleChange({ target: { name: 'email', value: '' } });
        formProps.handleChange({ target: { name: 'password', value: '' } });
        formProps.handleChange({ target: { name: 'first_name', value: '' } });
        formProps.handleChange({ target: { name: 'last_name', value: '' } });
        formProps.handleChange({ target: { name: 'roleId', value: '' } });
        formProps.handleChange({ target: { name: 'farmId', value: '' } });
        formProps.handleChange({ target: { name: 'is_active', value: true } });
    };

    const handleCreateClick = () => {
        resetForm();
        setShowForm(true);
    };

    const handleEditClick = (userId, user) => {
        // Cargar datos del usuario en el formulario, incluyendo el id
        formProps.handleChange({ target: { name: 'id', value: userId } });
        formProps.handleChange({ target: { name: 'username', value: user.username || '' } });
        formProps.handleChange({ target: { name: 'email', value: user.email || '' } });
        formProps.handleChange({ target: { name: 'password', value: '' } }); // No mostrar contraseña
        formProps.handleChange({ target: { name: 'first_name', value: user.first_name || '' } });
        formProps.handleChange({ target: { name: 'last_name', value: user.last_name || '' } });
        formProps.handleChange({ target: { name: 'roleId', value: user.role_id || user.roleId || '' } });
        formProps.handleChange({ target: { name: 'farmId', value: user.farm_id || user.farmId || '' } });
        formProps.handleChange({ target: { name: 'is_active', value: user.is_active !== undefined ? user.is_active : true } });
        setShowForm(true);
    };

    const handleDeleteClick = (userId, user) => {
        setDeleteItem({ id: userId, name: user.username || user.email || 'este usuario' });
        setShowDeleteDialog(true);
    };

    const handleCloseForm = () => {
        // Limpiar errores al cerrar el formulario
        if (formProps.resetErrors) {
            formProps.resetErrors();
        }
        setShowForm(false);
    };

    const handleCloseDeleteDialog = () => {
        setShowDeleteDialog(false);
        setDeleteItem(null);
    };

    const handleConfirmDelete = () => {
        if (deleteItem) {
            formProps.handleDelete && formProps.handleDelete(deleteItem.id);
        }
    };

    return {
        showForm,
        showDeleteDialog,
        deleteItem,
        handleCreateClick,
        handleEditClick,
        handleDeleteClick,
        handleCloseForm,
        handleCloseDeleteDialog,
        handleConfirmDelete
    };
}

export default ManageUserForm;

