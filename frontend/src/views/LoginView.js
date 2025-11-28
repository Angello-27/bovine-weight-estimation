// src/views/LoginView.js

import React from 'react';
import LoginContainer from '../containers/LoginContainer';
import LoginTemplate from '../templates/LoginTemplate';

function LoginView() {

    const loginProps = LoginContainer(); // Usamos LoginContainer para obtener las props

    return (
        <LoginTemplate {...loginProps} /> // Pasamos las props al LoginTemplate
    );
}

export default LoginView;
