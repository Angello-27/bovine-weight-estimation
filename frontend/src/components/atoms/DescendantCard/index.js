// frontend/src/components/atoms/DescendantCard/index.js

import Box from "@mui/material/Box";
import Card from '../Card';
import CustomTypography from '../CustomTypography';
import Chip from '@mui/material/Chip';
import LinkButton from '../LinkButton';
import TagIcon from '@mui/icons-material/Tag';
import PetsIcon from '@mui/icons-material/Pets';
import WcIcon from '@mui/icons-material/Wc';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import { useNavigate } from 'react-router-dom';

/**
 * DescendantCard - Componente atómico para mostrar información de un descendiente
 * 
 * @param {Object} descendant - Objeto con información del descendiente
 * @param {Function} getBreedLabel - Función para obtener el label de la raza
 * @param {Function} getGenderLabel - Función para obtener el label del género
 * @param {Function} getStatusLabel - Función para obtener el label del estado
 * @param {Function} getStatusColor - Función para obtener el color del estado
 * @param {Function} formatDate - Función para formatear fechas
 * @param {Function} calculateAge - Función para calcular la edad
 */
function DescendantCard({ 
    descendant, 
    getBreedLabel, 
    getGenderLabel, 
    getStatusLabel, 
    getStatusColor,
    formatDate,
    calculateAge
}) {
    const navigate = useNavigate();
    const age = calculateAge(descendant.birth_date);

    return (
        <Card
            sx={{
                p: 2.5,
                width: '100%',
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                '&:hover': { boxShadow: 4 },
                transition: 'box-shadow 0.3s ease'
            }}
        >
            {/* Caravana con Estado */}
            <Box sx={{ mb: 1.5, display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 1 }}>
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
                        fontWeight: 600,
                        flex: 1
                    }}
                >
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        <TagIcon fontSize="small" color="primary" />
                        {descendant.ear_tag || 'Sin caravana'}
                    </Box>
                </LinkButton>
                <Chip
                    label={getStatusLabel(descendant.status)}
                    size="small"
                    color={getStatusColor(descendant.status)}
                    variant="outlined"
                />
            </Box>
            
            {/* Nombre */}
            {descendant.name && (
                <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 1.5, ml: 3.5 }}>
                    {descendant.name}
                </CustomTypography>
            )}
            
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
            </Box>
        </Card>
    );
}

export default DescendantCard;

