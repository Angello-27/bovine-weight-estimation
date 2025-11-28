// frontend/src/utils/transformers/userToComboBox.js

/**
 * Transforma una lista de usuarios en formato para ComboBox
 * @param {Array} users - Lista de usuarios
 * @returns {Array} Lista transformada para ComboBox
 */
export const userToComboBox = (users = []) => {
    if (!Array.isArray(users)) return [];
    
    return users.map(user => ({
        id: user.id,
        label: user.username || `Usuario ${user.id}`,
        value: user.id
    }));
};

