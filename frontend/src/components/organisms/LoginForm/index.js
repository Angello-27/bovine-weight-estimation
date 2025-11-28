// src/components/LoginForm/index.js

import * as React from 'react';
import Box from '@mui/material/Box';
import EmailInput from '../../molecules/EmailInput';
import PasswordInput from '../../molecules/PasswordInput';
import RememberMe from '../../molecules/RememberMe';
import Copyright from '../../atoms/Copyright';
import CustomButton from '../../atoms/CustomButton';

function LoginForm({ username, password, onUsernameChange, onPasswordChange, onSubmit, rememberMe, onRememberMeChange }) {
    return (
        <Box component="form" noValidate onSubmit={onSubmit} sx={{ mt: 1 }}>
            <EmailInput value={username} onChange={onUsernameChange} />
            <PasswordInput value={password} onChange={onPasswordChange} />
            <RememberMe onRememberMeChange={onRememberMeChange} rememberMe={rememberMe} /> {/* Pasas el manejador de cambios a RememberMe */}
            <CustomButton type="submit" fullWidth variant="contained" sx={{ mt: 5, mb: 2 }}>
                Sign In
            </CustomButton>
            <Copyright sx={{ mt: 5 }} />
        </Box>
    );
}

export default LoginForm;
