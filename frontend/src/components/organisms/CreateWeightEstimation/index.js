// frontend/src/components/organisms/CreateWeightEstimation/index.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import CustomButton from '../../atoms/CustomButton';
import ImageUploader from '../../molecules/ImageUploader';
import EstimationOptions from '../../molecules/EstimationOptions';
import EstimationResult from '../../molecules/EstimationResult';
import EstimationError from '../../molecules/EstimationError';

function CreateWeightEstimation({
    formData,
    estimationResult,
    loading,
    error,
    imagePreview,
    cattleOptions,
    onImageChange,
    onChange,
    onComboBoxChange,
    onEstimate,
    onSaveEstimation,
    onReset
}) {
    return (
        <Grid container spacing={3}>
            {/* Sección de Upload */}
            <Grid item xs={12} md={6}>
                <ImageUploader
                    imagePreview={imagePreview}
                    onImageChange={onImageChange}
                    loading={loading}
                />
                
                {formData.image && (
                    <Box mt={2}>
                        <CustomButton
                            variant="contained"
                            fullWidth
                            onClick={onEstimate}
                            disabled={loading}
                        >
                            {loading ? 'Procesando...' : 'Estimar Peso'}
                        </CustomButton>
                    </Box>
                )}
            </Grid>

            {/* Sección de Opciones */}
            <Grid item xs={12} md={6}>
                <EstimationOptions
                    cattleOptions={cattleOptions}
                    formData={formData}
                    onComboBoxChange={onComboBoxChange}
                />
            </Grid>

            {/* Resultado de Estimación */}
            {estimationResult && (
                <Grid item xs={12}>
                    <EstimationResult
                        result={estimationResult}
                        loading={loading}
                        onSave={onSaveEstimation}
                        onReset={onReset}
                    />
                </Grid>
            )}

            {/* Error */}
            {error && (
                <Grid item xs={12}>
                    <EstimationError error={error} />
                </Grid>
            )}
        </Grid>
    );
}

export default CreateWeightEstimation;

