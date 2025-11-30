// components/atoms/LogoutButton/index.js
import Button from '@mui/material/Button';
import { useAuth } from '../../../services/auth/AuthContext';
import { logoutUser } from '../../../services/auth/authService';

function LogoutButton() {
    const { logout } = useAuth();

    const handleLogout = () => {
        // Limpiar contexto de sesión
        logout();
        // Limpiar localStorage y redirigir (logoutUser ya hace esto)
        logoutUser();
    };

    return <Button
        variant="outlined" size="medium" onClick={handleLogout}
        // Añadir estilos para el estado hover
        sx={{
            '&:hover': {
                backgroundColor: 'primary.main', // Cambia el color de fondo a primary.main en hover
                color: 'white', // Cambia el color del texto a blanco en hover
            }
        }}
    >Logout</Button>;
}

export default LogoutButton;
