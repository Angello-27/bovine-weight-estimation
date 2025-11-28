import React from 'react';
import PanelTemplate from '../templates/PanelTemplate';
import CattleTemplate from '../templates/CattleTemplate';
import GetAllCattle from '../containers/cattle/GetAllCattle';
import FilterCattle from '../containers/cattle/FilterCattle';
import CreateNewCattle from '../containers/cattle/CreateNewCattle';
import ManageCattleForm from '../containers/cattle/ManageCattleForm';
import ManageCattleNavigation from '../containers/cattle/ManageCattleNavigation';

function CattleView() {
    const cattleProps = GetAllCattle();
    const filterProps = FilterCattle(cattleProps.items);
    const formProps = CreateNewCattle();
    const formActions = ManageCattleForm(formProps);
    const navigation = ManageCattleNavigation();

    return (
        <PanelTemplate content={
            <CattleTemplate
                items={filterProps.filteredItems}
                loading={cattleProps.loading}
                error={cattleProps.error}
                searchQuery={filterProps.searchQuery}
                filters={filterProps.filters}
                onSearchChange={filterProps.handleSearchChange}
                onFilterChange={filterProps.handleFilterChange}
                formData={formProps.formData}
                handleChange={formProps.handleChange}
                handleComboBoxChange={formProps.handleComboBoxChange}
                handleSubmit={formProps.handleSubmit}
                showForm={formActions.showForm}
                onCloseForm={formActions.handleCloseForm}
                onViewClick={navigation.handleViewClick}
                onCreateClick={formActions.handleCreateClick}
            />
        } />
    );
}

export default CattleView;

