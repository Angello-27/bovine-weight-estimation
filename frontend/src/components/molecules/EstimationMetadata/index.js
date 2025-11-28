// frontend/src/components/molecules/EstimationMetadata/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import Chip from '@mui/material/Chip';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import MemoryIcon from '@mui/icons-material/Memory';
import InfoIcon from '@mui/icons-material/Info';

/**
 * EstimationMetadata molecule - Muestra metadata de la estimación
 * @param {Object} estimation - Datos de la estimación
 */
function EstimationMetadata({ estimation }) {
    if (!estimation) return null;

    const formatDate = (dateString) => {
        if (!dateString) return '-';
        return new Date(dateString).toLocaleString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const formatProcessingTime = (ms) => {
        if (!ms) return '-';
        if (ms < 1000) return `${ms} ms`;
        return `${(ms / 1000).toFixed(2)} s`;
    };

    return (
        <Card>
            <Box display="flex" alignItems="center" gap={1} mb={3}>
                <InfoIcon color="primary" />
                <CustomTypography variant="h6">
                    Información de la Estimación
                </CustomTypography>
            </Box>
            
            <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                    <Box mb={2}>
                        <CustomTypography variant="body2" color="text.secondary" mb={0.5}>
                            Fecha y Hora
                        </CustomTypography>
                        <Box display="flex" alignItems="center" gap={1}>
                            <AccessTimeIcon fontSize="small" color="action" />
                            <CustomTypography variant="body1">
                                {formatDate(estimation.timestamp)}
                            </CustomTypography>
                        </Box>
                    </Box>
                </Grid>

                {estimation.method && (
                    <Grid item xs={12} md={6}>
                        <Box mb={2}>
                            <CustomTypography variant="body2" color="text.secondary" mb={0.5}>
                                Método
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
                    <Grid item xs={12} md={6}>
                        <Box mb={2}>
                            <CustomTypography variant="body2" color="text.secondary" mb={0.5}>
                                Versión del Modelo
                            </CustomTypography>
                            <Box display="flex" alignItems="center" gap={1}>
                                <MemoryIcon fontSize="small" color="action" />
                                <CustomTypography variant="body1">
                                    {estimation.model_version}
                                </CustomTypography>
                            </Box>
                        </Box>
                    </Grid>
                )}

                {estimation.processing_time_ms && (
                    <Grid item xs={12} md={6}>
                        <Box mb={2}>
                            <CustomTypography variant="body2" color="text.secondary" mb={0.5}>
                                Tiempo de Procesamiento
                            </CustomTypography>
                            <CustomTypography variant="body1">
                                {formatProcessingTime(estimation.processing_time_ms)}
                            </CustomTypography>
                        </Box>
                    </Grid>
                )}

                {(estimation.gps_latitude && estimation.gps_longitude) && (
                    <Grid item xs={12}>
                        <Box mb={2}>
                            <CustomTypography variant="body2" color="text.secondary" mb={0.5}>
                                Ubicación GPS
                            </CustomTypography>
                            <Box display="flex" alignItems="center" gap={1}>
                                <LocationOnIcon fontSize="small" color="action" />
                                <CustomTypography variant="body1">
                                    {estimation.gps_latitude.toFixed(6)}, {estimation.gps_longitude.toFixed(6)}
                                </CustomTypography>
                            </Box>
                        </Box>
                    </Grid>
                )}

                {estimation.cattle_id && (
                    <Grid item xs={12}>
                        <Box mb={2}>
                            <CustomTypography variant="body2" color="text.secondary" mb={0.5}>
                                Animal Asociado
                            </CustomTypography>
                            <Chip
                                label={`ID: ${estimation.cattle_id}`}
                                size="small"
                                color="secondary"
                                variant="outlined"
                            />
                        </Box>
                    </Grid>
                )}
            </Grid>
        </Card>
    );
}

export default EstimationMetadata;

