// src/config/themes.js
import { createTheme } from '@mui/material/styles';
import { colors } from './colors'; // Importa los colores


export const lightTheme = createTheme({
    palette: {
        type: 'light',
        mode: 'light',
        primary: {
            main: colors.primary,
            light: colors.lightPrimary, // Añade el nuevo color claro
            dark: colors.darkPrimary, // Añade el nuevo color oscuro
        },
        secondary: {
            main: colors.accent,
            light: colors.lightAccent, // Añade el nuevo color claro
            dark: colors.darkAccent, // Añade el nuevo color oscuro
        },
        // ...otros valores del tema light que desees añadir
    },
    typography: {
        fontFamily: 'Roboto, sans-serif',
    },
});


export const darkTheme = createTheme({
    palette: {
        type: 'dark',
        mode: 'dark',
        primary: {
            main: colors.accent,
            light: colors.lightAccent, // Añade el nuevo color claro
            dark: colors.darkAccent, // Añade el nuevo color oscuro
        },
        secondary: {
            main: colors.primary,
            light: colors.lightPrimary, // Añade el nuevo color claro
            dark: colors.darkPrimary, // Añade el nuevo color oscuro
        },
        // ...otros valores del tema dark que desees añadir
    },
    typography: {
        fontFamily: 'Roboto, sans-serif',
    },
});
