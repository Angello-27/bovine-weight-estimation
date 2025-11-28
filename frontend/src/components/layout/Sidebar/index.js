import * as React from 'react';
import Divider from '@mui/material/Divider';
import List from '@mui/material/List';

import DrawerHeader from '../../molecules/DrawerHeader';
import DrawerContent from '../../organisms/DrawerContent';
import SidebarItem from '../../atoms/SidebarItem';
import { sidebarItems } from '../../../config/constants';

function Sidebar({ menu, open, handleDrawerClose }) {

    return (
        <DrawerContent open={open}>
            <DrawerHeader handleDrawerClose={handleDrawerClose} />
            <Divider />
            <List>
                {/* Aquí va el resto de tu código relacionado con la lista del Sidebar */}
                {sidebarItems.map(item => {
                    // Verifica si el role actual puede ver este ítem
                    if (item.roles.includes(menu)) {
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