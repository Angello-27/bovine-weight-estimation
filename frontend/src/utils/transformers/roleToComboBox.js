// frontend/src/utils/transformers/roleToComboBox.js

/**
 * Transforma la lista de roles a un formato para el ComboBox.
 * @param {Array} data - Lista de roles desde el servidor (puede ser array directo o objeto con propiedad roles).
 * @return {Array} - Lista adaptada para el ComboBox.
 */
export function roleToComboBox(data) {
    if (!data) return [];
    
    // Si data es un objeto con propiedad roles, usar esa propiedad
    if (data.roles && Array.isArray(data.roles)) {
        return data.roles.map(role => ({
            id: role.id,
            label: role.name || role.label || '-',
            level: role.priority
        }));
    }
    
    // Si data es un array directo, usar directamente
    if (Array.isArray(data)) {
        return data.map(role => ({
            id: role.id,
            label: role.name || role.label || '-',
            level: role.priority
        }));
    }
    
    return [];
}
