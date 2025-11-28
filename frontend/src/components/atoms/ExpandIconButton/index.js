import React from 'react';
import Fab from '@mui/material/Fab';
import FullscreenIcon from '@mui/icons-material/Fullscreen';
import FullscreenExitIcon from '@mui/icons-material/FullscreenExit';

const fabStyles = {
    top: 0,
    right: 0,
    margin: '8px',
    position: 'absolute',
    color: 'white',
    backgroundColor: 'primary.main',
    '&:hover': {
        backgroundColor: 'primary.dark', // Cambia el color de fondo a primary.main en hover
        color: 'white', // Cambia el color del texto a blanco en hover
    }
};

function ExpandIconButton({ isFullscreen, toggleFullscreen }) {
    return (
        <Fab onClick={toggleFullscreen} sx={fabStyles} size="medium" >
            {isFullscreen ? <FullscreenExitIcon /> : <FullscreenIcon />}
        </Fab >
    );
}

export default ExpandIconButton;
