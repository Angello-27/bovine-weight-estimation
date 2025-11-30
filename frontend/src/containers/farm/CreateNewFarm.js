// frontend/src/containers/farm/CreateNewFarm.js

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createFarm } from '../../services/farm/createFarm';
import { updateFarm } from '../../services/farm/updateFarm';
import { deleteFarm } from '../../services/farm/deleteFarm';

function CreateNewFarm() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        id: "",
        name: "",
        owner_id: "",
        latitude: "",
        longitude: "",
        capacity: "",
    });

    const [errors, setErrors] = useState({});

    const validateForm = () => {
        const newErrors = {};

        // Validar nombre
        if (!formData.name || formData.name.trim() === '') {
            newErrors.name = 'El nombre de la hacienda es requerido';
        }

        // Validar propietario
        if (!formData.owner_id || formData.owner_id === '') {
            newErrors.owner_id = 'El propietario es requerido';
        }

        // Validar latitud
        if (!formData.latitude || formData.latitude === '') {
            newErrors.latitude = 'La latitud es requerida';
        } else {
            const lat = parseFloat(formData.latitude);
            if (isNaN(lat) || lat < -90 || lat > 90) {
                newErrors.latitude = 'La latitud debe ser un número entre -90 y 90';
            }
        }

        // Validar longitud
        if (!formData.longitude || formData.longitude === '') {
            newErrors.longitude = 'La longitud es requerida';
        } else {
            const lon = parseFloat(formData.longitude);
            if (isNaN(lon) || lon < -180 || lon > 180) {
                newErrors.longitude = 'La longitud debe ser un número entre -180 y 180';
            }
        }

        // Validar capacidad
        if (!formData.capacity || formData.capacity === '') {
            newErrors.capacity = 'La capacidad máxima es requerida';
        } else {
            const cap = parseInt(formData.capacity, 10);
            if (isNaN(cap) || cap < 1) {
                newErrors.capacity = 'La capacidad debe ser un número mayor a 0';
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
            [fieldName]: value ? value.id : ''
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
            // No cerrar el dialog si hay errores de validación
            return false;
        }

        try {
            const payload = {
                name: formData.name.trim(),
                owner_id: formData.owner_id,
                latitude: parseFloat(formData.latitude),
                longitude: parseFloat(formData.longitude),
                capacity: parseInt(formData.capacity, 10),
            };

            if (formData.id) {
                // Editar
                const data = await updateFarm(formData.id, payload);
                console.log('Hacienda actualizada: ', data);
            } else {
                // Crear
                const data = await createFarm(payload);
                console.log('Nueva hacienda creada: ', data);
            }

            // Resetear formulario después de crear/editar
            setFormData({
                id: "",
                name: "",
                owner_id: "",
                latitude: "",
                longitude: "",
                capacity: "",
            });
            setErrors({});
            // Retornar true para indicar éxito
            return true;
        } catch (error) {
            console.error(error);
            throw error; // Re-lanzar para que el componente padre pueda manejarlo
        }
    };

    const resetErrors = () => {
        setErrors({});
    };

    const handleDelete = async (farmId) => {
        try {
            await deleteFarm(farmId);
            console.log('Hacienda eliminada:', farmId);
            // Recargar la lista (se manejará desde el componente padre)
        } catch (error) {
            console.error(error);
            throw error; // Re-lanzar para que el componente padre pueda manejarlo
        }
    };

    return {
        formData,
        errors,
        handleChange,
        handleSubmit,
        handleComboBoxChange,
        handleDelete,
        resetErrors
    };
}

export default CreateNewFarm;

