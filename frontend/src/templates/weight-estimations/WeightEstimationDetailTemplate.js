// frontend/src/templates/weight-estimations/WeightEstimationDetailTemplate.js

import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Divider from '@mui/material/Divider';
import CustomTypography from '../../components/atoms/CustomTypography';
import LoadingState from '../../components/molecules/LoadingState';
import ErrorState from '../../components/molecules/ErrorState';
import Card from '../../components/atoms/Card';
import InfoField from '../../components/atoms/InfoField';
import CustomButton from '../../components/atoms/CustomButton';
import LinkButton from '../../components/atoms/LinkButton';
import NavigationCard from '../../components/molecules/NavigationCard';
import EstimationInfoCard from '../../components/molecules/EstimationInfoCard';
import EstimationTechnicalCard from '../../components/molecules/EstimationTechnicalCard';
import EstimationComparisonCard from '../../components/molecules/EstimationComparisonCard';
import EstimationImageCard from '../../components/molecules/EstimationImageCard';
import WeightHistoryTable from '../../components/molecules/WeightHistoryTable';
import WeightLineChart from '../../components/molecules/WeightLineChart';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import PetsIcon from '@mui/icons-material/Pets';
import MonitorWeightIcon from '@mui/icons-material/MonitorWeight';
import HistoryIcon from '@mui/icons-material/History';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { breedToComboBox as getBreedOptions } from '../../utils/transformers/breedToComboBox';

