// frontend/src/views/CattleDetailView.js

import React from 'react';
import { useParams } from 'react-router-dom';
import PanelTemplate from '../templates/PanelTemplate';
import CattleDetailTemplate from '../templates/CattleDetailTemplate';
import GetCattleById from '../containers/cattle/GetCattleById';
import GetCattleLineage from '../containers/cattle/GetCattleLineage';
import GetWeightHistoryByCattle from '../containers/weight-estimations/GetWeightHistoryByCattle';
import TransformCattleDetailData from '../containers/cattle/TransformCattleDetailData';
import ManageCattleNavigation from '../containers/cattle/ManageCattleNavigation';
import CombineCattleLoading from '../containers/cattle/CombineCattleLoading';
import GenerateCattleReport from '../containers/cattle/GenerateCattleReport';

function CattleDetailView() {
    const { id } = useParams();
    
    const cattleProps = GetCattleById(id);
    const estimationsProps = GetWeightHistoryByCattle(id);
    const lineageProps = GetCattleLineage(cattleProps.cattle);
    const transformedData = TransformCattleDetailData(
        cattleProps.cattle,
        estimationsProps.estimations
    );
    const navigation = ManageCattleNavigation();
    const { loading, error } = CombineCattleLoading(cattleProps, estimationsProps, lineageProps);
    const reportProps = GenerateCattleReport(
        cattleProps.cattle,
        estimationsProps.estimations,
        transformedData.timelineEvents,
        lineageProps.father,
        lineageProps.mother
    );

    return (
        <PanelTemplate content={
            <CattleDetailTemplate
                cattle={cattleProps.cattle}
                estimations={estimationsProps.estimations}
                timelineEvents={transformedData.timelineEvents}
                chartData={transformedData.chartData}
                galleryImages={transformedData.galleryImages}
                father={lineageProps.father}
                mother={lineageProps.mother}
                loading={loading}
                error={error}
                onViewFather={navigation.handleViewFather}
                onViewMother={navigation.handleViewMother}
                onGenerateReport={reportProps.handleGenerateReport}
                reportLoading={reportProps.loading}
                reportError={reportProps.error}
            />
        } />
    );
}

export default CattleDetailView;

