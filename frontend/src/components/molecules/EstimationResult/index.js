// frontend/src/components/molecules/EstimationResult/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import CustomButton from '../../atoms/CustomButton';
import CustomTypography from '../../atoms/CustomTypography';
import LinearProgress from '@mui/material/LinearProgress';
import Chip from '@mui/material/Chip';
import Card from '../../atoms/Card';
import MonitorWeightIcon from '@mui/icons-material/MonitorWeight';

function EstimationResult({ result, loading, onSave, onReset, showActions = true }) {
    if (!result) return null;

    const getConfidenceColor = (score) => {
        if (score >= 0.9) return 'success';
        if (score >= 0.7) return 'warning';
        return 'error';
    };

    return (
        <Card>
            <Box display="flex" alignItems="center" gap={1} mb={2}>
                <MonitorWeightIcon color="primary" />
                <CustomTypography variant="h6">
                    Resultado de Estimación
                </CustomTypography>
            </Box>
            
            <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                    <Box textAlign="center">
                        <CustomTypography variant="h4" color="primary" mb={1}>
                            {result.estimated_weight?.toFixed(1)} kg
                        </CustomTypography>
                        <CustomTypography variant="body2" color="text.secondary">
                            Peso Estimado
                        </CustomTypography>
                    </Box>
                </Grid>
                
                <Grid item xs={12} md={4}>
                    <Box>
                        <CustomTypography variant="body2" mb={1}>
                            Confianza
                        </CustomTypography>
                        <LinearProgress
                            variant="determinate"
                            value={(result.confidence_score * 100) || 0}
                            color={getConfidenceColor(result.confidence_score)}
                            sx={{ height: 8, borderRadius: 4, mb: 1 }}
                        />
                        <CustomTypography variant="body2" color="text.secondary">
                            {((result.confidence_score * 100) || 0).toFixed(0)}%
                        </CustomTypography>
                    </Box>
                </Grid>
                
                <Grid item xs={12} md={4}>
                    <Box>
                        <CustomTypography variant="body2" mb={1}>
                            Raza Detectada
                        </CustomTypography>
                        <Chip
                            label={result.breed || 'No detectada'}
                            color="primary"
                            variant="outlined"
                        />
                        {result.breed_confidence && (
                            <CustomTypography variant="caption" color="text.secondary" display="block" mt={0.5}>
                                {(result.breed_confidence * 100).toFixed(0)}% confianza
                            </CustomTypography>
                        )}
                    </Box>
                </Grid>
                
                {result.processing_time_ms && (
                    <Grid item xs={12}>
                        <CustomTypography variant="body2" color="text.secondary">
                            Tiempo de procesamiento: {(result.processing_time_ms / 1000).toFixed(2)} segundos
                        </CustomTypography>
                    </Grid>
                )}
            </Grid>

            {showActions && (
                <Box mt={3} display="flex" gap={2}>
                    <CustomButton
                        variant="contained"
                        onClick={onSave}
                        disabled={loading}
                    >
                        Guardar Estimación
                    </CustomButton>
                    <CustomButton
                        variant="outlined"
                        onClick={onReset}
                        disabled={loading}
                    >
                        Estimar Otra Vez
                    </CustomButton>
                </Box>
            )}
        </Card>
    );
}

export default EstimationResult;

