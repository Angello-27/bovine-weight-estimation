// frontend/src/views/role/RoleView.js
import React from 'react';
import PanelTemplate from '../../templates/PanelTemplate';
import Content from '../../templates/role/RoleTemplate';
import SnackbarNotification from '../../components/molecules/SnackbarNotification';
import useRoleView from '../../containers/role/useRoleView';

function RoleView() {
    const {
        rolesProps,
        formProps,
        formActions,
        handleSubmit,
        handleConfirmDelete,
        errorSnackbar,
        successSnackbar,
        closeErrorSnackbar,
        closeSuccessSnackbar,
    } = useRoleView();

    return (
        <>
            <PanelTemplate content={
                <Content
                    {...rolesProps}
                    formData={formProps.formData}
                    formErrors={formProps.errors || {}}
                    handleChange={formProps.handleChange}
                    handleSubmit={handleSubmit}
                    showForm={formActions.showForm}
                    onCloseForm={formActions.handleCloseForm}
                    onCreateClick={formActions.handleCreateClick}
                    onEditClick={formActions.handleEditClick}
                    onDeleteClick={formActions.handleDeleteClick}
                    pagination={rolesProps.pagination}
                    onPageChange={rolesProps.onPageChange}
                    onPageSizeChange={rolesProps.onPageSizeChange}
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

export default RoleView;
