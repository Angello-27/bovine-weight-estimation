// frontend/src/views/CattleView.js

import React from 'react';
import PanelTemplate from '../../templates/PanelTemplate';
import Content from '../../templates/cattle/CattleTemplate';
import SnackbarNotification from '../../components/molecules/SnackbarNotification';
import useAnimalView from '../../containers/cattle/useAnimalView';

function CattleView() {
    const {
        animalsProps,
        formProps,
        formActions,
        handleSubmit,
        handleConfirmDelete,
        handleViewClick,
        errorSnackbar,
        successSnackbar,
        closeErrorSnackbar,
        closeSuccessSnackbar,
    } = useAnimalView();

    return (
        <>
            <PanelTemplate content={
                <Content
                    items={animalsProps.items}
                    loading={animalsProps.loading}
                    error={animalsProps.error}
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
                    pagination={animalsProps.pagination}
                    onPageChange={animalsProps.onPageChange}
                    onPageSizeChange={animalsProps.onPageSizeChange}
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

export default CattleView;

