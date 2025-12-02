// frontend/src/components/organisms/CattleLineageTree/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import Chip from '@mui/material/Chip';
import EmptyState from '../../molecules/EmptyState';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';
import TagIcon from '@mui/icons-material/Tag';
import PetsIcon from '@mui/icons-material/Pets';
import WcIcon from '@mui/icons-material/Wc';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import { breedToComboBox } from '../../../utils/transformers/breedToComboBox';
import { useNavigate } from 'react-router-dom';
import LinkButton from '../../atoms/LinkButton';

function CattleLineageTree({ cattle, father, mother, descendants = [], onViewFather, onViewMother }) {
    const navigate = useNavigate();
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
                    <Grid container spacing={2}>
                        {descendants.map((descendant) => {
                            const age = calculateAge(descendant.birth_date);
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
                                <Grid item xs={12} sm={6} md={4} key={descendant.id}>
                                    <Card
                                        sx={{
                                            p: 2.5,
                                            height: '100%',
                                            display: 'flex',
                                            flexDirection: 'column',
                                            '&:hover': { boxShadow: 4 },
                                            transition: 'box-shadow 0.3s ease'
                                        }}
                                    >
                                        {/* Caravana/Nombre como link */}
                                        <Box sx={{ mb: 1.5 }}>
                                            <LinkButton
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    navigate(`/cattle/${descendant.id}`);
                                                }}
                                                sx={{ 
                                                    textTransform: 'none',
                                                    p: 0,
                                                    justifyContent: 'flex-start',
                                                    fontSize: '1rem',
                                                    fontWeight: 600
                                                }}
                                            >
                                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                                    <TagIcon fontSize="small" color="primary" />
                                                    {descendant.ear_tag || 'Sin caravana'}
                                                </Box>
                                            </LinkButton>
                                            {descendant.name && (
                                                <CustomTypography variant="body2" color="text.secondary" sx={{ mt: 0.5, ml: 3.5 }}>
                                                    {descendant.name}
                                                </CustomTypography>
                                            )}
                                        </Box>
                                        
                                        {/* Información del animal */}
                                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5, flex: 1 }}>
                                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                                <PetsIcon fontSize="small" color="action" />
                                                <CustomTypography variant="body2" color="text.secondary">
                                                    {getBreedLabel(descendant.breed)}
                                                </CustomTypography>
                                            </Box>
                                            
                                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                                <WcIcon fontSize="small" color="action" />
                                                <CustomTypography variant="body2" color="text.secondary">
                                                    {getGenderLabel(descendant.gender)}
                                                </CustomTypography>
                                            </Box>
                                            
                                            {descendant.birth_date && (
                                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                                    <CalendarTodayIcon fontSize="small" color="action" />
                                                    <CustomTypography variant="body2" color="text.secondary">
                                                        {formatDate(descendant.birth_date)}
                                                        {age !== null && ` (${age} meses)`}
                                                    </CustomTypography>
                                                </Box>
                                            )}
                                            
                                            {/* Estado como Chip */}
                                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 'auto' }}>
                                                <Chip
                                                    label={getStatusLabel(descendant.status)}
                                                    size="small"
                                                    color={getStatusColor(descendant.status)}
                                                    variant="outlined"
                                                />
                                            </Box>
                                        </Box>
                                    </Card>
                                </Grid>
                            );
                        })}
                    </Grid>
                </>
            ) : (
                <EmptyState message="Este animal no tiene descendencia registrada." />
            )}
        </Card>
    );
}

export default CattleLineageTree;

