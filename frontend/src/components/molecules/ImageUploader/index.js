// frontend/src/components/molecules/ImageUploader/index.js

import Box from "@mui/material/Box";
import CustomButton from '../../atoms/CustomButton';
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

function ImageUploader({ imagePreview, onImageChange, loading }) {
    return (
        <Card>
            <CustomTypography variant="h6" mb={2}>
                Subir Imagen
            </CustomTypography>
            
            <Box
                sx={{
                    border: '2px dashed',
                    borderColor: 'primary.main',
                    borderRadius: 2,
                    p: 3,
                    textAlign: 'center',
                    cursor: loading ? 'not-allowed' : 'pointer',
                    opacity: loading ? 0.6 : 1,
                    '&:hover': {
                        borderColor: loading ? 'primary.main' : 'primary.dark',
                        bgcolor: loading ? 'transparent' : 'action.hover'
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
                                maxHeight: '300px',
                                borderRadius: '8px',
                                marginBottom: '16px'
                            }}
                        />
                        <CustomTypography variant="body2" color="text.secondary">
                            Click para cambiar imagen
                        </CustomTypography>
                    </Box>
                ) : (
                    <Box>
                        <Box display="flex" alignItems="center" justifyContent="center" gap={1} mb={1}>
                            <CloudUploadIcon color="primary" />
                            <CustomTypography variant="body1">
                                Arrastra imagen aquí o
                            </CustomTypography>
                        </Box>
                        <CustomButton variant="outlined" component="span" disabled={loading}>
                            Seleccionar archivo
                        </CustomButton>
                        <CustomTypography variant="body2" color="text.secondary" mt={2}>
                            Formatos: JPG, PNG, WEBP<br />
                            Tamaño máximo: 10MB
                        </CustomTypography>
                    </Box>
                )}
            </Box>
        </Card>
    );
}

export default ImageUploader;

