// frontend/src/containers/weight-estimations/EstimateWeightFromImage.js

import { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import estimateWeightFromImage from '../../services/weight-estimations/estimateWeightFromImage';
import { clearCache } from '../../utils/cache/weightEstimationsCache';

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

    // No filtrar aquí, se hará en el componente que obtiene los datos
    const filteredCattle = useMemo(() => {
        // Retornar array vacío, los datos se obtendrán desde el servicio
        return [];
    }, []);

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

        // El endpoint /api/v1/ml/estimate ya guarda automáticamente, así que si tiene ID, solo redirigir
        if (estimationResult.id) {
            clearCache();
            navigate(`/weight-estimations/${estimationResult.id}`);
            return;
        }

        // Si por alguna razón no tiene ID, guardar nuevamente con la imagen
        if (!formData.image) {
            setError('No hay imagen para guardar.');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            // Usar el endpoint /api/v1/ml/estimate que guarda automáticamente con la imagen
            const savedEstimation = await estimateWeightFromImage(
                formData.image,
                estimationResult.breed || formData.breed,
                formData.cattle_id || null
            );

            // Invalidar caché
            clearCache();

            // Redirigir al detalle de la estimación guardada
            if (savedEstimation.id) {
                navigate(`/weight-estimations/${savedEstimation.id}`);
            } else {
                // Si no tiene ID, redirigir a la lista
                navigate('/weight-estimations');
            }
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

    const handleGoBack = () => {
        setSelectedBreed('');
        setFormData(prev => ({
            ...prev,
            breed: '',
            cattle_id: ''
        }));
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
        onReset: handleReset,
        onGoBack: handleGoBack
    };
}

export default EstimateWeightFromImage;

