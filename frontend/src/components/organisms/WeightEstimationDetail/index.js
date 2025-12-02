// frontend/src/components/organisms/WeightEstimationDetail/index.js

import EstimationImage from '../../molecules/EstimationImage';

/**
 * WeightEstimationDetail organism - Muestra la imagen de la estimación
 * La información detallada ahora se muestra en el template
 * @param {Object} estimation - Datos de la estimación
 * @param {string} apiBaseUrl - URL base de la API (opcional)
 */
function WeightEstimationDetail({ estimation, apiBaseUrl }) {
    if (!estimation) return null;

    return (
        <EstimationImage 
            imagePath={estimation.frame_image_path} 
            apiBaseUrl={apiBaseUrl}
        />
    );
}

export default WeightEstimationDetail;

