// frontend/src/components/organisms/SyncStatusCard/index.js

import Grid from "@mui/material/Grid";
import Card from '../../atoms/Card';
import CustomTypography from '../../atoms/CustomTypography';
import Chip from '@mui/material/Chip';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';

function SyncStatusCard({ health, stats }) {
    return (
        <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
                <Card>
                    <Grid container alignItems="center" spacing={2} mb={2}>
                        <Grid item>
                            <CustomTypography variant="h6">
                                Estado del Servicio
                            </CustomTypography>
                        </Grid>
                        <Grid item>
                            <Chip
                                icon={health?.status === 'online' ? <CheckCircleIcon /> : <ErrorIcon />}
                                label={health?.status === 'online' ? 'Online' : 'Offline'}
                                color={health?.status === 'online' ? 'success' : 'error'}
                                size="small"
                            />
                        </Grid>
                    </Grid>
                    <CustomTypography variant="body2" color="text.secondary" mb={1}>
                        Base de datos: {health?.database || 'unknown'}
                    </CustomTypography>
                    <CustomTypography variant="body2" color="text.secondary">
                        {health?.status === 'online' 
                            ? 'El servicio de sincronización está operativo.'
                            : 'El servicio de sincronización no está disponible.'}
                    </CustomTypography>
                </Card>
            </Grid>

            <Grid item xs={12} md={6}>
                <Card>
                    <CustomTypography variant="h6" mb={2}>
                        Estadísticas
                    </CustomTypography>
                    <CustomTypography variant="body2" color="text.secondary" mb={1}>
                        Total sincronizado: {stats?.totalSynced || 0}
                    </CustomTypography>
                    <CustomTypography variant="body2" color="text.secondary" mb={1}>
                        Items pendientes: {stats?.pendingItems || 0}
                    </CustomTypography>
                    {stats?.lastSync && (
                        <CustomTypography variant="body2" color="text.secondary">
                            Última sincronización: {new Date(stats.lastSync).toLocaleString()}
                        </CustomTypography>
                    )}
                </Card>
            </Grid>

            <Grid item xs={12}>
                <Card>
                    <CustomTypography variant="h6" mb={2}>
                        Items Pendientes
                    </CustomTypography>
                    <CustomTypography variant="body2" color="text.secondary">
                        {stats?.pendingItems > 0 
                            ? `Hay ${stats.pendingItems} items pendientes de sincronizar desde móviles.`
                            : 'No hay items pendientes de sincronizar.'}
                    </CustomTypography>
                </Card>
            </Grid>
        </Grid>
    );
}

export default SyncStatusCard;

