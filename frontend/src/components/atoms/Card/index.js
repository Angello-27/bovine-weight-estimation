// frontend/src/components/atoms/Card/index.js

import Box from '@mui/material/Box';

/**
 * Card atom - Box con estilo consistente para cards
 * Reemplaza el uso directo de Box con estilos repetidos
 */
function Card({ children, sx, ...props }) {
    return (
        <Box
            sx={{
                p: 3,
                bgcolor: 'background.paper',
                borderRadius: 2,
                boxShadow: 1,
                ...sx,
            }}
            {...props}
        >
            {children}
        </Box>
    );
}

export default Card;

