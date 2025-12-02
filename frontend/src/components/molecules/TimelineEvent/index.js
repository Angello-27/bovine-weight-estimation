// frontend/src/components/molecules/TimelineEvent/index.js

import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Chip from '@mui/material/Chip';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ChildCareIcon from '@mui/icons-material/ChildCare';
import MonitorWeightIcon from '@mui/icons-material/MonitorWeight';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';

function TimelineEvent({ event }) {
    const formatDate = (dateString) => {
        if (!dateString) return 'Fecha no disponible';
        
        try {
            const date = new Date(dateString);
            // Verificar si la fecha es válida
            if (isNaN(date.getTime())) {
                return 'Fecha inválida';
            }
            return date.toLocaleDateString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            });
        } catch (error) {
            console.warn('Error al formatear fecha:', dateString, error);
            return 'Fecha inválida';
        }
    };

    // Obtener la fecha del evento (puede ser 'date' o 'timestamp')
    const eventDate = event.date || event.timestamp;
    // Obtener el título (puede ser 'title' o 'description')
    const eventTitle = event.title || event.description || 'Evento';
    // Obtener la descripción
    const eventDescription = event.description || '';

    const getEventIcon = () => {
        switch (event.type) {
            case 'registration':
                return <CheckCircleIcon />;
            case 'birth':
                return <ChildCareIcon />;
            case 'weight_estimation':
                return <MonitorWeightIcon />;
            default:
                return <CalendarTodayIcon />;
        }
    };

    return (
        <Box
            sx={{
                display: 'flex',
                gap: 2,
                pb: 3,
                position: 'relative',
                '&::after': {
                    content: '""',
                    position: 'absolute',
                    left: '20px',
                    top: '40px',
                    bottom: 0,
                    width: '2px',
                    bgcolor: 'divider'
                },
                '&:last-child::after': {
                    display: 'none'
                }
            }}
        >
            <Box
                sx={{
                    width: 40,
                    height: 40,
                    borderRadius: '50%',
                    bgcolor: 'primary.main',
                    color: 'white',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                    zIndex: 1
                }}
            >
                {getEventIcon()}
            </Box>
            
            <Box flex={1}>
                <Box display="flex" alignItems="center" gap={1} mb={0.5} flexWrap="wrap">
                    <CustomTypography variant="subtitle1" fontWeight="bold">
                        {eventTitle}
                    </CustomTypography>
                    {eventDate && (
                        <Chip
                            label={formatDate(eventDate)}
                            size="small"
                            variant="outlined"
                        />
                    )}
                </Box>
                {eventDescription && (
                    <CustomTypography variant="body2" color="text.secondary">
                        {eventDescription}
                    </CustomTypography>
                )}
                {event.metadata?.gps && (
                    <Box display="flex" alignItems="center" gap={0.5} mt={0.5}>
                        <LocationOnIcon fontSize="small" color="action" />
                        <CustomTypography variant="caption" color="text.secondary">
                            GPS: {event.metadata.gps.lat.toFixed(4)}, {event.metadata.gps.lng.toFixed(4)}
                        </CustomTypography>
                    </Box>
                )}
            </Box>
        </Box>
    );
}

export default TimelineEvent;

