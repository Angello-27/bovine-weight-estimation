// frontend/src/containers/farm/ManageFarmForm.js

import { useState } from 'react';

/**
 * ManageFarmForm container hook - Maneja el estado y acciones del formulario de haciendas
 * @param {Object} formProps - Props del formulario de CreateNewFarm
 * @returns {Object} { showForm, showDeleteDialog, deleteItem, handleCreateClick, handleEditClick, handleDeleteClick, handleCloseForm, handleCloseDeleteDialog, handleConfirmDelete }
 */
function ManageFarmForm(formProps) {
    const [showForm, setShowForm] = useState(false);
    const [showDeleteDialog, setShowDeleteDialog] = useState(false);
    const [deleteItem, setDeleteItem] = useState(null);

    const resetForm = () => {
        formProps.handleChange({ target: { name: 'id', value: '' } });
        formProps.handleChange({ target: { name: 'name', value: '' } });
        formProps.handleChange({ target: { name: 'owner_id', value: '' } });
        formProps.handleChange({ target: { name: 'latitude', value: '' } });
        formProps.handleChange({ target: { name: 'longitude', value: '' } });
        formProps.handleChange({ target: { name: 'capacity', value: '' } });
    };

    const handleCreateClick = () => {
        resetForm();
        setShowForm(true);
    };

    const handleEditClick = (farmId, farm) => {
        // Cargar datos de la hacienda en el formulario, incluyendo el id
        formProps.handleChange({ target: { name: 'id', value: farmId } });
        formProps.handleChange({ target: { name: 'name', value: farm.name || '' } });
        formProps.handleChange({ target: { name: 'owner_id', value: farm.owner_id || '' } });
        formProps.handleChange({ target: { name: 'latitude', value: farm.latitude || '' } });
        formProps.handleChange({ target: { name: 'longitude', value: farm.longitude || '' } });
        formProps.handleChange({ target: { name: 'capacity', value: farm.capacity || '' } });
        setShowForm(true);
    };

    const handleDeleteClick = (farmId, farm) => {
        setDeleteItem({ id: farmId, name: farm.name });
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

export default ManageFarmForm;

