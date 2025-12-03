// frontend/src/utils/cache/dashboardCache.js

/**
 * Sistema de caché para estadísticas del dashboard usando localStorage
 * 
 * Características:
 * - Almacena datos en localStorage con TTL (Time To Live)
 * - Invalida automáticamente después de X minutos
 * - Permite invalidación manual cuando se actualizan datos relacionados
 */

const CACHE_KEY = 'dashboard_stats_cache';
const CACHE_VERSION = '1.0.0';
const DEFAULT_TTL_MINUTES = 15; // 15 minutos por defecto (más corto que estimaciones porque cambia más frecuentemente)

/**
 * Obtiene el caché de estadísticas del dashboard
 * @returns {Object|null} Datos del caché o null si no existe o está expirado
 */
export const getCachedDashboardStats = () => {
    try {
        const cached = localStorage.getItem(CACHE_KEY);
        if (!cached) return null;

        const cacheData = JSON.parse(cached);
        
        // Verificar versión del caché
        if (cacheData.version !== CACHE_VERSION) {
            clearCache();
            return null;
        }

        // Verificar si el caché expiró
        const now = Date.now();
        if (cacheData.expiresAt && now > cacheData.expiresAt) {
            clearCache();
            return null;
        }

        return cacheData.data;
    } catch (error) {
        console.error('Error al leer caché de estadísticas del dashboard:', error);
        clearCache();
        return null;
    }
};

/**
 * Guarda estadísticas del dashboard en el caché
 * @param {Object} stats - Objeto con las estadísticas
 * @param {number} ttlMinutes - Tiempo de vida en minutos (opcional)
 */
export const setCachedDashboardStats = (stats, ttlMinutes = DEFAULT_TTL_MINUTES) => {
    try {
        const now = Date.now();
        const expiresAt = now + (ttlMinutes * 60 * 1000);

        const cacheData = {
            version: CACHE_VERSION,
            data: stats,
            expiresAt,
            cachedAt: now,
        };

        localStorage.setItem(CACHE_KEY, JSON.stringify(cacheData));
    } catch (error) {
        console.error('Error al guardar caché de estadísticas del dashboard:', error);
        // Si hay error (ej: localStorage lleno), limpiar caché antiguo
        try {
            clearCache();
        } catch (clearError) {
            console.error('Error al limpiar caché:', clearError);
        }
    }
};

/**
 * Limpia el caché de estadísticas del dashboard
 */
export const clearDashboardCache = () => {
    try {
        localStorage.removeItem(CACHE_KEY);
    } catch (error) {
        console.error('Error al limpiar caché de estadísticas del dashboard:', error);
    }
};

// Alias para mantener consistencia con otros cachés
export const clearCache = clearDashboardCache;

