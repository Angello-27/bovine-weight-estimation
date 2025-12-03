// frontend/src/utils/getApiBaseUrl.js
/**
 * Utilidad para obtener la URL base de la API
 * 
 * Esta función usa la misma lógica que axiosClient para garantizar consistencia.
 * 
 * Prioridad:
 * 1. Variable de entorno (VITE_API_URL o REACT_APP_API_URL)
 * 2. Detección automática desde window.location (producción)
 * 3. Default localhost (desarrollo)
 * 
 * IMPORTANTE: Si el backend está en un subdominio o puerto diferente,
 * configura la variable de entorno REACT_APP_API_URL o VITE_API_URL.
 */

export function getApiBaseUrl() {
    // 1. Intentar desde variables de entorno (misma lógica que axiosClient)
    const envUrl = import.meta.env.VITE_API_URL || import.meta.env.REACT_APP_API_URL;
    if (envUrl) {
        return envUrl;
    }

    // 2. Detección automática en producción
    if (typeof window !== 'undefined') {
        const { protocol, hostname, port } = window.location;
        
        // Si estamos en producción (no localhost), usar el mismo dominio
        // Esto asume que el backend está en el mismo dominio que el frontend
        if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
            // Construir URL base desde el dominio actual
            // En producción, el backend generalmente está en el mismo dominio
            const baseUrl = port && port !== '80' && port !== '443'
                ? `${protocol}//${hostname}:${port}`
                : `${protocol}//${hostname}`;
            return baseUrl;
        }
    }

    // 3. Default para desarrollo local
    return 'http://localhost:8000';
}

export default getApiBaseUrl;

