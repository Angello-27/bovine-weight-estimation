// routes.js
import React from 'react';
import { Route, Routes } from 'react-router-dom';
import { AuthProvider } from '../services/auth/AuthContext';

// Importa tus componentes y vistas
import ErrorView from '../views/ErrorView';
import LoginView from '../views/LoginView';
import HomeView from '../views/HomeView';
// TODO: Importar nuevas vistas cuando se creen
// import CattleView from '../views/CattleView';
// import WeightEstimationsView from '../views/WeightEstimationsView';
// import SyncStatusView from '../views/SyncStatusView';
// import StatisticsView from '../views/StatisticsView';

function AppRoutes() {
    return (
        <AuthProvider>
            <Routes>
                <Route path="/" element={<LoginView />} />
                <Route path="/home" element={<HomeView />} />
                {/* TODO: Agregar rutas cuando se creen las vistas */}
                {/* <Route path="/cattle" element={<CattleView />} /> */}
                {/* <Route path="/cattle/:id" element={<CattleDetailView />} /> */}
                {/* <Route path="/weight-estimations" element={<WeightEstimationsView />} /> */}
                {/* <Route path="/weight-estimations/:id" element={<WeightEstimationDetailView />} /> */}
                {/* <Route path="/sync" element={<SyncStatusView />} /> */}
                {/* <Route path="/statistics" element={<StatisticsView />} /> */}
                {/* Asegúrate de que esta ruta esté al final */}
                <Route path="*" element={<ErrorView />} />
            </Routes>
        </AuthProvider>
    );
}

export default AppRoutes;
