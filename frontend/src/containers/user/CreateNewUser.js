// frontend/src/containers/user/CreateNewUser.js

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createUser } from '../../services/user/createUser';

function CreateNewUser() {
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        username: "",
        password: "",
        roleId: "",
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
            const data = await createUser(formData);
            console.log('Nuevo usuario creado: ', data);
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

export default CreateNewUser;
