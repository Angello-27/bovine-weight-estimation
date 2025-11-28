import { Box, Container } from '@mui/material';

import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider } from '@mui/material/styles';
import { useTheme } from '../../config/theme/ThemeContext'; // Asegúrate de importar tu tema

import ErrorContent from '../../components/organisms/ErrorContent';

function Error404Template() {
    const { currentTheme } = useTheme();

    return (
        <ThemeProvider theme={currentTheme}>
            <CssBaseline />
            <Box
                component="main"
                sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    minHeight: '100vh', // Ocupará al menos el alto de la pantalla del dispositivo.
                    m: 2, // margen en todas las direcciones
                    p: 2, // padding en todas las direcciones
                }} >
                <Container maxWidth="md">
                    <ErrorContent />
                </Container>
            </Box>
        </ThemeProvider>
    );
}

export default Error404Template;
