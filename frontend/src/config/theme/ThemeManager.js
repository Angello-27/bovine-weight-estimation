export class ThemeManager {
    constructor() {
        // Intenta recuperar el tema del almacenamiento local. Si no existe, usa 'light' por defecto.
        this.currentTheme = localStorage.getItem('themePreference') || 'light';
        // Aplica el tema actual al cargar la página.
        this.applyCurrentTheme();
    }

    toggleTheme() {
        if (this.currentTheme === 'light') {
            this.setDarkTheme();
        } else {
            this.setLightTheme();
        }
    }

    applyCurrentTheme() {
        if (this.currentTheme === 'light') {
            this.setLightTheme();
        } else {
            this.setDarkTheme();
        }
    }

    setLightTheme() {
        document.body.classList.remove('dark-theme');
        document.body.classList.add('light-theme');
        this.currentTheme = 'light';
        // Guarda la preferencia en el almacenamiento local.
        localStorage.setItem('themePreference', 'light');
    }

    setDarkTheme() {
        document.body.classList.remove('light-theme');
        document.body.classList.add('dark-theme');
        this.currentTheme = 'dark';
        // Guarda la preferencia en el almacenamiento local.
        localStorage.setItem('themePreference', 'dark');
    }
}
