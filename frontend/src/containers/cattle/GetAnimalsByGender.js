// frontend/src/containers/cattle/GetAnimalsByGender.js

import { useState, useEffect } from 'react';
import { getAnimalsByCriteria } from '../../services/cattle';
import { getCurrentUser } from '../../services/auth/authService';

/**
 * Hook para obtener animales filtrados por género
 * @param {string} gender - 'male' o 'female'
 * @returns {Object} { items, loading, error }
 */
function GetAnimalsByGender(gender) {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!gender) {
            setItems([]);
            return;
        }

        const fetchAnimals = async () => {
            try {
                setLoading(true);
                setError(null);

                // Obtener farm_id del usuario actual
                const currentUser = getCurrentUser();
                let farmId = currentUser?.farm_id || currentUser?.farm?.id;

                if (!farmId) {
                    throw new Error('No se encontró una hacienda asignada.');
                }

                // Obtener animales filtrados por género
                const data = await getAnimalsByCriteria(
                    { farm_id: farmId, gender },
                    { page: 1, page_size: 100 } // Obtener hasta 100 animales
                );

                setItems(data?.animals || []);
            } catch (err) {
                setError(err?.message || 'Error al cargar animales');
                setItems([]);
            } finally {
                setLoading(false);
            }
        };

        fetchAnimals();
    }, [gender]);

    return { items, loading, error };
}

export default GetAnimalsByGender;

