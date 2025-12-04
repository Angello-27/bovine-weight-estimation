// frontend/src/containers/profile/useProfileView.js

import { useState, useEffect } from 'react';
import { getCurrentUser } from '../../services/auth/authService';
import { getUserById } from '../../services/user/getUserById';
import { updateProfile } from '../../services/user/updateProfile';
import { changePassword } from '../../services/user/changePassword';
import ManageProfileForm from './ManageProfileForm';

function useProfileView() {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Estados para formularios
    const profileFormProps = ManageProfileForm();
    const [passwordFormData, setPasswordFormData] = useState({
        currentPassword: '',
        newPassword: '',
        confirmPassword: '',
    });
    const [passwordErrors, setPasswordErrors] = useState({});
    const [showPasswordForm, setShowPasswordForm] = useState(false);

    // Estados para notificaciones
    const [errorSnackbar, setErrorSnackbar] = useState({ open: false, message: '' });
    const [successSnackbar, setSuccessSnackbar] = useState({ open: false, message: '' });

    // Cargar datos del usuario actual
    useEffect(() => {
        const loadUser = async () => {
            try {
                const currentUser = getCurrentUser();
                if (currentUser && currentUser.id) {
                    // Obtener datos completos del usuario desde la API
                    const fullUserData = await getUserById(currentUser.id);
                    setUser(fullUserData);
                    // Inicializar formulario de perfil con datos del usuario
                    profileFormProps.setFormData({
                        id: fullUserData.id,
                        email: fullUserData.email || '',
                        first_name: fullUserData.first_name || '',
                        last_name: fullUserData.last_name || '',
                    });
                } else {
                    setError('No se pudo cargar la información del usuario');
                }
            } catch (err) {
                setError('Error al cargar el perfil');
                console.error('Error al cargar perfil:', err);
            } finally {
                setLoading(false);
            }
        };

        loadUser();
    }, []);

    // Función para mostrar errores
    const showError = (message) => {
        setErrorSnackbar({ open: true, message });
    };

    // Función para mostrar éxito
    const showSuccess = (message) => {
        setSuccessSnackbar({ open: true, message });
    };

    // Cerrar notificaciones
    const closeErrorSnackbar = () => {
        setErrorSnackbar({ open: false, message: '' });
    };

    const closeSuccessSnackbar = () => {
        setSuccessSnackbar({ open: false, message: '' });
    };

    // Manejar actualización de perfil
    const handleUpdateProfile = async (e) => {
        e.preventDefault();
        
        if (!profileFormProps.validateForm()) {
            return;
        }

        try {
            const updatedUser = await updateProfile(profileFormProps.formData);
            setUser(updatedUser);
            showSuccess('Perfil actualizado exitosamente');
        } catch (err) {
            showError(err.message || 'Error al actualizar el perfil');
        }
    };

    // Validar formulario de contraseña
    const validatePasswordForm = () => {
        const newErrors = {};

        if (!passwordFormData.currentPassword || passwordFormData.currentPassword.trim() === '') {
            newErrors.currentPassword = 'La contraseña actual es requerida';
        }

        if (!passwordFormData.newPassword || passwordFormData.newPassword.trim() === '') {
            newErrors.newPassword = 'La nueva contraseña es requerida';
        } else if (passwordFormData.newPassword.length < 6) {
            newErrors.newPassword = 'La contraseña debe tener al menos 6 caracteres';
        }

        if (!passwordFormData.confirmPassword || passwordFormData.confirmPassword.trim() === '') {
            newErrors.confirmPassword = 'Confirma la nueva contraseña';
        } else if (passwordFormData.newPassword !== passwordFormData.confirmPassword) {
            newErrors.confirmPassword = 'Las contraseñas no coinciden';
        }

        setPasswordErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    // Manejar cambio de contraseña
    const handleChangePassword = async (e) => {
        e.preventDefault();

        if (!validatePasswordForm()) {
            return;
        }

        try {
            await changePassword(passwordFormData);
            setPasswordFormData({
                currentPassword: '',
                newPassword: '',
                confirmPassword: '',
            });
            setPasswordErrors({});
            setShowPasswordForm(false);
            showSuccess('Contraseña cambiada exitosamente');
        } catch (err) {
            showError(err.message || 'Error al cambiar la contraseña');
        }
    };

    // Manejar cambios en formulario de contraseña
    const handlePasswordChange = (event) => {
        const { name, value } = event.target;
        setPasswordFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
        // Limpiar error del campo cuando el usuario empieza a escribir
        if (passwordErrors[name]) {
            setPasswordErrors((prevErrors) => {
                const newErrors = { ...prevErrors };
                delete newErrors[name];
                return newErrors;
            });
        }
    };

    return {
        user,
        loading,
        error,
        profileFormProps: {
            formData: profileFormProps.formData,
            errors: profileFormProps.errors,
            handleChange: profileFormProps.handleChange,
            handleSubmit: handleUpdateProfile,
        },
        passwordFormProps: {
            formData: passwordFormData,
            errors: passwordErrors,
            handleChange: handlePasswordChange,
            handleSubmit: handleChangePassword,
            showForm: showPasswordForm,
            onShowForm: () => setShowPasswordForm(true),
            onCloseForm: () => {
                setShowPasswordForm(false);
                setPasswordFormData({
                    currentPassword: '',
                    newPassword: '',
                    confirmPassword: '',
                });
                setPasswordErrors({});
            },
        },
        errorSnackbar,
        successSnackbar,
        closeErrorSnackbar,
        closeSuccessSnackbar,
    };
}

export default useProfileView;

