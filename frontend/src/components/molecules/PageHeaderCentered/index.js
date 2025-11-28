// frontend/src/components/molecules/PageHeaderCentered/index.js

import Grid from "@mui/material/Grid";
import CustomTypography from '../../atoms/CustomTypography';

/**
 * PageHeaderCentered molecule - Header centrado de página
 * @param {string} title - Título de la página
 * @param {string} description - Descripción opcional
 */
function PageHeaderCentered({ title, description }) {
    return (
        <Grid container item justifyContent="center" xs={12} mb={4} textAlign="center">
            <CustomTypography variant="h3" mb={description ? 2 : 0}>
                {title}
            </CustomTypography>
            {description && (
                <CustomTypography variant="body1" color="text.secondary">
                    {description}
                </CustomTypography>
            )}
        </Grid>
    );
}

export default PageHeaderCentered;

