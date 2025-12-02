// frontend/src/utils/cache/weightEstimationsCache.js

/**
 * Sistema de caché para estimaciones de peso usando localStorage
 * 
 * Características:
 * - Almacena datos en localStorage con TTL (Time To Live)
 * - Invalida automáticamente después de X minutos
 * - Permite invalidación manual cuando se crean/eliminan estimaciones
 */

const CACHE_KEY = 'weight_estimations_cache';
const CACHE_VERSION = '1.0.0';
const DEFAULT_TTL_MINUTES = 30; // 30 minutos por defecto

/**
 * Obtiene el caché de estimaciones
 * @returns {Object|null} Datos del caché o null si no existe o está expirado
 */
export const getCachedEstimations = () => {
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
        console.error('Error al leer caché de estimaciones:', error);
        clearCache();
        return null;
    }
};

/**
 * Guarda estimaciones en el caché
 * @param {Array} estimations - Array de estimaciones
 * @param {number} ttlMinutes - Tiempo de vida del caché en minutos (opcional)
 */
export const setCachedEstimations = (estimations, ttlMinutes = DEFAULT_TTL_MINUTES) => {
    try {
        const now = Date.now();
        const expiresAt = now + (ttlMinutes * 60 * 1000); // Convertir minutos a milisegundos

        const cacheData = {
            version: CACHE_VERSION,
            data: estimations,
            cachedAt: now,
            expiresAt: expiresAt,
            ttlMinutes: ttlMinutes
        };

        localStorage.setItem(CACHE_KEY, JSON.stringify(cacheData));
    } catch (error) {
        console.error('Error al guardar caché de estimaciones:', error);
        // Si el localStorage está lleno, intentar limpiar y guardar de nuevo
        if (error.name === 'QuotaExceededError') {
            console.warn('⚠️ localStorage lleno, limpiando caché antiguo...');
            clearCache();
            try {
                localStorage.setItem(CACHE_KEY, JSON.stringify({
                    version: CACHE_VERSION,
                    data: estimations,
                    cachedAt: Date.now(),
                    expiresAt: Date.now() + (ttlMinutes * 60 * 1000),
                    ttlMinutes: ttlMinutes
                }));
            } catch (retryError) {
                console.error('❌ No se pudo guardar en caché después de limpiar:', retryError);
            }
        }
    }
};

/**
 * Limpia el caché de estimaciones
 */
export const clearCache = () => {
    try {
        localStorage.removeItem(CACHE_KEY);
    } catch (error) {
        console.error('Error al limpiar caché:', error);
    }
};

/**
 * Verifica si el caché existe y es válido
 * @returns {boolean} true si el caché es válido
 */
export const isCacheValid = () => {
    const cached = getCachedEstimations();
    return cached !== null;
};

/**
 * Obtiene información del caché (útil para debugging)
 * @returns {Object|null} Información del caché
 */
export const getCacheInfo = () => {
    try {
        const cached = localStorage.getItem(CACHE_KEY);
        if (!cached) return null;

        const cacheData = JSON.parse(cached);
        const now = Date.now();
        const isExpired = cacheData.expiresAt && now > cacheData.expiresAt;
        const timeRemaining = cacheData.expiresAt ? Math.max(0, cacheData.expiresAt - now) : null;

        return {
            version: cacheData.version,
            itemCount: Array.isArray(cacheData.data) ? cacheData.data.length : 0,
            cachedAt: new Date(cacheData.cachedAt),
            expiresAt: cacheData.expiresAt ? new Date(cacheData.expiresAt) : null,
            isExpired,
            timeRemainingMinutes: timeRemaining ? Math.floor(timeRemaining / 60000) : null
        };
    } catch (error) {
        console.error('Error al obtener info del caché:', error);
        return null;
    }
};

/**
 * Agrega una nueva estimación al caché (optimista)
 * @param {Object} estimation - Nueva estimación a agregar
 */
export const addEstimationToCache = (estimation) => {
    const cached = getCachedEstimations();
    if (cached && Array.isArray(cached)) {
        // Agregar al inicio del array (más reciente primero)
        const updated = [estimation, ...cached];
        setCachedEstimations(updated, DEFAULT_TTL_MINUTES);
    }
};

/**
 * Elimina una estimación del caché
 * @param {string} estimationId - ID de la estimación a eliminar
 */
export const removeEstimationFromCache = (estimationId) => {
    const cached = getCachedEstimations();
    if (cached && Array.isArray(cached)) {
        const updated = cached.filter(est => est.id !== estimationId);
        setCachedEstimations(updated, DEFAULT_TTL_MINUTES);
    }
};

