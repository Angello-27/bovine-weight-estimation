// frontend\src\services\user\createUser.js

import apiClient from '../../api/axiosClient';

const createUser = async (credentials) => {
    try {
        const response = await apiClient.post('/user', credentials);
        return response.data;
    } catch (error) {
        if (error.response && error.response.status === 400) {
            throw new Error('Los datos proporcionados son incorrectos. Por favor verifica e intenta de nuevo.');
        } else {
            throw new Error('Ocurrió un error al intentar iniciar sesión. Por favor intenta de nuevo más tarde.');
        }
    }
};

export { createUser };

