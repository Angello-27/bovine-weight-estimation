// frontend/src/views/weight-estimations/WeightEstimationDetailView.js

import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import PanelTemplate from '../../templates/PanelTemplate';
import WeightEstimationDetailTemplate from '../../templates/weight-estimations/WeightEstimationDetailTemplate';
import useWeightEstimationDetail from '../../containers/weight-estimations/useWeightEstimationDetail';

function WeightEstimationDetailView() {
    const { id } = useParams();
    const navigate = useNavigate();
    
    // Hook para obtener todos los datos
    const { estimation, cattle, previousEstimations, loading, error } = useWeightEstimationDetail(id);

    // Obtener URL base de la API desde variables de entorno
    const apiBaseUrl = import.meta.env.REACT_APP_API_URL || '';

    // Handler para navegar al animal
    const handleViewCattle = (cattleId) => {
        if (cattleId) {
            navigate(`/cattle/${cattleId}`);
        }
    };

    return (
        <PanelTemplate content={
            <WeightEstimationDetailTemplate
                estimation={estimation}
                cattle={cattle}
                previousEstimations={previousEstimations}
                loading={loading}
                error={error}
                apiBaseUrl={apiBaseUrl}
                onViewCattle={handleViewCattle}
            />
        } />
    );
}

export default WeightEstimationDetailView;

