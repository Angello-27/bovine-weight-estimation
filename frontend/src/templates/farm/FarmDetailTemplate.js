// frontend/src/templates/farm/FarmDetailTemplate.js

import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import CustomTypography from '../../components/atoms/CustomTypography';
import CustomButton from '../../components/atoms/CustomButton';
import Card from '../../components/atoms/Card';
import InfoField from '../../components/atoms/InfoField';
import StatItem from '../../components/molecules/StatItem';
import NavigationCard from '../../components/molecules/NavigationCard';
import LoadingState from '../../components/molecules/LoadingState';
import ErrorState from '../../components/molecules/ErrorState';
import { useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import BusinessIcon from '@mui/icons-material/Business';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import MapIcon from '@mui/icons-material/Map';
import GroupsIcon from '@mui/icons-material/Groups';
import PetsIcon from '@mui/icons-material/Pets';
import ScaleIcon from '@mui/icons-material/Scale';
import BarChartIcon from '@mui/icons-material/BarChart';
import PersonIcon from '@mui/icons-material/Person';
import PlaceIcon from '@mui/icons-material/Place';
import Divider from '@mui/material/Divider';
import LinkButton from '../../components/atoms/LinkButton';

function FarmDetailTemplate({ farm, stats, loading, error, farmId }) {
    const navigate = useNavigate();

    const formatCoordinate = (value) => {
        if (value == null) return '-';
        return typeof value === 'number' ? value.toFixed(6) : value;
    };

    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                {/* Header con botón de regreso */}
                <Box sx={{ mb: 4 }}>
                    <CustomButton
                        startIcon={<ArrowBackIcon />}
                        onClick={() => navigate('/farms')}
                        sx={{ mb: 2 }}
                    >
                        Volver a Haciendas
                    </CustomButton>
                    <CustomTypography customVariant="pageTitle" sx={{ mb: 1 }}>
                        {farm?.name || 'Detalle de Hacienda'}
                    </CustomTypography>
                </Box>

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && farm && (
                        <>
                            {/* Información principal de la hacienda */}
                            <Grid container spacing={3} sx={{ mb: 4 }}>
                                <Grid item xs={12} md={8}>
                                    {/* Tarjeta de información de la hacienda */}
                                    <Card sx={{ p: 3, mb: 3 }}>
                                        <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                            <BusinessIcon />
                                            Información de la Hacienda
                                        </CustomTypography>
                                        <Divider sx={{ mb: 3 }} />
                                        
                                        <Grid container spacing={3}>
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Nombre"
                                                    value={farm.name}
                                                    icon={<BusinessIcon fontSize="small" />}
                                                />
                                            </Grid>
                                            
                                            {farm.owner_id && (
                                                <Grid item xs={12} sm={6}>
                                                    <Box>
                                                        <CustomTypography variant="body2" sx={{ mb: 1, fontWeight: 500, display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                                            <PersonIcon fontSize="small" />
                                                            Propietario
                                                        </CustomTypography>
                                                        <LinkButton
                                                            onClick={(e) => {
                                                                e.stopPropagation();
                                                                navigate(`/users/${farm.owner_id}`);
                                                            }}
                                                            sx={{ textTransform: 'none' }}
                                                        >
                                                            {farm.owner?.first_name && farm.owner?.last_name
                                                                ? `${farm.owner.first_name} ${farm.owner.last_name}`
                                                                : farm.owner?.first_name || farm.owner?.last_name || farm.owner?.username || '-'}
                                                        </LinkButton>
                                                    </Box>
                                                </Grid>
                                            )}
                                            
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Latitud"
                                                    value={formatCoordinate(farm.latitude)}
                                                    icon={<LocationOnIcon fontSize="small" />}
                                                />
                                            </Grid>
                                            
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Longitud"
                                                    value={formatCoordinate(farm.longitude)}
                                                    icon={<MapIcon fontSize="small" />}
                                                />
                                            </Grid>
                                            
                                            {farm.capacity && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Capacidad Máxima"
                                                        value={`${farm.capacity} animales`}
                                                        icon={<GroupsIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}
                                        </Grid>
                                    </Card>

                                    {/* Tarjetas de navegación independientes */}
                                    <Grid container spacing={3}>
                                        <Grid item xs={12} sm={6}>
                                            <NavigationCard
                                                icon={<PetsIcon fontSize="large" />}
                                                title="Ver Animales"
                                                description={`${stats.totalAnimals || 0} animales registrados en esta hacienda`}
                                                onClick={() => navigate(`/cattle?farm_id=${farmId}`)}
                                                iconBgColor="primary.light"
                                                iconColor="primary.contrastText"
                                            />
                                        </Grid>
                                        
                                        <Grid item xs={12} sm={6}>
                                            <NavigationCard
                                                icon={<ScaleIcon fontSize="large" />}
                                                title="Ver Estimaciones"
                                                description={`${stats.totalEstimations || 0} estimaciones de peso registradas`}
                                                onClick={() => navigate(`/weight-estimations?farm_id=${farmId}`)}
                                                iconBgColor="secondary.light"
                                                iconColor="secondary.contrastText"
                                            />
                                        </Grid>
                                    </Grid>
                                </Grid>

                                {/* Estadísticas resumidas */}
                                <Grid item xs={12} md={4}>
                                    <Card sx={{ p: 3 }}>
                                        <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                            <BarChartIcon />
                                            Resumen
                                        </CustomTypography>
                                        <Divider sx={{ mb: 3 }} />
                                        
                                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                                            <StatItem
                                                label="Total de Animales"
                                                value={stats.totalAnimals || 0}
                                                color="primary.main"
                                                subtitle={farm.capacity ? `de ${farm.capacity} capacidad máxima` : null}
                                            />
                                            
                                            <StatItem
                                                label="Animales Activos"
                                                value={stats.activeAnimals || 0}
                                                color="success.main"
                                            />
                                            
                                            <StatItem
                                                label="Estimaciones Realizadas"
                                                value={stats.totalEstimations || 0}
                                            />
                                            
                                            {stats.averageWeight > 0 && (
                                                <StatItem
                                                    label="Peso Promedio"
                                                    value={`${stats.averageWeight.toFixed(2)} kg`}
                                                />
                                            )}
                                            
                                            {stats.totalBreeds > 0 && (
                                                <StatItem
                                                    label="Razas Diferentes"
                                                    value={stats.totalBreeds}
                                                    showDivider={false}
                                                />
                                            )}
                                        </Box>
                                    </Card>
                                </Grid>
                            </Grid>

                        </>
                    )}
                </LoadingState>
            </Container>
        </Box>
    );
}

export default FarmDetailTemplate;

