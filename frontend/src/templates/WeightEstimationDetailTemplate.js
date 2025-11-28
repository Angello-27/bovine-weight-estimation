// frontend/src/templates/WeightEstimationDetailTemplate.js

import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import CustomTypography from '../components/atoms/CustomTypography';
import LoadingState from '../components/molecules/LoadingState';
import ErrorState from '../components/molecules/ErrorState';
import PageHeader from '../components/molecules/PageHeader';
import WeightEstimationDetail from '../components/organisms/WeightEstimationDetail';

function WeightEstimationDetailTemplate({
    estimation,
    loading,
    error,
    apiBaseUrl
}) {
    return (
        <Grid component="section" py={12}>
            <Container>
                <PageHeader
                    title={estimation ? `Estimación de Peso` : 'Detalle de Estimación'}
                    description="Información completa de la estimación de peso"
                />

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && estimation && (
                        <WeightEstimationDetail 
                            estimation={estimation}
                            apiBaseUrl={apiBaseUrl}
                        />
                    )}
                </LoadingState>
            </Container>
        </Grid>
    );
}

export default WeightEstimationDetailTemplate;

