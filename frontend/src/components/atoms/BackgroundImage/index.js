import React from 'react';
import Grid from '@mui/material/Grid';
import { styled } from '@mui/material/styles';

// Imagen local de ganado bovino
const CATTLE_IMAGE = '/cattle.jpeg';

const ImageGrid = styled(Grid)(({ theme }) => ({
    backgroundImage: `url(${CATTLE_IMAGE})`,
    backgroundRepeat: 'no-repeat',
    backgroundColor: theme.palette.mode === 'light' 
        ? theme.palette.grey[100]
        : theme.palette.grey[900],
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    minHeight: '100vh',
    display: 'flex',
}));

function BackgroundImage() {
    return <ImageGrid item xs={false} sm={4} md={7} />;
}

export default BackgroundImage;