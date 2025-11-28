// src/components/LoginForm/index.js

import * as React from 'react';
import Box from '@mui/material/Box';
import EmailInput from '../../molecules/EmailInput';
import PasswordInput from '../../molecules/PasswordInput';
import CustomButton from '../../atoms/CustomButton';

import Grid from '@mui/material/Grid';
import PolygonInput from '../../molecules/PolygonInput';
import ZoomInput from '../../molecules/ZoomInput';

function RegisterForm({ username, password, onUsernameChange, onPasswordChange, onSubmit, rememberMe, onRememberMeChange }) {
    return (
        <Box component="form" noValidate onSubmit={onSubmit} sx={{ mt: 1 }}>
            <EmailInput value={username} onChange={onUsernameChange} />
            <PasswordInput value={password} onChange={onPasswordChange} />
            <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                    <PolygonInput />
                </Grid>
                <Grid item xs={12} sm={6}>
                    <ZoomInput />
                </Grid>
            </Grid>
            <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                    <CustomButton type="submit" fullWidth variant="contained" sx={{ mt: 5, mb: 2 }}>
                        Cancelar
                    </CustomButton>
                </Grid>
                <Grid item xs={12} sm={6}>
                    <CustomButton type="submit" fullWidth variant="contained" sx={{ mt: 5, mb: 2 }}>
                        Guardar
                    </CustomButton>
                </Grid>
            </Grid>

        </Box>
    );
}

export default RegisterForm
