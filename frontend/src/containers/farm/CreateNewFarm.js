// frontend/src/containers/farm/CreateNewFarm.js

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createFarm } from '../../services/farm/createFarm';

function CreateNewFarm() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        name: "",
        owner_id: "",
        latitude: "",
        longitude: "",
        capacity: "",
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
            [fieldName]: value ? value.id : ''
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const payload = {
                name: formData.name,
                owner_id: formData.owner_id,
                latitude: parseFloat(formData.latitude),
                longitude: parseFloat(formData.longitude),
                capacity: parseInt(formData.capacity, 10),
            };
            const data = await createFarm(payload);
            console.log('Nueva finca creada: ', data);
            // Resetear formulario después de crear
            setFormData({
                name: "",
                owner_id: "",
                latitude: "",
                longitude: "",
                capacity: "",
            });
            navigate('/home');
        } catch (error) {
            console.error(error);
            // TODO: Mostrar un mensaje de error al usuario
        }
    };

    return {
        formData,
        handleChange,
        handleSubmit,
        handleComboBoxChange
    };
}

export default CreateNewFarm;

