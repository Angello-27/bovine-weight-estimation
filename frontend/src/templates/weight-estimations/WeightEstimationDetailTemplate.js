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
import EstimationComparisonCard from '../../components/molecules/EstimationComparisonCard';
import EstimationImageCard from '../../components/molecules/EstimationImageCard';
import ImageGallery from '../../components/molecules/ImageGallery';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import PetsIcon from '@mui/icons-material/Pets';
import MonitorWeightIcon from '@mui/icons-material/MonitorWeight';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import MemoryIcon from '@mui/icons-material/Memory';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import ScienceIcon from '@mui/icons-material/Science';
import InfoIcon from '@mui/icons-material/Info';
import Chip from '@mui/material/Chip';
import LinearProgress from '@mui/material/LinearProgress';
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
    onViewCattle
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

    const formatDate = (dateString) => {
        if (!dateString) return '-';
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('es-ES', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        } catch {
            return dateString;
        }
    };

    const formatProcessingTime = (ms) => {
        if (!ms) return '-';
        if (ms < 1000) return `${ms} ms`;
        return `${(ms / 1000).toFixed(2)} s`;
    };

    const getConfidenceColor = (score) => {
        if (score >= 0.9) return 'success';
        if (score >= 0.7) return 'warning';
        return 'error';
    };

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
                                {/* Columna izquierda: Información y detalles técnicos fusionados */}
                                <Grid item xs={12} md={9}>
                                    <Card sx={{ p: 3 }}>
                                        <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                            <MonitorWeightIcon />
                                            Información de la Estimación
                                        </CustomTypography>
                                        <Divider sx={{ mb: 3 }} />
                                        
                                        <Grid container spacing={3}>
                                            {/* Información de la estimación */}
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Peso Estimado"
                                                    value={`${(estimation.estimated_weight || estimation.estimated_weight_kg || 0).toFixed(1)} kg`}
                                                    icon={<MonitorWeightIcon fontSize="small" />}
                                                />
                                            </Grid>
                                            
                                            <Grid item xs={12} sm={6}>
                                                <Box>
                                                    <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                                                        Confianza de la Estimación
                                                    </CustomTypography>
                                                    <LinearProgress
                                                        variant="determinate"
                                                        value={(estimation.confidence_score || estimation.confidence || 0) * 100}
                                                        color={getConfidenceColor(estimation.confidence_score || estimation.confidence || 0)}
                                                        sx={{ height: 10, borderRadius: 5, mb: 1 }}
                                                    />
                                                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                                        <CustomTypography variant="body1" sx={{ fontWeight: 500, color: `${getConfidenceColor(estimation.confidence_score || estimation.confidence || 0)}.main` }}>
                                                            {((estimation.confidence_score || estimation.confidence || 0) * 100).toFixed(1)}%
                                                        </CustomTypography>
                                                        <Chip
                                                            label={(estimation.confidence_score || estimation.confidence || 0) >= 0.9 ? 'Alta' : (estimation.confidence_score || estimation.confidence || 0) >= 0.7 ? 'Media' : 'Baja'}
                                                            size="small"
                                                            color={getConfidenceColor(estimation.confidence_score || estimation.confidence || 0)}
                                                            variant="outlined"
                                                        />
                                                    </Box>
                                                </Box>
                                            </Grid>
                                            
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Fecha y Hora"
                                                    value={formatDate(estimation.timestamp)}
                                                    icon={<CalendarTodayIcon fontSize="small" />}
                                                />
                                            </Grid>
                                            
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Raza Detectada"
                                                    value={getBreedLabel(estimation.breed)}
                                                    icon={<PetsIcon fontSize="small" />}
                                                />
                                                {estimation.breed_confidence && (
                                                    <CustomTypography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                                                        Confianza: {(estimation.breed_confidence * 100).toFixed(0)}%
                                                    </CustomTypography>
                                                )}
                                            </Grid>

                                            {/* Detalles técnicos */}
                                            {estimation.model_version && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Versión del Modelo ML"
                                                        value={estimation.model_version || estimation.ml_model_version || '-'}
                                                        icon={<MemoryIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}
                                            
                                            {estimation.processing_time_ms && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Tiempo de Procesamiento"
                                                        value={formatProcessingTime(estimation.processing_time_ms)}
                                                        icon={<AccessTimeIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}
                                            
                                            {(estimation.gps_latitude && estimation.gps_longitude) && (
                                                <Grid item xs={12}>
                                                    <InfoField
                                                        label="Ubicación GPS"
                                                        value={`${estimation.gps_latitude.toFixed(6)}, ${estimation.gps_longitude.toFixed(6)}`}
                                                        icon={<LocationOnIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}

                                            {estimation.method && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Método de Estimación"
                                                        value={estimation.method}
                                                        icon={<ScienceIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}

                                            {estimation.meets_quality_criteria !== undefined && (
                                                <Grid item xs={12} sm={6}>
                                                    <Box>
                                                        <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                                                            Cumple Criterios de Calidad
                                                        </CustomTypography>
                                                        <CustomTypography variant="body1" sx={{ fontWeight: 500, color: estimation.meets_quality_criteria ? 'success.main' : 'error.main' }}>
                                                            {estimation.meets_quality_criteria ? 'Sí' : 'No'}
                                                        </CustomTypography>
                                                    </Box>
                                                </Grid>
                                            )}
                                        </Grid>
                                    </Card>
                                </Grid>

                                {/* Columna derecha: Animal asociado */}
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
                                                            <Box>
                                                                <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 0.5, display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                                                    Caravana
                                                                </CustomTypography>
                                                                <LinkButton
                                                                    onClick={(e) => {
                                                                        e.stopPropagation();
                                                                        if (onViewCattle && cattle.id) {
                                                                            onViewCattle(cattle.id);
                                                                        }
                                                                    }}
                                                                    sx={{ textTransform: 'none', p: 0, minWidth: 'auto' }}
                                                                >
                                                                    {cattle.ear_tag || '-'}
                                                                </LinkButton>
                                                            </Box>
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
                                                    </Grid>
                                                </Card>

                                            </>
                                        ) : (estimation.animal_id || estimation.cattle_id) && (
                                            <Card sx={{ p: 3 }}>
                                                <CustomTypography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                                                    Animal ID: {estimation.animal_id || estimation.cattle_id}
                                                </CustomTypography>
                                                <LinkButton
                                                    onClick={(e) => {
                                                        e.stopPropagation();
                                                        const animalId = estimation.animal_id || estimation.cattle_id;
                                                        if (onViewCattle && animalId) {
                                                            onViewCattle(animalId);
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
                                    <Tab label="Galería" />
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

                            {tabValue === 2 && (
                                <Grid container spacing={3}>
                                    <Grid item xs={12}>
                                        <ImageGallery 
                                            images={[
                                                // Imagen actual de la estimación
                                                {
                                                    id: estimation.id,
                                                    url: estimation.frame_image_path || estimation.image_path,
                                                    title: `Estimación de Peso - ${(estimation.estimated_weight || estimation.estimated_weight_kg || 0).toFixed(1)} kg`,
                                                    date: estimation.timestamp
                                                },
                                                // Imágenes de estimaciones anteriores
                                                ...(previousEstimations || [])
                                                    .filter(est => est.frame_image_path)
                                                    .map(est => ({
                                                        id: est.id,
                                                        url: est.frame_image_path,
                                                        title: `Estimación Anterior - ${(est.estimated_weight || est.estimated_weight_kg || 0).toFixed(1)} kg`,
                                                        date: est.timestamp
                                                    })),
                                                // Foto del animal si existe
                                                ...(cattle?.photo_url ? [{
                                                    id: `animal-photo-${cattle.id}`,
                                                    url: cattle.photo_url,
                                                    title: `Foto del Animal - ${cattle.name || cattle.ear_tag || 'Sin nombre'}`,
                                                    date: cattle.registration_date || cattle.last_updated
                                                }] : [])
                                            ]}
                                            apiBaseUrl={apiBaseUrl}
                                        />
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

export default WeightEstimationDetailTemplate;
