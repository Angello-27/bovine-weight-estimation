// frontend/src/components/organisms/WeightEstimationDetail/index.js

import Grid from "@mui/material/Grid";
import EstimationImage from '../../molecules/EstimationImage';
import EstimationResult from '../../molecules/EstimationResult';
import EstimationMetadata from '../../molecules/EstimationMetadata';

/**
 * WeightEstimationDetail organism - Muestra el detalle completo de una estimación
 * @param {Object} estimation - Datos de la estimación
 * @param {string} apiBaseUrl - URL base de la API (opcional)
 */
function WeightEstimationDetail({ estimation, apiBaseUrl }) {
    if (!estimation) return null;

    // Transformar estimación al formato que espera EstimationResult
    const resultData = {
        estimated_weight: estimation.estimated_weight,
        confidence_score: estimation.confidence_score,
        breed: estimation.breed,
        breed_confidence: estimation.breed_confidence,
        processing_time_ms: estimation.processing_time_ms,
        model_version: estimation.model_version
    };

    return (
        <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
                <EstimationImage 
                    imagePath={estimation.frame_image_path} 
                    apiBaseUrl={apiBaseUrl}
                />
            </Grid>
            
            <Grid item xs={12} md={6}>
                <EstimationResult 
                    result={resultData}
                    loading={false}
                    showActions={false}
                />
            </Grid>

            <Grid item xs={12}>
                <EstimationMetadata estimation={estimation} />
            </Grid>
        </Grid>
    );
}

export default WeightEstimationDetail;

