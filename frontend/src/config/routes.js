// routes.js
/**
 * Configuración de rutas de la aplicación
 * Utiliza routesConfig.js para obtener la configuración centralizada de rutas y roles
 */
import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import { AuthProvider } from '../services/auth/AuthContext';
import ProtectedRoute from '../components/molecules/ProtectedRoute';
import { appRoutes } from './routesConfig';

// Importa tus componentes y vistas
import ErrorView from '../views/ErrorView';
import LoginView from '../views/LoginView';
import DashboardView from '../views/DashboardView';
import CattleView from '../views/CattleView';
import WeightEstimationsView from '../views/WeightEstimationsView';
import SyncStatusView from '../views/SyncStatusView';
import CattleDetailView from '../views/CattleDetailView';
import WeightEstimationFromWebView from '../views/WeightEstimationFromWebView';
import WeightEstimationDetailView from '../views/WeightEstimationDetailView';
import UserView from '../views/UserView';
import RoleView from '../views/RoleView';
import FarmView from '../views/FarmView';
// import StatisticsView from '../views/StatisticsView';

// Mapeo de paths a componentes
const routeComponents = {
    '/home': DashboardView,
    '/cattle': CattleView,
    '/cattle/:id': CattleDetailView,
    '/weight-estimations': WeightEstimationsView,
    '/weight-estimations/estimate': WeightEstimationFromWebView,
    '/weight-estimations/:id': WeightEstimationDetailView,
    '/sync': SyncStatusView,
    '/users': UserView,
    '/roles': RoleView,
    '/farms': FarmView,
    // '/statistics': StatisticsView,
};

function AppRoutes() {
    return (
        <AuthProvider>
            <Routes>
                {/* Rutas públicas */}
                <Route path="/login" element={<LoginView />} />
                <Route path="/" element={<Navigate to="/home" replace />} />

                {/* Rutas dinámicas desde configuración centralizada */}
                {appRoutes.map((routeConfig) => {
                    const Component = routeComponents[routeConfig.path];
                    if (!Component) return null;

                    return (
                        <Route
                            key={routeConfig.path}
                            path={routeConfig.path}
                            element={
                                <ProtectedRoute requiredRoles={routeConfig.roles}>
                                    <Component />
                                </ProtectedRoute>
                            }
                        />
                    );
                })}

                {/* Rutas con parámetros dinámicos (no están en appRoutes por tener :id) */}
                <Route
                    path="/cattle/:id"
                    element={
                        <ProtectedRoute requiredRoles={['Administrador', 'Usuario']}>
                            <CattleDetailView />
                        </ProtectedRoute>
                    }
                />
                <Route
                    path="/weight-estimations/:id"
                    element={
                        <ProtectedRoute requiredRoles={['Administrador', 'Usuario']}>
                            <WeightEstimationDetailView />
                        </ProtectedRoute>
                    }
                />

                {/* Ruta de error debe estar al final */}
                <Route path="*" element={<ErrorView />} />
            </Routes>
        </AuthProvider>
    );
}

export default AppRoutes;
