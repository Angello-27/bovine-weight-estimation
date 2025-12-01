// components/atoms/RadioButtonGroup/index.js
import Grid from "@mui/material/Grid";
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import RadioGroup from '@mui/material/RadioGroup';
import RadioButton from '../RadioButton';
import FormHelperText from '@mui/material/FormHelperText';

/**
 * RadioButtonGroup atom - Grupo de radio buttons con label
 * @param {number} xs - Tamaño en grid para pantallas pequeñas
 * @param {number} md - Tamaño en grid para pantallas medianas
 * @param {Array} options - Array de opciones con formato {id, label}
 * @param {string} label - Label del grupo
 * @param {string} name - Nombre del campo
 * @param {string} value - Valor seleccionado
 * @param {Function} onChange - Callback cuando cambia la selección
 * @param {boolean} required - Si el campo es requerido
 * @param {boolean} error - Si hay error
 * @param {string} helperText - Texto de ayuda o error
 * @param {boolean} row - Si los radio buttons deben mostrarse en fila
 * @param {Object} ...props - Props adicionales para RadioGroup
 */
function RadioButtonGroup({ 
    xs, 
    md, 
    options = [], 
    label, 
    name, 
    value, 
    onChange, 
    required, 
    error, 
    helperText,
    row = false,
    ...props 
}) {
    return (
        <Grid item xs={xs} md={md}>
            <FormControl error={error} required={required} fullWidth>
                {label && (
                    <FormLabel 
                        id={`radio-buttons-${name}`}
                        required={required}
                        sx={{
                            mb: 1,
                            ...(required && {
                                '& .MuiFormLabel-asterisk': {
                                    color: 'error.main',
                                    fontSize: '1.5em',
                                    fontWeight: 'bold',
                                    verticalAlign: 'baseline',
                                    display: 'inline-block',
                                    lineHeight: '1em',
                                    transform: 'translateY(0.1em)',
                                    marginLeft: '2px',
                                }
                            })
                        }}
                    >
                        {label}
                    </FormLabel>
                )}
                <RadioGroup 
                    name={name}
                    value={value || ''} 
                    onChange={(e) => {
                        // Crear evento sintético con target.name para que funcione con handleChange del formulario
                        const syntheticEvent = {
                            target: {
                                name: name,
                                value: e.target.value
                            }
                        };
                        if (onChange) {
                            onChange(syntheticEvent);
                        }
                    }}
                    row={row}
                    aria-labelledby={`radio-buttons-${name}`}
                    {...props}
                >
                    {options.map(option => (
                        <RadioButton 
                            key={option.id || option.value} 
                            value={option.id || option.value} 
                            label={option.label} 
                        />
                    ))}
                </RadioGroup>
                {helperText && (
                    <FormHelperText>{helperText}</FormHelperText>
                )}
            </FormControl>
        </Grid>
    );
}

export default RadioButtonGroup;

