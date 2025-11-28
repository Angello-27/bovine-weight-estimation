import React from 'react';
import PanelTemplate from '../templates/PanelTemplate';
import Content from '../templates/UserTemplate';
import GetAllRoles from '../containers/role/GetAllRoles';
import GetAllUsers from '../containers/user/GetAllUsers';
import CreateNewUser from '../containers/user/CreateNewUser';
import ManageUserForm from '../containers/user/ManageUserForm';

function UserView() {
    const rolesProps = GetAllRoles();
    const usersProps = GetAllUsers();
    const formProps = CreateNewUser();
    const formActions = ManageUserForm(formProps);

    return (
        <PanelTemplate content={
            <Content
                {...usersProps}
                roles={rolesProps}
                formData={formProps.formData}
                handleChange={formProps.handleChange}
                handleSubmit={formProps.handleSubmit}
                handleComboBoxChange={formProps.handleComboBoxChange}
                showForm={formActions.showForm}
                onCloseForm={formActions.handleCloseForm}
                onCreateClick={formActions.handleCreateClick}
                onEditClick={formActions.handleEditClick}
                onDeleteClick={formActions.handleDeleteClick}
            />
        } />
    );
}

export default UserView;
