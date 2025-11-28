// src/templates/LoginTemplate.js
import React from 'react';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider } from '@mui/material/styles';
import { useTheme } from '../config/theme/ThemeContext'; // Asegúrate de importar tu tema


import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import BackgroundImage from '../components/atoms/BackgroundImage';
import LoginForm from '../components/organisms/LoginForm';
import ErrorAlert from '../components/atoms/ErrorAlert';
import FormHeader from '../components/atoms/FormHeader';
import { StyledSignInContainer } from '../components/organisms/LoginForm/BoxLogin';
import ToggleThemeButton from '../components/atoms/ToggleThemeButton'; // Importa el componente del botón

function LoginTemplate(props) {
    const { currentTheme } = useTheme();

    return (
        <ThemeProvider theme={currentTheme}>
            <CssBaseline />
            <Grid container component="main" sx={{ height: '100vh' }}>
                <BackgroundImage />
                <Grid item xs={12} sm={8} md={5} component={Paper} elevation={3} square>
                    <ToggleThemeButton />
                    <StyledSignInContainer>
                        <FormHeader title={'login'}>
                            <LockOutlinedIcon />
                        </FormHeader>
                        <LoginForm
                            username={props.username}
                            password={props.password}
                            onUsernameChange={props.handleUsernameChange}
                            onPasswordChange={props.handlePasswordChange}
                            onSubmit={props.handleSubmit}
                            rememberMe={props.rememberMe}
                            onRememberMeChange={props.handleRememberMeChange}
                        />
                        <ErrorAlert errorMessage={props.error} />
                        {/* Y cualquier otro componente o contenido que quieras incluir */}
                    </StyledSignInContainer>
                </Grid>
            </Grid>
        </ThemeProvider>
    );
}

export default LoginTemplate;
