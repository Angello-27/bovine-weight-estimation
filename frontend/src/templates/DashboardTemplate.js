import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import CustomTypography from '../components/atoms/CustomTypography';
import StatisticsCards from '../components/organisms/StatisticsCards';
import LoadingState from '../components/molecules/LoadingState';
import ErrorState from '../components/molecules/ErrorState';
import PageHeaderCentered from '../components/molecules/PageHeaderCentered';
import Card from '../components/atoms/Card';

function DashboardTemplate({ stats, loading, error }) {
    return (
        <Grid component="section" py={12}>
            <Container>
                <PageHeaderCentered
                    title="Dashboard"
                    description="Panel de control y estadísticas del sistema"
                />

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && (
                        <Grid container spacing={3} mt={2}>
                            <Grid item xs={12}>
                                <StatisticsCards stats={stats} />
                            </Grid>
                        </Grid>
                    )}
                </LoadingState>

                {/* TODO: Agregar gráficos cuando se creen */}
                {!loading && !error && (
                    <Grid container spacing={3} mt={2}>
                        <Grid item xs={12}>
                            <Card sx={{ minHeight: 300 }}>
                                <CustomTypography variant="h6" mb={2}>
                                    Gráficos (Próximamente)
                                </CustomTypography>
                                <CustomTypography variant="body2" color="text.secondary">
                                    Aquí se mostrarán gráficos de evolución de peso, distribución por raza, etc.
                                </CustomTypography>
                            </Card>
                        </Grid>
                    </Grid>
                )}
            </Container>
        </Grid>
    );
}

export default DashboardTemplate;

