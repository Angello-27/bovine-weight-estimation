// frontend/src/templates/weight-estimations/WeightEstimationFromWebTemplate.js

import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import LoadingState from '../../components/molecules/LoadingState';
import ErrorState from '../../components/molecules/ErrorState';
import EstimationResult from '../../components/molecules/EstimationResult';
import {
    EstimationHeader,
    EstimationBreedStep,
    EstimationCattleStep,
    EstimationImageStep,
    EstimationWizard
} from '../../components/organisms/EstimationForm';
import { breedToComboBox } from '../../utils/transformers/breedToComboBox';

function WeightEstimationFromWebTemplate({
    formData,
    estimationResult,
    loading,
    error,
    imagePreview,
    selectedBreed,
    filteredCattle,
    cattleLoading,
    onBreedSelect,
    onCattleSelect,
    onImageChange,
    onEstimate,
    onSaveEstimation,
    onReset,
    onGoBack
}) {
    const breeds = breedToComboBox();
    const breedLabel = breeds.find(b => b.id === selectedBreed)?.label || '';
    
    // Determinar el paso activo del wizard
    // Paso 0: Seleccionar raza
    // Paso 1: Seleccionar animal y estimar (se muestra cuando hay raza seleccionada)
    const activeStep = selectedBreed ? 1 : 0;

    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                <EstimationHeader />

                <ErrorState error={error} />

                <LoadingState loading={loading || cattleLoading}>
                    {!error && (
                        <EstimationWizard 
                            activeStep={activeStep}
                            onStepClick={onGoBack}
                        >
                            {activeStep === 0 && (
                                <Grid container spacing={3}>
                                    <EstimationBreedStep
                                        selectedBreed={selectedBreed}
                                        onBreedSelect={onBreedSelect}
                                    />
                                </Grid>
                            )}

                            {activeStep === 1 && (
                                <Grid container spacing={3}>
                                    <EstimationCattleStep
                                        cattle={filteredCattle}
                                        selectedCattleId={formData.cattle_id}
                                        onCattleSelect={onCattleSelect}
                                        breedLabel={breedLabel}
                                    />

                                    <Grid item xs={12} md={8}>
                                        <Grid container spacing={3}>
                                            <EstimationImageStep
                                                imagePreview={imagePreview}
                                                onImageChange={onImageChange}
                                                loading={loading}
                                                hasImage={!!formData.image}
                                                onEstimate={onEstimate}
                                            />

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
                                        </Grid>
                                    </Grid>
                                </Grid>
                            )}
                        </EstimationWizard>
                    )}
                </LoadingState>
            </Container>
        </Box>
    );
}

export default WeightEstimationFromWebTemplate;

