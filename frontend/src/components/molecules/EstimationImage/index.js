// frontend/src/components/molecules/EstimationImage/index.js

import Box from "@mui/material/Box";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';
import ImageIcon from '@mui/icons-material/Image';

/**
 * EstimationImage molecule - Muestra la imagen de la estimación
 * @param {string} imagePath - Path de la imagen
 * @param {string} apiBaseUrl - URL base de la API (opcional)
 */
function EstimationImage({ imagePath, apiBaseUrl }) {
    if (!imagePath) {
        return (
            <Card>
                <Box textAlign="center" p={4}>
                    <ImageIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                    <CustomTypography variant="body2" color="text.secondary">
                        No hay imagen disponible
                    </CustomTypography>
                </Box>
            </Card>
        );
    }

    // Construir URL completa de la imagen
    const getImageUrl = (path) => {
        if (!path) return null;
        
        // Si ya es una URL completa, retornarla tal cual
        if (path.startsWith('http://') || path.startsWith('https://')) {
            return path;
        }
        
        // Obtener URL base de la API con detección automática
        // Usar la misma lógica que axiosClient para garantizar consistencia
        let baseUrl = apiBaseUrl;
        if (!baseUrl) {
            // Intentar desde variables de entorno (misma lógica que axiosClient)
            baseUrl = import.meta.env.VITE_API_URL || import.meta.env.REACT_APP_API_URL;
            
            // Si no hay variable de entorno, detectar automáticamente desde window.location
            if (!baseUrl && typeof window !== 'undefined') {
                const { protocol, hostname, port } = window.location;
                // Si estamos en producción (no localhost), usar el mismo dominio
                // Esto asume que el backend está en el mismo dominio que el frontend
                if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
                    // En producción, generalmente no hay puerto en la URL (puerto 80/443)
                    baseUrl = port && port !== '80' && port !== '443'
                        ? `${protocol}//${hostname}:${port}`
                        : `${protocol}//${hostname}`;
                } else {
                    // Desarrollo local
                    baseUrl = 'http://localhost:8000';
                }
            }
        }
        
        // Si el path ya incluye /uploads/, usarlo directamente
        // Si no, agregar /uploads/ antes del path
        let finalPath = path;
        if (!finalPath.startsWith('/uploads/') && !finalPath.startsWith('uploads/')) {
            // Si el path es relativo (ej: "brahman/animal_123.jpg"), agregar /uploads/
            if (!finalPath.startsWith('/')) {
                finalPath = `/uploads/${finalPath}`;
            } else {
                finalPath = `/uploads${finalPath}`;
            }
        } else if (finalPath.startsWith('uploads/')) {
            // Si empieza con "uploads/" sin barra inicial, agregarla
            finalPath = `/${finalPath}`;
        }
        
        // Construir URL completa
        const cleanBaseUrl = (baseUrl || '').replace(/\/$/, ''); // Remover barra final si existe
        return `${cleanBaseUrl}${finalPath}`;
    };
    
    const imageUrl = getImageUrl(imagePath);

    return (
        <Card>
            <CustomTypography variant="h6" mb={2}>
                Imagen de la Estimación
            </CustomTypography>
            <Box
                sx={{
                    width: '100%',
                    borderRadius: 2,
                    overflow: 'hidden',
                    bgcolor: 'action.hover'
                }}
            >
                <img
                    src={imageUrl}
                    alt="Estimación de peso"
                    style={{
                        width: '100%',
                        height: 'auto',
                        display: 'block'
                    }}
                    onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'flex';
                    }}
                />
                <Box
                    sx={{
                        display: 'none',
                        width: '100%',
                        minHeight: '200px',
                        alignItems: 'center',
                        justifyContent: 'center',
                        flexDirection: 'column',
                        p: 4
                    }}
                >
                    <ImageIcon sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                    <CustomTypography variant="body2" color="text.secondary">
                        Error al cargar la imagen
                    </CustomTypography>
                </Box>
            </Box>
        </Card>
    );
}

export default EstimationImage;

