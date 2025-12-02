// frontend/src/components/molecules/EstimationInfoCard/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Divider from '@mui/material/Divider';
import Card from '../../atoms/Card';
import InfoField from '../../atoms/InfoField';
import CustomTypography from '../../atoms/CustomTypography';
import Chip from '@mui/material/Chip';
import LinearProgress from '@mui/material/LinearProgress';
import MonitorWeightIcon from '@mui/icons-material/MonitorWeight';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import PetsIcon from '@mui/icons-material/Pets';
import { breedToComboBox as getBreedOptions } from '../../../utils/transformers/breedToComboBox';

/**
 * EstimationInfoCard molecule - Muestra la información principal de una estimación
 * @param {Object} estimation - Datos de la estimación
 */
function EstimationInfoCard({ estimation }) {
    if (!estimation) return null;

    const formatDate = (dateString) => {
        if (!dateString) return '-';
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('es-ES', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return dateString;
        }
    };

    const getBreedLabel = (breed) => {
        if (!breed) return '-';
        const breedOptions = getBreedOptions();
        const breedOption = breedOptions.find(b => b.id === breed);
        return breedOption ? breedOption.label : breed;
    };

    const getConfidenceColor = (score) => {
        if (score >= 0.9) return 'success';
        if (score >= 0.7) return 'warning';
        return 'error';
    };

    const confidenceScore = estimation.confidence_score || estimation.confidence || 0;
    const estimatedWeight = estimation.estimated_weight || estimation.estimated_weight_kg || 0;

    return (
        <Card sx={{ p: 3 }}>
            <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                <MonitorWeightIcon />
                Información de la Estimación
            </CustomTypography>
            <Divider sx={{ mb: 3 }} />
            
            <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                    <InfoField
                        label="Peso Estimado"
                        value={`${estimatedWeight.toFixed(1)} kg`}
                        icon={<MonitorWeightIcon fontSize="small" />}
                    />
                </Grid>
                
                <Grid item xs={12} sm={6}>
                    <Box>
                        <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                            Confianza de la Estimación
                        </CustomTypography>
                        <LinearProgress
                            variant="determinate"
                            value={confidenceScore * 100}
                            color={getConfidenceColor(confidenceScore)}
                            sx={{ height: 10, borderRadius: 5, mb: 1 }}
                        />
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <CustomTypography variant="body1" sx={{ fontWeight: 500, color: `${getConfidenceColor(confidenceScore)}.main` }}>
                                {(confidenceScore * 100).toFixed(1)}%
                            </CustomTypography>
                            <Chip
                                label={confidenceScore >= 0.9 ? 'Alta' : confidenceScore >= 0.7 ? 'Media' : 'Baja'}
                                size="small"
                                color={getConfidenceColor(confidenceScore)}
                                variant="outlined"
                            />
                        </Box>
                    </Box>
                </Grid>
                
                <Grid item xs={12} sm={6}>
                    <InfoField
                        label="Fecha y Hora"
                        value={formatDate(estimation.timestamp)}
                        icon={<CalendarTodayIcon fontSize="small" />}
                    />
                </Grid>
                
                <Grid item xs={12} sm={6}>
                    <InfoField
                        label="Raza Detectada"
                        value={getBreedLabel(estimation.breed)}
                        icon={<PetsIcon fontSize="small" />}
                    />
                    {estimation.breed_confidence && (
                        <CustomTypography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                            Confianza: {(estimation.breed_confidence * 100).toFixed(0)}%
                        </CustomTypography>
                    )}
                </Grid>
            </Grid>
        </Card>
    );
}

export default EstimationInfoCard;

