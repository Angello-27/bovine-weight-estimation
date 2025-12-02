// frontend/src/views/cattle/CattleDetailView.js

import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import PanelTemplate from '../../templates/PanelTemplate';
import CattleDetailTemplate from '../../templates/cattle/CattleDetailTemplate';
import useAnimalDetail from '../../containers/cattle/useAnimalDetail';
import TransformCattleDetailData from '../../containers/cattle/TransformCattleDetailData';
import GenerateCattleReport from '../../containers/cattle/GenerateCattleReport';

function CattleDetailView() {
    const { id } = useParams();
    const navigate = useNavigate();
    
    // Hook unificado para obtener todos los datos
    const animalDetailProps = useAnimalDetail(id);
    
    // Transformar datos para el template
    const transformedData = TransformCattleDetailData(
        animalDetailProps.cattle,
        animalDetailProps.estimations,
        animalDetailProps.timeline
    );
    
    // Navegación a padre/madre
    const handleViewFather = (fatherId) => {
        if (fatherId) {
            navigate(`/cattle/${fatherId}`);
        }
    };
    
    const handleViewMother = (motherId) => {
        if (motherId) {
            navigate(`/cattle/${motherId}`);
        }
    };
    
    // Generar reporte
    const reportProps = GenerateCattleReport(
        animalDetailProps.cattle,
        animalDetailProps.estimations,
        transformedData.timelineEvents,
        animalDetailProps.lineage?.father,
        animalDetailProps.lineage?.mother
    );

    return (
        <PanelTemplate content={
            <CattleDetailTemplate
                cattle={animalDetailProps.cattle}
                estimations={animalDetailProps.estimations}
                timelineEvents={transformedData.timelineEvents}
                chartData={transformedData.chartData}
                galleryImages={transformedData.galleryImages}
                father={animalDetailProps.lineage?.father}
                mother={animalDetailProps.lineage?.mother}
                loading={animalDetailProps.loading}
                error={animalDetailProps.error}
                onViewFather={handleViewFather}
                onViewMother={handleViewMother}
                onGenerateReport={reportProps.handleGenerateReport}
                reportLoading={reportProps.loading}
                reportError={reportProps.error}
            />
        } />
    );
}

export default CattleDetailView;

