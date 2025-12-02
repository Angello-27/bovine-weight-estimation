// frontend/src/components/organisms/CattleLineageTree/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Divider from '@mui/material/Divider';
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import Chip from '@mui/material/Chip';
import Button from '@mui/material/Button';
import EmptyState from '../../molecules/EmptyState';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';
import TagIcon from '@mui/icons-material/Tag';
import PetsIcon from '@mui/icons-material/Pets';
import WcIcon from '@mui/icons-material/Wc';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import { breedToComboBox } from '../../../utils/transformers/breedToComboBox';
import { useNavigate } from 'react-router-dom';

function CattleLineageTree({ cattle, father, mother, descendants = [], onViewFather, onViewMother }) {
    const navigate = useNavigate();
    const hasLineage = father || mother || (descendants && descendants.length > 0);

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
                    Linaje
                </CustomTypography>
            </Box>
            
            {/* Sección de Padres */}
            {(father || mother) && (
                <>
                    <CustomTypography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
                        Ascendencia
                    </CustomTypography>
                    <Grid container spacing={3} sx={{ mb: 4 }}>
                        {father && (
                            <Grid item xs={12} md={6}>
                                <Box
                                    sx={{
                                        p: 2,
                                        border: '1px solid',
                                        borderColor: 'divider',
                                        borderRadius: 2,
                                        textAlign: 'center',
                                        bgcolor: 'info.light',
                                        '&:hover': { boxShadow: 2 }
                                    }}
                                >
                                    <CustomTypography variant="subtitle2" color="text.secondary" mb={1}>
                                        Padre
                                    </CustomTypography>
                                    <CustomTypography variant="h6" mb={1}>
                                        {father.ear_tag || 'Sin caravana'}
                                    </CustomTypography>
                                    {father.name && (
                                        <CustomTypography variant="body2" color="text.secondary" mb={1}>
                                            {father.name}
                                        </CustomTypography>
                                    )}
                                    <Chip
                                        label={getBreedLabel(father.breed)}
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
                                        textAlign: 'center',
                                        bgcolor: 'success.light',
                                        '&:hover': { boxShadow: 2 }
                                    }}
                                >
                                    <CustomTypography variant="subtitle2" color="text.secondary" mb={1}>
                                        Madre
                                    </CustomTypography>
                                    <CustomTypography variant="h6" mb={1}>
                                        {mother.ear_tag || 'Sin caravana'}
                                    </CustomTypography>
                                    {mother.name && (
                                        <CustomTypography variant="body2" color="text.secondary" mb={1}>
                                            {mother.name}
                                        </CustomTypography>
                                    )}
                                    <Chip
                                        label={getBreedLabel(mother.breed)}
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
                </>
            )}

            {/* Sección de Descendencia (Hijos) */}
            {descendants && descendants.length > 0 && (
                <>
                    {(father || mother) && <Divider sx={{ my: 3 }} />}
                    <CustomTypography variant="subtitle1" sx={{ mb: 2, fontWeight: 600 }}>
                        Descendencia Directa ({descendants.length} {descendants.length === 1 ? 'hijo' : 'hijos'})
                    </CustomTypography>
                    <Grid container spacing={2}>
                        {descendants.map((descendant) => {
                            const age = calculateAge(descendant.birth_date);
                            return (
                                <Grid item xs={12} sm={6} md={4} key={descendant.id}>
                                    <Card
                                        sx={{
                                            p: 2,
                                            cursor: 'pointer',
                                            '&:hover': { boxShadow: 4 },
                                            transition: 'box-shadow 0.3s ease',
                                            height: '100%'
                                        }}
                                        onClick={() => navigate(`/cattle/${descendant.id}`)}
                                    >
                                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                                            <TagIcon fontSize="small" color="primary" />
                                            <CustomTypography variant="subtitle1" sx={{ fontWeight: 600 }}>
                                                {descendant.ear_tag || 'Sin caravana'}
                                            </CustomTypography>
                                        </Box>
                                        
                                        {descendant.name && (
                                            <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 1.5 }}>
                                                {descendant.name}
                                            </CustomTypography>
                                        )}
                                        
                                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                                <PetsIcon fontSize="small" color="action" />
                                                <CustomTypography variant="caption" color="text.secondary">
                                                    {getBreedLabel(descendant.breed)}
                                                </CustomTypography>
                                            </Box>
                                            
                                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                                <WcIcon fontSize="small" color="action" />
                                                <CustomTypography variant="caption" color="text.secondary">
                                                    {getGenderLabel(descendant.gender)}
                                                </CustomTypography>
                                            </Box>
                                            
                                            {descendant.birth_date && (
                                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                                    <CalendarTodayIcon fontSize="small" color="action" />
                                                    <CustomTypography variant="caption" color="text.secondary">
                                                        {formatDate(descendant.birth_date)}
                                                        {age !== null && ` (${age} meses)`}
                                                    </CustomTypography>
                                                </Box>
                                            )}
                                            
                                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                                <CheckCircleIcon fontSize="small" color="action" />
                                                <CustomTypography variant="caption" color="text.secondary">
                                                    {getStatusLabel(descendant.status)}
                                                </CustomTypography>
                                            </Box>
                                        </Box>
                                        
                                        <Button
                                            size="small"
                                            variant="text"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                navigate(`/cattle/${descendant.id}`);
                                            }}
                                            sx={{ mt: 1.5, textTransform: 'none' }}
                                        >
                                            Ver Detalle →
                                        </Button>
                                    </Card>
                                </Grid>
                            );
                        })}
                    </Grid>
                </>
            )}

            {/* Mensaje si no hay linaje */}
            {!father && !mother && (!descendants || descendants.length === 0) && (
                <EmptyState message="No hay información de linaje disponible para este animal." />
            )}
        </Card>
    );
}

export default CattleLineageTree;

