// src/components/atoms/CustomLink.js
import { Link } from '@mui/material';
import Typography from '@mui/material/Typography';

function Copyright({ children, ...props }) {
    return (
        <Typography variant="subtitle2" color="text.secondary" align="center" {...props} >
            {'Copyright © '}
            <Link color="inherit" href="https://agrocom.com.bo/site/">
                agrocom.com.bo
            </Link>
            {' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}

export default Copyright;
