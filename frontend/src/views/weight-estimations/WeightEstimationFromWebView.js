// frontend/src/views/weight-estimations/WeightEstimationFromWebView.js

import React, { useState, useEffect, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import PanelTemplate from '../../templates/PanelTemplate';
import WeightEstimationFromWebTemplate from '../../templates/weight-estimations/WeightEstimationFromWebTemplate';
import EstimateWeightFromImage from '../../containers/weight-estimations/EstimateWeightFromImage';
import { getAnimalsByCriteria } from '../../services/cattle';
import { getCurrentUser } from '../../services/auth/authService';
import { getAllFarms } from '../../services/farm/getAllFarms';

function WeightEstimationFromWebView() {
    const [searchParams] = useSearchParams();
    const animalId = searchParams.get('animal_id');
    
    const estimationProps = EstimateWeightFromImage(animalId);
    const [cattleByBreed, setCattleByBreed] = useState([]);
    const [cattleLoading, setCattleLoading] = useState(false);
    
    // Obtener ganado filtrado por raza cuando se selecciona una raza
    useEffect(() => {
        const fetchCattleByBreed = async () => {
            if (!estimationProps.selectedBreed) {
                setCattleByBreed([]);
                return;
            }

            try {
                setCattleLoading(true);
                
                // Obtener farm_id del usuario
                const currentUser = getCurrentUser();
                let farmId = currentUser?.farm_id;
                
                if (!farmId) {
                    try {
                        const farmsResponse = await getAllFarms({ limit: 1 });
                        if (farmsResponse?.farms && farmsResponse.farms.length > 0) {
                            farmId = farmsResponse.farms[0].id;
                        }
                    } catch (e) {
                        console.warn('No se pudo obtener haciendas:', e);
                    }
                }
                
                if (!farmId) {
                    setCattleByBreed([]);
                    return;
                }
                
                // Obtener animales filtrados por raza con límite de 100
                const data = await getAnimalsByCriteria(
                    {
                        farm_id: farmId,
                        breed: estimationProps.selectedBreed
                    },
                    { page: 1, page_size: 100 } // Obtener hasta 100 animales de esa raza
                );
                
                setCattleByBreed(data?.animals || []);
            } catch (error) {
                console.error('Error al obtener ganado por raza:', error);
                setCattleByBreed([]);
            } finally {
                setCattleLoading(false);
            }
        };

        fetchCattleByBreed();
    }, [estimationProps.selectedBreed]);

    return (
        <PanelTemplate content={
            <WeightEstimationFromWebTemplate
                {...estimationProps}
                filteredCattle={cattleByBreed}
                cattleLoading={cattleLoading}
            />
        } />
    );
}

export default WeightEstimationFromWebView;

