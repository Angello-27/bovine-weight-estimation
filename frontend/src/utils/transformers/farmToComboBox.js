// frontend/src/utils/transformers/farmToComboBox.js

/**
 * Transforma una lista de farms en formato para ComboBox
 * @param {Array} farms - Lista de farms
 * @returns {Array} Lista transformada para ComboBox
 */
export const farmToComboBox = (farms = []) => {
    if (!Array.isArray(farms)) return [];
    
    return farms.map(farm => ({
        id: farm.id,
        label: farm.name || `Finca ${farm.id}`,
        value: farm.id
    }));
};

