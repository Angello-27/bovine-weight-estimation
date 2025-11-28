import { styled } from '@mui/system';
import Avatar from '@mui/material/Avatar';

export const StyledAvatar = styled(Avatar)(({ theme }) => ({
    margin: 1,
    backgroundColor: theme.palette.secondary.main // o cualquier color que prefieras para el tema oscuro
}));
