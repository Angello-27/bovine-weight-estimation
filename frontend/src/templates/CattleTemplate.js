import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import CattleList from '../components/organisms/CattleList';
import CreateCattle from '../components/organisms/CreateCattle';
import ActionButton from '../components/molecules/ActionButton';
import LoadingState from '../components/molecules/LoadingState';
import ErrorState from '../components/molecules/ErrorState';
import PageHeader from '../components/molecules/PageHeader';
import AddIcon from '@mui/icons-material/Add';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';

function CattleTemplate({ items, loading, error, formData, handleChange, handleComboBoxChange, handleSubmit, showForm, onCloseForm, onViewClick, onCreateClick }) {
    return (
        <Grid component="section" py={12}>
            <Container>
                <PageHeader
                    title="Ganado"
                    description="Gestión de animales registrados"
                    action={
                        <ActionButton
                            icon={<AddIcon />}
                            label="Registrar Animal"
                            onClick={onCreateClick}
                        />
                    }
                />

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && (
                        <Grid container spacing={3}>
                            <Grid item xs={12}>
                                <CattleList items={items} onViewClick={onViewClick} />
                            </Grid>
                        </Grid>
                    )}
                </LoadingState>

                {/* Dialog para crear/editar animal */}
                <Dialog open={showForm} onClose={onCloseForm} maxWidth="md" fullWidth>
                    <DialogTitle>{formData?.id ? 'Editar Animal' : 'Registrar Animal'}</DialogTitle>
                    <DialogContent>
                        <Grid container item xs={12} sx={{ mt: 2 }}>
                            <CreateCattle
                                formData={formData}
                                onInputChange={handleChange}
                                onComboBoxChange={handleComboBoxChange}
                                onSubmit={(e) => {
                                    handleSubmit(e);
                                    onCloseForm();
                                }}
                            />
                        </Grid>
                    </DialogContent>
                </Dialog>
            </Container>
        </Grid>
    );
}

export default CattleTemplate;

