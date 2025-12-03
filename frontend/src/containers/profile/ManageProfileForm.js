// frontend/src/containers/profile/ManageProfileForm.js

import { useState } from 'react';

function ManageProfileForm() {
    const [formData, setFormData] = useState({
        id: '',
        email: '',
        first_name: '',
        last_name: '',
    });

    const [errors, setErrors] = useState({});

    const validateForm = () => {
        const newErrors = {};

        // Validar email
        if (!formData.email || formData.email.trim() === '') {
            newErrors.email = 'El email es requerido';
        } else {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(formData.email)) {
                newErrors.email = 'El email no es válido';
            }
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
        // Limpiar error del campo cuando el usuario empieza a escribir
        if (errors[name]) {
            setErrors((prevErrors) => {
                const newErrors = { ...prevErrors };
                delete newErrors[name];
                return newErrors;
            });
        }
    };

    return {
        formData,
        errors,
        handleChange,
        validateForm,
        setFormData,
    };
}

export default ManageProfileForm;

