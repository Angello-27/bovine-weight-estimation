// frontend/src/containers/cattle/ManageCattleForm.js

import { useState } from 'react';

/**
 * ManageCattleForm container hook - Maneja el estado y acciones del formulario de ganado
 * @param {Object} formProps - Props del formulario de CreateNewCattle
 * @returns {Object} { showForm, handleCreateClick, handleCloseForm }
 */
function ManageCattleForm(formProps) {
    const [showForm, setShowForm] = useState(false);

    const resetForm = () => {
        formProps.handleChange({ target: { name: 'ear_tag', value: '' } });
        formProps.handleChange({ target: { name: 'breed', value: '' } });
        formProps.handleChange({ target: { name: 'birth_date', value: '' } });
        formProps.handleChange({ target: { name: 'gender', value: '' } });
        formProps.handleChange({ target: { name: 'name', value: '' } });
        formProps.handleChange({ target: { name: 'color', value: '' } });
        formProps.handleChange({ target: { name: 'birth_weight_kg', value: '' } });
        formProps.handleChange({ target: { name: 'observations', value: '' } });
    };

    const handleCreateClick = () => {
        resetForm();
        setShowForm(true);
    };

    const handleCloseForm = () => {
        setShowForm(false);
    };

    return {
        showForm,
        handleCreateClick,
        handleCloseForm
    };
}

export default ManageCattleForm;

