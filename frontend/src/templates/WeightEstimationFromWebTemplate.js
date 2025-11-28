// frontend/src/templates/WeightEstimationFromWebTemplate.js

import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import CreateWeightEstimation from '../components/organisms/CreateWeightEstimation';
import LoadingState from '../components/molecules/LoadingState';
import PageHeaderCentered from '../components/molecules/PageHeaderCentered';

function WeightEstimationFromWebTemplate({
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
        <Grid component="section" py={12}>
            <Container>
                <PageHeaderCentered
                    title="Estimar Peso desde Imagen"
                    description="Sube una imagen del animal para estimar su peso usando inteligencia artificial"
                />

                <LoadingState loading={loading}>
                    <CreateWeightEstimation
                        formData={formData}
                        estimationResult={estimationResult}
                        loading={loading}
                        error={error}
                        imagePreview={imagePreview}
                        cattleOptions={cattleOptions}
                        onImageChange={onImageChange}
                        onChange={onChange}
                        onComboBoxChange={onComboBoxChange}
                        onEstimate={onEstimate}
                        onSaveEstimation={onSaveEstimation}
                        onReset={onReset}
                    />
                </LoadingState>
            </Container>
        </Grid>
    );
}

export default WeightEstimationFromWebTemplate;

