import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';

import { AppThemeProvider } from './config/theme/ThemeContext';
import AppRoutes from './config/routes';

function App() {
  return (
    <AppThemeProvider>
      <Router>
        <AppRoutes />
      </Router>
    </AppThemeProvider>
  );
}

export default App;