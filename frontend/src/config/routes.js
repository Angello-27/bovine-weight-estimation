// routes.js
import React from 'react';
import { Route, Routes } from 'react-router-dom';
import { AuthProvider } from '../services/auth/AuthContext';

// Importa tus componentes y vistas
import ErrorView from '../views/ErrorView';
import LoginView from '../views/LoginView';
import DashboardView from '../views/DashboardView';
import CattleView from '../views/CattleView';
import WeightEstimationsView from '../views/WeightEstimationsView';
import SyncStatusView from '../views/SyncStatusView';
import CattleDetailView from '../views/CattleDetailView';
// TODO: Importar cuando se creen
// import WeightEstimationDetailView from '../views/WeightEstimationDetailView';
import WeightEstimationFromWebView from '../views/WeightEstimationFromWebView';
// import StatisticsView from '../views/StatisticsView';

function AppRoutes() {
    return (
        <AuthProvider>
            <Routes>
                <Route path="/" element={<LoginView />} />
                <Route path="/home" element={<DashboardView />} />
                <Route path="/dashboard" element={<DashboardView />} />
                <Route path="/cattle" element={<CattleView />} />
                <Route path="/cattle/:id" element={<CattleDetailView />} />
                <Route path="/weight-estimations" element={<WeightEstimationsView />} />
                <Route path="/weight-estimations/estimate" element={<WeightEstimationFromWebView />} />
                <Route path="/sync" element={<SyncStatusView />} />
                {/* TODO: Agregar cuando se creen */}
                {/* <Route path="/weight-estimations/:id" element={<WeightEstimationDetailView />} /> */}
                {/* <Route path="/statistics" element={<StatisticsView />} /> */}
                {/* Asegúrate de que esta ruta esté al final */}
                <Route path="*" element={<ErrorView />} />
            </Routes>
        </AuthProvider>
    );
}

export default AppRoutes;
