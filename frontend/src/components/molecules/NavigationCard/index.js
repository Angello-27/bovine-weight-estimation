// frontend/src/components/molecules/NavigationCard/index.js

import Card from '../../atoms/Card';
import CustomTypography from '../../atoms/CustomTypography';
import Box from '@mui/material/Box';

/**
 * NavigationCard molecule - Tarjeta clickeable para navegar a otra sección
 * @param {ReactNode} icon - Icono a mostrar
 * @param {string} title - Título de la tarjeta
 * @param {string} description - Descripción/subtítulo
 * @param {Function} onClick - Handler del click
 * @param {string} iconBgColor - Color de fondo del icono (default: 'primary.light')
 * @param {string} iconColor - Color del icono (default: 'primary.contrastText')
 */
function NavigationCard({ 
    icon, 
    title, 
    description, 
    onClick,
    iconBgColor = 'primary.light',
    iconColor = 'primary.contrastText'
}) {
    return (
        <Card 
            sx={{ 
                p: 3, 
                cursor: 'pointer', 
                '&:hover': { boxShadow: 4 },
                transition: 'box-shadow 0.3s ease'
            }} 
            onClick={onClick}
        >
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Box sx={{ 
                    p: 2, 
                    borderRadius: 2, 
                    bgcolor: iconBgColor, 
                    color: iconColor,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center'
                }}>
                    {icon}
                </Box>
                <Box sx={{ flex: 1 }}>
                    <CustomTypography variant="h6" sx={{ mb: 0.5 }}>
                        {title}
                    </CustomTypography>
                    <CustomTypography variant="body2" color="text.secondary">
                        {description}
                    </CustomTypography>
                </Box>
            </Box>
        </Card>
    );
}

export default NavigationCard;

