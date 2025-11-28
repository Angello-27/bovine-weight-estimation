import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import SyncStatusCard from '../components/organisms/SyncStatusCard';
import LoadingState from '../components/molecules/LoadingState';
import ErrorState from '../components/molecules/ErrorState';
import PageHeaderCentered from '../components/molecules/PageHeaderCentered';

function SyncStatusTemplate({ health, stats, loading, error }) {
    return (
        <Grid component="section" py={12}>
            <Container>
                <PageHeaderCentered
                    title="Estado de Sincronización"
                    description="Visualización del estado de sincronización con la app móvil"
                />

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && (
                        <Grid container spacing={3} mt={2}>
                            <Grid item xs={12}>
                                <SyncStatusCard health={health} stats={stats} />
                            </Grid>
                        </Grid>
                    )}
                </LoadingState>
            </Container>
        </Grid>
    );
}

export default SyncStatusTemplate;

