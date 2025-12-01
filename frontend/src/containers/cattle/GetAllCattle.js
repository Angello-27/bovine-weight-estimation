// frontend/src/containers/cattle/GetAllCattle.js

import { useState, useEffect } from 'react';
import { getAnimalsByCriteria } from '../../services/cattle/getAnimalsByCriteria';
import { getCurrentUser } from '../../services/auth/authService';
import { getAllFarms } from '../../services/farm/getAllFarms';

function GetAllCattle() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                // Intentar obtener farm_id del usuario
                const currentUser = getCurrentUser();
                let farmId = currentUser?.farm_id;
                
                // Si el usuario no tiene farm_id, obtener la primera hacienda disponible
                if (!farmId) {
                    try {
                        const farmsResponse = await getAllFarms({ limit: 1 });
                        if (farmsResponse?.farms && farmsResponse.farms.length > 0) {
                            farmId = farmsResponse.farms[0].id;
                            console.log('Usando primera hacienda disponible:', farmId);
                        }
                    } catch (e) {
                        console.warn('No se pudo obtener haciendas:', e);
                    }
                }
                
                // Llamar al servicio con farm_id
                if (!farmId) {
                    throw new Error('No se encontró una hacienda. Por favor, contacta al administrador para asignarte una hacienda.');
                }
                
                const data = await getAnimalsByCriteria(
                    { farm_id: farmId },
                    { page: 1, page_size: 1000 } // Obtener todos los animales
                );
                
                // El servicio retorna { animals: [...], total, page, page_size }
                const cattleList = data?.animals || [];
                setItems(cattleList);
            } catch (err) {
                // Asegurar que el error sea un string
                const errorMessage = err?.message || err?.toString() || 'Error al obtener animales';
                setError(errorMessage);
                console.error('Error al obtener animales:', err);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    return { items, loading, error };
}

export default GetAllCattle;

