// frontend/src/components/molecules/StatItem/index.js

import Box from '@mui/material/Box';
import Divider from '@mui/material/Divider';
import CustomTypography from '../../atoms/CustomTypography';

/**
 * StatItem molecule - Item de estadística con label y valor
 * @param {string} label - Etiqueta de la estadística
 * @param {string|number} value - Valor a mostrar
 * @param {string} color - Color del valor (opcional)
 * @param {ReactNode} subtitle - Subtítulo opcional debajo del valor
 * @param {boolean} showDivider - Mostrar divisor debajo (default: true)
 */
function StatItem({ label, value, color, subtitle, showDivider = true }) {
    return (
        <>
            <Box>
                <CustomTypography variant="body2" color="text.secondary">
                    {label}
                </CustomTypography>
                <CustomTypography 
                    variant="h5" 
                    sx={{ 
                        fontWeight: 600,
                        ...(color && { color })
                    }}
                >
                    {value}
                </CustomTypography>
                {subtitle && (
                    <CustomTypography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                        {subtitle}
                    </CustomTypography>
                )}
            </Box>
            {showDivider && <Divider />}
        </>
    );
}

export default StatItem;

