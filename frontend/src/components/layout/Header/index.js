import React from 'react';
import { useLocation } from 'react-router-dom';
import Toolbar from '@mui/material/Toolbar';
import CustomTypography from '../../atoms/CustomTypography';
import ToggleThemeButton from '../../atoms/ToggleThemeButton';
import UserMenu from '../../molecules/UserMenu';
import { Paper } from '@mui/material';
import { getRouteConfig } from '../../../config/routesConfig';

import MenuButton from '../../atoms/MenuButton';
import AppBarHeader from '../../molecules/AppBarHeader';

function Header({ open, handleDrawerOpen }) {
    const location = useLocation();
    
    // Obtener el nombre de la sección actual basado en la ruta
    const routeConfig = getRouteConfig(location.pathname);
    const sectionTitle = routeConfig?.sidebar?.text || 'Dashboard';

    return (
        <AppBarHeader open={open}>
            <Toolbar component={Paper}>
                <MenuButton open={open} onClick={handleDrawerOpen} />
                <ToggleThemeButton />
                <CustomTypography 
                    customVariant="sectionTitle"
                    noWrap
                >
                    {sectionTitle}
                </CustomTypography>
                <UserMenu />
            </Toolbar>
        </AppBarHeader>
    );
}

export default Header;
