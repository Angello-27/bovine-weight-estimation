// frontend/src/components/molecules/CattleInfoCard/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Chip from '@mui/material/Chip';
import Card from '../../atoms/Card';

function CattleInfoCard({ cattle }) {
    if (!cattle) return null;

    const calculateAge = (birthDate) => {
        if (!birthDate) return null;
        const birth = new Date(birthDate);
        const today = new Date();
        const months = (today.getFullYear() - birth.getFullYear()) * 12 + (today.getMonth() - birth.getMonth());
        return months;
    };

    const age = calculateAge(cattle.birth_date);
    const genderLabel = cattle.gender === 'male' ? 'Macho' : 'Hembra';

    return (
        <Card>
            <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                    <Box mb={2}>
                        <CustomTypography variant="h5" mb={1}>
                            {cattle.ear_tag}
                        </CustomTypography>
                        {cattle.name && (
                            <CustomTypography variant="h6" color="text.secondary" mb={2}>
                                {cattle.name}
                            </CustomTypography>
                        )}
                    </Box>
                    
                    <Grid container spacing={2}>
                        <Grid item xs={6}>
                            <CustomTypography variant="body2" color="text.secondary">
                                Raza
                            </CustomTypography>
                            <Chip label={cattle.breed} size="small" color="primary" variant="outlined" />
                        </Grid>
                        <Grid item xs={6}>
                            <CustomTypography variant="body2" color="text.secondary">
                                Género
                            </CustomTypography>
                            <CustomTypography variant="body1">
                                {genderLabel}
                            </CustomTypography>
                        </Grid>
                        {age !== null && (
                            <Grid item xs={6}>
                                <CustomTypography variant="body2" color="text.secondary">
                                    Edad
                                </CustomTypography>
                                <CustomTypography variant="body1">
                                    {age} meses
                                </CustomTypography>
                            </Grid>
                        )}
                        {cattle.birth_weight_kg && (
                            <Grid item xs={6}>
                                <CustomTypography variant="body2" color="text.secondary">
                                    Peso al Nacer
                                </CustomTypography>
                                <CustomTypography variant="body1">
                                    {cattle.birth_weight_kg} kg
                                </CustomTypography>
                            </Grid>
                        )}
                    </Grid>
                </Grid>
                
                <Grid item xs={12} md={6}>
                    {cattle.color && (
                        <Box mb={2}>
                            <CustomTypography variant="body2" color="text.secondary">
                                Color
                            </CustomTypography>
                            <CustomTypography variant="body1">
                                {cattle.color}
                            </CustomTypography>
                        </Box>
                    )}
                    {cattle.observations && (
                        <Box>
                            <CustomTypography variant="body2" color="text.secondary" mb={1}>
                                Observaciones
                            </CustomTypography>
                            <CustomTypography variant="body2">
                                {cattle.observations}
                            </CustomTypography>
                        </Box>
                    )}
                </Grid>
            </Grid>
        </Card>
    );
}

export default CattleInfoCard;

