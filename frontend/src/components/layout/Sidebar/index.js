import * as React from 'react';
import Divider from '@mui/material/Divider';
import List from '@mui/material/List';

import DrawerHeader from '../../molecules/DrawerHeader';
import DrawerContent from '../../organisms/DrawerContent';
import SidebarItem from '../../atoms/SidebarItem';
import { getAllSidebarItems } from '../../../config/routesConfig';

function Sidebar({ menu, open, handleDrawerClose }) {
    const sidebarItems = getAllSidebarItems();

    return (
        <DrawerContent open={open}>
            <DrawerHeader handleDrawerClose={handleDrawerClose} />
            <Divider />
            <List>
                {/* Renderiza items del sidebar filtrados por rol del usuario */}
                {sidebarItems.map(item => {
                    // Verifica si el role actual puede ver este ítem
                    if (item.roles && item.roles.includes(menu)) {
                        return (
                            <SidebarItem
                                key={item.text}
                                text={item.text}
                                icon={item.icon}
                                to={item.to}
                            />
                        );
                    }
                    return null; // No muestra el elemento si el role no está en la lista
                })}
            </List>
        </DrawerContent>
    );
}

export default Sidebar;