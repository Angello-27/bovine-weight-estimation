// frontend/src/containers/cattle/CreateNewCattle.js

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import createCattle from '../../services/cattle/createCattle';

function CreateNewCattle() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        ear_tag: '',
        breed: '',
        birth_date: '',
        gender: '',
        name: '',
        color: '',
        birth_weight_kg: '',
        observations: ''
    });

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    };

    const handleComboBoxChange = (fieldName, value) => {
        setFormData((prevData) => ({
            ...prevData,
            [fieldName]: value
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            // Preparar datos para enviar (convertir strings vacíos a null para campos opcionales)
            const cattleData = {
                ear_tag: formData.ear_tag,
                breed: formData.breed,
                birth_date: formData.birth_date,
                gender: formData.gender,
                name: formData.name || null,
                color: formData.color || null,
                birth_weight_kg: formData.birth_weight_kg ? parseFloat(formData.birth_weight_kg) : null,
                observations: formData.observations || null
            };

            const data = await createCattle(cattleData);
            console.log('Nuevo animal creado: ', data);
            
            // Reset form
            setFormData({
                ear_tag: '',
                breed: '',
                birth_date: '',
                gender: '',
                name: '',
                color: '',
                birth_weight_kg: '',
                observations: ''
            });

            // Recargar la página o actualizar la lista
            window.location.reload();
        } catch (error) {
            console.error('Error al crear animal:', error);
            throw error;
        }
    };

    return {
        formData,
        handleChange,
        handleComboBoxChange,
        handleSubmit
    };
}

export default CreateNewCattle;

