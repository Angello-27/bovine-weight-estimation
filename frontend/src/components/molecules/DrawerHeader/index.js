import * as React from 'react';
import { styled } from '@mui/material/styles';
import BackIconButton from '../../atoms/BackIconButton';

const DrawerHeaderStyle = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    ...theme.mixins.toolbar,
}));

function DrawerHeader({ handleDrawerClose }) {
    return (
        <DrawerHeaderStyle>
            <BackIconButton onClick={handleDrawerClose} />
        </DrawerHeaderStyle>
    );
}

export default DrawerHeader;
