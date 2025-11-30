// frontend/src/services/auth/AuthContext.js
/**
 * Context API para autenticación
 * 
 * IMPORTANTE: Este contexto usa authService como fuente única de verdad.
 * NO mantiene su propio storage, solo sincroniza con localStorage a través de authService.
 * 
 * Diferencia con authService:
 * - authService: Casos de uso de autenticación (login, logout, validación) → localStorage
 * - AuthContext: Estado reactivo compartido entre componentes → sincroniza con authService
 */

import React, { createContext, useContext, useEffect, useState } from 'react';
import { getCurrentUser, logoutUser as serviceLogout } from './authService';

const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) throw new Error('useAuth must be used within AuthProvider');
    return context;
};

export const AuthProvider = ({ children }) => {
    // Estado sincronizado con authService (localStorage)
    const [user, setUser] = useState(() => {
        return getCurrentUser(); // Leer desde localStorage al inicializar
    });

    // Sincronizar con cambios en localStorage (por si hay cambios externos)
    useEffect(() => {
        const handleStorageChange = () => {
            setUser(getCurrentUser());
        };

        // Escuchar cambios en localStorage
        window.addEventListener('storage', handleStorageChange);
        
        // También verificar periódicamente (por cambios en la misma pestaña)
        const interval = setInterval(() => {
            const currentUser = getCurrentUser();
            if (JSON.stringify(currentUser) !== JSON.stringify(user)) {
                setUser(currentUser);
            }
        }, 1000);

        return () => {
            window.removeEventListener('storage', handleStorageChange);
            clearInterval(interval);
        };
    }, [user]);

    /**
     * Actualiza el estado del usuario (llamado después de login)
     * @param {Object} userData - Datos del usuario desde authService
     */
    const setAuthUser = (userData) => {
        // authService ya guardó en localStorage, solo actualizamos el estado
        setUser(getCurrentUser());
    };

    /**
     * Cierra sesión (usa authService como fuente única de verdad)
     */
    const logout = () => {
        serviceLogout(); // Limpia localStorage y redirige
        setUser(null); // Actualizar estado local
    };

    // Valores derivados para compatibilidad con código existente
    const id = user?.id || null;
    const username = user?.username || null;
    const role = user?.role?.name || user?.role?.priority || user?.role || null;

    // Función login mantenida para compatibilidad (pero ya no guarda en sessionStorage)
    const login = (id, username, role) => {
        // No hace nada directamente, el estado se actualiza desde authService
        // Esto se mantiene solo por compatibilidad con código existente
        setUser(getCurrentUser());
    };

    return (
        <AuthContext.Provider value={{ 
            id, 
            username, 
            role, 
            user, // Objeto completo del usuario
            login, 
            logout,
            setAuthUser, // Nueva función para actualizar después de login
            isAuthenticated: !!user // Helper
        }}>
            {children}
        </AuthContext.Provider>
    );
};
