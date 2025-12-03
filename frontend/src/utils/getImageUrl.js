// frontend/src/utils/getImageUrl.js

import { getApiBaseUrl } from './getApiBaseUrl';

/**
 * Construye la URL completa para acceder a una imagen desde el backend.
 * Usa el endpoint /api/v1/resources/images/{image_path} para servir las imágenes.
 *
 * @param {string} imagePath - Ruta relativa de la imagen desde uploads/
 *                            (ej: "nelore/nelore_213.jpg" o "brahman/animal_123.jpg")
 * @returns {string} URL completa para acceder a la imagen
 */
export const getImageUrl = (imagePath) => {
    if (!imagePath) return null;

    // Si ya es una URL completa, retornarla tal cual
    if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
        return imagePath;
    }

    // Obtener la URL base de la API
    const baseUrl = getApiBaseUrl();

    // Limpiar la URL base (remover trailing slash)
    const cleanBaseUrl = baseUrl.replace(/\/$/, '');

    // Limpiar el path de la imagen (remover leading slash y normalizar)
    let cleanImagePath = imagePath.replace(/^\/+/, '');

    // Si el path incluye "uploads/", removerlo ya que el endpoint lo maneja
    if (cleanImagePath.startsWith('uploads/')) {
        cleanImagePath = cleanImagePath.replace(/^uploads\//, '');
    }

    // Construir la URL usando el endpoint de recursos
    return `${cleanBaseUrl}/api/v1/resources/images/${cleanImagePath}`;
};

