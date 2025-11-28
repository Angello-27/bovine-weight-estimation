// frontend/src/components/organisms/CattleWeightHistoryChart/index.js

import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import EmptyState from '../../molecules/EmptyState';
import MonitorWeightIcon from '@mui/icons-material/MonitorWeight';

function CattleWeightHistoryChart({ chartData }) {
    if (!chartData || !chartData.data || chartData.data.length === 0) {
        return (
            <Card>
                <EmptyState message="No hay datos de peso para mostrar en el gráfico." />
            </Card>
        );
    }

    // Preparar datos para tabla simple (hasta que se instale recharts)
    const latestWeight = chartData.data[chartData.data.length - 1]?.weight;
    const firstWeight = chartData.data[0]?.weight;
    const weightGain = latestWeight && firstWeight ? (latestWeight - firstWeight).toFixed(1) : null;

    return (
        <Card>
            <Box display="flex" alignItems="center" gap={1} mb={3}>
                <MonitorWeightIcon color="primary" />
                <CustomTypography variant="h6">
                    Evolución de Peso
                </CustomTypography>
            </Box>
            
            {weightGain && (
                <Box mb={3}>
                    <CustomTypography variant="body2" color="text.secondary">
                        Ganancia de peso: <strong>{weightGain} kg</strong>
                    </CustomTypography>
                </Box>
            )}
            
            <Box sx={{ width: '100%', height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'action.hover', borderRadius: 2 }}>
                <CustomTypography variant="body2" color="text.secondary">
                    Gráfico de evolución (Recharts pendiente de instalar)
                </CustomTypography>
            </Box>
            
            <Box mt={3}>
                <CustomTypography variant="subtitle2" mb={2}>
                    Historial de Pesos
                </CustomTypography>
                <Box component="table" sx={{ width: '100%', borderCollapse: 'collapse' }}>
                    <Box component="thead">
                        <Box component="tr" sx={{ borderBottom: '1px solid', borderColor: 'divider' }}>
                            <Box component="th" sx={{ textAlign: 'left', p: 1, fontWeight: 'bold' }}>Fecha</Box>
                            <Box component="th" sx={{ textAlign: 'right', p: 1, fontWeight: 'bold' }}>Peso (kg)</Box>
                            <Box component="th" sx={{ textAlign: 'center', p: 1, fontWeight: 'bold' }}>Confianza</Box>
                        </Box>
                    </Box>
                    <Box component="tbody">
                        {chartData.data.map((point, index) => (
                            <Box component="tr" key={index} sx={{ borderBottom: '1px solid', borderColor: 'divider' }}>
                                <Box component="td" sx={{ p: 1 }}>{point.label}</Box>
                                <Box component="td" sx={{ textAlign: 'right', p: 1, fontWeight: 'bold' }}>
                                    {point.weight.toFixed(1)}
                                </Box>
                                <Box component="td" sx={{ textAlign: 'center', p: 1 }}>
                                    {point.confidence ? `${(point.confidence * 100).toFixed(0)}%` : '-'}
                                </Box>
                            </Box>
                        ))}
                    </Box>
                </Box>
            </Box>
        </Card>
    );
}

export default CattleWeightHistoryChart;

