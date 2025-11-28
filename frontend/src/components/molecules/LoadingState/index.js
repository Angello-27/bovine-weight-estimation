// frontend/src/components/molecules/LoadingState/index.js

import Grid from "@mui/material/Grid";
import CircularProgress from '@mui/material/CircularProgress';

/**
 * LoadingState molecule - Estado de carga reutilizable
 * @param {boolean} loading - Si está cargando
 * @param {ReactNode} children - Contenido a mostrar cuando no está cargando
 */
function LoadingState({ loading, children }) {
    if (loading) {
        return (
            <Grid container justifyContent="center" mt={4}>
                <CircularProgress />
            </Grid>
        );
    }

    return children;
}

export default LoadingState;

