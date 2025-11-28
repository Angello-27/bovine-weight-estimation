import React, { useState } from 'react';
import PanelTemplate from '../templates/PanelTemplate';
import Content from '../templates/RoleTemplate';
import GetAllRoles from '../containers/role/GetAllRoles';
import CreateNewRole from '../containers/role/CreateNewRole';

function RoleView() {
    const rolesProps = GetAllRoles();
    const formProps = CreateNewRole();
    const [showForm, setShowForm] = useState(false);

    const handleCreateClick = () => {
        // Reset form data when creating new
        formProps.handleChange({ target: { name: 'name', value: '' } });
        formProps.handleChange({ target: { name: 'descripcion', value: '' } });
        formProps.handleChange({ target: { name: 'priority', value: 'Invitado' } });
        setShowForm(true);
    };

    const handleEditClick = (roleId, role) => {
        // TODO: Implementar edición - cargar datos del rol en el formulario
        console.log('Editar rol:', roleId, role);
        formProps.handleChange({ target: { name: 'name', value: role.name || '' } });
        formProps.handleChange({ target: { name: 'descripcion', value: role.descripcion || '' } });
        formProps.handleChange({ target: { name: 'priority', value: role.priority || 'Invitado' } });
        setShowForm(true);
    };

    const handleDeleteClick = (roleId, role) => {
        // TODO: Implementar eliminación
        if (window.confirm(`¿Estás seguro de eliminar el rol "${role.name}"?`)) {
            console.log('Eliminar rol:', roleId, role);
        }
    };

    const handleCloseForm = () => {
        setShowForm(false);
    };

    return (
        <PanelTemplate content={
            <Content
                {...rolesProps}
                formData={formProps.formData}
                handleChange={formProps.handleChange}
                handleSubmit={formProps.handleSubmit}
                showForm={showForm}
                onCloseForm={handleCloseForm}
                onCreateClick={handleCreateClick}
                onEditClick={handleEditClick}
                onDeleteClick={handleDeleteClick}
            />
        } />
    );
}

export default RoleView;
