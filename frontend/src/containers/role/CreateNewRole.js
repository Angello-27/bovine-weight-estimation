// frontend/src/containers/role/CreateNewRole.js

import { useState } from 'react';
import { createRole } from '../../services/role/createRole';
import { updateRole } from '../../services/role/updateRole';
import { deleteRole } from '../../services/role/deleteRole';

function CreateNewRole() {
    // Valor por defecto para el grupo de radio buttons
    const defaultValue = 'Invitado';

    const [formData, setFormData] = useState({
        id: "",
        name: "",
        description: "",
        priority: defaultValue
    });

    const [errors, setErrors] = useState({});

    const validateForm = () => {
        const newErrors = {};

        // Validar nombre
        if (!formData.name || formData.name.trim() === '') {
            newErrors.name = 'El nombre del rol es requerido';
        } else if (formData.name.trim().length > 50) {
            newErrors.name = 'El nombre del rol no puede exceder 50 caracteres';
        }

        // Validar priority
        const validPriorities = ['Invitado', 'Usuario', 'Administrador'];
        if (!formData.priority || !validPriorities.includes(formData.priority)) {
            newErrors.priority = 'El nivel de acceso es requerido';
        }

        // Validar descripción (opcional, pero si se proporciona no debe exceder 500 caracteres)
        if (formData.description && formData.description.length > 500) {
            newErrors.description = 'La descripción no puede exceder 500 caracteres';
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
                description: formData.description?.trim() || null,
                priority: formData.priority,
            };

            if (formData.id) {
                // Editar
                const data = await updateRole(formData.id, payload);
                console.log('Rol actualizado: ', data);
            } else {
                // Crear
                const data = await createRole(payload);
                console.log('Nuevo rol creado: ', data);
            }

            // Resetear formulario después de crear/editar
            setFormData({
                id: "",
                name: "",
                description: "",
                priority: defaultValue
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

    const handleDelete = async (roleId) => {
        try {
            await deleteRole(roleId);
            console.log('Rol eliminado:', roleId);
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
        handleDelete,
        resetErrors
    };
}

export default CreateNewRole;
