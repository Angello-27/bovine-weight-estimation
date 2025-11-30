// frontend/src/components/molecules/ProtectedRoute/index.js
import React from 'react';
import { Navigate } from 'react-router-dom';
import { getCurrentUser } from '../../../services/auth/authService';

/**
 * Componente para proteger rutas que requieren autenticación
 * 
 * Según Atomic Design, este es un "Molecule" porque:
 * - Combina múltiples elementos (Navigate, lógica de autenticación)
 * - Tiene comportamiento propio (validación de roles)
 * - Es reutilizable en múltiples contextos
 * 
 * @param {Object} props
 * @param {React.ReactNode} props.children - Componente hijo a renderizar si está autenticado
 * @param {Array<string>} props.requiredRoles - Roles requeridos (opcional). Si está vacío, solo requiere autenticación
 * @returns {React.ReactElement}
 */
const ProtectedRoute = ({ children, requiredRoles = [] }) => {
    const user = getCurrentUser();

    // Si no hay usuario autenticado, redirigir a login
    if (!user) {
        return <Navigate to="/login" replace />;
    }

    // Si se especifican roles requeridos, verificar que el usuario tenga uno de ellos
    if (requiredRoles.length > 0) {
        const userRole = user.role?.name || user.role?.priority || user.role;
        
        // Si el usuario no tiene un rol válido o no coincide con los requeridos
        if (!userRole || !requiredRoles.includes(userRole)) {
            // Redirigir a dashboard con mensaje de acceso denegado (opcional)
            return <Navigate to="/home" replace />;
        }
    }

    return <>{children}</>;
};

export default ProtectedRoute;

