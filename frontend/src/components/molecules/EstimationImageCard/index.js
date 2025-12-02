// frontend/src/components/molecules/EstimationImageCard/index.js

import Box from "@mui/material/Box";
import Card from '../../atoms/Card';
import CustomTypography from '../../atoms/CustomTypography';
import ImageIcon from '@mui/icons-material/Image';
import PhotoCameraIcon from '@mui/icons-material/PhotoCamera';

/**
 * EstimationImageCard molecule - Muestra la imagen de la estimación con mejor diseño
 * @param {string} imagePath - Path de la imagen
 * @param {string} apiBaseUrl - URL base de la API (opcional)
 */
function EstimationImageCard({ imagePath, apiBaseUrl }) {
    // Construir URL completa de la imagen
    const imageUrl = imagePath 
        ? (imagePath.startsWith('http') 
            ? imagePath 
            : `${apiBaseUrl || import.meta.env.REACT_APP_API_URL || ''}${imagePath.startsWith('/') ? '' : '/'}${imagePath}`)
        : null;

    return (
        <Card sx={{ p: 3 }}>
            <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                <PhotoCameraIcon />
                Imagen de la Estimación
            </CustomTypography>
            
            {imageUrl ? (
                <Box
                    sx={{
                        width: '100%',
                        borderRadius: 2,
                        overflow: 'hidden',
                        bgcolor: 'action.hover',
                        position: 'relative',
                        '&:hover': {
                            boxShadow: 4
                        },
                        transition: 'box-shadow 0.3s ease'
                    }}
                >
                    <img
                        src={imageUrl}
                        alt="Imagen de la estimación de peso"
                        style={{
                            width: '100%',
                            height: 'auto',
                            display: 'block'
                        }}
                        onError={(e) => {
                            e.target.style.display = 'none';
                            if (e.target.nextSibling) {
                                e.target.nextSibling.style.display = 'flex';
                            }
                        }}
                    />
                    <Box
                        sx={{
                            display: 'none',
                            width: '100%',
                            minHeight: '300px',
                            alignItems: 'center',
                            justifyContent: 'center',
                            flexDirection: 'column',
                            p: 4,
                            bgcolor: 'action.hover'
                        }}
                    >
                        <ImageIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                        <CustomTypography variant="body2" color="text.secondary">
                            Error al cargar la imagen
                        </CustomTypography>
                    </Box>
                </Box>
            ) : (
                <Box sx={{ 
                    textAlign: 'center', 
                    py: 6,
                    bgcolor: 'action.hover',
                    borderRadius: 2
                }}>
                    <ImageIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                    <CustomTypography variant="body2" color="text.secondary">
                        No hay imagen disponible para esta estimación
                    </CustomTypography>
                </Box>
            )}
        </Card>
    );
}

export default EstimationImageCard;

