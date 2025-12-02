// frontend/src/templates/weight-estimations/WeightEstimationDetailTemplate.js

import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import CustomTypography from '../../components/atoms/CustomTypography';
import LoadingState from '../../components/molecules/LoadingState';
import ErrorState from '../../components/molecules/ErrorState';
import WeightEstimationDetail from '../../components/organisms/WeightEstimationDetail';
import CustomButton from '../../components/atoms/CustomButton';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { useNavigate } from 'react-router-dom';

function WeightEstimationDetailTemplate({
    estimation,
    loading,
    error,
    apiBaseUrl
}) {
    const navigate = useNavigate();

    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                {/* Header con botón de regreso */}
                <Box sx={{ mb: 4 }}>
                    <CustomButton
                        startIcon={<ArrowBackIcon />}
                        onClick={() => navigate('/weight-estimations')}
                        sx={{ mb: 2 }}
                    >
                        Volver a Estimaciones
                    </CustomButton>
                    <CustomTypography customVariant="pageTitle" sx={{ mb: 1 }}>
                        {estimation ? 'Detalle de Estimación de Peso' : 'Estimación de Peso'}
                    </CustomTypography>
                </Box>

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && estimation && (
                        <Box sx={{ width: '100%' }}>
                            <WeightEstimationDetail 
                                estimation={estimation}
                                apiBaseUrl={apiBaseUrl}
                            />
                        </Box>
                    )}
                </LoadingState>
            </Container>
        </Box>
    );
}

export default WeightEstimationDetailTemplate;

