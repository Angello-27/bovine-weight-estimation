// frontend/src/components/organisms/EstimationForm/EstimationHeader.js

import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';

function EstimationHeader() {
    return (
        <Box sx={{ mb: 4 }}>
            <CustomTypography customVariant="pageTitle" sx={{ mb: 1 }}>
                Estimar Peso desde Imagen
            </CustomTypography>
            <CustomTypography variant="body1" color="text.secondary">
                Selecciona la raza del animal, elige un animal registrado (opcional) y sube una imagen para estimar su peso usando inteligencia artificial
            </CustomTypography>
        </Box>
    );
}

export default EstimationHeader;

