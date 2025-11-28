import * as React from 'react';
import IconButton from '@mui/material/IconButton';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';

function BackIconButton({ onClick }) {
    return (
        <IconButton onClick={onClick}
            sx={{
                padding: '12px',
                color: 'primary.main',
                '&:hover': {
                    backgroundColor: 'primary.dark', // Cambia el color de fondo a primary.main en hover
                    color: 'white', // Cambia el color del texto a blanco en hover
                }
            }}>
            <ChevronLeftIcon />
        </IconButton>
    );
}

export default BackIconButton;