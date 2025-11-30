// frontend/src/components/atoms/CustomButton/index.js

import Button from '@mui/material/Button';

/**
 * CustomButton atom - Botón personalizado con estilos consistentes del tema
 * 
 * Características:
 * - Estilos adaptados al tema (light/dark)
 * - Altura consistente
 * - Soportan todas las props de Button de MUI
 */
function CustomButton({ children, sx, ...props }) {
    return (
        <Button
            sx={{
                minHeight: '48px',
                textTransform: 'none',
                fontWeight: 500,
                borderRadius: 2,
                px: 3,
                ...sx,
            }}
            {...props}
        >
            {children}
        </Button>
    );
}

export default CustomButton;
