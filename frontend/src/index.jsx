import { StrictMode } from 'react';

// importando ahora desde react-dom/client
import { createRoot } from 'react-dom/client';

import './assets/styles/main.css';
import App from './App';

// IMPORTANTE: asegúrese de especificar el ID correcto
// debe ser el ID del elemento div en su archivo index.html
const rootElement = document.getElementById('root');
const root = createRoot(rootElement);

root.render(
  <StrictMode>
    <App />
  </StrictMode>,
);
