// src/config/ThemeContext.js
import { createContext, useContext, useState } from 'react';
import { ThemeManager } from './ThemeManager';  // Asegúrate de reemplazar 'path-to-Theme.js' con la ruta correcta al archivo.
import { lightTheme, darkTheme } from '../themes'; // Importa los temas definidos previamente

export const useTheme = () => {
    return useContext(ThemeContext);
};

export const AppThemeProvider = ({ children }) => {
    const themeManager = new ThemeManager();
    const [currentThemeString, setCurrentThemeString] = useState(themeManager.currentTheme);

    // Aquí determinamos qué tema usar basado en la cadena de texto.
    const muiTheme = currentThemeString === 'light' ? lightTheme : darkTheme;

    const toggleTheme = () => {
        themeManager.toggleTheme();
        setCurrentThemeString(themeManager.currentTheme); // Actualiza el estado para que React re-renderice los componentes
    };

    return (
        <ThemeContext.Provider value={{ currentTheme: muiTheme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
};

export const ThemeContext = createContext();