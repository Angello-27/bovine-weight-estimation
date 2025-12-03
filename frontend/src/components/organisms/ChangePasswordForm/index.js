// frontend/src/components/organisms/ChangePasswordForm/index.js

import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import InputField from '../../atoms/InputFieldForm';
import CustomButton from '../../atoms/CustomButton';
import LockIcon from '@mui/icons-material/Lock';
import LockOpenIcon from '@mui/icons-material/LockOpen';
import VpnKeyIcon from '@mui/icons-material/VpnKey';

function ChangePasswordForm({ formData, errors = {}, onInputChange, onSubmit, onCancel }) {
    return (
        <Box component="form" method="post" onSubmit={onSubmit} sx={{ width: '100%' }}>
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <InputField
                        xs={12}
                        label="Contraseña Actual"
                        name="currentPassword"
                        type="password"
                        value={formData.currentPassword || ''}
                        onChange={onInputChange}
                        required
                        error={!!errors.currentPassword}
                        helperText={errors.currentPassword}
                        startIcon={<LockIcon />}
                    />
                </Grid>
                <Grid item xs={12}>
                    <InputField
                        xs={12}
                        label="Nueva Contraseña"
                        name="newPassword"
                        type="password"
                        value={formData.newPassword || ''}
                        onChange={onInputChange}
                        required
                        error={!!errors.newPassword}
                        helperText={errors.newPassword}
                        startIcon={<LockOpenIcon />}
                    />
                </Grid>
                <Grid item xs={12}>
                    <InputField
                        xs={12}
                        label="Confirmar Nueva Contraseña"
                        name="confirmPassword"
                        type="password"
                        value={formData.confirmPassword || ''}
                        onChange={onInputChange}
                        required
                        error={!!errors.confirmPassword}
                        helperText={errors.confirmPassword}
                        startIcon={<VpnKeyIcon />}
                    />
                </Grid>
            </Grid>
            <Box sx={{ mt: 4, mb: 2, display: 'flex', gap: 2 }}>
                <CustomButton
                    type="button"
                    variant="outlined"
                    fullWidth
                    onClick={onCancel}
                >
                    Cancelar
                </CustomButton>
                <CustomButton type="submit" fullWidth variant="contained">
                    Cambiar Contraseña
                </CustomButton>
            </Box>
        </Box>
    );
}

export default ChangePasswordForm;

