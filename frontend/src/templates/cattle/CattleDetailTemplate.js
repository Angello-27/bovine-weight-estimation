// frontend/src/templates/cattle/CattleDetailTemplate.js

import Grid from "@mui/material/Grid";
import Container from "@mui/material/Container";
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from "@mui/material/Box";
import Divider from '@mui/material/Divider';
import LoadingState from '../../components/molecules/LoadingState';
import ErrorState from '../../components/molecules/ErrorState';
import ActionButton from '../../components/molecules/ActionButton';
import Alert from '@mui/material/Alert';
import Snackbar from '@mui/material/Snackbar';
import Card from '../../components/atoms/Card';
import InfoField from '../../components/atoms/InfoField';
import CustomTypography from '../../components/atoms/CustomTypography';
import CustomButton from '../../components/atoms/CustomButton';
import CattleTraceabilityTimeline from '../../components/organisms/CattleTraceabilityTimeline';
import CattleLineageTree from '../../components/organisms/CattleLineageTree';
import CattleWeightHistoryChart from '../../components/organisms/CattleWeightHistoryChart';
import ImageGallery from '../../components/molecules/ImageGallery';
import NavigationCard from '../../components/molecules/NavigationCard';
import LinkButton from '../../components/atoms/LinkButton';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import TagIcon from '@mui/icons-material/Tag';
import PetsIcon from '@mui/icons-material/Pets';
import WcIcon from '@mui/icons-material/Wc';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import ScaleIcon from '@mui/icons-material/Scale';
import PaletteIcon from '@mui/icons-material/Palette';
import NotesIcon from '@mui/icons-material/Notes';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import BusinessIcon from '@mui/icons-material/Business';
import FamilyRestroomIcon from '@mui/icons-material/FamilyRestroom';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { breedToComboBox } from '../../utils/transformers/breedToComboBox';

