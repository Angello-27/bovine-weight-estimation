import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react({
      // Permite JSX en archivos .js y .jsx
      include: /\.(jsx|js)$/,
      // Configuración adicional para JSX en archivos .js
      jsxRuntime: 'automatic',
      // Babel options para transformar JSX en archivos .js
      babel: {
        parserOpts: {
          plugins: ['jsx'],
        },
      },
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
    extensions: ['.jsx', '.js', '.json'],
  },
  server: {
    port: 3000,
    open: true,
  },
  build: {
    outDir: 'build',
    sourcemap: true,
  },
  // Variables de entorno
  envPrefix: 'REACT_APP_',
  esbuild: {
    // Configura esbuild para manejar JSX en archivos .js
    loader: 'jsx',
    include: /src\/.*\.jsx?$/,
    exclude: [],
  },
  optimizeDeps: {
    esbuildOptions: {
      loader: {
        '.js': 'jsx',
      },
    },
  },
});

