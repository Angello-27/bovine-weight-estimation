import * as React from 'react';
import Divider from '@mui/material/Divider';
import List from '@mui/material/List';

import DrawerHeader from '../../molecules/DrawerHeader';
import DrawerContent from '../../organisms/DrawerContent';
import SidebarItem from '../../atoms/SidebarItem';
import { getSidebarItems } from '../../../config/routesConfig';

function Sidebar({ menu, open, handleDrawerClose }) {
    // menu es la prioridad del rol del usuario (pasado desde PanelTemplate)
    // getSidebarItems filtra por prioridad del rol
    const sidebarItems = getSidebarItems(menu || '');

    return (
        <DrawerContent open={open}>
            <DrawerHeader handleDrawerClose={handleDrawerClose} />
            <Divider />
            <List>
                {/* Renderiza items del sidebar filtrados por prioridad del rol del usuario */}
                {sidebarItems.map(item => (
                            <SidebarItem
                                key={item.text}
                                text={item.text}
                                icon={item.icon}
                                to={item.to}
                            />
                ))}
            </List>
        </DrawerContent>
    );
}

export default Sidebar;