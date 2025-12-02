// frontend/src/utils/transformers/animalToComboBox.js

/**
 * Transforma una lista de animales en formato para ComboBox
 * @param {Array} animals - Lista de animales
 * @returns {Array} Lista transformada para ComboBox
 */
export const animalToComboBox = (animals = []) => {
    if (!Array.isArray(animals)) return [];
    
    return animals.map(animal => ({
        id: animal.id,
        label: `${animal.ear_tag || 'Sin caravana'}${animal.name ? ` - ${animal.name}` : ''}`,
        value: animal.id
    }));
};

