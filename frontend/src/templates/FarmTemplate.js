// frontend/src/templates/FarmTemplate.js

import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import CreateFarm from '../components/organisms/CreateFarm';
import FarmList from '../components/organisms/FarmList';
import ActionButton from '../components/molecules/ActionButton';
import LoadingState from '../components/molecules/LoadingState';
import ErrorState from '../components/molecules/ErrorState';
import PageHeader from '../components/molecules/PageHeader';
import AddIcon from '@mui/icons-material/Add';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import { userToComboBox } from '../utils/transformers/userToComboBox.js';

function FarmTemplate({ items, loading, error, owners, formData, handleChange, handleSubmit, handleComboBoxChange, showForm, onCloseForm, onCreateClick, onEditClick, onDeleteClick }) {
    const transformedOwners = userToComboBox(owners?.items || []);

    return (
        <Grid component="section" py={12}>
            <Container>
                <PageHeader
                    title="Fincas"
                    description="Gestión de fincas del sistema"
                    action={
                        <ActionButton
                            icon={<AddIcon />}
                            label="Crear Finca"
                            onClick={onCreateClick}
                        />
                    }
                />

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && (
                        <Grid container spacing={3}>
                            <Grid item xs={12}>
                                <FarmList
                                    items={items}
                                    owners={owners?.items || []}
                                    onEditClick={onEditClick}
                                    onDeleteClick={onDeleteClick}
                                />
                            </Grid>
                        </Grid>
                    )}
                </LoadingState>

                {/* Dialog para crear/editar finca */}
                <Dialog open={showForm} onClose={onCloseForm} maxWidth="md" fullWidth>
                    <DialogTitle>{formData.id ? 'Editar Finca' : 'Crear Finca'}</DialogTitle>
                    <DialogContent>
                        <Grid container item xs={12} sx={{ mt: 2 }}>
                            <CreateFarm
                                formData={formData}
                                onInputChange={handleChange}
                                onSubmit={(e) => {
                                    handleSubmit(e);
                                    onCloseForm();
                                }}
                                owners={transformedOwners}
                                onComboBoxChange={handleComboBoxChange}
                            />
                        </Grid>
                    </DialogContent>
                </Dialog>
            </Container>
        </Grid>
    );
}

export default FarmTemplate;

