// frontend/src/components/organisms/CattleWeightHistoryChart/index.js

import { useState, useEffect } from 'react';
import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import EmptyState from '../../molecules/EmptyState';
import LoadingState from '../../molecules/LoadingState';
import ErrorState from '../../molecules/ErrorState';
import MonitorWeightIcon from '@mui/icons-material/MonitorWeight';
import WeightStatsCards from '../../molecules/WeightStatsCards';
import WeightLineChart from '../../molecules/WeightLineChart';
import WeightHistoryTable from '../../molecules/WeightHistoryTable';
import getWeightEstimationsByCattleId from '../../../services/weight-estimations/getWeightEstimationsByCattleId';

/**
 * CattleWeightHistoryChart organism - Muestra la evolución de peso de un animal
 * @param {string} animalId - ID del animal para cargar el historial de pesos
 */
function CattleWeightHistoryChart({ animalId }) {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        const loadWeightHistory = async () => {
            if (!animalId) {
                setLoading(false);
                return;
            }

            setLoading(true);
            setError(null);

            try {
                const response = await getWeightEstimationsByCattleId(animalId, 1, 100);
                
                if (!response.weighings || response.weighings.length === 0) {
                    setChartData(null);
                    setLoading(false);
                    return;
                }

                // Transformar datos de la API al formato esperado
                const formattedData = response.weighings.map((weighing) => {
                    const date = new Date(weighing.timestamp);
                    const label = date.toLocaleDateString('es-ES', {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric'
                    });

                    return {
                        label,
                        weight: weighing.estimated_weight_kg || weighing.estimated_weight,
                        confidence: weighing.confidence || weighing.confidence_score || null,
                        timestamp: weighing.timestamp,
                        id: weighing.id
                    };
                });

                // Ordenar por fecha (más reciente primero)
                formattedData.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

                setChartData({ data: formattedData });
            } catch (err) {
                setError(err.message || 'Error al cargar el historial de pesos');
                setChartData(null);
            } finally {
                setLoading(false);
            }
        };

        loadWeightHistory();
    }, [animalId]);

    // Preparar datos para Recharts (invertir orden para mostrar evolución temporal de izquierda a derecha)
    const chartDataFormatted = chartData?.data 
        ? [...chartData.data].reverse().map((point) => ({
            fecha: point.label,
            peso: point.weight,
            confianza: point.confidence ? (point.confidence * 100).toFixed(0) : null
        }))
        : [];

    // Calcular estadísticas (el primer elemento es el más reciente)
    const latestWeight = chartData?.data?.[0]?.weight;
    const firstWeight = chartData?.data?.[chartData.data.length - 1]?.weight;
    const weightGain = latestWeight && firstWeight ? (latestWeight - firstWeight).toFixed(1) : null;
    const averageWeight = chartData?.data 
        ? chartData.data.reduce((sum, point) => sum + point.weight, 0) / chartData.data.length 
        : null;

    return (
        <Card>
            <Box display="flex" alignItems="center" gap={1} mb={3}>
                <MonitorWeightIcon color="primary" />
                <CustomTypography variant="h6">
                    Evolución de Peso
                </CustomTypography>
            </Box>

            <LoadingState loading={loading}>
                <ErrorState error={error} />
                
                {!error && (!chartData || !chartData.data || chartData.data.length === 0) ? (
                    <EmptyState message="No hay datos de peso para mostrar en el gráfico." />
                ) : (
                    <>
                        <WeightStatsCards 
                            weightGain={weightGain}
                            latestWeight={latestWeight}
                            averageWeight={averageWeight}
                        />
                        
                        {chartDataFormatted.length > 0 && (
                            <WeightLineChart data={chartDataFormatted} />
                        )}
                        
                        {chartData?.data && chartData.data.length > 0 && (
                            <WeightHistoryTable data={chartData.data} />
                        )}
                    </>
                )}
            </LoadingState>
        </Card>
    );
}

export default CattleWeightHistoryChart;

