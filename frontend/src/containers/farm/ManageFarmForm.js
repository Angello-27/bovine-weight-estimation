// frontend/src/containers/farm/ManageFarmForm.js

import { useState } from 'react';

/**
 * ManageFarmForm container hook - Maneja el estado y acciones del formulario de fincas
 * @param {Object} formProps - Props del formulario de CreateNewFarm
 * @returns {Object} { showForm, handleCreateClick, handleEditClick, handleDeleteClick, handleCloseForm }
 */
function ManageFarmForm(formProps) {
    const [showForm, setShowForm] = useState(false);

    const resetForm = () => {
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
        // Cargar datos de la finca en el formulario
        formProps.handleChange({ target: { name: 'name', value: farm.name || '' } });
        formProps.handleChange({ target: { name: 'latitude', value: farm.latitude || '' } });
        formProps.handleChange({ target: { name: 'longitude', value: farm.longitude || '' } });
        formProps.handleChange({ target: { name: 'capacity', value: farm.capacity || '' } });
        setShowForm(true);
    };

    const handleDeleteClick = (farmId, farm) => {
        // TODO: Implementar eliminación con servicio
        if (window.confirm(`¿Estás seguro de eliminar la finca "${farm.name}"?`)) {
            console.log('Eliminar finca:', farmId, farm);
            // Aquí se llamaría al servicio de eliminación
        }
    };

    const handleCloseForm = () => {
        setShowForm(false);
    };

    return {
        showForm,
        handleCreateClick,
        handleEditClick,
        handleDeleteClick,
        handleCloseForm
    };
}

export default ManageFarmForm;

