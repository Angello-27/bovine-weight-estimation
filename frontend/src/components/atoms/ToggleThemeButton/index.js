// src/components/atoms/ToggleThemeButton.js
import React from 'react';
import IconButton from '@mui/material/IconButton';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { useTheme } from '../../../config/theme/ThemeContext';

function ToggleThemeButton() {
    const { currentTheme, toggleTheme } = useTheme();
    const isLight = currentTheme.palette.mode === 'light';

    return (
        <IconButton onClick={toggleTheme} sx={{ padding: '12px' }}>
            {isLight ? <Brightness4Icon /> : <Brightness7Icon />}
        </IconButton>
    );
}

export default ToggleThemeButton;
