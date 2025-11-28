import React, { useState } from 'react';
import PanelTemplate from '../templates/PanelTemplate';
import Content from '../templates/UserTemplate';
import GetAllRoles from '../containers/role/GetAllRoles';
import GetAllUsers from '../containers/user/GetAllUsers';
import CreateNewUser from '../containers/user/CreateNewUser';

function UserView() {
    const rolesProps = GetAllRoles();
    const usersProps = GetAllUsers();
    const formProps = CreateNewUser();
    const [showForm, setShowForm] = useState(false);

    const handleCreateClick = () => {
        // Reset form data when creating new
        formProps.handleChange({ target: { name: 'username', value: '' } });
        formProps.handleChange({ target: { name: 'password', value: '' } });
        formProps.handleChange({ target: { name: 'roleId', value: '' } });
        setShowForm(true);
    };

    const handleEditClick = (userId, user) => {
        // TODO: Implementar edición - cargar datos del usuario en el formulario
        console.log('Editar usuario:', userId, user);
        formProps.handleChange({ target: { name: 'username', value: user.username || '' } });
        formProps.handleChange({ target: { name: 'password', value: '' } }); // No mostrar contraseña
        formProps.handleChange({ target: { name: 'roleId', value: user.roleId || '' } });
        setShowForm(true);
    };

    const handleDeleteClick = (userId, user) => {
        // TODO: Implementar eliminación
        if (window.confirm(`¿Estás seguro de eliminar el usuario "${user.username}"?`)) {
            console.log('Eliminar usuario:', userId, user);
        }
    };

    const handleCloseForm = () => {
        setShowForm(false);
    };

    return (
        <PanelTemplate content={
            <Content
                {...usersProps}
                roles={rolesProps}
                formData={formProps.formData}
                handleChange={formProps.handleChange}
                handleSubmit={formProps.handleSubmit}
                handleComboBoxChange={formProps.handleComboBoxChange}
                showForm={showForm}
                onCloseForm={handleCloseForm}
                onCreateClick={handleCreateClick}
                onEditClick={handleEditClick}
                onDeleteClick={handleDeleteClick}
            />
        } />
    );
}

export default UserView;
