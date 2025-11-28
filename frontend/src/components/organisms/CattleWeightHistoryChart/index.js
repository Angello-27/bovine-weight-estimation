// frontend/src/components/organisms/CattleWeightHistoryChart/index.js

import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import EmptyState from '../../molecules/EmptyState';
import MonitorWeightIcon from '@mui/icons-material/MonitorWeight';
import WeightStatsCards from '../../molecules/WeightStatsCards';
import WeightLineChart from '../../molecules/WeightLineChart';
import WeightHistoryTable from '../../molecules/WeightHistoryTable';

/**
 * CattleWeightHistoryChart organism - Muestra la evolución de peso de un animal
 * @param {Object} chartData - Datos del gráfico { data: [{ label, weight, confidence }] }
 */
function CattleWeightHistoryChart({ chartData }) {
    if (!chartData || !chartData.data || chartData.data.length === 0) {
        return (
            <Card>
                <EmptyState message="No hay datos de peso para mostrar en el gráfico." />
            </Card>
        );
    }

    // Preparar datos para Recharts
    const chartDataFormatted = chartData.data.map((point) => ({
        fecha: point.label,
        peso: point.weight,
        confianza: point.confidence ? (point.confidence * 100).toFixed(0) : null
    }));

    // Calcular estadísticas
    const latestWeight = chartData.data[chartData.data.length - 1]?.weight;
    const firstWeight = chartData.data[0]?.weight;
    const weightGain = latestWeight && firstWeight ? (latestWeight - firstWeight).toFixed(1) : null;
    const averageWeight = chartData.data.reduce((sum, point) => sum + point.weight, 0) / chartData.data.length;

    return (
        <Card>
            <Box display="flex" alignItems="center" gap={1} mb={3}>
                <MonitorWeightIcon color="primary" />
                <CustomTypography variant="h6">
                    Evolución de Peso
                </CustomTypography>
            </Box>
            
            <WeightStatsCards 
                weightGain={weightGain}
                latestWeight={latestWeight}
                averageWeight={averageWeight}
            />
            
            <WeightLineChart data={chartDataFormatted} />
            
            <WeightHistoryTable data={chartData.data} />
        </Card>
    );
}

export default CattleWeightHistoryChart;

