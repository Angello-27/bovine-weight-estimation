// frontend/src/containers/user/ManageUserForm.js

import { useState } from 'react';

/**
 * ManageUserForm container hook - Maneja el estado y acciones del formulario de usuarios
 * @param {Object} formProps - Props del formulario de CreateNewUser
 * @returns {Object} { showForm, handleCreateClick, handleEditClick, handleDeleteClick, handleCloseForm }
 */
function ManageUserForm(formProps) {
    const [showForm, setShowForm] = useState(false);

    const resetForm = () => {
        formProps.handleChange({ target: { name: 'username', value: '' } });
        formProps.handleChange({ target: { name: 'password', value: '' } });
        formProps.handleChange({ target: { name: 'roleId', value: '' } });
    };

    const handleCreateClick = () => {
        resetForm();
        setShowForm(true);
    };

    const handleEditClick = (userId, user) => {
        // Cargar datos del usuario en el formulario
        formProps.handleChange({ target: { name: 'username', value: user.username || '' } });
        formProps.handleChange({ target: { name: 'password', value: '' } }); // No mostrar contraseña
        formProps.handleChange({ target: { name: 'roleId', value: user.roleId || '' } });
        setShowForm(true);
    };

    const handleDeleteClick = (userId, user) => {
        // TODO: Implementar eliminación con servicio
        if (window.confirm(`¿Estás seguro de eliminar el usuario "${user.username}"?`)) {
            console.log('Eliminar usuario:', userId, user);
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

export default ManageUserForm;

