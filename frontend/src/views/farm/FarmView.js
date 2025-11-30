// frontend/src/views/farm/FarmView.js
import React from 'react';
import PanelTemplate from '../../templates/PanelTemplate';
import Content from '../../templates/farm/FarmTemplate';
import SnackbarNotification from '../../components/molecules/SnackbarNotification';
import useFarmView from '../../containers/farm/useFarmView';

function FarmView() {
    const {
        farmsProps,
        usersProps,
        formProps,
        formActions,
        handleSubmit,
        handleConfirmDelete,
        handleViewClick,
        errorSnackbar,
        successSnackbar,
        closeErrorSnackbar,
        closeSuccessSnackbar,
    } = useFarmView();

    return (
        <>
            <PanelTemplate content={
                <Content
                    {...farmsProps}
                    owners={usersProps}
                    formData={formProps.formData}
                    formErrors={formProps.errors || {}}
                    handleChange={formProps.handleChange}
                    handleSubmit={handleSubmit}
                    handleComboBoxChange={formProps.handleComboBoxChange}
                    showForm={formActions.showForm}
                    onCloseForm={formActions.handleCloseForm}
                    onCreateClick={formActions.handleCreateClick}
                    onViewClick={handleViewClick}
                    onEditClick={formActions.handleEditClick}
                    onDeleteClick={formActions.handleDeleteClick}
                    pagination={farmsProps.pagination}
                    onPageChange={farmsProps.onPageChange}
                    onPageSizeChange={farmsProps.onPageSizeChange}
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

export default FarmView;

