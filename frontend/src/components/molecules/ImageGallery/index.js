// frontend/src/components/molecules/ImageGallery/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import EmptyState from '../EmptyState';
import ImageIcon from '@mui/icons-material/Image';
import ExpandedImageDialog from '../../atoms/ExpandedImageDialog';
import { useState } from 'react';
import { getImageUrl } from '../../../utils/getImageUrl';

/**
 * ImageGallery molecule - Galería de imágenes con vista ampliada
 * @param {Array} images - Array de objetos { id, url, title?, date? }
 * @param {string} apiBaseUrl - URL base de la API (opcional)
 */
function ImageGallery({ images, apiBaseUrl }) {
    const [selectedImage, setSelectedImage] = useState(null);
    const [openDialog, setOpenDialog] = useState(false);

    if (!images || images.length === 0) {
        return (
            <Card>
                <EmptyState message="No hay imágenes disponibles para este animal." />
            </Card>
        );
    }

    const handleImageClick = (image) => {
        setSelectedImage(image);
        setOpenDialog(true);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
        setSelectedImage(null);
    };

    // Usar la función utilitaria para construir URLs de imágenes
    const buildImageUrl = (imagePath) => {
        return getImageUrl(imagePath);
    };

    return (
        <>
            <Card>
                <Box display="flex" alignItems="center" gap={1} mb={3}>
                    <ImageIcon color="primary" />
                    <CustomTypography variant="h6">
                        Galería de Fotos ({images.length})
                    </CustomTypography>
                </Box>
                
                <Grid container spacing={2}>
                    {images.map((image, index) => {
                        const imageUrl = buildImageUrl(image.url);
                        if (!imageUrl) return null;

                        return (
                            <Grid item xs={6} sm={4} md={3} key={image.id || index}>
                                <Box
                                    sx={{
                                        position: 'relative',
                                        width: '100%',
                                        paddingTop: '100%', // Aspect ratio 1:1
                                        borderRadius: 2,
                                        overflow: 'hidden',
                                        cursor: 'pointer',
                                        bgcolor: 'action.hover',
                                        '&:hover': {
                                            opacity: 0.8,
                                            transform: 'scale(1.02)',
                                            transition: 'all 0.2s'
                                        }
                                    }}
                                    onClick={() => handleImageClick(image)}
                                >
                                    <img
                                        src={imageUrl}
                                        alt={image.title || `Imagen ${index + 1}`}
                                        style={{
                                            position: 'absolute',
                                            top: 0,
                                            left: 0,
                                            width: '100%',
                                            height: '100%',
                                            objectFit: 'cover'
                                        }}
                                        onError={(e) => {
                                            e.target.style.display = 'none';
                                        }}
                                    />
                                    {image.date && (
                                        <Box
                                            sx={{
                                                position: 'absolute',
                                                bottom: 0,
                                                left: 0,
                                                right: 0,
                                                bgcolor: 'rgba(0, 0, 0, 0.6)',
                                                color: 'white',
                                                p: 0.5,
                                                fontSize: '1.05rem'
                                            }}
                                        >
                                            {new Date(image.date).toLocaleDateString('es-ES')}
                                        </Box>
                                    )}
                                </Box>
                            </Grid>
                        );
                    })}
                </Grid>
            </Card>

            {/* Dialog para vista ampliada */}
            <ExpandedImageDialog
                open={openDialog}
                onClose={handleCloseDialog}
                image={selectedImage}
            />
        </>
    );
}

export default ImageGallery;

