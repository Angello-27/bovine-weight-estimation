import React from 'react';
import { styled } from '@mui/material/styles';
import MuiAppBar from '@mui/material/AppBar';
import { drawer } from '../../../config/constants';

const AppBar = styled(MuiAppBar, { shouldForwardProp: (prop) => prop !== 'open' })
    (({ theme, open }) => ({
        zIndex: theme.zIndex.drawer + 1,
        ...(open && {
            marginLeft: drawer.width,
            width: `calc(100% - ${drawer.width}px)`,
        }),
    }));

function AppBarHeader({ open, children }) {
    return (
        <AppBar position="sticky" open={open}>
            {children}
        </AppBar>
    );
}

export default AppBarHeader;
