// frontend/src/components/molecules/WeightStatsCards/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';

/**
 * WeightStatsCards molecule - Tarjetas de estadísticas de peso
 * @param {number} weightGain - Ganancia total de peso
 * @param {number} latestWeight - Peso actual
 * @param {number} averageWeight - Peso promedio
 */
function WeightStatsCards({ weightGain, latestWeight, averageWeight }) {
    if (!weightGain && !latestWeight && !averageWeight) {
        return null;
    }

    return (
        <Grid container spacing={2} mb={3}>
            {weightGain && (
                <Grid item xs={12} md={4}>
                    <Box textAlign="center" p={2} sx={{ bgcolor: 'action.hover', borderRadius: 2 }}>
                        <CustomTypography variant="body2" color="text.secondary">
                            Ganancia Total
                        </CustomTypography>
                        <CustomTypography variant="h6" color="primary">
                            {weightGain} kg
                        </CustomTypography>
                    </Box>
                </Grid>
            )}
            {latestWeight && (
                <Grid item xs={12} md={4}>
                    <Box textAlign="center" p={2} sx={{ bgcolor: 'action.hover', borderRadius: 2 }}>
                        <CustomTypography variant="body2" color="text.secondary">
                            Peso Actual
                        </CustomTypography>
                        <CustomTypography variant="h6" color="primary">
                            {latestWeight.toFixed(1)} kg
                        </CustomTypography>
                    </Box>
                </Grid>
            )}
            {averageWeight && (
                <Grid item xs={12} md={4}>
                    <Box textAlign="center" p={2} sx={{ bgcolor: 'action.hover', borderRadius: 2 }}>
                        <CustomTypography variant="body2" color="text.secondary">
                            Peso Promedio
                        </CustomTypography>
                        <CustomTypography variant="h6" color="primary">
                            {averageWeight.toFixed(1)} kg
                        </CustomTypography>
                    </Box>
                </Grid>
            )}
        </Grid>
    );
}

export default WeightStatsCards;

