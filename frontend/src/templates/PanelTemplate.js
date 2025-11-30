import React from 'react';
import MainLayout from '../components/layout/MainLayout';
import { useAuth } from '../services/auth/AuthContext';

function PanelTemplate({ content }) {
    const { role } = useAuth(); // Accedes al rol del usuario para filtrar el sidebar

    // No retornar nada si no hay rol (no está autenticado)
    if (!role) return null;

    return (
        <MainLayout menu={role}>
            {content}
        </MainLayout>
    );
}

export default PanelTemplate;
