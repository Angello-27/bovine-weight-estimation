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

                // Obtener usuarios con este rol usando el endpoint de criterios
                try {
                    // Obtener usuarios con paginación (el backend tiene límite de 100 por petición)
                    let allUsers = [];
                    let totalUsers = 0;
                    let skip = 0;
                    const limit = 100; // Límite máximo del backend
                    
                    // Primera petición para obtener el total
                    const firstPage = await getUsersByCriteria(
                        { role_id: roleId },
                        { skip: 0, limit: limit }
                    );
                    
                    totalUsers = firstPage?.total || 0;
                    const firstPageUsers = firstPage?.users || [];
                    allUsers = [...allUsers, ...firstPageUsers];
                    
                    // Si hay más usuarios, obtener las siguientes páginas
                    if (totalUsers > limit) {
                        skip = limit;
                        while (skip < totalUsers && allUsers.length < 500) { // Limitar a 500 usuarios para no sobrecargar
                            const nextPage = await getUsersByCriteria(
                                { role_id: roleId },
                                { skip: skip, limit: limit }
                            );
                            const nextPageUsers = nextPage?.users || [];
                            allUsers = [...allUsers, ...nextPageUsers];
                            skip += limit;
                            
                            if (nextPageUsers.length === 0) break; // No hay más usuarios
                        }
                    }
                    
                    // Calcular usuarios activos del array obtenido
                    const activeUsersCount = allUsers.filter(u => u.is_active === true).length;
                    
                    setUsers(allUsers);
                    setStats({
                        totalUsers: totalUsers, // Total real del backend
                        activeUsers: activeUsersCount,
                    });
                } catch (usersError) {
                    console.error('❌ Error al obtener usuarios del rol:', {
                        error: usersError,
                        message: usersError?.message,
                        stack: usersError?.stack,
                        response: usersError?.response,
                        responseData: usersError?.response?.data,
                        responseStatus: usersError?.response?.status,
                        roleId: roleId
                    });
                    setUsers([]);
                    setStats({
                        totalUsers: 0,
                        activeUsers: 0,
                    });
                    // No detenemos la carga si falla obtener usuarios, solo mostramos 0
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

