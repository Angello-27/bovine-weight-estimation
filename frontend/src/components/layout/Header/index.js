import React from 'react';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import ToggleThemeButton from '../../atoms/ToggleThemeButton';
import LogoutButton from '../../atoms/LogoutButton'; // Importa tu componente LogoutButton atómico
import { Paper } from '@mui/material';

import MenuButton from '../../atoms/MenuButton';
import AppBarHeader from '../../molecules/AppBarHeader';

function Header({ title, open, handleDrawerOpen }) {
    return (
        <AppBarHeader open={open}>
            <Toolbar component={Paper}>
                <MenuButton open={open} onClick={handleDrawerOpen} />
                <ToggleThemeButton />
                <Typography component="h2" variant="h5" noWrap sx={{ flex: 1, marginLeft: '16px' }}>
                    {title}
                </Typography>
                <LogoutButton /> {/* Utiliza tu componente LogoutButton atómico */}
            </Toolbar>
        </AppBarHeader>
    );
}

export default Header;
