// frontend/src/utils/transformers/roleToComboBox.js

/**
 * Transforma la lista de roles a un formato para el ComboBox.
 * @param {Array} data - Lista de roles desde el servidor.
 * @return {Array} - Lista adaptada para el ComboBox.
 */
export function roleToComboBox(data) {
    if (data.roles) {  // Asegúrate de que estás recibiendo "roles" y no "companies" en tu respuesta.
        var roles = data.roles;
        return roles.map(role => ({
            id: role.id,
            label: role.name, // Usamos 'name' porque parece ser la propiedad más descriptiva para representar el rol en un ComboBox.
            level: role.priority
        }));
    }
    return [];
}
