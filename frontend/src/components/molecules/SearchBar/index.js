// frontend/src/components/molecules/SearchBar/index.js

import Box from "@mui/material/Box";
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import SearchIcon from '@mui/icons-material/Search';

/**
 * SearchBar molecule - Barra de búsqueda reutilizable
 * @param {string} value - Valor del campo de búsqueda
 * @param {Function} onChange - Callback cuando cambia el valor
 * @param {string} placeholder - Texto placeholder
 */
function SearchBar({ value, onChange, placeholder = "Buscar..." }) {
    return (
        <Box mb={2}>
            <TextField
                fullWidth
                variant="outlined"
                placeholder={placeholder}
                value={value}
                onChange={onChange}
                InputProps={{
                    startAdornment: (
                        <InputAdornment position="start">
                            <SearchIcon color="action" />
                        </InputAdornment>
                    ),
                }}
            />
        </Box>
    );
}

export default SearchBar;

