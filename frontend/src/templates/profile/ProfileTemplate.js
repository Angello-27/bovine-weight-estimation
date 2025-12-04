// frontend/src/templates/profile/ProfileTemplate.js

import React from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Divider from '@mui/material/Divider';
import Card from '../../components/atoms/Card';
import CustomTypography from '../../components/atoms/CustomTypography';
import CustomButton from '../../components/atoms/CustomButton';
import InfoField from '../../components/atoms/InfoField';
import LoadingState from '../../components/molecules/LoadingState';
import ErrorState from '../../components/molecules/ErrorState';
import CreateProfile from '../../components/organisms/CreateProfile';
import ChangePasswordForm from '../../components/organisms/ChangePasswordForm';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import PersonIcon from '@mui/icons-material/Person';
import LockIcon from '@mui/icons-material/Lock';
import EmailIcon from '@mui/icons-material/Email';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import BadgeIcon from '@mui/icons-material/Badge';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import CancelIcon from '@mui/icons-material/Cancel';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import UpdateIcon from '@mui/icons-material/Update';
import LoginIcon from '@mui/icons-material/Login';
import FingerprintIcon from '@mui/icons-material/Fingerprint';

function ProfileTemplate({
    user,
    loading,
    error,
    profileFormData,
    profileFormErrors,
    handleProfileChange,
    handleProfileSubmit,
    passwordFormData,
    passwordFormErrors,
    handlePasswordChange,
    handlePasswordSubmit,
    showPasswordForm,
    onShowPasswordForm,
    onClosePasswordForm,
}) {
    // Función para formatear fechas
    const formatDate = (dateString) => {
        if (!dateString) return '-';
        try {
            const date = new Date(dateString);
            return date.toLocaleString('es-ES', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
            });
        } catch (error) {
            return dateString;
        }
    };

    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="xl" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                {/* Header */}
                <Box sx={{ mb: 4 }}>
                    <CustomTypography customVariant="pageTitle" sx={{ mb: 1 }}>
                        Mi Perfil
                    </CustomTypography>
                    <CustomTypography variant="body2" color="text.secondary">
                        Gestiona tu información personal y configuración de cuenta
                    </CustomTypography>
                </Box>

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && user && (
                        <>
                            <Grid container spacing={3} sx={{ mb: 4 }}>
                                <Grid item xs={12} md={8}>
                                    {/* Información del Usuario */}
                                    <Card sx={{ p: 3, mb: 3 }}>
                                        <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                            <AccountCircleIcon />
                                            Información del Usuario
                                        </CustomTypography>
                                        <Divider sx={{ mb: 3 }} />

                                        <Grid container spacing={3}>

                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Nombre de Usuario"
                                                    value={user.username}
                                                    icon={<PersonIcon fontSize="small" />}
                                                />
                                            </Grid>

                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Correo Electrónico"
                                                    value={user.email}
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
                                                    <InfoField
                                                        label="Rol"
                                                        value={user.role}
                                                        icon={<BadgeIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}

                                            <Grid item xs={12} sm={6}>
                                                <InfoField
                                                    label="Estado"
                                                    value={user.is_active ? 'Activo' : 'Inactivo'}
                                                    icon={user.is_active ? <CheckCircleIcon fontSize="small" sx={{ color: 'success.main' }} /> : <CancelIcon fontSize="small" sx={{ color: 'error.main' }} />}
                                                />
                                            </Grid>

                                            {user.is_superuser !== undefined && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Super Usuario"
                                                        value={user.is_superuser ? 'Sí' : 'No'}
                                                        icon={<AdminPanelSettingsIcon fontSize="small" sx={{ color: user.is_superuser ? 'warning.main' : 'text.secondary' }} />}
                                                    />
                                                </Grid>
                                            )}

                                            {user.created_at && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Fecha de Creación"
                                                        value={formatDate(user.created_at)}
                                                        icon={<CalendarTodayIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}

                                            {user.last_updated && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Última Actualización"
                                                        value={formatDate(user.last_updated)}
                                                        icon={<UpdateIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}

                                            {user.last_login && (
                                                <Grid item xs={12} sm={6}>
                                                    <InfoField
                                                        label="Último Inicio de Sesión"
                                                        value={formatDate(user.last_login)}
                                                        icon={<LoginIcon fontSize="small" />}
                                                    />
                                                </Grid>
                                            )}
                                        </Grid>
                                    </Card>

                                    {/* Formulario de Perfil */}
                                    <Card sx={{ p: 3, mb: 3 }}>
                                        <CustomTypography variant="h6" sx={{ mb: 3, display: 'flex', alignItems: 'center', gap: 1 }}>
                                            <PersonIcon />
                                            Información Personal
                                        </CustomTypography>
                                        <Divider sx={{ mb: 3 }} />
                                        <CreateProfile
                                            formData={profileFormData}
                                            errors={profileFormErrors}
                                            onInputChange={handleProfileChange}
                                            onSubmit={handleProfileSubmit}
                                        />
                                    </Card>

                                </Grid>

                                {/* Resumen */}
                                <Grid item xs={12} md={4}>

                                    {/* Cambio de Contraseña */}
                                    <Card sx={{ p: 3 }}>
                                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                                            <CustomTypography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                                <LockIcon />
                                                Cambiar Contraseña
                                            </CustomTypography>
                                            <CustomButton
                                                variant="outlined"
                                                onClick={onShowPasswordForm}
                                            >
                                                Cambiar Contraseña
                                            </CustomButton>
                                        </Box>
                                        <Divider sx={{ mb: 2 }} />
                                        <CustomTypography variant="body2" color="text.secondary">
                                            Asegúrate de usar una contraseña segura con al menos 6 caracteres.
                                        </CustomTypography>
                                    </Card>
                                </Grid>
                            </Grid>

                            {/* Dialog para Cambio de Contraseña */}
                            <Dialog
                                open={showPasswordForm}
                                onClose={onClosePasswordForm}
                                maxWidth="sm"
                                fullWidth
                                PaperProps={{
                                    sx: {
                                        borderRadius: 2,
                                    },
                                }}
                            >
                                <DialogTitle sx={{ pb: 3, pt: 4, px: 3 }}>
                                    Cambiar Contraseña
                                </DialogTitle>
                                <DialogContent sx={{ px: 3, pb: 3 }}>
                                    <ChangePasswordForm
                                        formData={passwordFormData}
                                        errors={passwordFormErrors}
                                        onInputChange={handlePasswordChange}
                                        onSubmit={handlePasswordSubmit}
                                        onCancel={onClosePasswordForm}
                                    />
                                </DialogContent>
                            </Dialog>
                        </>
                    )}
                </LoadingState>
            </Container>
        </Box>
    );
}

export default ProfileTemplate;

