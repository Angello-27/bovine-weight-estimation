// src/components/molecules/ErrorAlert.js
import { useState, forwardRef, useEffect } from 'react';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

const Alert = forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

function ErrorAlert({ errorMessage }) {
    const [open, setOpen] = useState(Boolean(errorMessage));

    // Actualiza el estado `open` si `errorMessage` cambia.
    useEffect(() => {
        setOpen(Boolean(errorMessage));
    }, [errorMessage]);

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setOpen(false);
    };

    return errorMessage ?
        <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
            <Alert onClose={handleClose} severity="error" sx={{ width: '100%' }}>
                {errorMessage}
            </Alert>
        </Snackbar>
        : null;
}

export default ErrorAlert;
