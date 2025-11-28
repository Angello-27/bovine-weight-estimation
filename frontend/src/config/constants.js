// src/config/constants.js

import DashboardIcon from '@mui/icons-material/Dashboard';
import PetsIcon from '@mui/icons-material/Pets';
import ScaleIcon from '@mui/icons-material/Scale';
import SyncIcon from '@mui/icons-material/Sync';
import BarChartIcon from '@mui/icons-material/BarChart';

export const drawer = {
    width: 304,
};

export const radioButtonsRoles = [
    { id: "Administrador", label: "Administrador" },
    { id: "Usuario", label: "Usuario" },
    { id: "Invitado", label: "Invitado" }
];

export const sidebarItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, to: "/home", roles: ['Administrador', 'Usuario', 'Invitado'] },
    { text: 'Ganado', icon: <PetsIcon />, to: "/cattle", roles: ['Administrador', 'Usuario'] },
    { text: 'Estimaciones de Peso', icon: <ScaleIcon />, to: "/weight-estimations", roles: ['Administrador', 'Usuario'] },
    { text: 'Sincronización', icon: <SyncIcon />, to: "/sync", roles: ['Administrador'] },
    { text: 'Estadísticas', icon: <BarChartIcon />, to: "/statistics", roles: ['Administrador', 'Usuario'] }
];

