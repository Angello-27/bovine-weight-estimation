// src/api/axiosClient.js
import axios from 'axios';

// En Vite, las variables de entorno se acceden con import.meta.env
const apiClient = axios.create({
    baseURL: import.meta.env.REACT_APP_API_URL || 'http://localhost:8000',  // Backend FastAPI bovino
    headers: {
        'Content-Type': 'application/json',
    },
    // withCredentials: true,  // Descomentar si se implementa autenticación con cookies
});

export default apiClient;
