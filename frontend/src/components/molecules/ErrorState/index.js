// frontend/src/components/molecules/ErrorState/index.js

import Grid from "@mui/material/Grid";
import Alert from '@mui/material/Alert';

/**
 * ErrorState molecule - Estado de error reutilizable
 * @param {string|null} error - Mensaje de error
 */
function ErrorState({ error }) {
    if (!error) return null;

    return (
        <Grid container mt={2}>
            <Alert severity="error">{error}</Alert>
        </Grid>
    );
}

export default ErrorState;

