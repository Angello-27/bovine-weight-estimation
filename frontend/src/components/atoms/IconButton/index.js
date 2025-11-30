// frontend/src/components/atoms/IconButton/index.js

import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';

/**
 * IconButton atom - Botón con solo icono y tooltip
 * @param {ReactNode} icon - Icono a mostrar
 * @param {string} tooltip - Texto del tooltip (requerido)
 * @param {string} color - Color del botón (default, primary, secondary, error, etc.)
 * @param {Function} onClick - Handler del click
 * @param {Object} sx - Estilos adicionales
 * @param {string} size - Tamaño (small, medium, large)
 */
function CustomIconButton({ 
    icon, 
    tooltip, 
    color = 'default', 
    onClick, 
    sx = {},
    size = 'medium',
    ...props 
}) {
    return (
        <Tooltip title={tooltip || ''} arrow>
            <IconButton
                color={color}
                onClick={onClick}
                size={size}
                sx={sx}
                {...props}
            >
                {icon}
            </IconButton>
        </Tooltip>
    );
}

export default CustomIconButton;

