import React from 'react';
import PanelTemplate from '../templates/PanelTemplate';
import Content from '../templates/RoleTemplate';
import GetAllRoles from '../containers/role/GetAllRoles';
import CreateNewRole from '../containers/role/CreateNewRole';
import ManageRoleForm from '../containers/role/ManageRoleForm';

function RoleView() {
    const rolesProps = GetAllRoles();
    const formProps = CreateNewRole();
    const formActions = ManageRoleForm(formProps);

    return (
        <PanelTemplate content={
            <Content
                {...rolesProps}
                formData={formProps.formData}
                handleChange={formProps.handleChange}
                handleSubmit={formProps.handleSubmit}
                showForm={formActions.showForm}
                onCloseForm={formActions.handleCloseForm}
                onCreateClick={formActions.handleCreateClick}
                onEditClick={formActions.handleEditClick}
                onDeleteClick={formActions.handleDeleteClick}
            />
        } />
    );
}

export default RoleView;
