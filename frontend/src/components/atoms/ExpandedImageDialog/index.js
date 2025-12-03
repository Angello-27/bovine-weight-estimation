// frontend/src/components/atoms/ExpandedImageDialog/index.js

import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import IconButton from '@mui/material/IconButton';
import Box from '@mui/material/Box';
import CloseIcon from '@mui/icons-material/Close';
import CustomTypography from '../CustomTypography';
import { getImageUrl } from '../../../utils/getImageUrl';

/**
 * ExpandedImageDialog atom - Diálogo para mostrar imagen ampliada con información sobrepuesta
 * @param {boolean} open - Estado de apertura del diálogo
 * @param {Function} onClose - Función para cerrar el diálogo
 * @param {Object} image - Objeto con { url, title?, date? }
 */
function ExpandedImageDialog({ open, onClose, image }) {
    if (!image) return null;

    const imageUrl = getImageUrl(image.url);
    const hasInfo = image.title || image.date;

    return (
        <Dialog
            open={open}
            onClose={onClose}
            maxWidth="lg"
            fullWidth
        >
            <DialogContent sx={{ p: 0, position: 'relative' }}>
                {/* Botón de cerrar */}
                <IconButton
                    onClick={onClose}
                    sx={{
                        position: 'absolute',
                        top: 8,
                        right: 8,
                        padding: 1.5,
                        zIndex: 2,
                        bgcolor: 'rgba(0, 0, 0, 0.5)',
                        color: 'white',
                        '&:hover': {
                            bgcolor: 'rgba(0, 0, 0, 0.6)'
                        }
                    }}
                >
                    <CloseIcon />
                </IconButton>

                {/* Imagen */}
                <Box sx={{ position: 'relative', width: '100%' }}>
                    <img
                        src={imageUrl}
                        alt={image.title || 'Imagen ampliada'}
                        style={{
                            width: '100%',
                            height: 'auto',
                            display: 'block'
                        }}
                    />

                    {/* Información sobrepuesta en la parte inferior */}
                    {hasInfo && (
                        <Box
                            sx={{
                                position: 'absolute',
                                bottom: 0,
                                left: 0,
                                right: 0,
                                bgcolor: 'rgba(0, 0, 0, 0.7)',
                                color: 'white',
                                p: 2,
                                zIndex: 1
                            }}
                        >
                            {image.title && (
                                <CustomTypography 
                                    variant="h6" 
                                    sx={{ 
                                        fontWeight: 'bold',
                                        mb: image.date ? 1 : 0,
                                        color: 'white'
                                    }}
                                >
                                    {image.title}
                                </CustomTypography>
                            )}
                            {image.date && (
                                <CustomTypography 
                                    variant="body1" 
                                    sx={{ 
                                        color: 'rgba(255, 255, 255, 0.9)'
                                    }}
                                >
                                    Fecha: {new Date(image.date).toLocaleString('es-ES')}
                                </CustomTypography>
                            )}
                        </Box>
                    )}
                </Box>
            </DialogContent>
        </Dialog>
    );
}

export default ExpandedImageDialog;

