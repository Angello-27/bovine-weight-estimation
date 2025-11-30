// frontend/src/components/molecules/UserMenu/index.js
/**
 * Componente UserMenu - Menú de usuario con dropdown
 * 
 * Según Atomic Design, es un "Molecule" porque:
 * - Combina múltiples elementos (Avatar, Typography, Menu, MenuItems)
 * - Tiene comportamiento propio (dropdown, acciones de usuario)
 * - Es reutilizable en diferentes contextos
 * 
 * Usa el hook useUserMenu para separar la lógica del componente
 */

import React from 'react';
import Avatar from '@mui/material/Avatar';
import Menu from '@mui/material/Menu';
import Divider from '@mui/material/Divider';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import LogoutIcon from '@mui/icons-material/Logout';
import PersonIcon from '@mui/icons-material/Person';
import SettingsIcon from '@mui/icons-material/Settings';
import CustomTypography from '../../atoms/CustomTypography';
import { useUserMenu } from './useUserMenu';
import UserMenuItem from './UserMenuItem';

function UserMenu() {
    const {
        displayName,
        userRole,
        anchorEl,
        open,
        handleClick,
        handleClose,
        handleLogout,
        getInitials,
    } = useUserMenu();

    return (
        <>
            <Box
                component="button"
                onClick={handleClick}
                sx={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1.5,
                    border: 'none',
                    background: 'none',
                    cursor: 'pointer',
                    padding: '8px 12px',
                    borderRadius: 2,
                    transition: 'background-color 0.2s',
                    '&:hover': {
                        backgroundColor: 'action.hover',
                    },
                }}
            >
                <Avatar 
                    sx={{ 
                        width: 36, 
                        height: 36, 
                        bgcolor: 'primary.main',
                        fontSize: '0.875rem'
                    }}
                >
                    {getInitials(displayName)}
                </Avatar>
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                    <CustomTypography customVariant="userName" noWrap>
                        {displayName}
                    </CustomTypography>
                    <Chip 
                        label={userRole} 
                        size="small" 
                        color="primary"
                        variant="outlined"
                        sx={{ 
                            height: 18, 
                            fontSize: '0.65rem',
                            mt: 0.25,
                            '& .MuiChip-label': {
                                padding: '0 6px'
                            }
                        }}
                    />
                </Box>
            </Box>

            <Menu
                anchorEl={anchorEl}
                open={open}
                onClose={handleClose}
                onClick={handleClose}
                transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                PaperProps={{
                    elevation: 3,
                    sx: {
                        mt: 1.5,
                        minWidth: 200,
                        '& .MuiMenuItem-root': {
                            px: 2,
                            py: 1,
                        },
                    },
                }}
            >
                <UserMenuItem
                    icon={<PersonIcon fontSize="small" />}
                    text="Mi Perfil"
                    onClick={handleClose}
                />
                <UserMenuItem
                    icon={<SettingsIcon fontSize="small" />}
                    text="Configuración"
                    onClick={handleClose}
                />
                <Divider />
                <UserMenuItem
                    icon={<LogoutIcon fontSize="small" />}
                    text="Cerrar Sesión"
                    onClick={handleLogout}
                />
            </Menu>
        </>
    );
}

export default UserMenu;

