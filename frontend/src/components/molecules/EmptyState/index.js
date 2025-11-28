// frontend/src/components/molecules/EmptyState/index.js

import CustomTypography from '../../atoms/CustomTypography';
import Card from '../../atoms/Card';

/**
 * EmptyState molecule - Estado vacío reutilizable
 * @param {string} message - Mensaje a mostrar
 */
function EmptyState({ message = 'No hay datos disponibles.' }) {
    return (
        <Card>
            <CustomTypography variant="body2" color="text.secondary" textAlign="center">
                {message}
            </CustomTypography>
        </Card>
    );
}

export default EmptyState;

