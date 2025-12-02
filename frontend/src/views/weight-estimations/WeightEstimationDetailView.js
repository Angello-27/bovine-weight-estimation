// frontend/src/views/weight-estimations/WeightEstimationDetailView.js

import React from 'react';
import { useParams } from 'react-router-dom';
import PanelTemplate from '../../templates/PanelTemplate';
import WeightEstimationDetailTemplate from '../../templates/weight-estimations/WeightEstimationDetailTemplate';
import GetWeightEstimationById from '../../containers/weight-estimations/GetWeightEstimationById';

function WeightEstimationDetailView() {
    const { id } = useParams();
    const estimationProps = GetWeightEstimationById(id);

    // Obtener URL base de la API desde variables de entorno
    const apiBaseUrl = import.meta.env.REACT_APP_API_URL || '';

    return (
        <PanelTemplate content={
            <WeightEstimationDetailTemplate
                estimation={estimationProps.estimation}
                loading={estimationProps.loading}
                error={estimationProps.error}
                apiBaseUrl={apiBaseUrl}
            />
        } />
    );
}

export default WeightEstimationDetailView;

