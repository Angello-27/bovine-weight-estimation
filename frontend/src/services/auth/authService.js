import apiClient from '../../api/axiosClient';

/**
 * Autentica un usuario y guarda el token y datos del usuario
 * @param {Object} credentials - { username, password }
 * @returns {Promise<Object>} Datos del usuario autenticado
 */
const loginUser = async (credentials) => {
    try {
        const response = await apiClient.post('/api/v1/auth/login', credentials);
        const userData = response.data;

        // Guardar token y datos del usuario en localStorage
        if (userData.access_token) {
            localStorage.setItem('access_token', userData.access_token);
        }
        if (userData.id) {
            // Guardar datos del usuario (sin el token por seguridad)
            const { access_token, ...userWithoutToken } = userData;
            localStorage.setItem('user', JSON.stringify(userWithoutToken));
        }

        return userData;
    } catch (error) {
        if (error.response) {
            const status = error.response.status;
            if (status === 400 || status === 401) {
                throw new Error('Credenciales inválidas. Por favor verifica e intenta de nuevo.');
            } else if (status === 500) {
                throw new Error('Error del servidor. Por favor intenta de nuevo más tarde.');
            } else {
                throw new Error(error.response.data?.detail || 'Error al iniciar sesión.');
            }
        } else if (error.request) {
            throw new Error('Error de conexión. Verifica tu conexión a internet.');
        } else {
            throw new Error('Ocurrió un error inesperado. Por favor intenta de nuevo.');
        }
    }
};

/**
 * Cierra la sesión del usuario actual
 */
const logoutUser = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
};

/**
 * Obtiene el usuario actual desde localStorage
 * @returns {Object|null} Datos del usuario o null si no hay sesión
 */
const getCurrentUser = () => {
    const userStr = localStorage.getItem('user');
    if (userStr) {
        try {
            return JSON.parse(userStr);
        } catch (error) {
            console.error('Error al parsear usuario:', error);
            return null;
        }
    }
    return null;
};

/**
 * Verifica si hay un usuario autenticado
 * @returns {boolean}
 */
const isAuthenticated = () => {
    const token = localStorage.getItem('access_token');
    const user = getCurrentUser();
    return !!(token && user);
};

/**
 * Obtiene el token de acceso actual
 * @returns {string|null}
 */
const getAccessToken = () => {
    return localStorage.getItem('access_token');
};

export { loginUser, logoutUser, getCurrentUser, isAuthenticated, getAccessToken };

