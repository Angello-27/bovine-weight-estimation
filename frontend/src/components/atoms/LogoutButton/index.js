// components/atoms/LogoutButton/index.js
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../../services/auth/AuthContext';

function LogoutButton() {
    const { logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
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
