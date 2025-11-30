import * as React from 'react';
import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import BackIconButton from '../../atoms/BackIconButton';

const DrawerHeaderStyle = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: theme.spacing(1, 2),
    ...theme.mixins.toolbar,
    borderBottom: `1px solid ${theme.palette.divider}`,
}));

function DrawerHeader({ handleDrawerClose }) {
    return (
        <DrawerHeaderStyle>
            <Typography 
                variant="h6" 
                component="div" 
                sx={{ 
                    fontWeight: 600,
                    color: 'primary.main',
                    fontSize: '1.25rem'
                }}
            >
                Gamelera
            </Typography>
            <BackIconButton onClick={handleDrawerClose} />
        </DrawerHeaderStyle>
    );
}

export default DrawerHeader;
