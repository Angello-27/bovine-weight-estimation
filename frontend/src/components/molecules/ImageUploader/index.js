// frontend/src/components/molecules/ImageUploader/index.js

import Box from "@mui/material/Box";
import CustomButton from '../../atoms/CustomButton';
import CustomTypography from '../../atoms/CustomTypography';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { useTheme } from "@mui/material/styles";

function ImageUploader({ imagePreview, onImageChange, loading, showTitle = true }) {
    const theme = useTheme();

    return (
        <Box>
            {showTitle && (
                <CustomTypography variant="h6" mb={2}>
                    Subir Imagen
                </CustomTypography>
            )}

            <Box
                sx={{
                    position: 'relative',
                    border: '3px dashed',
                    borderColor: imagePreview ? theme.palette.success.main : theme.palette.primary.main,
                    borderRadius: 3,
                    p: 3,
                    textAlign: 'center',
                    cursor: loading ? 'not-allowed' : 'pointer',
                    opacity: loading ? 0.6 : 1,
                    backgroundColor: imagePreview
                        ? `${theme.palette.success.main}05`
                        : `${theme.palette.primary.main}05`,
                    transition: 'all 0.3s ease',
                    '&:hover': {
                        borderColor: loading
                            ? (imagePreview ? theme.palette.success.main : theme.palette.primary.main)
                            : (imagePreview ? theme.palette.success.dark : theme.palette.primary.dark),
                        backgroundColor: loading
                            ? (imagePreview ? `${theme.palette.success.main}05` : `${theme.palette.primary.main}05`)
                            : (imagePreview ? `${theme.palette.success.main}10` : `${theme.palette.primary.main}10`),
                        transform: loading ? 'none' : 'scale(1.01)',
                    }
                }}
                onClick={() => !loading && document.getElementById('image-upload').click()}
            >
                <input
                    id="image-upload"
                    type="file"
                    accept="image/jpeg,image/jpg,image/png,image/webp"
                    onChange={onImageChange}
                    style={{ display: 'none' }}
                    disabled={loading}
                />

                {imagePreview ? (
                    <Box>
                        <img
                            src={imagePreview}
                            alt="Preview"
                            style={{
                                maxWidth: '100%',
                                maxHeight: '400px',
                                borderRadius: '12px',
                                boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
                                objectFit: 'contain',
                            }}
                        />
                        <CustomTypography
                            variant="caption"
                            color="text.secondary"
                            sx={{
                                display: 'block',
                                mt: 2,
                                opacity: 0.8,
                            }}
                        >
                            Click para cambiar imagen
                        </CustomTypography>
                    </Box>
                ) : (
                    <Box>
                        <Box
                            sx={{
                                display: 'inline-flex',
                                p: 3,
                                borderRadius: '50%',
                                backgroundColor: `${theme.palette.primary.main}15`,
                                mb: 2,
                            }}
                        >
                            <CloudUploadIcon
                                sx={{
                                    fontSize: 56,
                                    color: theme.palette.primary.main,
                                }}
                            />
                        </Box>

                        <CustomTypography
                            variant="h6"
                            sx={{
                                mb: 1,
                                color: theme.palette.text.primary,
                                fontWeight: 600,
                            }}
                        >
                            Arrastra tu imagen aquí
                        </CustomTypography>

                        <CustomTypography
                            variant="body2"
                            color="text.secondary"
                            sx={{ mb: 3 }}
                        >
                            o haz click para seleccionar
                        </CustomTypography>

                        <CustomButton
                            variant="contained"
                            component="span"
                            disabled={loading}
                            size="large"
                            startIcon={<CloudUploadIcon />}
                            sx={{
                                px: 4,
                                py: 1.5,
                                borderRadius: 2,
                            }}
                        >
                            Seleccionar Imagen
                        </CustomButton>

                        <Box
                            sx={{
                                mt: 3,
                                pt: 2,
                                borderTop: `1px solid ${theme.palette.grey[200]}`,
                            }}
                        >
                            <CustomTypography
                                variant="caption"
                                color="text.secondary"
                                sx={{ display: 'block' }}
                            >
                                <strong>Formatos aceptados:</strong> JPG, PNG, WEBP
                            </CustomTypography>
                            <CustomTypography
                                variant="caption"
                                color="text.secondary"
                                sx={{ display: 'block', mt: 0.5 }}
                            >
                                <strong>Tamaño máximo:</strong> 10MB
                            </CustomTypography>
                        </Box>
                    </Box>
                )}
            </Box>
        </Box>
    );
}

export default ImageUploader;
