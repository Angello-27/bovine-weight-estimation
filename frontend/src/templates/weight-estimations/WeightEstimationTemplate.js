// frontend/src/templates/weight-estimations/WeightEstimationTemplate.js

import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import WeightEstimationList from '../../components/organisms/WeightEstimationList';
import CustomButton from '../../components/atoms/CustomButton';
import CustomTypography from '../../components/atoms/CustomTypography';
import LoadingState from '../../components/molecules/LoadingState';
import ErrorState from '../../components/molecules/ErrorState';
import ConfirmDialog from '../../components/molecules/ConfirmDialog';
import AddIcon from '@mui/icons-material/Add';
import RefreshIcon from '@mui/icons-material/Refresh';

function WeightEstimationTemplate({ 
    items, 
    loading, 
    error, 
    onViewClick,
    onDeleteClick,
    onEstimateClick,
    pagination,
    onPageChange,
    onPageSizeChange,
    showDeleteDialog,
    deleteItem,
    onCloseDeleteDialog,
    onConfirmDelete,
    refreshData
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
                        <Box sx={{ display: 'flex', gap: 2 }}>
                            {refreshData && (
                                <CustomButton
                                    variant="outlined"
                                    startIcon={<RefreshIcon />}
                                    onClick={refreshData}
                                    disabled={loading}
                                    sx={{ ml: 2 }}
                                >
                                    Actualizar
                                </CustomButton>
                            )}
                            <CustomButton
                                variant="contained"
                                startIcon={<AddIcon />}
                                onClick={onEstimateClick}
                            >
                                Estimar Peso
                            </CustomButton>
                        </Box>
                    </Box>
                </Box>

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && (
                        <Box sx={{ width: '100%' }}>
                            <WeightEstimationList 
                                items={items} 
                                onViewClick={onViewClick}
                                onDeleteClick={onDeleteClick}
                                pagination={pagination}
                                onPageChange={onPageChange}
                                onPageSizeChange={onPageSizeChange}
                            />
                        </Box>
                    )}
                </LoadingState>

                {/* Dialog de confirmación para eliminar */}
                <ConfirmDialog
                    open={showDeleteDialog || false}
                    onClose={onCloseDeleteDialog}
                    onConfirm={onConfirmDelete}
                    title="Eliminar Estimación de Peso"
                    message={
                        deleteItem?.estimation
                            ? `¿Estás seguro de que deseas eliminar esta estimación de peso (${deleteItem.estimation.estimated_weight_kg?.toFixed(1) || 'N/A'} kg)? Esta acción no se puede deshacer.`
                            : '¿Estás seguro de que deseas eliminar esta estimación de peso? Esta acción no se puede deshacer.'
                    }
                    confirmText="Eliminar"
                    cancelText="Cancelar"
                    confirmColor="error"
                />
            </Container>
        </Box>
    );
}

export default WeightEstimationTemplate;

