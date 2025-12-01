// frontend/src/containers/role/ManageRoleForm.js

import { useState } from 'react';

/**
 * ManageRoleForm container hook - Maneja el estado y acciones del formulario de roles
 * @param {Object} formProps - Props del formulario de CreateNewRole
 * @returns {Object} { showForm, showDeleteDialog, deleteItem, handleCreateClick, handleEditClick, handleDeleteClick, handleCloseForm, handleCloseDeleteDialog, handleConfirmDelete }
 */
function ManageRoleForm(formProps) {
    const [showForm, setShowForm] = useState(false);
    const [showDeleteDialog, setShowDeleteDialog] = useState(false);
    const [deleteItem, setDeleteItem] = useState(null);

    const resetForm = () => {
        formProps.handleChange({ target: { name: 'id', value: '' } });
        formProps.handleChange({ target: { name: 'name', value: '' } });
        formProps.handleChange({ target: { name: 'description', value: '' } });
        formProps.handleChange({ target: { name: 'priority', value: 'Invitado' } });
    };

    const handleCreateClick = () => {
        resetForm();
        setShowForm(true);
    };

    const handleEditClick = (roleId, role) => {
        // Cargar datos del rol en el formulario, incluyendo el id
        formProps.handleChange({ target: { name: 'id', value: roleId } });
        formProps.handleChange({ target: { name: 'name', value: role.name || '' } });
        formProps.handleChange({ target: { name: 'description', value: role.description || '' } });
        formProps.handleChange({ target: { name: 'priority', value: role.priority || 'Invitado' } });
        setShowForm(true);
    };

    const handleDeleteClick = (roleId, role) => {
        setDeleteItem({ id: roleId, name: role.name });
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

export default ManageRoleForm;

