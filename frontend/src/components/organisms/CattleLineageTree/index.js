// frontend/src/components/organisms/CattleLineageTree/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import Chip from '@mui/material/Chip';
import Button from '@mui/material/Button';
import EmptyState from '../../molecules/EmptyState';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';

function CattleLineageTree({ cattle, father, mother, onViewFather, onViewMother }) {
    const hasLineage = father || mother;

    if (!hasLineage) {
        return (
            <Card>
                <EmptyState message="No hay información de linaje disponible para este animal." />
            </Card>
        );
    }

    return (
        <Card>
            <Box display="flex" alignItems="center" gap={1} mb={3}>
                <FamilyRestroomIcon color="primary" />
                <CustomTypography variant="h6">
                    Linaje
                </CustomTypography>
            </Box>
            
            <Grid container spacing={3}>
                {father && (
                    <Grid item xs={12} md={6}>
                        <Box
                            sx={{
                                p: 2,
                                border: '1px solid',
                                borderColor: 'divider',
                                borderRadius: 2,
                                textAlign: 'center'
                            }}
                        >
                            <CustomTypography variant="subtitle2" color="text.secondary" mb={1}>
                                Padre
                            </CustomTypography>
                            <CustomTypography variant="h6" mb={1}>
                                {father.ear_tag}
                            </CustomTypography>
                            {father.name && (
                                <CustomTypography variant="body2" color="text.secondary" mb={1}>
                                    {father.name}
                                </CustomTypography>
                            )}
                            <Chip
                                label={father.breed}
                                size="small"
                                color="primary"
                                variant="outlined"
                                sx={{ mb: 1 }}
                            />
                            {onViewFather && (
                                <Button
                                    size="small"
                                    variant="outlined"
                                    onClick={() => onViewFather(father.id)}
                                    sx={{ mt: 1 }}
                                >
                                    Ver Detalle
                                </Button>
                            )}
                        </Box>
                    </Grid>
                )}
                
                {mother && (
                    <Grid item xs={12} md={6}>
                        <Box
                            sx={{
                                p: 2,
                                border: '1px solid',
                                borderColor: 'divider',
                                borderRadius: 2,
                                textAlign: 'center'
                            }}
                        >
                            <CustomTypography variant="subtitle2" color="text.secondary" mb={1}>
                                Madre
                            </CustomTypography>
                            <CustomTypography variant="h6" mb={1}>
                                {mother.ear_tag}
                            </CustomTypography>
                            {mother.name && (
                                <CustomTypography variant="body2" color="text.secondary" mb={1}>
                                    {mother.name}
                                </CustomTypography>
                            )}
                            <Chip
                                label={mother.breed}
                                size="small"
                                color="primary"
                                variant="outlined"
                                sx={{ mb: 1 }}
                            />
                            {onViewMother && (
                                <Button
                                    size="small"
                                    variant="outlined"
                                    onClick={() => onViewMother(mother.id)}
                                    sx={{ mt: 1 }}
                                >
                                    Ver Detalle
                                </Button>
                            )}
                        </Box>
                    </Grid>
                )}
            </Grid>
        </Card>
    );
}

export default CattleLineageTree;

