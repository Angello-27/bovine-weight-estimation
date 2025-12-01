// frontend/src/containers/role/useRoleDetail.js

import { useState, useEffect } from 'react';
import { getRoleById } from '../../services/role/getRoleById';
import { getUsersByCriteria } from '../../services/user/getUsersByCriteria';

/**
 * Hook para obtener datos de detalle de un rol y usuarios asociados
 * @param {string} roleId - ID del rol
 */
function useRoleDetail(roleId) {
    const [role, setRole] = useState(null);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    
    // Estadísticas relacionadas
    const [stats, setStats] = useState({
        totalUsers: 0,
        activeUsers: 0,
    });

    useEffect(() => {
        async function fetchData() {
            if (!roleId) {
                setError('ID de rol no proporcionado');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                setError(null);

                // Obtener datos del rol
                const roleData = await getRoleById(roleId);
                setRole(roleData);

                // Obtener usuarios con este rol usando el nuevo endpoint de criterios
                try {
                    // Consulta 1: Obtener todos los usuarios con este rol (para la tabla)
                    const usersData = await getUsersByCriteria(
                        { role_id: roleId },
                        { skip: 0, limit: 1000 } // Obtener hasta 1000 usuarios para mostrar en la tabla
                    );
                    const usersWithRole = usersData.users || [];
                    const totalUsers = usersData.total || 0; // Usar el total del backend, no el length del array
                    
                    setUsers(usersWithRole);

                    // Consulta 2: Obtener el total exacto de usuarios activos con este rol
                    let totalActiveUsers = 0;
                    try {
                        const activeUsersData = await getUsersByCriteria(
                            { role_id: roleId, is_active: true },
                            { skip: 0, limit: 1 } // Solo necesitamos el total, no los datos
                        );
                        totalActiveUsers = activeUsersData.total || 0;
                    } catch (activeUsersError) {
                        console.warn('Error al obtener total de usuarios activos:', activeUsersError);
                        // Si falla, contar los activos del array obtenido como fallback
                        totalActiveUsers = usersWithRole.filter(u => u.is_active === true).length;
                    }

                    setStats({
                        totalUsers: totalUsers, // Total real del backend
                        activeUsers: totalActiveUsers, // Total real de usuarios activos del backend
                    });
                } catch (usersError) {
                    console.error('Error al obtener usuarios del rol:', usersError);
                    setUsers([]);
                    setStats({
                        totalUsers: 0,
                        activeUsers: 0,
                    });
                    // No detenemos la carga si falla obtener usuarios
                }

            } catch (err) {
                setError(err?.message || 'Error al cargar los datos del rol');
                console.error('Error al cargar detalle de rol:', err);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [roleId]);

    return {
        role,
        users,
        stats,
        loading,
        error,
        roleId
    };
}

export default useRoleDetail;

