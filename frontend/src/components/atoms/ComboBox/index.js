// frontend/src/components/atoms/ComboBox/index.js

import * as React from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import InputAdornment from '@mui/material/InputAdornment';
import { Grid } from '@mui/material';
import styled from '@emotion/styled';

const StyledAutocomplete = styled(Autocomplete)(({ theme }) => ({
    '& .MuiAutocomplete-clearIndicator': {
        padding: theme.spacing(0.5),
    },
    '& .MuiAutocomplete-popupIndicator': {
        padding: theme.spacing(0.5),
    },
    '& .MuiAutocomplete-endAdornment': {
        right: theme.spacing(1),
        '& .MuiAutocomplete-popupIndicator': {
            transform: 'translateY(0)',
        }
    }
}));

/**
 * ComboBox atom - Campo de selección con autocompletado y soporte para iconos
 * @param {number} xs - Tamaño en grid para pantallas pequeñas
 * @param {number} md - Tamaño en grid para pantallas medianas
 * @param {Array} options - Opciones para el combobox (debe tener formato {id, label, value})
 * @param {string} label - Etiqueta del campo
 * @param {string} fieldName - Nombre del campo
 * @param {Function} onChange - Callback cuando cambia la selección (fieldName, value)
 * @param {ReactNode} startIcon - Icono al inicio del campo
 * @param {Object} ...props - Props adicionales para Autocomplete/TextField
 */
function ComboBox({ xs, md, options, label, fieldName, onChange, startIcon, value, required, ...props }) {
    const handleSelectionChange = (event, selectedValue) => {
        onChange(fieldName, selectedValue);  // Pasamos el fieldName junto con el valor al onChange
    };

    // Encontrar el valor seleccionado basado en el value prop (puede ser un ID o el objeto completo)
    const selectedOption = React.useMemo(() => {
        if (!value) return null;
        if (typeof value === 'object') return value;
        return options.find(opt => opt.id === value || opt.value === value) || null;
    }, [value, options]);

    return (
        <Grid item xs={xs} md={md}>
            <StyledAutocomplete
                disablePortal
                options={options || []}
                value={selectedOption}
                onChange={handleSelectionChange}
                getOptionLabel={(option) => option?.label || ''}
                isOptionEqualToValue={(option, val) => {
                    if (!option || !val) return false;
                    return option.id === val.id || (option.value && option.value === val.value);
                }}
                renderInput={(params) => {
                    const { InputLabelProps: paramsInputLabelProps, ...restParams } = params;
                    return (
                        <TextField
                            {...restParams}
                            label={label}
                            variant="standard"
                            fullWidth
                            required={required}
                            InputLabelProps={{
                                ...paramsInputLabelProps,
                                ...(required && {
                                    sx: {
                                        ...paramsInputLabelProps?.sx,
                                        '& .MuiInputLabel-asterisk': {
                                            color: 'error.main',
                                            fontSize: '1.5em',
                                            fontWeight: 'bold',
                                            verticalAlign: 'baseline',
                                            display: 'inline-block',
                                            lineHeight: '1em',
                                            transform: 'translateY(0.1em)',
                                            marginLeft: '2px',
                                        }
                                    }
                                })
                            }}
                            InputProps={{
                                ...params.InputProps,
                                startAdornment: startIcon ? (
                                    <InputAdornment position="start">
                                        {startIcon}
                                    </InputAdornment>
                                ) : null,
                            }}
                            {...props}
                        />
                    );
                }}
            />
        </Grid>
    );
}

export default ComboBox;

