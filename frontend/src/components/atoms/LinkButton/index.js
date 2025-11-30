// frontend/src/components/atoms/LinkButton/index.js

import CustomButton from '../CustomButton';
import VisibilityIcon from '@mui/icons-material/Visibility';
import Box from '@mui/material/Box';

/**
 * LinkButton atom - Botón que parece un link con icono opcional
 * @param {string} children - Texto a mostrar
 * @param {Function} onClick - Handler del click
 * @param {boolean} showIcon - Mostrar icono de ojo (default: true)
 * @param {Object} sx - Estilos adicionales
 */
function LinkButton({ 
    children, 
    onClick, 
    showIcon = true,
    sx = {},
    ...props 
}) {
    return (
        <CustomButton
            variant="text"
            onClick={onClick}
            sx={{
                textTransform: 'none',
                fontWeight: 600,
                color: 'primary.main',
                '&:hover': {
                    textDecoration: 'underline',
                    backgroundColor: 'transparent'
                },
                padding: 0,
                minWidth: 'auto',
                justifyContent: 'flex-start',
                gap: 0.5,
                ...sx
            }}
            {...props}
        >
            {showIcon && (
                <VisibilityIcon 
                    sx={{ 
                        fontSize: 18
                    }} 
                />
            )}
            <Box component="span">
                {children}
            </Box>
        </CustomButton>
    );
}

export default LinkButton;

