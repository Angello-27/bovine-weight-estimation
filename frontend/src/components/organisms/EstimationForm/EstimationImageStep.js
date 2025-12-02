// frontend/src/components/organisms/EstimationForm/EstimationImageStep.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Card from '../../atoms/Card';
import CustomTypography from '../../atoms/CustomTypography';
import CustomButton from '../../atoms/CustomButton';
import ImageUploader from '../../molecules/ImageUploader';

function EstimationImageStep({ 
    imagePreview, 
    onImageChange, 
    loading, 
    hasImage, 
    onEstimate 
}) {
    return (
        <Grid item xs={12}>
            <Card sx={{ p: 3 }}>
                <CustomTypography variant="h6" sx={{ mb: 3 }}>
                    Subir Imagen del Animal
                </CustomTypography>
                <ImageUploader
                    imagePreview={imagePreview}
                    onImageChange={onImageChange}
                    loading={loading}
                    showTitle={false}
                />
                {hasImage && (
                    <Box mt={3}>
                        <CustomButton
                            variant="contained"
                            fullWidth
                            onClick={onEstimate}
                            disabled={loading}
                            size="large"
                        >
                            {loading ? 'Procesando...' : 'Estimar Peso'}
                        </CustomButton>
                    </Box>
                )}
            </Card>
        </Grid>
    );
}

export default EstimationImageStep;

