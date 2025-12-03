// frontend/src/components/organisms/CreateProfile/index.js

import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import InputField from '../../atoms/InputFieldForm';
import CustomButton from '../../atoms/CustomButton';
import PersonIcon from '@mui/icons-material/Person';
import EmailIcon from '@mui/icons-material/Email';
import AccountBoxIcon from '@mui/icons-material/AccountBox';

function CreateProfile({ formData, errors = {}, onInputChange, onSubmit }) {
    return (
        <Box component="form" method="post" onSubmit={onSubmit} sx={{ width: '100%' }}>
            <Grid container spacing={3}>
                <Grid item xs={12} sm={6}>
                    <InputField
                        xs={12}
                        label="Nombre"
                        name="first_name"
                        value={formData.first_name || ''}
                        onChange={onInputChange}
                        error={!!errors.first_name}
                        helperText={errors.first_name}
                        startIcon={<PersonIcon />}
                    />
                </Grid>
                <Grid item xs={12} sm={6}>
                    <InputField
                        xs={12}
                        label="Apellido"
                        name="last_name"
                        value={formData.last_name || ''}
                        onChange={onInputChange}
                        error={!!errors.last_name}
                        helperText={errors.last_name}
                        startIcon={<AccountBoxIcon />}
                    />
                </Grid>
                <Grid item xs={12}>
                    <InputField
                        xs={12}
                        label="Email"
                        name="email"
                        type="email"
                        value={formData.email || ''}
                        onChange={onInputChange}
                        required
                        error={!!errors.email}
                        helperText={errors.email}
                        startIcon={<EmailIcon />}
                    />
                </Grid>
            </Grid>
            <Box sx={{ mt: 4, mb: 2 }}>
                <CustomButton type="submit" fullWidth variant="contained">
                    Guardar Cambios
                </CustomButton>
            </Box>
        </Box>
    );
}

export default CreateProfile;

