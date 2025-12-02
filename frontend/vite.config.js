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
    // Configuración para mejorar chunking y reducir tamaño de bundles
    rollupOptions: {
      output: {
        manualChunks: {
          // Separar vendor chunks grandes
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'ui-vendor': ['@mui/material', '@mui/icons-material'],
          'chart-vendor': ['recharts', 'chart.js'],
        },
      },
    },
    // Aumentar límite de warning para chunks grandes (1.6MB es aceptable para esta app)
    chunkSizeWarningLimit: 1000,
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

