// frontend/src/templates/role/RoleDetailTemplate.js

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
import DataTable from '../../components/molecules/DataTable';
import LinkButton from '../../components/atoms/LinkButton';
import { useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import BadgeIcon from '@mui/icons-material/Badge';
import DescriptionIcon from '@mui/icons-material/Description';
import SecurityIcon from '@mui/icons-material/Security';
import BarChartIcon from '@mui/icons-material/BarChart';
import PeopleIcon from '@mui/icons-material/People';
import Chip from '@mui/material/Chip';
import Divider from '@mui/material/Divider';

function RoleDetailTemplate({ role, users, stats, loading, error, roleId }) {
    const navigate = useNavigate();

    const getPriorityColor = (priority) => {
        const colors = {
            'Administrador': 'error',
            'Usuario': 'primary',
            'Invitado': 'default'
        };
        return colors[priority] || 'default';
    };

    const userColumns = [
        {
            label: 'Usuario',
            field: 'username',
            render: (value, row) => (
                <LinkButton
                    onClick={(e) => {
                        e.stopPropagation();
                        navigate(`/users/${row.id}`);
                    }}
                >
                    {value || '-'}
                </LinkButton>
            )
        },
        {
            label: 'Nombre',
            field: 'first_name',
            render: (value, row) => {
                if (row.first_name && row.last_name) {
                    return `${row.first_name} ${row.last_name}`;
                }
                return row.first_name || row.last_name || '-';
            }
        },
        { label: 'Email', field: 'email' },
        {
            label: 'Estado',
            field: 'is_active',
            render: (value) => (
                <Chip
                    label={value ? 'Activo' : 'Inactivo'}
                    size="small"
                    color={value ? 'success' : 'default'}
                    variant="outlined"
                />
            )
        },
    ];

    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                {/* Header con botón de regreso */}
                <Box sx={{ mb: 4 }}>
                    <CustomButton
                        startIcon={<ArrowBackIcon />}
                        onClick={() => navigate('/roles')}
                        sx={{ mb: 2 }}
                    >
                        Volver a Roles
                    </CustomButton>
                    <CustomTypography customVariant="pageTitle" sx={{ mb: 1 }}>
                        {role?.name || 'Detalle de Rol'}
                    </CustomTypography>
                </Box>

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && role && (
                        <>
                            {/* Información principal del rol */}
                            <Grid container spacing={3} sx={{ mb: 4 }}>
                                <Grid item xs={12} md={8}>
                                    {/* Tarjeta de información del rol */}
                                    <Card sx={{ p: 3, mb: 3 }}>
                                        <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                            <BadgeIcon />
                                            Información del Rol
                                        </CustomTypography>
                                        <Divider sx={{ mb: 3 }} />
                                        
                                        <Grid container spacing={3}>
                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Nombre"
                                                    value={role.name || '-'}
                                                    icon={<BadgeIcon fontSize="small" />}
                                                />
                                            </Grid>
                                            
                                            {role.description && (
                                                <Grid item xs={12}>
                                                    <InfoField
                                                        label="Descripción"
                                                        value={role.description}
                                                        icon={<DescriptionIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}

                                            <Grid item xs={12} sm={6}>
                                                <Box>
                                                    <CustomTypography variant="body2" sx={{ mb: 1, fontWeight: 500 }}>
                                                        Nivel de Acceso
                                                    </CustomTypography>
                                                    <Chip
                                                        label={role.priority || '-'}
                                                        icon={<SecurityIcon />}
                                                        color={getPriorityColor(role.priority)}
                                                        variant="outlined"
                                                    />
                                                </Box>
                                            </Grid>

                                            {role.permissions && role.permissions.length > 0 && (
                                                <Grid item xs={12}>
                                                    <Box>
                                                        <CustomTypography variant="body2" sx={{ mb: 1, fontWeight: 500 }}>
                                                            Permisos
                                                        </CustomTypography>
                                                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                                                            {role.permissions.map((permission, index) => (
                                                                <Chip
                                                                    key={index}
                                                                    label={permission}
                                                                    size="small"
                                                                    variant="outlined"
                                                                />
                                                            ))}
                                                        </Box>
                                                    </Box>
                                                </Grid>
                                            )}
                                        </Grid>
                                    </Card>

                                    {/* Tabla de usuarios con este rol */}
                                    {users && users.length > 0 && (
                                        <Card sx={{ p: 3 }}>
                                            <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                                <PeopleIcon />
                                                Usuarios con este Rol
                                            </CustomTypography>
                                            <Divider sx={{ mb: 3 }} />
                                            
                                            <DataTable
                                                columns={userColumns}
                                                rows={users}
                                                emptyMessage="No hay usuarios con este rol."
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
                                                label="Total de Usuarios"
                                                value={stats.totalUsers || 0}
                                                color="primary.main"
                                            />
                                            
                                            <StatItem
                                                label="Usuarios Activos"
                                                value={stats.activeUsers || 0}
                                                color="success.main"
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

export default RoleDetailTemplate;

