// frontend/src/templates/WeightEstimationFromWebTemplate.js

import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import CustomTypography from '../components/atoms/CustomTypography';
import LoadingState from '../components/molecules/LoadingState';
import ErrorState from '../components/molecules/ErrorState';
import BreedSelector from '../components/molecules/BreedSelector';
import CattleListByBreed from '../components/molecules/CattleListByBreed';
import ImageUploader from '../components/molecules/ImageUploader';
import EstimationResult from '../components/molecules/EstimationResult';
import CustomButton from '../components/atoms/CustomButton';
import Card from '../components/atoms/Card';
import { breedToComboBox } from '../utils/transformers/breedToComboBox';

function WeightEstimationFromWebTemplate({
    formData,
    estimationResult,
    loading,
    error,
    imagePreview,
    selectedBreed,
    filteredCattle,
    onBreedSelect,
    onCattleSelect,
    onImageChange,
    onEstimate,
    onSaveEstimation,
    onReset
}) {
    const breeds = breedToComboBox();
    const breedLabel = breeds.find(b => b.id === selectedBreed)?.label || '';

    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                {/* Header */}
                <Box sx={{ mb: 4 }}>
                    <CustomTypography customVariant="pageTitle" sx={{ mb: 1 }}>
                        Estimar Peso desde Imagen
                    </CustomTypography>
                    <CustomTypography variant="body1" color="text.secondary">
                        Selecciona la raza del animal, elige un animal registrado (opcional) y sube una imagen para estimar su peso usando inteligencia artificial
                    </CustomTypography>
                </Box>

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && (
                        <Grid container spacing={3}>
                            {/* Paso 1: Selección de Raza */}
                            <Grid item xs={12}>
                                <Card sx={{ p: 3 }}>
                                    <BreedSelector
                                        selectedBreed={selectedBreed}
                                        onBreedSelect={onBreedSelect}
                                    />
                                </Card>
                            </Grid>

                            {/* Paso 2 y 3: Layout de dos columnas cuando hay raza seleccionada */}
                            {selectedBreed && (
                                <>
                                    {/* Columna izquierda: Lista de Ganado */}
                                    <Grid item xs={12} md={4}>
                                        <Card
                                            sx={{
                                                p: 3,
                                                height: '100%',
                                                minHeight: { md: '500px' },
                                                maxHeight: { md: 'calc(100vh - 200px)' },
                                                position: 'sticky',
                                                top: 20,
                                                display: 'flex',
                                                flexDirection: 'column',
                                            }}
                                        >
                                            <CattleListByBreed
                                                cattle={filteredCattle}
                                                selectedCattleId={formData.cattle_id}
                                                onCattleSelect={onCattleSelect}
                                                breed={breedLabel}
                                            />
                                        </Card>
                                    </Grid>

                                    {/* Columna derecha: Subida de Imagen y Resultado */}
                                    <Grid item xs={12} md={8}>
                                        <Grid container spacing={3}>
                                            {/* Área de subida de imagen */}
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
                                                    {formData.image && (
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
                                        </Grid>
                                    </Grid>
                                </>
                            )}
                        </Grid>
                    )}
                </LoadingState>
            </Container>
        </Box>
    );
}

export default WeightEstimationFromWebTemplate;

