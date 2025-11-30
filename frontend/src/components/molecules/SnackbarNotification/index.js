// frontend/src/components/molecules/SnackbarNotification/index.js

import React from 'react';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

/**
 * SnackbarNotification - Componente para mostrar notificaciones (errores y éxito)
 * @param {boolean} errorSnackbar.open - Estado de apertura del snackbar de error
 * @param {string} errorSnackbar.message - Mensaje de error
 * @param {boolean} successSnackbar.open - Estado de apertura del snackbar de éxito
 * @param {string} successSnackbar.message - Mensaje de éxito
 * @param {Function} onCloseError - Callback para cerrar snackbar de error
 * @param {Function} onCloseSuccess - Callback para cerrar snackbar de éxito
 */
function SnackbarNotification({
    errorSnackbar,
    successSnackbar,
    onCloseError,
    onCloseSuccess
}) {
    return (
        <>
            {/* Snackbar para errores */}
            <Snackbar
                open={errorSnackbar.open}
                autoHideDuration={5000}
                onClose={onCloseError}
                anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            >
                <Alert 
                    onClose={onCloseError}
                    severity="error" 
                    variant="filled"
                    sx={{ 
                        width: '100%',
                        display: 'flex',
                        alignItems: 'center',
                        '& .MuiAlert-message': {
                            display: 'flex',
                            alignItems: 'center',
                            padding: '4px 0',
                            flex: 1,
                        },
                        '& .MuiAlert-action': {
                            paddingTop: 0,
                            paddingBottom: 0,
                            display: 'flex',
                            alignItems: 'center',
                            alignSelf: 'center',
                        }
                    }}
                >
                    {errorSnackbar.message}
                </Alert>
            </Snackbar>

            {/* Snackbar para éxito */}
            <Snackbar
                open={successSnackbar.open}
                autoHideDuration={3000}
                onClose={onCloseSuccess}
                anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            >
                <Alert 
                    onClose={onCloseSuccess}
                    severity="success" 
                    variant="filled"
                    sx={{ 
                        width: '100%',
                        display: 'flex',
                        alignItems: 'center',
                        '& .MuiAlert-message': {
                            display: 'flex',
                            alignItems: 'center',
                            padding: '4px 0',
                            flex: 1,
                        },
                        '& .MuiAlert-action': {
                            paddingTop: 0,
                            paddingBottom: 0,
                            display: 'flex',
                            alignItems: 'center',
                            alignSelf: 'center',
                        }
                    }}
                >
                    {successSnackbar.message}
                </Alert>
            </Snackbar>
        </>
    );
}

export default SnackbarNotification;

