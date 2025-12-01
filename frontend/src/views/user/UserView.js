// frontend/src/views/user/UserView.js
import React from 'react';
import PanelTemplate from '../../templates/PanelTemplate';
import Content from '../../templates/user/UserTemplate';
import SnackbarNotification from '../../components/molecules/SnackbarNotification';
import useUserView from '../../containers/user/useUserView';

function UserView() {
    const {
        usersProps,
        rolesProps,
        farmsProps,
        formProps,
        formActions,
        handleSubmit,
        handleConfirmDelete,
        errorSnackbar,
        successSnackbar,
        closeErrorSnackbar,
        closeSuccessSnackbar,
    } = useUserView();

    return (
        <>
            <PanelTemplate content={
                <Content
                    {...usersProps}
                    roles={rolesProps}
                    farms={farmsProps}
                    formData={formProps.formData}
                    formErrors={formProps.errors || {}}
                    handleChange={formProps.handleChange}
                    handleSubmit={handleSubmit}
                    handleComboBoxChange={formProps.handleComboBoxChange}
                    showForm={formActions.showForm}
                    onCloseForm={formActions.handleCloseForm}
                    onCreateClick={formActions.handleCreateClick}
                    onEditClick={formActions.handleEditClick}
                    onDeleteClick={formActions.handleDeleteClick}
                    pagination={usersProps.pagination}
                    onPageChange={usersProps.onPageChange}
                    onPageSizeChange={usersProps.onPageSizeChange}
                    showDeleteDialog={formActions.showDeleteDialog}
                    deleteItem={formActions.deleteItem}
                    onCloseDeleteDialog={formActions.handleCloseDeleteDialog}
                    onConfirmDelete={handleConfirmDelete}
                />
            } />
            
            <SnackbarNotification
                errorSnackbar={errorSnackbar}
                successSnackbar={successSnackbar}
                onCloseError={closeErrorSnackbar}
                onCloseSuccess={closeSuccessSnackbar}
            />
        </>
    );
}

export default UserView;
