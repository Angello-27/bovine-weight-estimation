import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PanelTemplate from '../templates/PanelTemplate';
import CattleTemplate from '../templates/CattleTemplate';
import GetAllCattle from '../containers/cattle/GetAllCattle';
import CreateNewCattle from '../containers/cattle/CreateNewCattle';

function CattleView() {
    const navigate = useNavigate();
    const cattleProps = GetAllCattle();
    const formProps = CreateNewCattle();
    const [showForm, setShowForm] = useState(false);

    const handleViewClick = (cattleId) => {
        navigate(`/cattle/${cattleId}`);
    };

    const handleCreateClick = () => {
        // Reset form data when creating new
        formProps.handleChange({ target: { name: 'ear_tag', value: '' } });
        formProps.handleChange({ target: { name: 'breed', value: '' } });
        formProps.handleChange({ target: { name: 'birth_date', value: '' } });
        formProps.handleChange({ target: { name: 'gender', value: '' } });
        formProps.handleChange({ target: { name: 'name', value: '' } });
        formProps.handleChange({ target: { name: 'color', value: '' } });
        formProps.handleChange({ target: { name: 'birth_weight_kg', value: '' } });
        formProps.handleChange({ target: { name: 'observations', value: '' } });
        setShowForm(true);
    };

    const handleCloseForm = () => {
        setShowForm(false);
    };

    return (
        <PanelTemplate content={
            <CattleTemplate
                {...cattleProps}
                formData={formProps.formData}
                handleChange={formProps.handleChange}
                handleComboBoxChange={formProps.handleComboBoxChange}
                handleSubmit={formProps.handleSubmit}
                showForm={showForm}
                onCloseForm={handleCloseForm}
                onViewClick={handleViewClick}
                onCreateClick={handleCreateClick}
            />
        } />
    );
}

export default CattleView;

