// frontend/src/containers/cattle/FilterCattle.js

import { useState, useMemo } from 'react';

/**
 * FilterCattle container hook - Maneja la lógica de búsqueda y filtrado de ganado
 * @param {Array} items - Lista de animales a filtrar
 * @returns {Object} { filteredItems, searchQuery, filters, handleSearchChange, handleFilterChange }
 */
function FilterCattle(items) {
    const [searchQuery, setSearchQuery] = useState('');
    const [filters, setFilters] = useState({
        breed: '',
        gender: ''
    });

    const handleSearchChange = (event) => {
        setSearchQuery(event.target.value);
    };

    const handleFilterChange = (name, value) => {
        setFilters(prev => ({
            ...prev,
            [name]: value
        }));
    };

    // Filtrar items basado en búsqueda y filtros
    const filteredItems = useMemo(() => {
        if (!items) return [];

        return items.filter(item => {
            // Búsqueda por texto (caravana, nombre, raza)
            const matchesSearch = !searchQuery || 
                item.ear_tag?.toLowerCase().includes(searchQuery.toLowerCase()) ||
                item.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
                item.breed?.toLowerCase().includes(searchQuery.toLowerCase());

            // Filtro por raza
            const matchesBreed = !filters.breed || item.breed === filters.breed;

            // Filtro por género
            const matchesGender = !filters.gender || item.gender === filters.gender;

            return matchesSearch && matchesBreed && matchesGender;
        });
    }, [items, searchQuery, filters]);

    return {
        filteredItems,
        searchQuery,
        filters,
        handleSearchChange,
        handleFilterChange
    };
}

export default FilterCattle;

