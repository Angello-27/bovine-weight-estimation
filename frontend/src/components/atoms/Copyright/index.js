// src/components/atoms/Copyright/index.js
import { Link } from '@mui/material';
import Typography from '@mui/material/Typography';

function Copyright({ children, ...props }) {
    const currentYear = new Date().getFullYear();
    
    return (
        <Typography variant="subtitle2" color="text.secondary" align="center" {...props}>
            {'Copyright © '}
            {currentYear}
            {' '}
            <Link color="inherit" href="https://taller.agrocom.com.bo/" target="_blank" rel="noopener noreferrer">
                Hacienda Gamelera
            </Link>
            {'. Todos los derechos reservados.'}
        </Typography>
    );
}

export default Copyright;
