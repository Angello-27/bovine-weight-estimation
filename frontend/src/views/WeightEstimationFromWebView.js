// frontend/src/views/WeightEstimationFromWebView.js

import React from 'react';
import PanelTemplate from '../templates/PanelTemplate';
import WeightEstimationFromWebTemplate from '../templates/WeightEstimationFromWebTemplate';
import EstimateWeightFromImage from '../containers/weight-estimations/EstimateWeightFromImage';
import GetAllCattle from '../containers/cattle/GetAllCattle';

function WeightEstimationFromWebView() {
    const estimationProps = EstimateWeightFromImage();
    const cattleProps = GetAllCattle();

    // Transformar animales a formato ComboBox
    const cattleOptions = cattleProps.items?.map(cattle => ({
        id: cattle.id,
        label: `${cattle.ear_tag}${cattle.name ? ` - ${cattle.name}` : ''}`
    })) || [];

    return (
        <PanelTemplate content={
            <WeightEstimationFromWebTemplate
                {...estimationProps}
                cattleOptions={cattleOptions}
            />
        } />
    );
}

export default WeightEstimationFromWebView;

