// frontend/src/utils/cache/useWeightEstimationsCache.js

/**
 * Hook para gestionar el caché de estimaciones de peso
 * Proporciona funciones para invalidar el caché cuando sea necesario
 */

import { useCallback } from 'react';
import {
    clearCache,
    addEstimationToCache,
    removeEstimationFromCache
} from './weightEstimationsCache';

/**
 * Hook para invalidar caché de estimaciones
 * Útil para usar en componentes que crean/eliminan estimaciones
 */
export const useWeightEstimationsCache = () => {
    /**
     * Invalida completamente el caché
     * Útil cuando se crea una nueva estimación
     */
    const invalidateCache = useCallback(() => {
        clearCache();
    }, []);

    /**
     * Agrega una estimación al caché (actualización optimista)
     * @param {Object} estimation - Estimación a agregar
     */
    const addToCache = useCallback((estimation) => {
        addEstimationToCache(estimation);
    }, []);

    /**
     * Elimina una estimación del caché
     * @param {string} estimationId - ID de la estimación
     */
    const removeFromCache = useCallback((estimationId) => {
        removeEstimationFromCache(estimationId);
    }, []);

    return {
        invalidateCache,
        addToCache,
        removeFromCache
    };
};

