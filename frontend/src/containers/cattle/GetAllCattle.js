// frontend/src/containers/cattle/GetAllCattle.js

import { useState, useEffect } from 'react';
import getAllCattle from '../../services/cattle/getAllCattle';
import { getAllFarms } from '../../services/farm/getAllFarms';

function GetAllCattle() {
    const [items, setItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function fetchData() {
            try {
                // Intentar obtener farm_id del usuario
                const userStr = localStorage.getItem('user');
                let farmId = null;
                
                if (userStr) {
                    try {
                        const user = JSON.parse(userStr);
                        farmId = user.farm_id;
                    } catch (e) {
                        console.warn('Error al parsear usuario:', e);
                    }
                }
                
                // Si el usuario no tiene farm_id, obtener la primera finca disponible
                if (!farmId) {
                    try {
                        const farmsResponse = await getAllFarms({ limit: 1 });
                        if (farmsResponse?.farms && farmsResponse.farms.length > 0) {
                            farmId = farmsResponse.farms[0].id;
                            console.log('Usando primera finca disponible:', farmId);
                        }
                    } catch (e) {
                        console.warn('No se pudo obtener fincas:', e);
                    }
                }
                
                // Llamar al servicio con farm_id
                if (!farmId) {
                    throw new Error('No se encontró una finca. Por favor, contacta al administrador para asignarte una finca.');
                }
                
                const filters = { farm_id: farmId };
                const data = await getAllCattle(filters);
                
                // El servicio retorna { animals: [...], total, page, page_size }
                const cattleList = data.animals || data || [];
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

