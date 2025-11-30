// frontend/src/components/atoms/InfoField/index.js

import Box from '@mui/material/Box';
import CustomTypography from '../CustomTypography';

/**
 * InfoField atom - Campo de información con label y valor
 * @param {string} label - Etiqueta del campo
 * @param {ReactNode} value - Valor a mostrar
 * @param {ReactNode} icon - Icono opcional para el label
 */
function InfoField({ label, value, icon }) {
    return (
        <Box>
            <CustomTypography 
                variant="body2" 
                color="text.secondary" 
                sx={{ 
                    mb: 0.5, 
                    display: 'flex', 
                    alignItems: 'center', 
                    gap: 0.5 
                }}
            >
                {icon && icon}
                {label}
            </CustomTypography>
            <CustomTypography variant="body1" sx={{ fontWeight: 500 }}>
                {value || '-'}
            </CustomTypography>
        </Box>
    );
}

export default InfoField;

