// frontend/src/components/atoms/Card/index.js

import Paper from '@mui/material/Paper';

/**
 * Card atom - Componente Paper con estilo consistente para cards
 * 
 * Características:
 * - Usa background.paper del tema para mejor contraste
 * - Sombra personalizada que se adapta al tema
 * - Padding y borderRadius consistentes
 */
function Card({ children, sx, ...props }) {
    return (
        <Paper
            elevation={0}
            sx={{
                p: 3,
                borderRadius: 2,
                backgroundColor: 'background.paper',
                boxShadow: (theme) => 
                    theme.palette.mode === 'light' 
                        ? '0 2px 8px rgba(0, 0, 0, 0.1)' 
                        : '0 2px 8px rgba(0, 0, 0, 0.3)',
                border: (theme) => 
                    theme.palette.mode === 'light' 
                        ? '1px solid rgba(0, 0, 0, 0.08)' 
                        : '1px solid rgba(255, 255, 255, 0.1)',
                ...sx,
            }}
            {...props}
        >
            {children}
        </Paper>
    );
}

export default Card;

