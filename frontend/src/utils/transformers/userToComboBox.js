// frontend/src/utils/transformers/userToComboBox.js

/**
 * Transforma una lista de usuarios en formato para ComboBox
 * @param {Array} users - Lista de usuarios
 * @returns {Array} Lista transformada para ComboBox
 */
export const userToComboBox = (users = []) => {
    if (!Array.isArray(users)) return [];
    
    return users.map(user => {
        // Priorizar nombre completo, luego nombre o apellido individual, finalmente username
        let label = '';
        if (user.first_name && user.last_name) {
            label = `${user.first_name} ${user.last_name}`;
        } else if (user.first_name) {
            label = user.first_name;
        } else if (user.last_name) {
            label = user.last_name;
        } else {
            label = user.username || `Usuario ${user.id}`;
        }
        
        return {
            id: user.id,
            label: label,
            value: user.id
        };
    });
};

