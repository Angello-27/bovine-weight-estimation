// frontend/src/components/organisms/CattleLineageTree/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import EmptyState from '../../molecules/EmptyState';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';
import { breedToComboBox } from '../../../utils/transformers/breedToComboBox';
import DescendantCard from '../../atoms/DescendantCard';

function CattleLineageTree({ cattle, father, mother, descendants = [], onViewFather, onViewMother }) {
    const hasLineage = descendants && descendants.length > 0;

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

    const calculateAge = (birthDate) => {
        if (!birthDate) return null;
        try {
            const birth = new Date(birthDate);
            const today = new Date();
            const months = (today.getFullYear() - birth.getFullYear()) * 12 + (today.getMonth() - birth.getMonth());
            return months;
        } catch {
            return null;
        }
    };

    const getBreedLabel = (breed) => {
        const breeds = breedToComboBox();
        const breedOption = breeds.find(b => b.id === breed);
        return breedOption?.label || breed || '-';
    };

    const getGenderLabel = (gender) => {
        return gender === 'male' ? 'Macho' : gender === 'female' ? 'Hembra' : gender || '-';
    };

    const getStatusLabel = (status) => {
        const statusMap = {
            'active': 'Activo',
            'inactive': 'Inactivo',
            'sold': 'Vendido',
            'deceased': 'Fallecido'
        };
        return statusMap[status] || status || '-';
    };

    if (!hasLineage) {
        return (
            <Card>
                <EmptyState message="No hay información de linaje disponible para este animal." />
            </Card>
        );
    }

    return (
        <Card sx={{ p: 3 }}>
            <Box display="flex" alignItems="center" gap={1} mb={3}>
                <FamilyRestroomIcon color="primary" />
                <CustomTypography variant="h6">
                    Linaje - Descendencia
                </CustomTypography>
            </Box>
            
            {/* Sección de Descendencia (Hijos) */}
            {descendants && descendants.length > 0 ? (
                <>
                    <CustomTypography variant="subtitle1" sx={{ mb: 3, fontWeight: 600 }}>
                        Descendencia Directa ({descendants.length} {descendants.length === 1 ? 'hijo' : 'hijos'})
                    </CustomTypography>
                    <Box>
                        <Grid container spacing={2}>
                            {descendants.map((descendant) => {
                                const getStatusColor = (status) => {
                                    const colorMap = {
                                        'active': 'success',
                                        'inactive': 'default',
                                        'sold': 'warning',
                                        'deceased': 'error'
                                    };
                                    return colorMap[status] || 'default';
                                };
                                
                                return (
                                    <Grid item xs={12} sm={6} md={4} key={descendant.id} sx={{ display: 'flex' }}>
                                        <DescendantCard
                                            descendant={descendant}
                                            getBreedLabel={getBreedLabel}
                                            getGenderLabel={getGenderLabel}
                                            getStatusLabel={getStatusLabel}
                                            getStatusColor={getStatusColor}
                                            formatDate={formatDate}
                                            calculateAge={calculateAge}
                                        />
                                    </Grid>
                                );
                            })}
                        </Grid>
                    </Box>
                </>
            ) : (
                <EmptyState message="Este animal no tiene descendencia registrada." />
            )}
        </Card>
    );
}

export default CattleLineageTree;

