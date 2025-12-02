// frontend/src/components/molecules/EstimationComparisonCard/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Divider from '@mui/material/Divider';
import Card from '../../atoms/Card';
import InfoField from '../../atoms/InfoField';
import CustomTypography from '../../atoms/CustomTypography';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import RemoveIcon from '@mui/icons-material/Remove';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import Chip from '@mui/material/Chip';

/**
 * EstimationComparisonCard molecule - Compara la estimación actual con todas las anteriores del mismo animal
 * @param {Object} currentEstimation - Estimación actual
 * @param {Array} previousEstimations - Array de estimaciones anteriores (solo anteriores a la fecha actual, del mismo animal)
 */
function EstimationComparisonCard({ currentEstimation, previousEstimations = [] }) {
    if (!currentEstimation) return null;

    // Campos según endpoint GET /api/v1/weighings/{id} y GET /api/v1/weighings/animal/{id}
    // Devuelve: estimated_weight_kg, confidence (no confidence_score)
    const currentWeight = currentEstimation.estimated_weight_kg || currentEstimation.estimated_weight || 0;
    const currentTimestamp = new Date(currentEstimation.timestamp);

    const formatDate = (dateString) => {
        if (!dateString) return '-';
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('es-ES', { 
                year: 'numeric', 
                month: 'short', 
                day: 'numeric'
            });
        } catch {
            return dateString;
        }
    };

    // Calcular comparaciones con todas las estimaciones anteriores
    const comparisons = previousEstimations
        .filter(est => {
            const estTimestamp = new Date(est.timestamp);
            return estTimestamp < currentTimestamp;
        })
        .map(est => {
            const estWeight = est.estimated_weight_kg || est.estimated_weight || 0;
            const estConfidence = est.confidence || est.confidence_score || 0;
            const estTimestamp = new Date(est.timestamp);
            
            const weightDifference = currentWeight - estWeight;
            const weightDifferencePercent = estWeight > 0 
                ? ((weightDifference / estWeight) * 100).toFixed(1)
                : null;
            
            const daysDifference = Math.floor((currentTimestamp - estTimestamp) / (1000 * 60 * 60 * 24));
            const dailyGain = daysDifference > 0 ? (weightDifference / daysDifference).toFixed(2) : null;
            
            return {
                ...est,
                weight: estWeight,
                confidence: estConfidence,
                timestamp: est.timestamp,
                weightDifference,
                weightDifferencePercent,
                daysDifference,
                dailyGain
            };
        })
        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)); // Más reciente primero

    // Calcular días totales desde la primera estimación hasta la actual
    const totalDaysFromFirst = comparisons.length > 0 
        ? Math.floor((currentTimestamp - new Date(comparisons[comparisons.length - 1].timestamp)) / (1000 * 60 * 60 * 24))
        : 0;

    return (
        <Card sx={{ p: 3 }}>
            <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                <CompareArrowsIcon />
                Evolución del Peso - Comparación con Estimaciones Anteriores
            </CustomTypography>
            <Divider sx={{ mb: 3 }} />
            
            {comparisons.length > 0 ? (
                <>
                    {/* Resumen estadístico */}
                    {comparisons.length > 0 && (
                        <Box sx={{ mb: 3 }}>
                            <CustomTypography variant="subtitle1" sx={{ mb: 2, fontWeight: 'bold' }}>
                                Resumen de Evolución
                            </CustomTypography>
                            <Grid container spacing={2}>
                                <Grid item xs={12} sm={2.4}>
                                    <Box>
                                        <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                                            Total de Comparaciones
                                        </CustomTypography>
                                        <CustomTypography variant="h6" sx={{ fontWeight: 700, color: 'primary.main' }}>
                                            {comparisons.length}
                                        </CustomTypography>
                                    </Box>
                                </Grid>
                                <Grid item xs={12} sm={2.4}>
                                    <Box>
                                        <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                                            Ganancia Promedio
                                        </CustomTypography>
                                        <CustomTypography variant="h6" sx={{ fontWeight: 700, color: 'success.main' }}>
                                            {`${(comparisons.reduce((sum, c) => sum + (c.weightDifference > 0 ? c.weightDifference : 0), 0) / comparisons.length).toFixed(1)} kg`}
                                        </CustomTypography>
                                    </Box>
                                </Grid>
                                <Grid item xs={12} sm={2.4}>
                                    <Box>
                                        <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                                            Peso Inicial
                                        </CustomTypography>
                                        <CustomTypography variant="h6" sx={{ fontWeight: 700, color: 'info.main' }}>
                                            {`${comparisons[comparisons.length - 1].weight.toFixed(1)} kg`}
                                        </CustomTypography>
                                    </Box>
                                </Grid>
                                <Grid item xs={12} sm={2.4}>
                                    <Box>
                                        <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                                            Ganancia Total
                                        </CustomTypography>
                                        <CustomTypography variant="h6" sx={{ fontWeight: 700, color: 'success.main' }}>
                                            {`${(currentWeight - comparisons[comparisons.length - 1].weight).toFixed(1)} kg`}
                                        </CustomTypography>
                                    </Box>
                                </Grid>
                                <Grid item xs={12} sm={2.4}>
                                    <Box>
                                        <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                                            Días Totales
                                        </CustomTypography>
                                        <CustomTypography variant="h6" sx={{ fontWeight: 700, color: 'warning.main' }}>
                                            {`${totalDaysFromFirst} días`}
                                        </CustomTypography>
                                    </Box>
                                </Grid>
                            </Grid>
                        </Box>
                    )}

                    {/* Tabla de comparaciones */}
                    <TableContainer component={Paper} variant="outlined">
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell><strong>Fecha</strong></TableCell>
                                    <TableCell align="right"><strong>Peso (kg)</strong></TableCell>
                                    <TableCell align="right"><strong>Confianza</strong></TableCell>
                                    <TableCell align="right"><strong>Diferencia</strong></TableCell>
                                    <TableCell align="right"><strong>% Cambio</strong></TableCell>
                                    <TableCell align="right"><strong>Días</strong></TableCell>
                                    <TableCell align="right"><strong>GDP (kg/día)</strong></TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {comparisons.map((comp, index) => (
                                    <TableRow 
                                        key={comp.id || index}
                                        sx={{ 
                                            '&:hover': { bgcolor: 'action.hover' }
                                        }}
                                    >
                                        <TableCell>{formatDate(comp.timestamp)}</TableCell>
                                        <TableCell align="right">{comp.weight.toFixed(1)}</TableCell>
                                        <TableCell align="right">
                                            <Chip 
                                                label={`${(comp.confidence * 100).toFixed(0)}%`}
                                                size="small"
                                                variant="outlined"
                                            />
                                        </TableCell>
                                        <TableCell align="right">
                                            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: 0.5 }}>
                                                {comp.weightDifference > 0 && <TrendingUpIcon color="success" fontSize="small" />}
                                                {comp.weightDifference < 0 && <TrendingDownIcon color="error" fontSize="small" />}
                                                {comp.weightDifference === 0 && <RemoveIcon fontSize="small" />}
                                                <CustomTypography 
                                                    variant="body2"
                                                    sx={{ 
                                                        fontWeight: 'bold',
                                                        color: comp.weightDifference > 0 ? 'success.main' : comp.weightDifference < 0 ? 'error.main' : 'text.primary'
                                                    }}
                                                >
                                                    {comp.weightDifference > 0 ? '+' : ''}{comp.weightDifference.toFixed(1)} kg
                                                </CustomTypography>
                                            </Box>
                                        </TableCell>
                                        <TableCell align="right">
                                            <CustomTypography 
                                                variant="body2"
                                                sx={{ 
                                                    fontWeight: 'bold',
                                                    color: comp.weightDifferencePercent > 0 ? 'success.main' : comp.weightDifferencePercent < 0 ? 'error.main' : 'text.primary'
                                                }}
                                            >
                                                {comp.weightDifferencePercent > 0 ? '+' : ''}{comp.weightDifferencePercent}%
                                            </CustomTypography>
                                        </TableCell>
                                        <TableCell align="right">{comp.daysDifference}</TableCell>
                                        <TableCell align="right">
                                            {comp.dailyGain && (
                                                <CustomTypography 
                                                    variant="body2"
                                                    sx={{ 
                                                        fontWeight: 'bold',
                                                        color: comp.dailyGain > 0 ? 'success.main' : comp.dailyGain < 0 ? 'error.main' : 'text.primary'
                                                    }}
                                                >
                                                    {comp.dailyGain > 0 ? '+' : ''}{comp.dailyGain}
                                                </CustomTypography>
                                            )}
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </>
            ) : (
                <Box sx={{ textAlign: 'center', py: 3 }}>
                    <CustomTypography variant="body2" color="text.secondary">
                        No hay estimaciones anteriores del mismo animal para comparar
                    </CustomTypography>
                </Box>
            )}
        </Card>
    );
}

export default EstimationComparisonCard;
