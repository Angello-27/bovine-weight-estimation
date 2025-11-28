import { styled } from '@mui/material/styles';
import Grid from '@mui/material/Grid'; // Asegúrate de importar Grid

export const StyledGrid = styled(Grid)(({ theme }) => ({
    backgroundImage: 'url(https://source.unsplash.com/800x600/?irrigation,agriculture)',
    backgroundRepeat: 'no-repeat',
    backgroundColor: theme.palette.mode === 'light' ?
        'var(--color-light);' :
        'var(--color-dark);',
    backgroundSize: 'cover',
    backgroundPosition: 'center',
}));
