// frontend\src\containers\LoginContainer.js

import { useState, useEffect } from 'react';
import { loginUser } from '../services/authService';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../services/auth/AuthContext';

import CookieUtils from '../utils/cookies/CookieUtils'; // Asegúrate de usar la ruta correcta a tu archivo CookieUtils.js

function LoginContainer() {
    const navigate = useNavigate();
    const { login } = useAuth(); // Cambiado a 'login' para manejar tanto el token como los datos del usuario

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
            // Redirecciona al usuario, guarda el token, etc.
            login(data.id, data.username, data.role); // Almacena los datos del usuario en el contexto

            // Al establecer la cookie
            if (rememberMe) {
                var jsonDecoded = {
                    'username': username, 'password': password
                };
                CookieUtils.setUserCookie(jsonDecoded);
            } else {
                CookieUtils.removeUserCookie();
            }

            handleLoginSuccess(data.role);

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
