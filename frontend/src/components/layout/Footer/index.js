import React from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Copyright from '../../atoms/Copyright';

function Footer() {
    return (
        <Box sx={{
            py: 2, 
            mt: 'auto', // margin-top: auto para empujarlo hacia abajo
        }} >
            <Container maxWidth="lg">
                <Copyright />
            </Container>
        </Box>
    );
}

export default Footer;