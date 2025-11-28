// src/components/molecules/SidebarItem.js

import React from 'react';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { Link } from '@mui/material';

function SidebarItem({ text, icon, to }) {
    return (
        <ListItem disablePadding>
            <ListItemButton component={Link} to={to}>
                <ListItemIcon sx={{ color: 'primary.main' }}>
                    {icon}
                </ListItemIcon>
                <ListItemText primary={text} />
            </ListItemButton>
        </ListItem>
    );
}

export default SidebarItem;
