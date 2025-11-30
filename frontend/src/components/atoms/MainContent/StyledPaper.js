// components/atoms/StyledPaper/index.js
import Paper from '@mui/material/Paper';
import { styled } from '@mui/system';
import { drawer } from '../../../config/constants';

const StyledPaper = styled(Paper)(({ theme, open }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    margin: theme.spacing(2, 1), // margin-y: 3, margin-x: 0
    ...(open && {
        transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.easeOut,
            duration: theme.transitions.duration.enteringScreen,
        }),
        marginLeft: `calc(${theme.spacing(1)} + ${drawer.width}px)`,
    }),
}));

export default StyledPaper;
