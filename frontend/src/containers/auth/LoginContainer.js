// frontend/src/containers/auth/LoginContainer.js

import { useState, useEffect } from 'react';
import { loginUser } from '../../services/auth/authService';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../services/auth/AuthContext';

import CookieUtils from '../../utils/cookies/CookieUtils'; // Asegúrate de usar la ruta correcta a tu archivo CookieUtils.js

function LoginContainer() {
    const navigate = useNavigate();
    const { login, setAuthUser } = useAuth(); // setAuthUser es la nueva función recomendada

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [rememberMe, setRememberMe] = useState(false); // Nuevo estado para manejar "Remember Me"

    const handleUsernameChange = (e) => setUsername(e.target.value);
    const handlePasswordChange = (e) => setPassword(e.target.value);
    const handleRememberMeChange = (e) => setRememberMe(e.target.checked); // Nueva función de manejo para "Remember Me"
    const handleLoginSuccess = (role) => {
        // Aquí puedes usar el parámetro 'role' según lo necesites
        // Por ejemplo, podrías hacer diferentes acciones dependiendo del rol del usuario

        if (role === "Invitado") {
            navigate('/map');
        } else {
            navigate('/home');
        }
    }; // Navega a la otra ruta cuando el inicio de sesión sea exitoso


    // Al leer la cookie
    useEffect(() => {
        const parsedUser = CookieUtils.getUserCookie();
        if (parsedUser) {
            setUsername(parsedUser.username);
            setPassword(parsedUser.password);
            setRememberMe(true);
        }
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null); // Resetea el estado de error antes de hacer la llamada a la API.

        try {
            const data = await loginUser({ username, password });
            console.log('Usuario autenticado:', data);
            
            // El token y usuario ya se guardaron en localStorage en authService
            // Actualizar el contexto para que los componentes reactivos se actualicen
            // setAuthUser sincroniza el contexto con authService (localStorage)
            if (setAuthUser) {
                setAuthUser(data);
            }
            
            // Extraer el nombre del rol para handleLoginSuccess
            const roleName = data.role?.name || data.role?.priority || data.role;

            // Al establecer la cookie
            if (rememberMe) {
                var jsonDecoded = {
                    'username': username, 'password': password
                };
                CookieUtils.setUserCookie(jsonDecoded);
            } else {
                CookieUtils.removeUserCookie();
            }

            handleLoginSuccess(roleName);

        } catch (error) {
            setError(error.message); // Establece el mensaje de error para mostrarlo al usuario.
        }
    };

    return {
        username,
        password,
        error,
        rememberMe, // Se devuelve rememberMe
        handleUsernameChange,
        handlePasswordChange,
        handleRememberMeChange, // Se devuelve handleRememberMeChange
        handleSubmit
    };
}

export default LoginContainer;

