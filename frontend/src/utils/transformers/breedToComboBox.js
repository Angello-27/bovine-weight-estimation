// frontend/src/utils/transformers/breedToComboBox.js

/**
 * Transforma las razas disponibles a formato ComboBox
 * @returns {Array} - Lista de razas para el ComboBox
 */
export function breedToComboBox() {
    const breeds = [
        { id: 'nelore', label: 'Nelore' },
        { id: 'brahman', label: 'Brahman' },
        { id: 'guzerat', label: 'Guzerat' },
        { id: 'senepol', label: 'Senepol' },
        { id: 'girolando', label: 'Girolando' },
        { id: 'gyr_lechero', label: 'Gyr Lechero' },
        { id: 'sindi', label: 'Sindi' }
    ];

    return breeds;
}

