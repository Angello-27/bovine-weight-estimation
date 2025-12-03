// frontend/src/components/molecules/EstimationImage/index.js

import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import ImageIcon from '@mui/icons-material/Image';
import { getImageUrl } from '../../../utils/getImageUrl';

/**
 * EstimationImage molecule - Muestra la imagen de la estimación
 * @param {string} imagePath - Path de la imagen
 * @param {string} apiBaseUrl - URL base de la API (opcional)
 */
function EstimationImage({ imagePath, apiBaseUrl }) {
    if (!imagePath) {
        return (
            <Card>
                <Box textAlign="center" p={4}>
                    <ImageIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                    <CustomTypography variant="body2" color="text.secondary">
                        No hay imagen disponible
                    </CustomTypography>
                </Box>
            </Card>
        );
    }

    // Usar la función utilitaria para construir URLs de imágenes
    const imageUrl = getImageUrl(imagePath);

    return (
        <Card>
            <CustomTypography variant="h6" mb={2}>
                Imagen de la Estimación
            </CustomTypography>
            <Box
                sx={{
                    width: '100%',
                    borderRadius: 2,
                    overflow: 'hidden',
                    bgcolor: 'action.hover'
                }}
            >
                <img
                    src={imageUrl}
                    alt="Estimación de peso"
                    style={{
                        width: '100%',
                        height: 'auto',
                        display: 'block'
                    }}
                    onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'flex';
                    }}
                />
                <Box
                    sx={{
                        display: 'none',
                        width: '100%',
                        minHeight: '200px',
                        alignItems: 'center',
                        justifyContent: 'center',
                        flexDirection: 'column',
                        p: 4
                    }}
                >
                    <ImageIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                    <CustomTypography variant="body2" color="text.secondary">
                        Error al cargar la imagen
                    </CustomTypography>
                </Box>
            </Box>
        </Card>
    );
}

export default EstimationImage;

