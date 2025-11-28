import React from 'react';
import PanelTemplate from '../templates/PanelTemplate';
import Content from '../templates/FarmTemplate';
import GetAllFarms from '../containers/farm/GetAllFarms';
import GetAllUsers from '../containers/user/GetAllUsers';
import CreateNewFarm from '../containers/farm/CreateNewFarm';
import ManageFarmForm from '../containers/farm/ManageFarmForm';

function FarmView() {
    const farmsProps = GetAllFarms();
    const usersProps = GetAllUsers();
    const formProps = CreateNewFarm();
    const formActions = ManageFarmForm(formProps);

    return (
        <PanelTemplate content={
            <Content
                {...farmsProps}
                owners={usersProps}
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

export default FarmView;

