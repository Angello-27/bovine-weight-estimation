// frontend/src/components/atoms/DateField/index.js

import Grid from "@mui/material/Grid";
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';
import dayjs from 'dayjs';

/**
 * DateField atom - Campo de entrada de fecha elegante con DatePicker de MUI X
 * Usa el componente DatePicker de @mui/x-date-pickers para una mejor UX
 * @param {number} xs - Tamaño en grid para pantallas pequeñas
 * @param {number} md - Tamaño en grid para pantallas medianas
 * @param {ReactNode} startIcon - Icono al inicio del campo
 * @param {ReactNode} endIcon - Icono al final del campo
 * @param {string} value - Valor de la fecha en formato string (YYYY-MM-DD)
 * @param {Function} onChange - Callback cuando cambia la fecha
 * @param {Object} ...props - Props adicionales para DatePicker
 */
function DateField({ 
    xs, 
    md, 
    startIcon, 
    endIcon, 
    required, 
    value, 
    onChange, 
    name,
    error,
    helperText,
    label,
    InputLabelProps: customInputLabelProps,
    ...props 
}) {
    // Convertir string a dayjs object para el DatePicker
    const dateValue = value ? dayjs(value) : null;

    // Manejar cambio de fecha y convertir a string
    const handleDateChange = (newValue) => {
        if (onChange) {
            // Crear un evento sintético para mantener compatibilidad con otros formularios
            const event = {
                target: {
                    name: name,
                    value: newValue ? newValue.format('YYYY-MM-DD') : ''
                }
            };
            onChange(event);
        }
    };

    return (
        <Grid item xs={xs} md={md}>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
                <DatePicker
                    label={label}
                    value={dateValue}
                    onChange={handleDateChange}
                    required={required}
                    slotProps={{
                        textField: {
                            variant: "standard",
                            fullWidth: true,
                            error: error,
                            helperText: helperText,
                            InputLabelProps: {
                                shrink: true,
                                ...customInputLabelProps,
                                ...(required && {
                                    sx: {
                                        ...customInputLabelProps?.sx,
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
                            },
                            InputProps: {
                                startAdornment: startIcon ? (
                                    <InputAdornment position="start">
                                        {startIcon}
                                    </InputAdornment>
                                ) : null,
                                endAdornment: endIcon ? (
                                    <InputAdornment position="end">
                                        {endIcon}
                                    </InputAdornment>
                                ) : null,
                            },
                        }
                    }}
                    {...props}
                />
            </LocalizationProvider>
        </Grid>
    );
}

export default DateField;

