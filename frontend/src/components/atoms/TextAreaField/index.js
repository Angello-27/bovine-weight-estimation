// components/atoms/TextAreaField/index.js
import Grid from "@mui/material/Grid";
import TextField from '@mui/material/TextField';
import InputAdornment from '@mui/material/InputAdornment';

/**
 * TextAreaField atom - Campo de texto multilinea (textarea) con soporte para iconos
 * @param {number} xs - Tamaño en grid para pantallas pequeñas
 * @param {number} md - Tamaño en grid para pantallas medianas
 * @param {ReactNode} startIcon - Icono al inicio del campo
 * @param {ReactNode} endIcon - Icono al final del campo
 * @param {Object} ...props - Props adicionales para TextField
 */
function TextAreaField({ xs, md, startIcon, endIcon, required, InputLabelProps: customInputLabelProps, ...props }) {
    return (
        <Grid item xs={xs} md={md}>
            <TextField
                variant="standard"
                fullWidth
                multiline
                required={required}
                InputLabelProps={{
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
                }}
                InputProps={{
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
                }}
                {...props}
            />
        </Grid>
    );
}

export default TextAreaField;

