// src/services/sync/syncWeightEstimationsBatch.js
// NOTA: Este servicio NO se usa en el panel web.
// La sincronización es exclusiva de la app móvil (offline-first).
// Se mantiene por si se necesita en el futuro, pero no está en uso.

import apiClient from '../../api/axiosClient';

/**
 * Sincroniza un batch de estimaciones de peso (máximo 100)
 * 
 * ⚠️ NOTA: Este endpoint es principalmente para la app móvil.
 * El panel web normalmente solo visualiza las estimaciones ya sincronizadas.
 * 
 * @param {Object} syncData - Datos de sincronización
 * @param {string} syncData.device_id - ID del dispositivo
 * @param {Array} syncData.items - Array de estimaciones a sincronizar (máx 100)
 * @returns {Promise<Object>} Resultado de la sincronización
 */
const syncWeightEstimationsBatch = async (syncData) => {
    try {
        if (syncData.items.length > 100) {
            throw new Error('El batch no puede tener más de 100 items');
        }
        const response = await apiClient.post('/api/v1/sync/weight-estimations', syncData);
        return response.data;
    } catch (error) {
        console.error('Error al sincronizar estimaciones:', error);
        throw error;
    }
};

export default syncWeightEstimationsBatch;

