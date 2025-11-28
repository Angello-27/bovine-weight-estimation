// src/api/axiosClient.js
import axios from 'axios';

const apiClient = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',  // Backend FastAPI bovino
    headers: {
        'Content-Type': 'application/json',
    },
    // withCredentials: true,  // Descomentar si se implementa autenticación con cookies
});

export default apiClient;
