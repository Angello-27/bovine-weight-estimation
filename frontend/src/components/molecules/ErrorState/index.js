// frontend/src/components/molecules/ErrorState/index.js

import Grid from "@mui/material/Grid";
import Alert from '@mui/material/Alert';

/**
 * ErrorState molecule - Estado de error reutilizable
 * @param {string|Object|null} error - Mensaje de error (string o objeto Error)
 */
function ErrorState({ error }) {
    if (!error) return null;

    // Convertir error a string si es un objeto
    const errorMessage = typeof error === 'string' 
        ? error 
        : error?.message || error?.toString() || 'Ocurrió un error';

    return (
        <Grid container mt={2}>
            <Alert severity="error">{errorMessage}</Alert>
        </Grid>
    );
}

export default ErrorState;

