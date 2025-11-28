import * as React from 'react';
import { styled } from '@mui/material/styles';
import MuiDrawer from '@mui/material/Drawer';

import { drawer } from '../../../config/constants';

// Estilos omitidos para simplicidad. Reemplázalos con los tuyos.

const openedMixin = (theme) => ({
    width: drawer.width,
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
    }),
    overflowX: 'hidden',
});

const closedMixin = (theme) => ({
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: 'hidden',
    width: '1px',
    [theme.breakpoints.up('sm')]: {
        width: `1px`,
    },
});

// ...otros estilos y constantes aquí...
const DrawerPanel = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
    ({ theme, open }) => ({
        width: drawer.width,
        flexShrink: 0,
        whiteSpace: 'nowrap',
        boxSizing: 'border-box',
        ...(open && {
            ...openedMixin(theme),
            '& .MuiDrawer-paper': openedMixin(theme),
        }),
        ...(!open && {
            ...closedMixin(theme),
            '& .MuiDrawer-paper': closedMixin(theme),
        }),
    }),
);

function DrawerContent({ open, children }) {
    return (
        <DrawerPanel variant="permanent" open={open} PaperProps={{ elevation: 1 }} >
            {children}
        </DrawerPanel>
    );
}

export default DrawerContent;
