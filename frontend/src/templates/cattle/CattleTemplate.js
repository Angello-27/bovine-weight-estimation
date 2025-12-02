// frontend/src/templates/cattle/CattleTemplate.js

import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import CreateCattle from '../../components/organisms/CreateCattle';
import CattleList from '../../components/organisms/CattleList';
import CustomButton from '../../components/atoms/CustomButton';
import CustomTypography from '../../components/atoms/CustomTypography';
import LoadingState from '../../components/molecules/LoadingState';
import ErrorState from '../../components/molecules/ErrorState';
import ConfirmDialog from '../../components/molecules/ConfirmDialog';
import AddIcon from '@mui/icons-material/Add';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';

function CattleTemplate({ 
    items, 
    loading, 
    error, 
    formData,
    formErrors = {},
    handleChange, 
    handleSubmit, 
    handleComboBoxChange, 
    showForm, 
    onCloseForm, 
    onCreateClick, 
    onEditClick, 
    onDeleteClick,
    onViewClick,
    pagination,
    onPageChange,
    onPageSizeChange,
    showDeleteDialog,
    deleteItem,
    onCloseDeleteDialog,
    onConfirmDelete
}) {
    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                {/* Header con botón de acción */}
                <Box sx={{ mb: 4 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                        <Box sx={{ flex: 1 }}>
                            <CustomTypography customVariant="pageTitle" sx={{ mb: 1 }}>
                                Animales
                            </CustomTypography>
                        </Box>
                        <CustomButton
                            variant="contained"
                            startIcon={<AddIcon />}
                            onClick={onCreateClick}
                            sx={{ ml: 3 }}
                        >
                            Registrar Animal
                        </CustomButton>
                    </Box>
                </Box>

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && (
                        <Box sx={{ width: '100%' }}>
                            <CattleList
                                items={items}
                                onViewClick={onViewClick}
                                onEditClick={onEditClick}
                                onDeleteClick={onDeleteClick}
                                pagination={pagination}
                                onPageChange={onPageChange}
                                onPageSizeChange={onPageSizeChange}
                            />
                        </Box>
                    )}
                </LoadingState>

                {/* Dialog para crear/editar animal */}
                <Dialog 
                    open={showForm} 
                    onClose={onCloseForm} 
                    maxWidth="md" 
                    fullWidth
                    PaperProps={{
                        sx: {
                            borderRadius: 2,
                        }
                    }}
                >
                    <DialogTitle sx={{ pb: 3, pt: 4, px: 3 }}>
                        {formData?.id ? 'Editar Animal' : 'Registrar Animal'}
                    </DialogTitle>
                    <DialogContent sx={{ px: 3, pb: 3 }}>
                        <CreateCattle
                            formData={formData}
                            errors={formErrors}
                            onInputChange={handleChange}
                            onSubmit={(e) => {
                                handleSubmit(e);
                                // El formulario se cierra automáticamente solo si el submit es exitoso
                            }}
                            onComboBoxChange={handleComboBoxChange}
                        />
                    </DialogContent>
                </Dialog>

                {/* Dialog de confirmación para eliminar */}
                <ConfirmDialog
                    open={showDeleteDialog || false}
                    onClose={onCloseDeleteDialog}
                    onConfirm={onConfirmDelete}
                    title="Eliminar Animal"
                    message={deleteItem ? `¿Estás seguro de que deseas eliminar el animal "${deleteItem.ear_tag || deleteItem.name || 'este animal'}"? Esta acción no se puede deshacer.` : ''}
                    confirmText="Eliminar"
                    cancelText="Cancelar"
                    confirmColor="error"
                />
            </Container>
        </Box>
    );
}

export default CattleTemplate;

