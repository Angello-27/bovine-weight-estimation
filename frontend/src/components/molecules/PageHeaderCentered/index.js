// frontend/src/components/molecules/PageHeaderCentered/index.js

import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';

/**
 * PageHeaderCentered molecule - Header centrado de página
 * @param {string} title - Título de la página
 * @param {string} description - Descripción opcional
 */
function PageHeaderCentered({ title, description }) {
    return (
        <Box 
            sx={{ 
                textAlign: 'center',
                mb: 4,
                py: 2
            }}
        >
            <CustomTypography 
                customVariant="pageTitle"
                sx={{ 
                    mb: description ? 2 : 0
                }}
            >
                {title}
            </CustomTypography>
            {description && (
                <CustomTypography 
                    customVariant="pageDescription"
                >
                    {description}
                </CustomTypography>
            )}
        </Box>
    );
}

export default PageHeaderCentered;

