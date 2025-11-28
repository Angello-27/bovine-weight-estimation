// src/services/sync/syncCattleBatch.js
// NOTA: Este servicio NO se usa en el panel web.
// La sincronización es exclusiva de la app móvil (offline-first).
// Se mantiene por si se necesita en el futuro, pero no está en uso.

import apiClient from '../../api/axiosClient';

/**
 * Sincroniza un batch de animales (máximo 100)
 * 
 * ⚠️ NOTA: Este endpoint es principalmente para la app móvil.
 * El panel web normalmente solo visualiza el estado de sincronización.
 * 
 * @param {Object} syncData - Datos de sincronización
 * @param {string} syncData.device_id - ID del dispositivo
 * @param {Array} syncData.items - Array de animales a sincronizar (máx 100)
 * @returns {Promise<Object>} Resultado de la sincronización
 */
const syncCattleBatch = async (syncData) => {
    try {
        if (syncData.items.length > 100) {
            throw new Error('El batch no puede tener más de 100 items');
        }
        const response = await apiClient.post('/api/v1/sync/cattle', syncData);
        return response.data;
    } catch (error) {
        console.error('Error al sincronizar ganado:', error);
        throw error;
    }
};

export default syncCattleBatch;

