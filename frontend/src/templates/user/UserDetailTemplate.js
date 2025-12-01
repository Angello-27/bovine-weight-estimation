// frontend/src/templates/user/UserDetailTemplate.js

import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import CustomTypography from '../../components/atoms/CustomTypography';
import CustomButton from '../../components/atoms/CustomButton';
import Card from '../../components/atoms/Card';
import InfoField from '../../components/atoms/InfoField';
import StatItem from '../../components/molecules/StatItem';
import LoadingState from '../../components/molecules/LoadingState';
import ErrorState from '../../components/molecules/ErrorState';
import { useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import PersonIcon from '@mui/icons-material/Person';
import EmailIcon from '@mui/icons-material/Email';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import BusinessIcon from '@mui/icons-material/Business';
import BarChartIcon from '@mui/icons-material/BarChart';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import Chip from '@mui/material/Chip';
import Divider from '@mui/material/Divider';
import DataTable from '../../components/molecules/DataTable';
import LinkButton from '../../components/atoms/LinkButton';
import HomeIcon from '@mui/icons-material/Home';

function UserDetailTemplate({ user, ownedFarms = [], stats, loading, error, userId }) {
    const navigate = useNavigate();

    const getUserDisplayName = () => {
        if (user?.first_name && user?.last_name) {
            return `${user.first_name} ${user.last_name}`;
        }
        return user?.first_name || user?.last_name || user?.username || 'Usuario';
    };

    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                {/* Header con botón de regreso */}
                <Box sx={{ mb: 4 }}>
                    <CustomButton
                        startIcon={<ArrowBackIcon />}
                        onClick={() => navigate('/users')}
                        sx={{ mb: 2 }}
                    >
                        Volver a Usuarios
                    </CustomButton>
                    <CustomTypography customVariant="pageTitle" sx={{ mb: 1 }}>
                        {getUserDisplayName()}
                    </CustomTypography>
                </Box>

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && user && (
                        <>
                            {/* Información principal del usuario */}
                            <Grid container spacing={3} sx={{ mb: 4 }}>
                                <Grid item xs={12} md={8}>
                                    {/* Tarjeta de información del usuario */}
                                    <Card sx={{ p: 3, mb: 3 }}>
                                        <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                            <PersonIcon />
                                            Información del Usuario
                                        </CustomTypography>
                                        <Divider sx={{ mb: 3 }} />
                                        
                                        <Grid container spacing={3}>
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Nombre de usuario"
                                                    value={user.username || '-'}
                                                    icon={<PersonIcon fontSize="small" />}
                                                />
                                            </Grid>
                                            
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Email"
                                                    value={user.email || '-'}
                                                    icon={<EmailIcon fontSize="small" />}
                                                />
                                            </Grid>

                                            {user.first_name && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Nombre"
                                                        value={user.first_name}
                                                        icon={<PersonIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}

                                            {user.last_name && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Apellido"
                                                        value={user.last_name}
                                                        icon={<PersonIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}
                                            
                                            {user.role && (
                                                <Grid item xs={12} sm={6}>
                                                    <Box>
                                                        <CustomTypography variant="body2" sx={{ mb: 1, fontWeight: 500 }}>
                                                            Rol
                                                        </CustomTypography>
                                                        <Chip
                                                            label={user.role.name || '-'}
                                                            icon={<AdminPanelSettingsIcon />}
                                                            color="primary"
                                                            variant="outlined"
                                                        />
                                                    </Box>
                                                </Grid>
                                            )}
                                            
                                            <Grid item xs={12} sm={6}>
                                                <Box>
                                                    <CustomTypography variant="body2" sx={{ mb: 1, fontWeight: 500 }}>
                                                        Estado
                                                    </CustomTypography>
                                                    <Chip
                                                        label={user.is_active ? 'Activo' : 'Inactivo'}
                                                        icon={user.is_active ? <CheckCircleIcon /> : <CancelIcon />}
                                                        color={user.is_active ? 'success' : 'default'}
                                                        variant="outlined"
                                                    />
                                                </Box>
                                            </Grid>
                                        </Grid>
                                    </Card>

                                    {/* Farms de las que el usuario es propietario */}
                                    {ownedFarms && ownedFarms.length > 0 && (
                                        <Card sx={{ p: 3, mb: 3 }}>
                                            <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                                <HomeIcon />
                                                Haciendas Propias
                                            </CustomTypography>
                                            <Divider sx={{ mb: 3 }} />
                                            
                                            <DataTable
                                                columns={[
                                                    {
                                                        label: 'Nombre',
                                                        field: 'name',
                                                        render: (value, row) => (
                                                            <LinkButton
                                                                onClick={(e) => {
                                                                    e.stopPropagation();
                                                                    navigate(`/farms/${row.id}`);
                                                                }}
                                                            >
                                                                {value || '-'}
                                                            </LinkButton>
                                                        )
                                                    },
                                                    {
                                                        label: 'Capacidad',
                                                        field: 'capacity',
                                                        render: (value) => value ? `${value} animales` : '-'
                                                    },
                                                    {
                                                        label: 'Total Animales',
                                                        field: 'total_animals',
                                                        render: (value) => value || 0
                                                    },
                                                    {
                                                        label: 'Ubicación GPS',
                                                        field: 'latitude',
                                                        render: (value, row) => {
                                                            if (row.latitude != null && row.longitude != null) {
                                                                return `${row.latitude.toFixed(6)}, ${row.longitude.toFixed(6)}`;
                                                            }
                                                            return '-';
                                                        }
                                                    },
                                                ]}
                                                rows={ownedFarms}
                                                emptyMessage="El usuario no es propietario de ninguna hacienda."
                                            />
                                        </Card>
                                    )}
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
                                                label="Haciendas Propias"   
                                                value={stats.ownedFarms || 0}
                                                color="primary.main"
                                                showDivider={false}
                                            />
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

export default UserDetailTemplate;

