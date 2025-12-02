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

/**
 * EstimationComparisonCard molecule - Compara la estimación actual con anteriores
 * @param {Object} currentEstimation - Estimación actual
 * @param {Array} previousEstimations - Array de estimaciones anteriores (ordenadas por fecha descendente)
 */
function EstimationComparisonCard({ currentEstimation, previousEstimations = [] }) {
    if (!currentEstimation) return null;

    const currentWeight = currentEstimation.estimated_weight || currentEstimation.estimated_weight_kg || 0;
    
    // Obtener la estimación anterior más reciente
    const previousEstimation = previousEstimations.length > 0 ? previousEstimations[0] : null;
    const previousWeight = previousEstimation ? (previousEstimation.estimated_weight || previousEstimation.estimated_weight_kg || 0) : null;
    
    // Calcular diferencia
    const weightDifference = previousWeight !== null ? currentWeight - previousWeight : null;
    const weightDifferencePercent = previousWeight !== null && previousWeight > 0 
        ? ((weightDifference / previousWeight) * 100).toFixed(1)
        : null;

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

    return (
        <Card sx={{ p: 3 }}>
            <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                <CompareArrowsIcon />
                Comparación con Estimaciones Anteriores
            </CustomTypography>
            <Divider sx={{ mb: 3 }} />
            
            {previousWeight !== null ? (
                <Grid container spacing={3}>
                    <Grid item xs={12} sm={6}>
                        <InfoField
                            label="Peso Anterior"
                            value={previousWeight ? `${previousWeight.toFixed(1)} kg` : '-'}
                        />
                        {previousEstimation.timestamp && (
                            <CustomTypography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                                {formatDate(previousEstimation.timestamp)}
                            </CustomTypography>
                        )}
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                        <InfoField
                            label="Peso Actual"
                            value={`${currentWeight.toFixed(1)} kg`}
                        />
                        {currentEstimation.timestamp && (
                            <CustomTypography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                                {formatDate(currentEstimation.timestamp)}
                            </CustomTypography>
                        )}
                    </Grid>
                    
                    {weightDifference !== null && (
                        <Grid item xs={12}>
                            <Box sx={{ 
                                p: 2, 
                                borderRadius: 2, 
                                bgcolor: weightDifference > 0 ? 'success.light' : weightDifference < 0 ? 'error.light' : 'grey.200',
                                display: 'flex',
                                alignItems: 'center',
                                gap: 2
                            }}>
                                {weightDifference > 0 && <TrendingUpIcon color="success" />}
                                {weightDifference < 0 && <TrendingDownIcon color="error" />}
                                {weightDifference === 0 && <RemoveIcon />}
                                <Box>
                                    <CustomTypography variant="body2" color="text.secondary">
                                        Diferencia
                                    </CustomTypography>
                                    <CustomTypography 
                                        variant="h6" 
                                        sx={{ 
                                            fontWeight: 'bold',
                                            color: weightDifference > 0 ? 'success.main' : weightDifference < 0 ? 'error.main' : 'text.primary'
                                        }}
                                    >
                                        {weightDifference > 0 ? '+' : ''}{weightDifference.toFixed(1)} kg
                                        {weightDifferencePercent && ` (${weightDifferencePercent > 0 ? '+' : ''}${weightDifferencePercent}%)`}
                                    </CustomTypography>
                                </Box>
                            </Box>
                        </Grid>
                    )}
                </Grid>
            ) : (
                <Box sx={{ textAlign: 'center', py: 3 }}>
                    <CustomTypography variant="body2" color="text.secondary">
                        No hay estimaciones anteriores para comparar
                    </CustomTypography>
                </Box>
            )}
        </Card>
    );
}

export default EstimationComparisonCard;

