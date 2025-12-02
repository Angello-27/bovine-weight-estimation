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
    const getImageUrl = (path) => {
        if (!path) return null;
        
        // Si ya es una URL completa, retornarla tal cual
        if (path.startsWith('http://') || path.startsWith('https://')) {
            return path;
        }
        
        // Obtener URL base de la API
        const baseUrl = apiBaseUrl || import.meta.env.REACT_APP_API_URL || import.meta.env.VITE_API_URL || '';
        
        // Si el path ya incluye /uploads/, usarlo directamente
        // Si no, agregar /uploads/ antes del path
        let finalPath = path;
        if (!finalPath.startsWith('/uploads/') && !finalPath.startsWith('uploads/')) {
            // Si el path es relativo (ej: "brahman/animal_123.jpg"), agregar /uploads/
            if (!finalPath.startsWith('/')) {
                finalPath = `/uploads/${finalPath}`;
            } else {
                finalPath = `/uploads${finalPath}`;
            }
        } else if (finalPath.startsWith('uploads/')) {
            // Si empieza con "uploads/" sin barra inicial, agregarla
            finalPath = `/${finalPath}`;
        }
        
        // Construir URL completa
        const cleanBaseUrl = baseUrl.replace(/\/$/, ''); // Remover barra final si existe
        return `${cleanBaseUrl}${finalPath}`;
    };
    
    const imageUrl = getImageUrl(imagePath);

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

