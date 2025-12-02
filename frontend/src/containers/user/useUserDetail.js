// frontend/src/containers/user/useUserDetail.js

import { useState, useEffect } from 'react';
import { getUserById } from '../../services/user/getUserById';
import { getRoleById } from '../../services/role/getRoleById';
import { getFarmById } from '../../services/farm/getFarmById';
import { getFarmsByCriteria } from '../../services/farm/getFarmsByCriteria';

/**
 * Hook para obtener datos de detalle de un usuario y sus relaciones
 * @param {string} userId - ID del usuario
 */
function useUserDetail(userId) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [ownedFarms, setOwnedFarms] = useState([]);
    
    // Estadísticas relacionadas
    const [stats, setStats] = useState({
        ownedFarms: 0,
    });

    useEffect(() => {
        async function fetchData() {
            if (!userId) {
                setError('ID de usuario no proporcionado');
                setLoading(false);
                return;
            }

            try {
                setLoading(true);
                setError(null);

                // Obtener datos del usuario
                const userData = await getUserById(userId);
                
                // Si hay role_id, obtener información del rol
                if (userData.role_id) {
                    try {
                        const roleData = await getRoleById(userData.role_id);
                        userData.role = roleData;
                    } catch (err) {
                        console.warn('No se pudo obtener información del rol:', err);
                    }
                }
                
                // Si hay farm_id, obtener información de la hacienda
                if (userData.farm_id) {
                    try {
                        const farmData = await getFarmById(userData.farm_id);
                        userData.farm = farmData;
                    } catch (err) {
                        console.warn('No se pudo obtener información de la hacienda:', err);
                    }
                }
                
                setUser(userData);

                // Obtener farms donde el usuario es propietario usando el endpoint by-criteria
                try {
                    // Obtener farms con paginación (el backend tiene límite de 100 por petición)
                    let allFarms = [];
                    let totalFarms = 0;
                    let skip = 0;
                    const limit = 100; // Límite máximo del backend
                    
                    // Primera petición para obtener el total
                    const firstPage = await getFarmsByCriteria(
                        { owner_id: userId },
                        { skip: 0, limit: limit }
                    );
                    
                    totalFarms = firstPage?.total || 0;
                    const firstPageFarms = firstPage?.farms || [];
                    allFarms = [...allFarms, ...firstPageFarms];
                    
                    // Si hay más farms, obtener las siguientes páginas
                    if (totalFarms > limit) {
                        skip = limit;
                        while (skip < totalFarms && allFarms.length < 500) { // Limitar a 500 farms para no sobrecargar
                            const nextPage = await getFarmsByCriteria(
                                { owner_id: userId },
                                { skip: skip, limit: limit }
                            );
                            const nextPageFarms = nextPage?.farms || [];
                            allFarms = [...allFarms, ...nextPageFarms];
                            skip += limit;
                            
                            if (nextPageFarms.length === 0) break; // No hay más farms
                        }
                    }
                    
                    setOwnedFarms(allFarms);
                    setStats({
                        ownedFarms: totalFarms, // Total real del backend
                    });
                } catch (statsError) {
                    console.error('Error al obtener farms del usuario:', statsError);
                    setOwnedFarms([]);
                    setStats({
                        ownedFarms: 0,
                    });
                    // No detenemos la carga si fallan las farms
                }

            } catch (err) {
                setError(err?.message || 'Error al cargar los datos del usuario');
                console.error('Error al cargar detalle de usuario:', err);
            } finally {
                setLoading(false);
            }
        }

        fetchData();
    }, [userId]);

    return {
        user,
        ownedFarms,
        stats,
        loading,
        error,
        userId
    };
}

export default useUserDetail;

