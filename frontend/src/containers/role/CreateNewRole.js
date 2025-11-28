import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createRole } from '../../services/role/createRole'; // Suponiendo que aquí esté tu función createRole

function CreateNewRole() {
    const navigate = useNavigate();

    // Valor por defecto para el grupo de radio buttons
    const defaultValue = 'Invitado';  // Puedes cambiar esto según lo que necesites

    const [formData, setFormData] = useState({
        name: "",
        descripcion: "",
        priority: defaultValue
    });

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    };

    const handleSubmit = async (event) => {
        event.preventDefault();

        try {
            const data = await createRole(formData);
            console.log('Nuevo elemento creado: ', data);
            navigate('/home');
            // Mostrar un mensaje de éxito, redirigir o actualizar la UI como necesites
        } catch (error) {
            console.error(error);
            // Mostrar un mensaje de error al usuario
        }
    };

    return {
        formData,
        handleChange,
        handleSubmit
    };
}

export default CreateNewRole;
