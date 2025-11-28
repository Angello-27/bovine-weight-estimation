// frontend/src/components/molecules/StatCard/index.js

import Grid from "@mui/material/Grid";
import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';

/**
 * StatCard molecule - Card de estadística reutilizable
 * @param {string} label - Etiqueta de la estadística
 * @param {string|number} value - Valor a mostrar
 * @param {string} unit - Unidad opcional (ej: "kg", "%")
 */
function StatCard({ label, value, unit = '' }) {
    return (
        <Grid item xs={12} md={3}>
            <Card>
                <CustomTypography variant="h6" color="text.secondary">
                    {label}
                </CustomTypography>
                <CustomTypography variant="h4" mt={1}>
                    {value || 0} {unit}
                </CustomTypography>
            </Card>
        </Grid>
    );
}

export default StatCard;

