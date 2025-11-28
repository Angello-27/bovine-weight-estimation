import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import CreateRole from '../components/organisms/CreateRole';
import RoleList from '../components/organisms/RoleList';
import ActionButton from '../components/molecules/ActionButton';
import LoadingState from '../components/molecules/LoadingState';
import ErrorState from '../components/molecules/ErrorState';
import PageHeader from '../components/molecules/PageHeader';
import AddIcon from '@mui/icons-material/Add';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';

function RoleTemplate({ items, loading, error, formData, handleChange, handleSubmit, showForm, onCloseForm, onCreateClick, onEditClick, onDeleteClick }) {

    return (
        <Grid component="section" py={12}>
            <Container>
                <PageHeader
                    title="Roles"
                    description="Gestión de roles del sistema"
                    action={
                        <ActionButton
                            icon={<AddIcon />}
                            label="Crear Rol"
                            onClick={handleCreateClick}
                        />
                    }
                />

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && (
                        <Grid container spacing={3}>
                            <Grid item xs={12}>
                                <RoleList
                                    items={items}
                                    onEditClick={onEditClick}
                                    onDeleteClick={onDeleteClick}
                                />
                            </Grid>
                        </Grid>
                    )}
                </LoadingState>

                {/* Dialog para crear/editar rol */}
                <Dialog open={showForm} onClose={onCloseForm} maxWidth="md" fullWidth>
                    <DialogTitle>{formData.id ? 'Editar Rol' : 'Crear Rol'}</DialogTitle>
                    <DialogContent>
                        <Grid container item xs={12} sx={{ mt: 2 }}>
                            <CreateRole
                                formData={formData}
                                onInputChange={handleChange}
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

export default RoleTemplate
