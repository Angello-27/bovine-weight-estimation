// src/components/molecules/GridContainer.js
import React from 'react';
import { Grid } from '@mui/material';

const gridStyles = {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
};

function MainContainer({ children }) {
    return (
        <Grid elevation={3} sx={gridStyles}>
            {children}
        </Grid>
    );
}

export default MainContainer;
