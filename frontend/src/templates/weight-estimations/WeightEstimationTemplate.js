// frontend/src/templates/weight-estimations/WeightEstimationTemplate.js

import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import WeightEstimationList from '../../components/organisms/WeightEstimationList';
import CustomButton from '../../components/atoms/CustomButton';
import CustomTypography from '../../components/atoms/CustomTypography';
import LoadingState from '../../components/molecules/LoadingState';
import ErrorState from '../../components/molecules/ErrorState';
import AddIcon from '@mui/icons-material/Add';

function WeightEstimationTemplate({ 
    items, 
    loading, 
    error, 
    onViewClick, 
    onEstimateClick,
    pagination,
    onPageChange,
    onPageSizeChange
}) {
    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                {/* Header con botón de acción */}
                <Box sx={{ mb: 4 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Box sx={{ flex: 1 }}>
                            <CustomTypography customVariant="pageTitle" sx={{ mb: 1 }}>
                                Estimaciones de Peso
                            </CustomTypography>
                        </Box>
                        <CustomButton
                            variant="contained"
                            startIcon={<AddIcon />}
                            onClick={onEstimateClick}
                            sx={{ ml: 3 }}
                        >
                            Estimar Peso
                        </CustomButton>
                    </Box>
                </Box>

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && (
                        <Box sx={{ width: '100%' }}>
                            <WeightEstimationList 
                                items={items} 
                                onViewClick={onViewClick}
                                pagination={pagination}
                                onPageChange={onPageChange}
                                onPageSizeChange={onPageSizeChange}
                            />
                        </Box>
                    )}
                </LoadingState>
            </Container>
        </Box>
    );
}

export default WeightEstimationTemplate;

