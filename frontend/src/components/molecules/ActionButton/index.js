// frontend/src/components/molecules/ActionButton/index.js

import Button from '@mui/material/Button';
import CustomButton from '../../atoms/CustomButton';

/**
 * ActionButton molecule - Botón de acción con icono
 * @param {ReactNode} icon - Icono a mostrar
 * @param {string} label - Texto del botón
 * @param {Function} onClick - Callback al hacer click
 * @param {string} variant - Variante del botón (contained, outlined, etc.)
 */
function ActionButton({ icon, label, onClick, variant = 'contained', ...props }) {
    return (
        <CustomButton
            variant={variant}
            startIcon={icon}
            onClick={onClick}
            {...props}
        >
            {label}
        </CustomButton>
    );
}

export default ActionButton;

