import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Copyright from '../../atoms/Copyright';

function Footer(props) {
    const { description } = props;

    return (
        <Box sx={{
            py: 2, mt: 'auto', // margin-top: auto para empujarlo hacia abajo
        }} >
            <Container maxWidth="lg">
                <Typography
                    variant="subtitle1"
                    align="center"
                    color="text.secondary"
                    component="p"
                >
                    {description}
                </Typography>
                <Copyright sx={{ mt: 2 }} />
            </Container>
        </Box>
    );
}

export default Footer;