// components/organisms/MainContent/index.js
import React from 'react';
import StyledPaper from './StyledPaper';

function MainContent({ open, children }) {
    return (
        <StyledPaper open={open} elevation={4}>
            {children}
            {/* Contenido del contenedor */}
        </StyledPaper>
    );
}

export default MainContent;
