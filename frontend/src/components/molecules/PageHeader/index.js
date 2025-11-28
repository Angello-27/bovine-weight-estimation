// frontend/src/components/molecules/PageHeader/index.js

import Grid from "@mui/material/Grid";
import CustomTypography from '../../atoms/CustomTypography';

/**
 * PageHeader molecule - Header de página reutilizable
 * @param {string} title - Título de la página
 * @param {string} description - Descripción opcional
 * @param {ReactNode} action - Acción opcional (botón, etc.)
 */
function PageHeader({ title, description, action }) {
    return (
        <Grid container item xs={12} mb={4} justifyContent="space-between" alignItems="center">
            <Grid item>
                <CustomTypography variant="h3" mb={description ? 1 : 0}>
                    {title}
                </CustomTypography>
                {description && (
                    <CustomTypography variant="body1" color="text.secondary">
                        {description}
                    </CustomTypography>
                )}
            </Grid>
            {action && (
                <Grid item>
                    {action}
                </Grid>
            )}
        </Grid>
    );
}

export default PageHeader;

