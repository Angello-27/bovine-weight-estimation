// frontend/src/containers/weight-estimations/EstimateWeightFromImage.js

import { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import estimateWeightFromImage from '../../services/weight-estimations/estimateWeightFromImage';
import createWeightEstimation from '../../services/weight-estimations/createWeightEstimation';

function EstimateWeightFromImage(initialAnimalId = null, allCattle = []) {
    const navigate = useNavigate();

    const [selectedBreed, setSelectedBreed] = useState('');
    const [formData, setFormData] = useState({
        image: null,
        cattle_id: initialAnimalId || '',
        breed: ''
    });

    const [estimationResult, setEstimationResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [imagePreview, setImagePreview] = useState(null);

    // Filtrar ganado por raza seleccionada
    const filteredCattle = useMemo(() => {
        if (!selectedBreed || !allCattle || allCattle.length === 0) {
            return [];
        }
        return allCattle.filter(cattle => cattle.breed === selectedBreed);
    }, [selectedBreed, allCattle]);

    const handleImageChange = (event) => {
        const file = event.target.files?.[0];
        if (file) {
            // Validar tipo de archivo
            const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
            if (!validTypes.includes(file.type)) {
                setError('Formato de imagen no válido. Use JPG, PNG o WEBP.');
                return;
            }

            // Validar tamaño (10MB máximo)
            const maxSize = 10 * 1024 * 1024; // 10MB
            if (file.size > maxSize) {
                setError('La imagen es demasiado grande. Máximo 10MB.');
                return;
            }

            setFormData(prev => ({ ...prev, image: file }));
            setError(null);

            // Crear preview
            const reader = new FileReader();
            reader.onloadend = () => {
                setImagePreview(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleBreedSelect = (breedId) => {
        setSelectedBreed(breedId);
        setFormData(prev => ({
            ...prev,
            breed: breedId,
            cattle_id: '' // Resetear selección de animal al cambiar raza
        }));
        setEstimationResult(null);
        setError(null);
    };

    const handleCattleSelect = (cattleId) => {
        setFormData(prev => ({
            ...prev,
            cattle_id: cattleId || ''
        }));
    };

    const handleEstimate = async () => {
        if (!formData.image) {
            setError('Por favor seleccione una imagen.');
            return;
        }

        if (!selectedBreed) {
            setError('Por favor seleccione una raza primero.');
            return;
        }

        setLoading(true);
        setError(null);
        setEstimationResult(null);

        try {
            const result = await estimateWeightFromImage(
                formData.image,
                selectedBreed,
                formData.cattle_id || null
            );

            setEstimationResult(result);
        } catch (err) {
            setError(err.message || 'Error al estimar el peso. Por favor intente de nuevo.');
        } finally {
            setLoading(false);
        }
    };

    const handleSaveEstimation = async () => {
        if (!estimationResult) {
            setError('No hay estimación para guardar.');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const estimationData = {
                animal_id: formData.cattle_id || null,
                breed: estimationResult.breed || formData.breed,
                estimated_weight_kg: estimationResult.estimated_weight,
                confidence: estimationResult.confidence_score,
                frame_image_path: estimationResult.image_path || '',
                method: 'web_upload',
                ml_model_version: estimationResult.model_version || '1.0.0',
                processing_time_ms: estimationResult.processing_time_ms || 0
            };

            await createWeightEstimation(estimationData);

            // Redirigir a la lista de estimaciones
            navigate('/weight-estimations');
        } catch (err) {
            setError(err.message || 'Error al guardar la estimación. Por favor intente de nuevo.');
        } finally {
            setLoading(false);
        }
    };

    const handleReset = () => {
        setSelectedBreed('');
        setFormData({
            image: null,
            cattle_id: '',
            breed: ''
        });
        setEstimationResult(null);
        setImagePreview(null);
        setError(null);
    };

    return {
        formData,
        estimationResult,
        loading,
        error,
        imagePreview,
        selectedBreed,
        filteredCattle,
        onImageChange: handleImageChange,
        onBreedSelect: handleBreedSelect,
        onCattleSelect: handleCattleSelect,
        onEstimate: handleEstimate,
        onSaveEstimation: handleSaveEstimation,
        onReset: handleReset
    };
}

export default EstimateWeightFromImage;

