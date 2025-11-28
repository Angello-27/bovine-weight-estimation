// frontend/src/views/CattleDetailView.js

import React, { useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import PanelTemplate from '../templates/PanelTemplate';
import CattleDetailTemplate from '../templates/CattleDetailTemplate';
import GetCattleById from '../containers/cattle/GetCattleById';
import GetWeightHistoryByCattle from '../containers/weight-estimations/GetWeightHistoryByCattle';
import { cattleToTimelineEvents } from '../utils/transformers/cattleToTimelineEvents';
import { weightEstimationToChartData } from '../utils/transformers/weightEstimationToChartData';
import getCattleById from '../services/cattle/getCattleById';

function CattleDetailView() {
    const { id } = useParams();
    const navigate = useNavigate();
    
    const cattleProps = GetCattleById(id);
    const estimationsProps = GetWeightHistoryByCattle(id);

    // Obtener padre y madre si existen
    const [father, setFather] = React.useState(null);
    const [mother, setMother] = React.useState(null);
    const [loadingLineage, setLoadingLineage] = React.useState(false);

    React.useEffect(() => {
        if (cattleProps.cattle) {
            const fetchLineage = async () => {
                setLoadingLineage(true);
                try {
                    if (cattleProps.cattle.father_id) {
                        const fatherData = await getCattleById(cattleProps.cattle.father_id);
                        setFather(fatherData);
                    }
                    if (cattleProps.cattle.mother_id) {
                        const motherData = await getCattleById(cattleProps.cattle.mother_id);
                        setMother(motherData);
                    }
                } catch (error) {
                    console.error('Error al obtener linaje:', error);
                } finally {
                    setLoadingLineage(false);
                }
            };
            fetchLineage();
        }
    }, [cattleProps.cattle]);

    // Transformar datos para timeline
    const timelineEvents = useMemo(() => {
        if (!cattleProps.cattle) return [];
        return cattleToTimelineEvents(cattleProps.cattle, estimationsProps.estimations);
    }, [cattleProps.cattle, estimationsProps.estimations]);

    // Transformar datos para gráfico
    const chartData = useMemo(() => {
        if (!estimationsProps.estimations || estimationsProps.estimations.length === 0) {
            return null;
        }
        return weightEstimationToChartData(
            estimationsProps.estimations,
            cattleProps.cattle?.birth_date,
            cattleProps.cattle?.birth_weight_kg
        );
    }, [estimationsProps.estimations, cattleProps.cattle]);

    const handleViewFather = (fatherId) => {
        navigate(`/cattle/${fatherId}`);
    };

    const handleViewMother = (motherId) => {
        navigate(`/cattle/${motherId}`);
    };

    const loading = cattleProps.loading || estimationsProps.loading || loadingLineage;
    const error = cattleProps.error || estimationsProps.error;

    return (
        <PanelTemplate content={
            <CattleDetailTemplate
                cattle={cattleProps.cattle}
                estimations={estimationsProps.estimations}
                timelineEvents={timelineEvents}
                chartData={chartData}
                father={father}
                mother={mother}
                loading={loading}
                error={error}
                onViewFather={handleViewFather}
                onViewMother={handleViewMother}
            />
        } />
    );
}

export default CattleDetailView;

