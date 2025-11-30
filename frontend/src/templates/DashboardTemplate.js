import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import { useNavigate } from 'react-router-dom';
import CustomTypography from '../components/atoms/CustomTypography';
import CustomButton from '../components/atoms/CustomButton';
import StatisticsCards from '../components/organisms/StatisticsCards';
import LoadingState from '../components/molecules/LoadingState';
import ErrorState from '../components/molecules/ErrorState';
import PageHeaderCentered from '../components/molecules/PageHeaderCentered';
import Card from '../components/atoms/Card';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import PetsIcon from '@mui/icons-material/Pets';
import ScaleIcon from '@mui/icons-material/Scale';
import DescriptionIcon from '@mui/icons-material/Description';

function DashboardTemplate({ stats, loading, error }) {
    const navigate = useNavigate();

    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                <PageHeaderCentered
                    title="Dashboard"
                    description="Panel de control y estadísticas del sistema"
                />

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && (
                        <>
                            {/* Tarjetas de estadísticas */}
                            <Grid container spacing={3} mt={2}>
                                <Grid item xs={12}>
                                    <StatisticsCards stats={stats} />
                                </Grid>
                            </Grid>

                            {/* Accesos directos rápidos */}
                            {!loading && (
                                <Grid container spacing={3} mt={4}>
                                    <Grid item xs={12}>
                                        <Card sx={{ p: 3 }}>
                                            <CustomTypography variant="h6" mb={3}>
                                                Accesos Directos
                                            </CustomTypography>
                                            <Grid container spacing={2}>
                                                <Grid item xs={12} sm={6} md={3}>
                                                    <CustomButton
                                                        fullWidth
                                                        variant="contained"
                                                        startIcon={<AddCircleIcon />}
                                                        onClick={() => navigate('/weight-estimations/estimate')}
                                                    >
                                                        Estimar Peso
                                                    </CustomButton>
                                                </Grid>
                                                <Grid item xs={12} sm={6} md={3}>
                                                    <CustomButton
                                                        fullWidth
                                                        variant="outlined"
                                                        startIcon={<PetsIcon />}
                                                        onClick={() => navigate('/cattle')}
                                                    >
                                                        Ver Ganado
                                                    </CustomButton>
                                                </Grid>
                                                <Grid item xs={12} sm={6} md={3}>
                                                    <CustomButton
                                                        fullWidth
                                                        variant="outlined"
                                                        startIcon={<ScaleIcon />}
                                                        onClick={() => navigate('/weight-estimations')}
                                                    >
                                                        Estimaciones
                                                    </CustomButton>
                                                </Grid>
                                                <Grid item xs={12} sm={6} md={3}>
                                                    <CustomButton
                                                        fullWidth
                                                        variant="outlined"
                                                        startIcon={<DescriptionIcon />}
                                                        onClick={() => navigate('/weight-estimations')}
                                                    >
                                                        Reportes
                                                    </CustomButton>
                                                </Grid>
                                            </Grid>
                                        </Card>
                                    </Grid>
                                </Grid>
                            )}

                            {/* Resumen rápido */}
                            {!loading && stats && (
                                <Grid container spacing={3} mt={2}>
                                    <Grid item xs={12}>
                                        <Card sx={{ p: 3 }}>
                                            <CustomTypography variant="h6" mb={2}>
                                                Resumen del Sistema
                                            </CustomTypography>
                                            <CustomTypography variant="body2" color="text.secondary" paragraph>
                                                Sistema gestionando <strong>{stats.totalCattle || 0}</strong> animales 
                                                {stats.totalBreeds > 0 && ` de ${stats.totalBreeds} razas diferentes`}.
                                                {stats.totalEstimations > 0 && (
                                                    <> Se han realizado <strong>{stats.totalEstimations}</strong> estimaciones de peso.</>
                                                )}
                                            </CustomTypography>
                                        </Card>
                                    </Grid>
                                </Grid>
                            )}
                        </>
                    )}
                </LoadingState>
            </Container>
        </Box>
    );
}

export default DashboardTemplate;

