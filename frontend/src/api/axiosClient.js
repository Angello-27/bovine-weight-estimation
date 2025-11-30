// src/api/axiosClient.js
/**
 * Cliente HTTP configurado con Axios
 * 
 * Middleware implementado mediante interceptores:
 * - Request Interceptor: Agrega token JWT automáticamente
 * - Response Interceptor: Maneja errores 401 (token expirado)
 * 
 * Variables de entorno (Vite):
 * - VITE_API_URL o REACT_APP_API_URL: URL base del backend
 */
import axios from 'axios';

// En Vite, las variables de entorno se acceden con import.meta.env
// Soporta tanto VITE_ como REACT_APP_ para compatibilidad
const API_BASE_URL = import.meta.env.VITE_API_URL 
    || import.meta.env.REACT_APP_API_URL 
    || 'http://localhost:8000';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000, // 30 segundos
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor para agregar token JWT automáticamente
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Interceptor para manejar errores (especialmente 401 - No autorizado)
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expirado o inválido
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            // Redirigir a login si no estamos ya allí
            if (window.location.pathname !== '/login' && window.location.pathname !== '/') {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default apiClient;
