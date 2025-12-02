// frontend/src/components/molecules/EstimationTechnicalCard/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Divider from '@mui/material/Divider';
import Card from '../../atoms/Card';
import InfoField from '../../atoms/InfoField';
import CustomTypography from '../../atoms/CustomTypography';
import Chip from '@mui/material/Chip';
import MemoryIcon from '@mui/icons-material/Memory';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import InfoIcon from '@mui/icons-material/Info';
import ScienceIcon from '@mui/icons-material/Science';

/**
 * EstimationTechnicalCard molecule - Muestra detalles técnicos de la estimación
 * @param {Object} estimation - Datos de la estimación
 */
function EstimationTechnicalCard({ estimation }) {
    if (!estimation) return null;

    const formatProcessingTime = (ms) => {
        if (!ms) return '-';
        if (ms < 1000) return `${ms} ms`;
        return `${(ms / 1000).toFixed(2)} s`;
    };

    return (
        <Card sx={{ p: 3 }}>
            <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                <InfoIcon />
                Detalles Técnicos
            </CustomTypography>
            <Divider sx={{ mb: 3 }} />
            
            <Grid container spacing={3}>
                {estimation.method && (
                    <Grid item xs={12}>
                        <Box>
                            <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 1, display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                <ScienceIcon fontSize="small" />
                                Método de Estimación
                            </CustomTypography>
                            <Chip
                                label={estimation.method}
                                size="small"
                                color="primary"
                                variant="outlined"
                            />
                        </Box>
                    </Grid>
                )}
                
                {estimation.model_version && (
                    <Grid item xs={12} sm={6}>
                        <InfoField
                            label="Versión del Modelo ML"
                            value={estimation.model_version || estimation.ml_model_version || '-'}
                            icon={<MemoryIcon fontSize="small" />}
                        />
                    </Grid>
                )}
                
                {estimation.processing_time_ms && (
                    <Grid item xs={12} sm={6}>
                        <InfoField
                            label="Tiempo de Procesamiento"
                            value={formatProcessingTime(estimation.processing_time_ms)}
                            icon={<AccessTimeIcon fontSize="small" />}
                        />
                    </Grid>
                )}
                
                {(estimation.gps_latitude && estimation.gps_longitude) && (
                    <Grid item xs={12}>
                        <InfoField
                            label="Ubicación GPS"
                            value={`${estimation.gps_latitude.toFixed(6)}, ${estimation.gps_longitude.toFixed(6)}`}
                            icon={<LocationOnIcon fontSize="small" />}
                        />
                    </Grid>
                )}

                {estimation.id && (
                    <Grid item xs={12} sm={6}>
                        <InfoField
                            label="ID de Estimación"
                            value={estimation.id}
                        />
                    </Grid>
                )}

                {estimation.meets_quality_criteria !== undefined && (
                    <Grid item xs={12} sm={6}>
                        <Box>
                            <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                                Cumple Criterios de Calidad
                            </CustomTypography>
                            <CustomTypography variant="body1" sx={{ fontWeight: 500, color: estimation.meets_quality_criteria ? 'success.main' : 'error.main' }}>
                                {estimation.meets_quality_criteria ? 'Sí' : 'No'}
                            </CustomTypography>
                        </Box>
                    </Grid>
                )}
            </Grid>
        </Card>
    );
}

export default EstimationTechnicalCard;

