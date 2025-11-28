// frontend/src/components/molecules/ImageGallery/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import EmptyState from '../EmptyState';
import ImageIcon from '@mui/icons-material/Image';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import { useState } from 'react';

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

    // Construir URL completa de la imagen
    const getImageUrl = (imagePath) => {
        if (!imagePath) return null;
        return imagePath.startsWith('http') 
            ? imagePath 
            : `${apiBaseUrl || import.meta.env.REACT_APP_API_URL || ''}${imagePath.startsWith('/') ? '' : '/'}${imagePath}`;
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
                        const imageUrl = getImageUrl(image.url);
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
                                                fontSize: '0.75rem'
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
            <Dialog
                open={openDialog}
                onClose={handleCloseDialog}
                maxWidth="lg"
                fullWidth
            >
                <DialogContent sx={{ p: 0, position: 'relative' }}>
                    <IconButton
                        onClick={handleCloseDialog}
                        sx={{
                            position: 'absolute',
                            top: 8,
                            right: 8,
                            zIndex: 1,
                            bgcolor: 'rgba(0, 0, 0, 0.5)',
                            color: 'white',
                            '&:hover': {
                                bgcolor: 'rgba(0, 0, 0, 0.7)'
                            }
                        }}
                    >
                        <CloseIcon />
                    </IconButton>
                    {selectedImage && (
                        <Box>
                            <img
                                src={getImageUrl(selectedImage.url)}
                                alt={selectedImage.title || 'Imagen ampliada'}
                                style={{
                                    width: '100%',
                                    height: 'auto',
                                    display: 'block'
                                }}
                            />
                            {(selectedImage.title || selectedImage.date) && (
                                <Box p={2} bgcolor="background.paper">
                                    {selectedImage.title && (
                                        <CustomTypography variant="h6" mb={1}>
                                            {selectedImage.title}
                                        </CustomTypography>
                                    )}
                                    {selectedImage.date && (
                                        <CustomTypography variant="body2" color="text.secondary">
                                            Fecha: {new Date(selectedImage.date).toLocaleString('es-ES')}
                                        </CustomTypography>
                                    )}
                                </Box>
                            )}
                        </Box>
                    )}
                </DialogContent>
            </Dialog>
        </>
    );
}

export default ImageGallery;

