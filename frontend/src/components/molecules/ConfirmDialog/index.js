// frontend/src/components/molecules/ConfirmDialog/index.js

import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import CustomButton from '../../atoms/CustomButton';
import CustomTypography from '../../atoms/CustomTypography';
import Box from '@mui/material/Box';
import WarningIcon from '@mui/icons-material/Warning';
import { useTheme } from '@mui/material/styles';

/**
 * ConfirmDialog molecule - Dialog de confirmación personalizado
 * @param {boolean} open - Estado de apertura del dialog
 * @param {Function} onClose - Callback cuando se cierra el dialog
 * @param {Function} onConfirm - Callback cuando se confirma la acción
 * @param {string} title - Título del dialog
 * @param {string} message - Mensaje de confirmación
 * @param {string} confirmText - Texto del botón de confirmar (default: "Confirmar")
 * @param {string} cancelText - Texto del botón de cancelar (default: "Cancelar")
 * @param {string} confirmColor - Color del botón de confirmar (default: "error")
 */
function ConfirmDialog({
    open,
    onClose,
    onConfirm,
    title = 'Confirmar acción',
    message,
    confirmText = 'Confirmar',
    cancelText = 'Cancelar',
    confirmColor = 'error'
}) {
    const theme = useTheme();

    const handleConfirm = () => {
        onConfirm();
        onClose();
    };

    return (
        <Dialog
            open={open}
            onClose={onClose}
            maxWidth="sm"
            fullWidth
            PaperProps={{
                sx: {
                    borderRadius: 2,
                }
            }}
        >
            <DialogTitle sx={{ pb: 2, pt: 4 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                    <WarningIcon 
                        sx={{ 
                            color: theme.palette.warning.main,
                            fontSize: 28
                        }} 
                    />
                    <CustomTypography variant="h6" component="span">
                        {title}
                    </CustomTypography>
                </Box>
            </DialogTitle>
            <DialogContent sx={{ pt: 2, pb: 2 }}>
                <CustomTypography variant="body1" color="text.secondary">
                    {message}
                </CustomTypography>
            </DialogContent>
            <DialogActions sx={{ px: 3, pb: 3, gap: 1 }}>
                <CustomButton
                    onClick={onClose}
                    variant="outlined"
                    color="inherit"
                >
                    {cancelText}
                </CustomButton>
                <CustomButton
                    onClick={handleConfirm}
                    variant="contained"
                    color={confirmColor}
                >
                    {confirmText}
                </CustomButton>
            </DialogActions>
        </Dialog>
    );
}

export default ConfirmDialog;

