// frontend/src/templates/profile/ProfileTemplate.js

import React from 'react';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Card from '../../components/atoms/Card';
import CustomTypography from '../../components/atoms/CustomTypography';
import CustomButton from '../../components/atoms/CustomButton';
import LoadingState from '../../components/molecules/LoadingState';
import ErrorState from '../../components/molecules/ErrorState';
import PageHeaderCentered from '../../components/molecules/PageHeaderCentered';
import CreateProfile from '../../components/organisms/CreateProfile';
import ChangePasswordForm from '../../components/organisms/ChangePasswordForm';
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import PersonIcon from '@mui/icons-material/Person';
import LockIcon from '@mui/icons-material/Lock';
import EmailIcon from '@mui/icons-material/Email';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

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
    return (
        <Box sx={{ width: '100%' }}>
            <Container maxWidth="md" sx={{ py: 3, px: { xs: 2, sm: 3 } }}>
                <PageHeaderCentered
                    title="Mi Perfil"
                    description="Gestiona tu información personal y configuración de cuenta"
                />

                <ErrorState error={error} />

                <LoadingState loading={loading}>
                    {!error && user && (
                        <>
                            {/* Información del Usuario */}
                            <Card sx={{ p: 3, mb: 3 }}>
                                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                                    <AccountCircleIcon sx={{ fontSize: 40, mr: 2, color: 'primary.main' }} />
                                    <Box>
                                        <CustomTypography variant="h6">
                                            {user.first_name && user.last_name
                                                ? `${user.first_name} ${user.last_name}`
                                                : user.username}
                                        </CustomTypography>
                                        <CustomTypography variant="body2" color="text.secondary">
                                            {user.email}
                                        </CustomTypography>
                                        {user.role && (
                                            <CustomTypography variant="caption" color="primary.main" sx={{ mt: 0.5 }}>
                                                {user.role}
                                            </CustomTypography>
                                        )}
                                    </Box>
                                </Box>
                            </Card>

                            {/* Formulario de Perfil */}
                            <Card sx={{ p: 3, mb: 3 }}>
                                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                                    <PersonIcon sx={{ mr: 1, color: 'primary.main' }} />
                                    <CustomTypography variant="h6">
                                        Información Personal
                                    </CustomTypography>
                                </Box>
                                <CreateProfile
                                    formData={profileFormData}
                                    errors={profileFormErrors}
                                    onInputChange={handleProfileChange}
                                    onSubmit={handleProfileSubmit}
                                />
                            </Card>

                            {/* Cambio de Contraseña */}
                            <Card sx={{ p: 3 }}>
                                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                        <LockIcon sx={{ mr: 1, color: 'primary.main' }} />
                                        <CustomTypography variant="h6">
                                            Cambiar Contraseña
                                        </CustomTypography>
                                    </Box>
                                    <CustomButton
                                        variant="outlined"
                                        onClick={onShowPasswordForm}
                                    >
                                        Cambiar Contraseña
                                    </CustomButton>
                                </Box>
                                <CustomTypography variant="body2" color="text.secondary">
                                    Asegúrate de usar una contraseña segura con al menos 6 caracteres.
                                </CustomTypography>
                            </Card>

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

