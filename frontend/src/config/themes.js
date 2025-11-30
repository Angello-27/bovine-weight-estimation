// src/config/themes.js
import { createTheme } from '@mui/material/styles';
import { colors } from './colors'; // Importa los colores


export const lightTheme = createTheme({
    palette: {
        type: 'light',
        mode: 'light',
        primary: {
            main: colors.primary,
            light: colors.lightPrimary,
            dark: colors.darkPrimary,
        },
        secondary: {
            main: colors.accent,
            light: colors.lightAccent,
            dark: colors.darkAccent,
        },
        background: {
            default: '#f8f9fa', // Color de fondo claro para mejor contraste
            paper: '#ffffff', // Color blanco puro para las cards/papers
        },
        // ...otros valores del tema light que desees añadir
    },
    typography: {
        fontFamily: 'Roboto, sans-serif',
    },
    components: {
        MuiPaper: {
            styleOverrides: {
                root: {
                    backgroundColor: '#ffffff',
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)', // Sombra más visible en light mode
                },
            },
        },
    },
});


export const darkTheme = createTheme({
    palette: {
        type: 'dark',
        mode: 'dark',
        primary: {
            main: colors.accent,
            light: colors.lightAccent,
            dark: colors.darkAccent,
        },
        secondary: {
            main: colors.primary,
            light: colors.lightPrimary,
            dark: colors.darkPrimary,
        },
        background: {
            default: '#27282A', // Fondo oscuro
            paper: '#1e1f21', // Paper más oscuro para mejor contraste
        },
        // ...otros valores del tema dark que desees añadir
    },
    typography: {
        fontFamily: 'Roboto, sans-serif',
    },
    components: {
        MuiPaper: {
            styleOverrides: {
                root: {
                    backgroundColor: '#1e1f21',
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.3)', // Sombra más pronunciada en dark mode
                },
            },
        },
    },
});
