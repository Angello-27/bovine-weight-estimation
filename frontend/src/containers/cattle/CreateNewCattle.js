// frontend/src/containers/cattle/CreateNewCattle.js

import { useState } from 'react';
import { createCattle, updateCattle, deleteCattle } from '../../services/cattle';
import { getCurrentUser } from '../../services/auth/authService';

function CreateNewCattle() {
    const [formData, setFormData] = useState({
        id: '',
        ear_tag: '',
        breed: '',
        birth_date: '',
        gender: '',
        name: '',
        color: '',
        birth_weight_kg: '',
        observations: '',
        farm_id: '',
        status: 'active',
        mother_id: '',
        father_id: ''
    });

    const [errors, setErrors] = useState({});

    const validateForm = () => {
        const newErrors = {};

        // Validar caravana
        if (!formData.ear_tag || formData.ear_tag.trim() === '') {
            newErrors.ear_tag = 'La caravana es requerida';
        }

        // Validar raza
        if (!formData.breed || formData.breed === '') {
            newErrors.breed = 'La raza es requerida';
        }

        // Validar fecha de nacimiento
        if (!formData.birth_date || formData.birth_date === '') {
            newErrors.birth_date = 'La fecha de nacimiento es requerida';
        } else {
            const birthDate = new Date(formData.birth_date);
            const today = new Date();
            if (birthDate > today) {
                newErrors.birth_date = 'La fecha de nacimiento no puede ser futura';
            }
        }

        // Validar género
        if (!formData.gender || formData.gender === '') {
            newErrors.gender = 'El género es requerido';
        } else if (formData.gender !== 'male' && formData.gender !== 'female') {
            newErrors.gender = 'El género debe ser "male" o "female"';
        }

        // Validar peso al nacer (si se proporciona)
        if (formData.birth_weight_kg && formData.birth_weight_kg !== '') {
            const weight = parseFloat(formData.birth_weight_kg);
            if (isNaN(weight) || weight < 0 || weight > 100) {
                newErrors.birth_weight_kg = 'El peso al nacer debe ser un número entre 0 y 100 kg';
            }
        }

        // Validar farm_id (requerido en creación)
        if (!formData.id && (!formData.farm_id || formData.farm_id === '')) {
            newErrors.farm_id = 'La hacienda es requerida';
        }

        // Validar status
        if (formData.status && !['active', 'inactive', 'sold', 'deceased'].includes(formData.status)) {
            newErrors.status = 'El estado debe ser uno de: active, inactive, sold, deceased';
        }

        // Validar que mother_id y father_id sean diferentes del animal actual (si se está editando)
        if (formData.id) {
            if (formData.mother_id && formData.mother_id === formData.id) {
                newErrors.mother_id = 'El animal no puede ser su propia madre';
            }
            if (formData.father_id && formData.father_id === formData.id) {
                newErrors.father_id = 'El animal no puede ser su propio padre';
            }
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value
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

    const handleComboBoxChange = (fieldName, value) => {
        setFormData((prevData) => ({
            ...prevData,
            [fieldName]: value ? (value.id || value) : ''
        }));
        // Limpiar error del campo cuando el usuario selecciona
        if (errors[fieldName]) {
            setErrors((prevErrors) => {
                const newErrors = { ...prevErrors };
                delete newErrors[fieldName];
                return newErrors;
            });
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        // Validar antes de enviar
        if (!validateForm()) {
            return false;
        }

        try {
            // Obtener farm_id del usuario actual si no está en formData
            let farmId = formData.farm_id;
            if (!farmId) {
                const currentUser = getCurrentUser();
                farmId = currentUser?.farm_id;
                if (!farmId) {
                    throw new Error('No se encontró una hacienda asignada. Por favor, contacta al administrador.');
                }
            }

            // Preparar datos para enviar
            const cattleData = {
                ear_tag: formData.ear_tag.trim(),
                breed: formData.breed,
                birth_date: formData.birth_date,
                gender: formData.gender,
                name: formData.name?.trim() || null,
                color: formData.color?.trim() || null,
                birth_weight_kg: formData.birth_weight_kg ? parseFloat(formData.birth_weight_kg) : null,
                observations: formData.observations?.trim() || null,
                farm_id: farmId,
                status: formData.status || 'active',
                mother_id: formData.mother_id && formData.mother_id !== '' ? formData.mother_id : null,
                father_id: formData.father_id && formData.father_id !== '' ? formData.father_id : null
            };

            if (formData.id) {
                // Editar - enviar campos actualizables incluyendo parentesco
                const updateData = {
                    name: cattleData.name,
                    color: cattleData.color,
                    observations: cattleData.observations,
                    status: cattleData.status,
                    mother_id: cattleData.mother_id,
                    father_id: cattleData.father_id
                };
                const data = await updateCattle(formData.id, updateData);
                console.log('Animal actualizado: ', data);
            } else {
                // Crear - enviar todos los campos
                const data = await createCattle(cattleData);
                console.log('Nuevo animal creado: ', data);
            }

            // Resetear formulario después de crear/editar
            setFormData({
                id: '',
                ear_tag: '',
                breed: '',
                birth_date: '',
                gender: '',
                name: '',
                color: '',
                birth_weight_kg: '',
                observations: '',
                farm_id: '',
                status: 'active',
                mother_id: '',
                father_id: ''
            });
            setErrors({});
            return true;
        } catch (error) {
            console.error(error);
            throw error;
        }
    };

    const resetErrors = () => {
        setErrors({});
    };

    const handleDelete = async (animalId) => {
        try {
            await deleteCattle(animalId);
            console.log('Animal eliminado:', animalId);
        } catch (error) {
            console.error(error);
            throw error;
        }
    };

    return {
        formData,
        errors,
        handleChange,
        handleSubmit,
        handleComboBoxChange,
        handleDelete,
        resetErrors,
        setFormData
    };
}

export default CreateNewCattle;

