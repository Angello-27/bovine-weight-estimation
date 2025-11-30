// frontend/src/components/molecules/UserMenu/UserMenuItem.js
/**
 * Componente UserMenuItem - Item de menú reutilizable
 * 
 * Similar a SidebarItem pero para MenuItems (dropdown)
 * Reutiliza el patrón de ListItemIcon + ListItemText
 */

import React from 'react';
import MenuItem from '@mui/material/MenuItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';

function UserMenuItem({ icon, text, onClick, disabled = false }) {
    return (
        <MenuItem onClick={onClick} disabled={disabled}>
            <ListItemIcon>
                {icon}
            </ListItemIcon>
            <ListItemText primary={text} />
        </MenuItem>
    );
}

export default UserMenuItem;