function WeightEstimationDetailTemplate({
    estimation,
    cattle,
    previousEstimations = [],
    loading,
    error,
    apiBaseUrl,
    onViewCattle,
    onViewCattleEstimations
}) {
    const [tabValue, setTabValue] = useState(0);
    const navigate = useNavigate();

    const handleTabChange = (event, newValue) => {
        setTabValue(newValue);
    };

    const getBreedLabel = (breed) => {
        if (!breed) return '-';
        const breedOptions = getBreedOptions();
        const breedOption = breedOptions.find(b => b.id === breed);
        return breedOption ? breedOption.label : breed;
    };

    // Preparar datos para el gráfico (incluyendo la estimación actual)
    const chartData = estimation && cattle ? [
        ...previousEstimations.map(w => ({
            label: new Date(w.timestamp).toLocaleDateString('es-ES', { month: 'short', day: 'numeric' }),
            weight: w.estimated_weight || w.estimated_weight_kg || 0,
            confidence: w.confidence_score || w.confidence || 0,
            timestamp: w.timestamp,
            id: w.id
        })),
        {
            label: new Date(estimation.timestamp).toLocaleDateString('es-ES', { month: 'short', day: 'numeric' }),
            weight: estimation.estimated_weight || estimation.estimated_weight_kg || 0,
            confidence: estimation.confidence_score || estimation.confidence || 0,
            timestamp: estimation.timestamp,
            id: estimation.id
        }
    ].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp)) : [];

    // Preparar datos para la tabla
    const tableData = estimation && cattle ? [
        ...previousEstimations.map(w => ({
            id: w.id,
            timestamp: w.timestamp,
            weight: w.estimated_weight || w.estimated_weight_kg || 0,
            confidence: w.confidence_score || w.confidence || 0
        })),
        {
            id: estimation.id,
            timestamp: estimation.timestamp,
            weight: estimation.estimated_weight || estimation.estimated_weight_kg || 0,
            confidence: estimation.confidence_score || estimation.confidence || 0
        }
    ].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)) : [];

    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                {/* Header con botón de regreso */}
                <Box sx={{ mb: 4 }}>
                    <CustomButton
                        startIcon={<ArrowBackIcon />}
                        onClick={() => navigate('/weight-estimations')}
                        sx={{ mb: 2 }}
                    >
                        Volver a Estimaciones
                    </CustomButton>
                    <CustomTypography customVariant="pageTitle" sx={{ mb: 1 }}>
                        {estimation ? 'Detalle de Estimación de Peso' : 'Estimación de Peso'}
                    </CustomTypography>
                </Box>

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && estimation && (
                        <>
                            {/* Información principal */}
                            <Grid container spacing={3} sx={{ mb: 4 }}>
                                {/* Columna izquierda: Información de la estimación */}
                                <Grid item xs={12} md={7}>
                                    <EstimationInfoCard estimation={estimation} />
                                </Grid>

                                {/* Columna central: Detalles técnicos */}
                                <Grid item xs={12} md={5}>
                                    <EstimationTechnicalCard estimation={estimation} />
                                </Grid>

                                {/* Columna derecha: Animal asociado y acciones */}
                                <Grid item xs={12} md={3}>
                                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                                        {cattle ? (
                                            <>
                                                <Card sx={{ p: 3 }}>
                                                    <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                                        <PetsIcon />
                                                        Animal Asociado
                                                    </CustomTypography>
                                                    <Divider sx={{ mb: 3 }} />
                                                    
                                                    <Grid container spacing={2}>
                                                        <Grid item xs={12}>
                                                            <InfoField
                                                                label="Caravana"
                                                                value={cattle.ear_tag || '-'}
                                                            />
                                                        </Grid>
                                                        
                                                        {cattle.name && (
                                                            <Grid item xs={12}>
                                                                <InfoField
                                                                    label="Nombre"
                                                                    value={cattle.name}
                                                                />
                                                            </Grid>
                                                        )}
                                                        
                                                        {cattle.breed && (
                                                            <Grid item xs={12}>
                                                                <InfoField
                                                                    label="Raza"
                                                                    value={getBreedLabel(cattle.breed)}
                                                                />
                                                            </Grid>
                                                        )}
                                                        
                                                        <Grid item xs={12}>
                                                            <Box sx={{ mt: 2 }}>
                                                                <LinkButton
                                                                    onClick={(e) => {
                                                                        e.stopPropagation();
                                                                        if (onViewCattle && cattle.id) {
                                                                            onViewCattle(cattle.id);
                                                                        }
                                                                    }}
                                                                    sx={{ textTransform: 'none' }}
                                                                >
                                                                    Ver Detalle del Animal
                                                                </LinkButton>
                                                            </Box>
                                                        </Grid>
                                                    </Grid>
                                                </Card>

                                                <NavigationCard
                                                    icon={<HistoryIcon sx={{ fontSize: 32 }} />}
                                                    title="Ver Historial Completo"
                                                    description={`Ver todas las estimaciones de peso del animal ${cattle.name || cattle.ear_tag || ''}`}
                                                    onClick={() => {
                                                        if (onViewCattleEstimations && cattle.id) {
                                                            onViewCattleEstimations(cattle.id);
                                                        }
                                                    }}
                                                    iconBgColor="primary.light"
                                                    iconColor="primary.contrastText"
                                                />
                                            </>
                                        ) : estimation.cattle_id && (
                                            <Card sx={{ p: 3 }}>
                                                <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                                                    Animal ID: {estimation.cattle_id}
                                                </CustomTypography>
                                                <LinkButton
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        if (onViewCattle && estimation.cattle_id) {
                                                            onViewCattle(estimation.cattle_id);
                                                        }
                                                    }}
                                                    sx={{ textTransform: 'none' }}
                                                >
                                                    Ver Animal
                                                </LinkButton>
                                            </Card>
                                        )}
                                    </Box>
                                </Grid>
                            </Grid>

                            {/* Tabs para diferentes secciones */}
                            <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
                                <Tabs value={tabValue} onChange={handleTabChange}>
                                    <Tab label="Imagen" />
                                    <Tab label="Comparación" />
                                    {cattle && <Tab label="Historial del Animal" />}
                                </Tabs>
                            </Box>

                            {/* Contenido de Tabs */}
                            {tabValue === 0 && (
                                <Grid container spacing={3}>
                                    <Grid item xs={12}>
                                        <EstimationImageCard 
                                            imagePath={estimation.frame_image_path || estimation.image_path}
                                            apiBaseUrl={apiBaseUrl}
                                        />
                                    </Grid>
                                </Grid>
                            )}

                            {tabValue === 1 && (
                                <Grid container spacing={3}>
                                    <Grid item xs={12}>
                                        <EstimationComparisonCard 
                                            currentEstimation={estimation}
                                            previousEstimations={previousEstimations}
                                        />
                                    </Grid>
                                </Grid>
                            )}

                            {tabValue === 2 && cattle && (
                                <Grid container spacing={3}>
                                    {chartData.length > 0 && (
                                        <>
                                            <Grid item xs={12}>
                                                <Card sx={{ p: 3 }}>
                                                    <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                                        <MonitorWeightIcon />
                                                        Evolución de Peso
                                                    </CustomTypography>
                                                    <Divider sx={{ mb: 3 }} />
                                                    <WeightLineChart data={chartData} />
                                                </Card>
                                            </Grid>
                                            <Grid item xs={12}>
                                                <Card sx={{ p: 3 }}>
                                                    <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                                        <HistoryIcon />
                                                        Historial Completo
                                                    </CustomTypography>
                                                    <Divider sx={{ mb: 3 }} />
                                                    <WeightHistoryTable data={tableData} />
                                                </Card>
                                            </Grid>
                                        </>
                                    )}
                                    {chartData.length === 0 && (
                                        <Grid item xs={12}>
                                            <Card sx={{ p: 3, textAlign: 'center' }}>
                                                <CustomTypography variant="body2" color="text.secondary">
                                                    No hay historial de estimaciones para este animal
                                                </CustomTypography>
                                            </Card>
                                        </Grid>
                                    )}
                                </Grid>
                            )}
                        </>
                    )}
                </LoadingState>
            </Container>
        </Box>
    );
}

export default WeightEstimationDetailTemplate;
