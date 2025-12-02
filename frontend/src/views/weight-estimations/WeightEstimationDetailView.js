// frontend/src/views/weight-estimations/WeightEstimationDetailView.js

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import PanelTemplate from '../../templates/PanelTemplate';
import WeightEstimationDetailTemplate from '../../templates/weight-estimations/WeightEstimationDetailTemplate';
import GetWeightEstimationById from '../../containers/weight-estimations/GetWeightEstimationById';
import GetCattleById from '../../containers/cattle/GetCattleById';
import getWeightEstimationsByCattleId from '../../services/weight-estimations/getWeightEstimationsByCattleId';

function WeightEstimationDetailView() {
    const { id } = useParams();
    const navigate = useNavigate();
    
    const estimationProps = GetWeightEstimationById(id);
    
    // Obtener información del animal asociado si existe
    const cattleId = estimationProps.estimation?.cattle_id;
    const cattleProps = GetCattleById(cattleId);

    // Estado para historial de estimaciones del animal
    const [previousEstimations, setPreviousEstimations] = useState([]);
    const [loadingHistory, setLoadingHistory] = useState(false);

    // Obtener historial de estimaciones del animal (excluyendo la actual)
    useEffect(() => {
        const loadHistory = async () => {
            if (!cattleId || !estimationProps.estimation) {
                return;
            }

            setLoadingHistory(true);
            try {
                const response = await getWeightEstimationsByCattleId(cattleId, 1, 100);
                if (response.weighings && Array.isArray(response.weighings)) {
                    // Filtrar la estimación actual y ordenar por fecha descendente
                    const filtered = response.weighings
                        .filter(w => w.id !== estimationProps.estimation.id)
                        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
                    setPreviousEstimations(filtered);
                }
            } catch (error) {
                console.error('Error al cargar historial de estimaciones:', error);
            } finally {
                setLoadingHistory(false);
            }
        };

        loadHistory();
    }, [cattleId, estimationProps.estimation?.id]);

    // Obtener URL base de la API desde variables de entorno
    const apiBaseUrl = import.meta.env.REACT_APP_API_URL || '';

    // Handler para navegar al animal
    const handleViewCattle = (cattleId) => {
        if (cattleId) {
            navigate(`/cattle/${cattleId}`);
        }
    };

    // Handler para ver más estimaciones del animal
    const handleViewCattleEstimations = (cattleId) => {
        if (cattleId) {
            navigate(`/cattle/${cattleId}`);
        }
    };

    return (
        <PanelTemplate content={
            <WeightEstimationDetailTemplate
                estimation={estimationProps.estimation}
                cattle={cattleProps.cattle}
                previousEstimations={previousEstimations}
                loading={estimationProps.loading || cattleProps.loading || loadingHistory}
                error={estimationProps.error || cattleProps.error}
                apiBaseUrl={apiBaseUrl}
                onViewCattle={handleViewCattle}
                onViewCattleEstimations={handleViewCattleEstimations}
            />
        } />
    );
}

export default WeightEstimationDetailView;

