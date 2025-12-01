// frontend/src/containers/user/CreateNewUser.js

import { useState } from 'react';
import { createUser } from '../../services/user/createUser';
import { updateUser } from '../../services/user/updateUser';
import { deleteUser } from '../../services/user/deleteUser';

function CreateNewUser() {
    const [formData, setFormData] = useState({
        id: "",
        username: "",
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        roleId: "",
        farmId: "",
        is_active: true,
    });

    const [errors, setErrors] = useState({});

    const validateForm = () => {
        const newErrors = {};

        // Validar username (solo en creación)
        if (!formData.id && (!formData.username || formData.username.trim() === '')) {
            newErrors.username = 'El nombre de usuario es requerido';
        } else if (!formData.id && formData.username.trim().length < 3) {
            newErrors.username = 'El nombre de usuario debe tener al menos 3 caracteres';
        }

        // Validar email
        if (!formData.email || formData.email.trim() === '') {
            newErrors.email = 'El email es requerido';
        } else {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(formData.email)) {
                newErrors.email = 'El email no es válido';
            }
        }

        // Password: en creación se genera automáticamente igual al username
        // En actualización, solo se valida si se proporciona
        if (formData.id && formData.password && formData.password.trim() !== '' && formData.password.length < 6) {
            newErrors.password = 'La contraseña debe tener al menos 6 caracteres';
        }

        // Validar role
        if (!formData.roleId || formData.roleId === '') {
            newErrors.roleId = 'El rol es requerido';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleChange = (event) => {
        const { name, value, type, checked } = event.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: type === 'checkbox' ? checked : value
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
                email: formData.email.trim(),
                role_id: formData.roleId,
                farm_id: formData.farmId || null,
                first_name: formData.first_name?.trim() || null,
                last_name: formData.last_name?.trim() || null,
                is_active: formData.is_active,
            };

            // Solo incluir username y password en creación
            if (!formData.id) {
                payload.username = formData.username.trim();
                // Generar password automáticamente igual al username
                payload.password = formData.username.trim();
            } else {
                // En actualización, solo incluir password si se proporciona
                if (formData.password && formData.password.trim() !== '') {
                    payload.password = formData.password;
                }
            }

            if (formData.id) {
                // Editar
                const data = await updateUser(formData.id, payload);
                console.log('Usuario actualizado: ', data);
            } else {
                // Crear
                const data = await createUser(payload);
                console.log('Nuevo usuario creado: ', data);
            }

            // Resetear formulario después de crear/editar
            setFormData({
                id: "",
                username: "",
                email: "",
                password: "",
                first_name: "",
                last_name: "",
                roleId: "",
                farmId: "",
                is_active: true,
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

    const handleDelete = async (userId) => {
        try {
            await deleteUser(userId);
            console.log('Usuario eliminado:', userId);
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

export default CreateNewUser;
