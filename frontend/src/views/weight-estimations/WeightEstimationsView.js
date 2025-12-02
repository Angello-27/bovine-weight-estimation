// frontend/src/views/weight-estimations/WeightEstimationsView.js

import React from 'react';
import { useNavigate } from 'react-router-dom';
import PanelTemplate from '../../templates/PanelTemplate';
import WeightEstimationTemplate from '../../templates/weight-estimations/WeightEstimationTemplate';
import GetAllWeightEstimations from '../../containers/weight-estimations/GetAllWeightEstimations';

function WeightEstimationsView() {
    const navigate = useNavigate();
    const estimationsProps = GetAllWeightEstimations();

    const handleViewClick = (estimationId) => {
        // TODO: Navegar a WeightEstimationDetailView cuando se cree
        // navigate(`/weight-estimations/${estimationId}`);
        console.log('Ver estimación:', estimationId);
    };

    const handleEstimateClick = () => {
        navigate('/weight-estimations/estimate');
    };

    return (
        <PanelTemplate 
            content={
                <WeightEstimationTemplate 
                    {...estimationsProps} 
                    onViewClick={handleViewClick} 
                    onEstimateClick={handleEstimateClick} 
                />
            } 
        />
    );
}

export default WeightEstimationsView;

