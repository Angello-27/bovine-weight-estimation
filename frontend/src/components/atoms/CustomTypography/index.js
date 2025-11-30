// components/atoms/CustomTypography/index.js
import Typography from '@mui/material/Typography';

/**
 * Variantes personalizadas de CustomTypography
 * Permite reutilizar estilos comunes sin repetir código
 */
const CUSTOM_VARIANTS = {
    sectionTitle: {
        variant: 'h6',
        component: 'h2',
        sx: {
            flex: 1,
            marginLeft: '16px',
            fontWeight: 500,
            textTransform: 'uppercase',
            letterSpacing: '0.5px',
            fontSize: '1rem',
        },
    },
    userName: {
        variant: 'body1',
        sx: {
            fontWeight: 500,
            fontSize: '0.875rem',
        },
    },
    pageTitle: {
        variant: 'h3',
        sx: {
            fontWeight: 600,
        },
    },
    pageDescription: {
        variant: 'body1',
        sx: {
            color: 'text.secondary',
            maxWidth: '600px',
            mx: 'auto',
        },
    },
};

/**
 * Componente CustomTypography - Atom que envuelve Typography de MUI
 * 
 * Características:
 * - Usa automáticamente el color del tema (text.primary) si no se especifica otro
 * - Se adapta automáticamente a dark/light mode
 * - Permite sobrescribir todos los estilos y props de Typography
 * - Soporta variantes personalizadas además de las nativas de MUI
 * 
 * @param {string} customVariant - Variante personalizada (ej: 'sectionTitle', 'userName')
 * @param {object} sx - Estilos personalizados (se mergean con los de la variante)
 * @param {string} color - Color del texto
 * @param {object} ...props - Resto de props de Typography de MUI
 */
function CustomTypography({ customVariant, sx, color, variant, component, ...props }) {
    // Obtener la configuración de la variante personalizada si existe
    const variantConfig = customVariant ? CUSTOM_VARIANTS[customVariant] : null;
    
    // Si existe una variante personalizada, usar sus valores por defecto
    // pero permitir sobrescribirlos con props explícitos
    const finalVariant = variant || (variantConfig?.variant);
    const finalComponent = component || (variantConfig?.component);
    const variantSx = variantConfig?.sx || {};
    
    // Si no se especifica un color explícito (ni en prop color ni en sx.color), 
    // usar text.primary por defecto para que se adapte al tema dark/light
    const hasExplicitColor = color !== undefined || (sx && sx.color !== undefined) || (variantSx && variantSx.color);
    
    // Mergear sx: primero la variante, luego el sx proporcionado, y finalmente el color por defecto si no hay explícito
    // El orden es importante: sx tiene prioridad sobre variantSx, y variantSx tiene prioridad sobre el color por defecto
    const mergedSx = hasExplicitColor 
        ? { ...variantSx, ...(sx || {}) }
        : { color: 'text.primary', ...variantSx, ...(sx || {}) };

    // Si se especifica color como prop, pasarlo directamente; si no, undefined
    return (
        <Typography 
            {...props} 
            variant={finalVariant}
            component={finalComponent}
            sx={mergedSx} 
            color={color} 
        />
    );
}

export default CustomTypography;
