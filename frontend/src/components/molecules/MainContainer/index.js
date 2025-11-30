// src/components/molecules/MainContainer/index.js
import React from 'react';
import Box from '@mui/material/Box';

const containerStyles = {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
    width: '100%',
};

function MainContainer({ children }) {
    return (
        <Box sx={containerStyles}>
            {children}
        </Box>
    );
}

export default MainContainer;