function CattleDetailTemplate({
    cattle,
    estimations,
    timelineEvents,
    galleryImages,
    father,
    mother,
    lineage,
    loading,
    error,
    onViewFather,
    onViewMother,
    onGenerateReport,
    reportLoading,
    reportError
}) {
    const [tabValue, setTabValue] = useState(0);
    const [showReportError, setShowReportError] = useState(false);
    const navigate = useNavigate();

    // Mostrar error del reporte cuando cambie
    useEffect(() => {
        if (reportError) {
            setShowReportError(true);
        }
    }, [reportError]);

    const handleTabChange = (event, newValue) => {
        setTabValue(newValue);
    };

    const handleEstimateWeight = () => {
        // Navegar a la página de estimación con el animal_id como query param
        navigate(`/weight-estimations/estimate?animal_id=${cattle?.id}`);
    };

    // Funciones auxiliares para formatear datos
    const formatDate = (dateString) => {
        if (!dateString) return '-';
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('es-ES', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
        } catch {
            return dateString;
        }
    };

    const calculateAge = (birthDate) => {
        if (!birthDate) return null;
        try {
            const birth = new Date(birthDate);
            const today = new Date();
            const months = (today.getFullYear() - birth.getFullYear()) * 12 + (today.getMonth() - birth.getMonth());
            return months;
        } catch {
            return null;
        }
    };

    const getBreedLabel = (breed) => {
        const breeds = breedToComboBox();
        const breedOption = breeds.find(b => b.id === breed);
        return breedOption?.label || breed || '-';
    };

    const getGenderLabel = (gender) => {
        return gender === 'male' ? 'Macho' : gender === 'female' ? 'Hembra' : gender || '-';
    };

    const getStatusLabel = (status) => {
        const statusMap = {
            'active': 'Activo',
            'inactive': 'Inactivo',
            'sold': 'Vendido',
            'deceased': 'Fallecido'
        };
        return statusMap[status] || status || '-';
    };

    const age = calculateAge(cattle?.birth_date);

    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                {/* Header con botón de regreso */}
                <Box sx={{ mb: 4 }}>
                    <CustomButton
                        startIcon={<ArrowBackIcon />}
                        onClick={() => navigate('/cattle')}
                        sx={{ mb: 2 }}
                    >
                        Volver a Animales
                    </CustomButton>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                        <CustomTypography customVariant="pageTitle">
                            {cattle ? `Animal: ${cattle.ear_tag}` : 'Detalle del Animal'}
                        </CustomTypography>
                        <ActionButton
                            icon={<PictureAsPdfIcon />}
                            label={reportLoading ? 'Generando...' : 'Generar Reporte PDF'}
                            onClick={onGenerateReport}
                            disabled={reportLoading || !cattle}
                            variant="contained"
                        />
                    </Box>
                </Box>

                <ErrorState error={error} />

                {/* Error del reporte */}
                {reportError && (
                    <Alert severity="error" sx={{ mb: 2 }} onClose={() => setShowReportError(false)}>
                        {reportError}
                    </Alert>
                )}

                <LoadingState loading={loading}>
                    {!error && cattle && (
                        <>
                            {/* Información principal del animal */}
                            <Grid container spacing={3} sx={{ mb: 4 }}>
                                <Grid item xs={12} md={8}>
                                    {/* Tarjeta de información del animal */}
                                    <Card sx={{ p: 3, mb: 3 }}>
                                        <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                            <PetsIcon />
                                            Información del Animal
                                        </CustomTypography>
                                        <Divider sx={{ mb: 3 }} />
                                        
                                        <Grid container spacing={3}>
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Caravana"
                                                    value={cattle.ear_tag || '-'}
                                                    icon={<TagIcon fontSize="small" />}
                                                />
                                            </Grid>
                                            
                                            {cattle.name && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Nombre"
                                                        value={cattle.name}
                                                        icon={<PetsIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}
                                            
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Raza"
                                                    value={getBreedLabel(cattle.breed)}
                                                    icon={<PetsIcon fontSize="small" />}
                                                />
                                            </Grid>
                                            
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Género"
                                                    value={getGenderLabel(cattle.gender)}
                                                    icon={<WcIcon fontSize="small" />}
                                                />
                                            </Grid>
                                            
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Fecha de Nacimiento"
                                                    value={formatDate(cattle.birth_date)}
                                                    icon={<CalendarTodayIcon fontSize="small" />}
                                                />
                                            </Grid>
                                            
                                            {age !== null && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Edad"
                                                        value={`${age} meses`}
                                                        icon={<CalendarTodayIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}
                                            
                                            {cattle.birth_weight_kg && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Peso al Nacer"
                                                        value={`${cattle.birth_weight_kg} kg`}
                                                        icon={<ScaleIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}
                                            
                                            {cattle.color && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Color"
                                                        value={cattle.color}
                                                        icon={<PaletteIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}
                                            
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Estado"
                                                    value={getStatusLabel(cattle.status)}
                                                    icon={<CheckCircleIcon fontSize="small" />}
                                                />
                                            </Grid>
                                            
                                            {cattle.observations && (
                                <Grid item xs={12}>
                                                    <Box>
                                                        <CustomTypography variant="body2" sx={{ mb: 1, fontWeight: 500, display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                                            <NotesIcon fontSize="small" />
                                                            Observaciones
                                                        </CustomTypography>
                                                        <CustomTypography variant="body2" color="text.secondary">
                                                            {cattle.observations}
                                                        </CustomTypography>
                                                    </Box>
                                                </Grid>
                                            )}

                                            {/* Vínculo a hacienda */}
                                            {cattle.farm_id && (
                                                <Grid item xs={12} sm={6}>
                                                    <Box>
                                                        <CustomTypography variant="body2" sx={{ mb: 1, fontWeight: 500, display: 'flex', alignItems: 'center', gap: 0.5 }}>
                                                            <BusinessIcon fontSize="small" />
                                                            Hacienda
                                                        </CustomTypography>
                                                        <LinkButton
                                                            onClick={(e) => {
                                                                e.stopPropagation();
                                                                navigate(`/farms/${cattle.farm_id}`);
                                                            }}
                                                            sx={{ textTransform: 'none' }}
                                                        >
                                                            Ver Hacienda
                                                        </LinkButton>
                                                    </Box>
                                                </Grid>
                                            )}
                                        </Grid>
                                    </Card>
                                </Grid>

                                {/* Columna derecha: Cards de acciones y parentesco */}
                                <Grid item xs={12} md={4}>
                                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                                        {/* Card de Estimación de Peso */}
                                        <NavigationCard
                                            icon={<CameraAltIcon sx={{ fontSize: 32 }} />}
                                            title="Estimar Peso por Imagen"
                                            description="Sube una imagen del animal para estimar su peso usando inteligencia artificial"
                                            onClick={handleEstimateWeight}
                                            iconBgColor="primary.light"
                                            iconColor="primary.contrastText"
                                        />

                                        {/* Card de Padre */}
                                        {(father || cattle?.father_id) && (
                                            <NavigationCard
                                                icon={<FamilyRestroomIcon sx={{ fontSize: 32 }} />}
                                                title="Padre"
                                                description={father ? `${father.ear_tag || 'Sin caravana'}${father.name ? ` - ${father.name}` : ''}` : 'Ver información del padre'}
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    const fatherId = father?.id || cattle?.father_id;
                                                    if (fatherId) {
                                                        onViewFather && onViewFather(fatherId);
                                                    }
                                                }}
                                                iconBgColor="info.light"
                                                iconColor="info.contrastText"
                                            />
                                        )}

                                        {/* Card de Madre */}
                                        {(mother || cattle?.mother_id) && (
                                            <NavigationCard
                                                icon={<FamilyRestroomIcon sx={{ fontSize: 32 }} />}
                                                title="Madre"
                                                description={mother ? `${mother.ear_tag || 'Sin caravana'}${mother.name ? ` - ${mother.name}` : ''}` : 'Ver información de la madre'}
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    const motherId = mother?.id || cattle?.mother_id;
                                                    if (motherId) {
                                                        onViewMother && onViewMother(motherId);
                                                    }
                                                }}
                                                iconBgColor="success.light"
                                                iconColor="success.contrastText"
                                            />
                                        )}
                                    </Box>
                                </Grid>
                            </Grid>

                            {/* Tabs para diferentes secciones */}
                            <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
                                <Tabs value={tabValue} onChange={handleTabChange}>
                                    <Tab label="Trazabilidad" />
                                    <Tab label="Historial de Pesos" />
                                    <Tab label="Linaje" />
                                    <Tab label="Galería" />
                                </Tabs>
                            </Box>

                            {/* Contenido de Tabs */}
                            {tabValue === 0 && (
                                <Grid container spacing={3}>
                                    <Grid item xs={12}>
                                        <CattleTraceabilityTimeline events={timelineEvents} />
                                    </Grid>
                                </Grid>
                            )}

                            {tabValue === 1 && (
                                <Grid container spacing={3}>
                                    <Grid item xs={12}>
                                        <CattleWeightHistoryChart animalId={cattle?.id} />
                                    </Grid>
                                </Grid>
                            )}

                            {tabValue === 2 && (
                                <Box sx={{ width: '100%', height: '100%' }}>
                                    <CattleLineageTree
                                        cattle={cattle}
                                        father={father}
                                        mother={mother}
                                        descendants={lineage?.descendants || []}
                                        onViewFather={onViewFather}
                                        onViewMother={onViewMother}
                                    />
                                </Box>
                            )}

                            {tabValue === 3 && (
                                <Grid container spacing={3}>
                                    <Grid item xs={12}>
                                        <ImageGallery 
                                            images={galleryImages}
                                            apiBaseUrl={import.meta.env.REACT_APP_API_URL || ''}
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

export default CattleDetailTemplate;

