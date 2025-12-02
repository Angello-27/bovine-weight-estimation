// frontend/src/components/atoms/SearchField/index.js

import React, { useState, useEffect } from 'react';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import IconButton from '@mui/material/IconButton';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';
import Box from '@mui/material/Box';

/**
 * SearchField atom - Campo de búsqueda con botón de búsqueda y limpiar
 * @param {string} value - Valor controlado del campo
 * @param {Function} onChange - Callback cuando cambia el valor (solo actualiza el input)
 * @param {Function} onSearch - Callback cuando se aplica la búsqueda (botón o Enter)
 * @param {Function} onClear - Callback cuando se limpia el campo
 * @param {string} placeholder - Placeholder del campo
 * @param {string} size - Tamaño del campo ('small' | 'medium')
 * @param {Object} sx - Estilos adicionales
 * @param {Object} ...props - Props adicionales para TextField
 */
function SearchField({
    value = '',
    onChange,
    onSearch,
    onClear,
    placeholder = 'Buscar...',
    size = 'small',
    sx = {},
    ...props
}) {
    // Estado interno para el valor del input (para permitir escribir sin buscar)
    const [inputValue, setInputValue] = useState(value);
    
    // Sincronizar con el prop cuando cambia externamente (ej: cuando se limpia)
    useEffect(() => {
        setInputValue(value);
    }, [value]);

    const handleInputChange = (e) => {
        const newValue = e.target.value;
        setInputValue(newValue);
        // Notificar cambio al componente padre
        if (onChange) {
            onChange(e);
        }
    };

    const handleSearch = () => {
        // Aplicar búsqueda con el valor actual del input
        if (onSearch) {
            onSearch(inputValue);
        }
    };

    const handleClear = () => {
        setInputValue('');
        // Limpiar en el componente padre
        if (onClear) {
            onClear();
        }
        // También notificar onChange con valor vacío
        if (onChange) {
            const syntheticEvent = {
                target: { value: '' },
                type: 'change'
            };
            onChange(syntheticEvent);
        }
    };

    const handleKeyPress = (e) => {
        // Permitir buscar con Enter
        if (e.key === 'Enter') {
            handleSearch();
        }
    };

    return (
        <Box sx={{ width: '100%', ...sx }}>
            <TextField
                fullWidth
                variant="outlined"
                size={size}
                placeholder={placeholder}
                value={inputValue}
                onChange={handleInputChange}
                onKeyPress={handleKeyPress}
                InputProps={{
                    startAdornment: (
                        <InputAdornment position="start">
                            <IconButton
                                size="small"
                                onClick={handleSearch}
                                edge="start"
                                sx={{ mr: 0 }}
                                aria-label="Buscar"
                            >
                                <SearchIcon color="action" fontSize="small" />
                            </IconButton>
                        </InputAdornment>
                    ),
                    endAdornment: inputValue && (
                        <InputAdornment position="end">
                            <IconButton
                                size="small"
                                onClick={handleClear}
                                edge="end"
                                aria-label="Limpiar búsqueda"
                            >
                                <ClearIcon fontSize="small" />
                            </IconButton>
                        </InputAdornment>
                    ),
                }}
                sx={{
                    '& .MuiOutlinedInput-root': {
                        backgroundColor: (theme) => 
                            theme.palette.mode === 'dark' 
                                ? theme.palette.grey[800] 
                                : theme.palette.grey[50],
                    }
                }}
                {...props}
            />
        </Box>
    );
}

export default SearchField;

