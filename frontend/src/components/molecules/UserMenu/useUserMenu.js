// frontend/src/components/molecules/UserMenu/useUserMenu.js
/**
 * Hook personalizado para manejar el estado y lógica del UserMenu
 */

import { useState } from 'react';
import { useAuth } from '../../../services/auth/AuthContext';
import { logoutUser } from '../../../services/auth/authService';

export const useUserMenu = () => {
    const { user, username, role, logout } = useAuth();
    const [anchorEl, setAnchorEl] = useState(null);
    const open = Boolean(anchorEl);

    const displayName = user?.full_name || username || 'Usuario';
    const userRole = role || user?.role?.name || user?.role?.priority || 'Usuario';

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleLogout = () => {
        handleClose();
        logout(); // Limpiar contexto
        logoutUser(); // Limpiar localStorage y redirigir
    };

    // Obtener iniciales para el avatar
    const getInitials = (name) => {
        if (!name) return 'U';
        const parts = name.trim().split(' ');
        if (parts.length >= 2) {
            return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
        }
        return name.substring(0, 2).toUpperCase();
    };

    return {
        displayName,
        userRole,
        anchorEl,
        open,
        handleClick,
        handleClose,
        handleLogout,
        getInitials,
    };
};

