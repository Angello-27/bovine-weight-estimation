// frontend/src/containers/role/ManageRoleForm.js

import { useState } from 'react';

/**
 * ManageRoleForm container hook - Maneja el estado y acciones del formulario de roles
 * @param {Object} formProps - Props del formulario de CreateNewRole
 * @returns {Object} { showForm, handleCreateClick, handleEditClick, handleDeleteClick, handleCloseForm }
 */
function ManageRoleForm(formProps) {
    const [showForm, setShowForm] = useState(false);

    const resetForm = () => {
        formProps.handleChange({ target: { name: 'name', value: '' } });
        formProps.handleChange({ target: { name: 'descripcion', value: '' } });
        formProps.handleChange({ target: { name: 'priority', value: 'Invitado' } });
    };

    const handleCreateClick = () => {
        resetForm();
        setShowForm(true);
    };

    const handleEditClick = (roleId, role) => {
        // Cargar datos del rol en el formulario
        formProps.handleChange({ target: { name: 'name', value: role.name || '' } });
        formProps.handleChange({ target: { name: 'descripcion', value: role.descripcion || '' } });
        formProps.handleChange({ target: { name: 'priority', value: role.priority || 'Invitado' } });
        setShowForm(true);
    };

    const handleDeleteClick = (roleId, role) => {
        // TODO: Implementar eliminación con servicio
        if (window.confirm(`¿Estás seguro de eliminar el rol "${role.name}"?`)) {
            console.log('Eliminar rol:', roleId, role);
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

export default ManageRoleForm;

