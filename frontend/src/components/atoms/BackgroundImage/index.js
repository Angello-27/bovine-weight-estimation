import React from 'react';
import Grid from '@mui/material/Grid'; // Asegúrate de importar Grid
import { styled } from '@mui/material/styles';

const ImageGrid = styled(Grid)(({ theme }) => ({
    backgroundImage: 'url(https://source.unsplash.com/800x600/?irrigation,agriculture)',
    backgroundRepeat: 'no-repeat',
    backgroundColor: theme.palette.mode === 'light' ?
        'var(--color-light);' :
        'var(--color-dark);',
    backgroundSize: 'cover',
    backgroundPosition: 'center',
}));

function BackgroundImage() {
    return <ImageGrid item sm={4} md={7} />;
}

export default BackgroundImage;